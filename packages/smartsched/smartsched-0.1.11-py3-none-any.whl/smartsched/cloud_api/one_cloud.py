from pprint import pprint as pp
from datetime import datetime

import xmlrpc.client  # Connect with XML RPC server
import xmltodict  # Convert XML to Python Dict

from smartsched.cloud_api import base_cloud
from smartsched.cloud_api.one_constants import HOST_STATES, VM_STATES, LCM_STATES


def xml_to_dict(xml):
    obj = xmltodict.parse(xml, encoding='utf-8', dict_constructor=dict,)
    return obj


def init_handler(config_dict):
    return ONECloud(config_dict)


class ONECloud(base_cloud.BaseCloud):

    config = {
        'active_hosts': ['MONITORED']
    }

    required_params = {
        'username': str,
        'password': str,
        'xml_server_url': str
    }

    def is_config_ok(self, config):
        for param in self.required_params:
            if param not in config:
                pp(param + ' param is missing')
                return False
        return True

    def __init__(self, config_dict):
        """Constructor for OpenNebula driver.

        Arguments:
            config_dict: dictionary of str with config parameters.
        """
        if self.is_config_ok(config_dict):
            self.server = config_dict['xml_server_url']
            self.one_auth = '{0}:{1}'.format(config_dict['username'],
                                             config_dict['password'])

    def _get_proxy(self):
        return xmlrpc.client.ServerProxy(self.server)

    # ==========================================================================
    #     Low Level functions
    # ==========================================================================
    def _get_cluster_list(self):
        """Low level function to get list of clusters from cloud"""
        response = self._get_proxy().one.clusterpool.info(self.one_auth)
        if response[0]:
            return xml_to_dict(response[1])['CLUSTER_POOL']['CLUSTER']
        else:
            raise Exception(response[1])

    def _get_host_list(self):
        """Low level function to get list of host s from cloud"""
        response = self._get_proxy().one.hostpool.info(self.one_auth)
        if response[0]:
            return xml_to_dict(response[1])['HOST_POOL']['HOST']
        else:
            raise Exception(response[1])

    def _get_vm_list(self, belongingFilter=-2, startId=-1, endId=-1, vmStateFilter=-1):
        """
        belongingFilter:
            -4: Resources belonging to the users primary group
            -3: Resources belonging to the user
            -2: All resources
            -1: Resources belonging to the user and any of his groups
            >= 0: UID Users Resources
        vmStateFilter:
            see OpenNebulaConstants: VM_STATES
        """
        response = self._get_proxy().one.vmpool.info(self.one_auth,
                                                     belongingFilter,
                                                     startId, endId,
                                                     vmStateFilter)
        if response[0]:
            xml = xml_to_dict(response[1])
            if xml['VM_POOL'] is not None:
                if isinstance(xml['VM_POOL']['VM'], list):
                    return xml['VM_POOL']['VM']
                else:
                    return [xml['VM_POOL']['VM']]
            else:
                return []
        else:
            raise Exception(response[1])

    def _get_cluster_info(self, cluster_id):
        response = self._get_proxy().one.cluster.info(self.one_auth, cluster_id)
        if response[0]:
            return xml_to_dict(response[1])['CLUSTER']
        else:
            raise Exception(response[1])

    def _get_host_info(self, host_id):
        """Host info: Low level"""
        response = self._get_proxy().one.host.info(self.one_auth, host_id)
        if response[0]:
            return xml_to_dict(response[1])['HOST']
        else:
            raise Exception(response[1])

    def _get_vm_info(self, vm_id):
        """VM info: Low level"""
        response = self._get_proxy().one.vm.info(self.one_auth, vm_id)
        if response[0]:
            return xml_to_dict(response[1])['VM']
        else:
            raise Exception(response[1])

    def _form_cluster_info(self, cluster):
        """Form Cluster object: low level
        Take important information from raw data coming from ONE and form new object."""
        current = {}
        current['id'] = int(cluster['ID'])
        current['name'] = str(cluster['NAME'])
        current['datastores'] = str(cluster['NAME'])

        if cluster['HOSTS']:  # not None
            current['hosts'] = [int(_id) for _id in cluster['HOSTS']['ID']]
        else:
            current['hosts'] = []

        if cluster['DATASTORES']:  # not None
            current['datastores'] = [int(_id) for _id in cluster['DATASTORES']['ID']]
        else:
            current['datastores'] = []

        if cluster['VNETS']:  # not None
            current['vnets'] = [int(_id) for _id in cluster['VNETS']['ID']]
        else:
            current['vnets'] = []

        return current

    def _form_vm_info(self, vm):
        """Form VM object: low level
        Take important information from raw data coming from ONE and form new object."""
        current = {}
        current['id'] = int(vm['ID'])
        current['name'] = str(vm['NAME'])
        current['state'] = VM_STATES[int(vm['STATE'])]
        current['lcm_state'] = LCM_STATES[int(vm['LCM_STATE'])]
        current['cpu_req'] = float(vm['TEMPLATE']['CPU'])
        current['mem_req'] = int(vm['TEMPLATE']['MEMORY'])
        current['cpu_allocated'] = float(vm['TEMPLATE']['CPU']) * 100
        current['mem_allocated'] = int(vm['TEMPLATE']['MEMORY']) * 1024
        #current['mem_used'] = int(vm['MONITORING']['USEDMEMORY'])
        #current['cpu_used'] = float(vm['MONITORING']['USEDCPU'])

        # HID - optional parameter, could be empty if VM was never running
        current['hid'] = -1
        current['rstime'] = datetime.utcfromtimestamp(0)
        current['retime'] = datetime.utcfromtimestamp(0)
        if vm['HISTORY_RECORDS'] is not None:
            history_obj = None
            if isinstance(vm['HISTORY_RECORDS']['HISTORY'], list):
                if len(vm['HISTORY_RECORDS']['HISTORY']) != 0:
                    history_obj = vm['HISTORY_RECORDS']['HISTORY'][-1]
            else:
                if 'HID' in vm['HISTORY_RECORDS']['HISTORY']:
                    history_obj = vm['HISTORY_RECORDS']['HISTORY']
            if history_obj is not None:
                current['hid'] = int(history_obj['HID'])
                current['rstime'] = datetime.utcfromtimestamp(int(history_obj['RSTIME']))
                current['retime'] = datetime.utcfromtimestamp(int(history_obj['RETIME']))

        current['cluster_id'] = -1
        if 'DISK' in vm['TEMPLATE']:
            if isinstance(vm['TEMPLATE']['DISK'], list):
                current['cluster_id'] = [int(disk['CLUSTER_ID']) for disk in vm['TEMPLATE']['DISK'] if 'CLUSTER_ID' in disk]
            else:
                if 'CLUSTER_ID' in vm['TEMPLATE']['DISK']:
                    current['cluster_id'] = [int(vm['TEMPLATE']['DISK']['CLUSTER_ID'])]

        current['template_id'] = -1
        if 'TEMPLATE_ID' in vm['TEMPLATE']:
            current['template_id'] = int(vm['TEMPLATE']['TEMPLATE_ID'])

        current['sched_message'] = ''
        if ('USER_TEMPLATE' in vm) and (vm['USER_TEMPLATE'] is not None):
            if 'SCHED_MESSAGE' in vm['USER_TEMPLATE']:
                current['sched_message'] = str(vm['USER_TEMPLATE']['SCHED_MESSAGE'])

        return current

    def _form_host_info(self, host):
        current = {}
        current['cluster'] = str(host['CLUSTER'])
        current['cluster_id'] = int(host['CLUSTER_ID'])
        current['id'] = int(host['ID'])
        current['im_mad'] = str(host['IM_MAD'])
        current['last_mon_time'] = datetime.utcfromtimestamp(int(host['LAST_MON_TIME']))
        current['name'] = str(host['NAME'])
        current['state'] = int(host['STATE'])
        current['vm_mad'] = str(host['VM_MAD'])
        # current['vn_mad'] = str(host['VN_MAD'])

        cpu_allocated = int(host['HOST_SHARE']['CPU_USAGE'])
        cpu_max = int(host['HOST_SHARE']['MAX_CPU'])
        cpu_used = int(host['HOST_SHARE']['USED_CPU'])
        cpu_used_ratio = (1.0 * cpu_used / cpu_max) if cpu_max != 0 else -1
        cpu_over_commitment = (1.0 * cpu_allocated / cpu_max) if cpu_max != 0 else -1
        current['usage_cpu'] = {
            'allocated': cpu_allocated,
            'max': cpu_max,
            'used': cpu_used,
            'ratio_used': cpu_used_ratio,
            'ratio_overc': cpu_over_commitment,
        }

        mem_allocated = int(host['HOST_SHARE']['MEM_USAGE'])
        mem_max = int(host['HOST_SHARE']['MAX_MEM'])
        mem_used = int(host['HOST_SHARE']['USED_MEM'])
        mem_used_ratio = (1.0 * mem_used / mem_max) if mem_max != 0 else -1
        mem_over_commitment = (1.0 * mem_allocated / mem_max) if mem_max != 0 else -1
        current['usage_mem'] = {
            'allocated': mem_allocated,
            'max': mem_max,
            'used': mem_used,
            'ratio_used': mem_used_ratio,
            'ratio_overc': mem_over_commitment,
        }
        current['vms'] = []
        if host['VMS']:
            current['vms'] = host['VMS']['ID'] if isinstance(host['VMS']['ID'], (list)) else [int(host['VMS']['ID'])]

        return current

    # ==========================================================================
    #     High Level functions
    # ==========================================================================

    def get_hosts_repr(self):
        """All Hosts info: high level"""
        hosts = self._get_host_list()
        hosts_repr = []
        for host in hosts:
            current = self._form_host_info(host)
            hosts_repr.append(current)
        return hosts_repr

    def get_host_repr(self, host_id):
        """High level one Host representation"""
        host = self._get_host_info(host_id)
        host_repr = self._form_host_info(host)
        return host_repr

    def get_vms_repr(self, belongingFilter=-2, startId=-1, endId=-1, vmStateFilter=-1):
        """High level VMs representation"""
        vms = self._get_vm_list(belongingFilter, startId, endId, vmStateFilter)
        vms_repr = []
        for vm in vms:
            current = self._form_vm_info(vm)
            vms_repr.append(current)
        return vms_repr

    def get_vm_repr(self, vm_id):
        """High level VM info"""
        obj = self._get_vm_info(vm_id)
        vm_repr = self._form_vm_info(obj)
        return vm_repr

    # This code does not belong to this part of code. This function should be called get_hosts_grouped_by_ clusters
    # def get_clusters(self):
    #     """Get Clusters: reordered data from Hosts"""
    #     representation = self.get_hosts_repr()
    #     clusters = {}
    #     for elem in representation:
    #         cluster_key = (elem['cluster_id'], elem['cluster'])
    #         if cluster_key not in clusters:
    #             clusters[cluster_key] = []
    #         clusters[cluster_key].append({'hostname': elem['name'],
    #                                       'cpu_ratio': elem['usage_cpu']['ratio_used'],
    #                                       'cpu_max': elem['usage_cpu']['max'],
    #                                       'cpu_overc':  elem['usage_cpu']['ratio_overc'],
    #                                       'mem_ratio': elem['usage_mem']['ratio_used'],
    #                                       'mem_max': elem['usage_mem']['max'],
    #                                       'mem_overc':  elem['usage_mem']['ratio_overc'],
    #                                       'vm_mad': elem['vm_mad'],
    #                                       'vms': elem['vms']})
    #    return clusters

    def get_clusters_repr(self):
        """Get all clusters high level info"""
        clusters = self._get_cluster_list()
        clusters_repr = []
        for cluster in clusters:
            clusters_repr.append(self._form_cluster_info(cluster))
        return clusters_repr

    def get_cluster_repr(self, cluster_id):
        """Get single cluster high level info"""
        cluster = self._get_cluster_info(cluster_id)
        cluster_repr = self._form_cluster_info(cluster)
        return cluster_repr

    # ==========================================================================
    #     Helper Level functions
    # ==========================================================================

    def get_hosts_of_cluster(self, cluster_id):
        hosts = self.get_hosts_repr()
        result = []
        cluster_id = cluster_id[0] if isinstance(cluster_id, list) else cluster_id
        for host in hosts:
            if host['cluster_id'] != cluster_id:
                continue
            if HOST_STATES[host['state']] not in self.config['active_hosts']:
                continue
            result.append(host)
        return result

    def get_pending_unscheduled(self):
        result = []
        pending_vm_list = self.get_vms_repr(vmStateFilter=1)
        for vm in pending_vm_list:
            if 'No host meets SCHED_REQUIREMENTS' in vm['sched_message']:
                vm['notEnoughSpace'] = True
                result.append(vm)
        return result

    def migrate(self, vm_id, dest_host_id, isLive, isCapable):
        """Sends signal to migrate the. Important to keep track on migration
        process, since this method does not do this."""
        response = self._get_proxy().one.vm.migrate(self.one_auth, vm_id, dest_host_id, isLive, isCapable)
        pp(response)

    def deploy(self, vm_id, dest_host_id, isCapable, data_store=-1):
        """Sends signal to migrate the. Important to keep track on migration
        process, since this method does not do this."""
        response = self._get_proxy().one.vm.deploy(self.one_auth, vm_id, dest_host_id, isCapable, data_store)
        pp(response)

    def action(self, vm_id, new_state):
        """Changes state of virtual machine"""
        response = self._get_proxy().one.vm.action(self.one_auth, new_state, vm_id)
        pp(response)
