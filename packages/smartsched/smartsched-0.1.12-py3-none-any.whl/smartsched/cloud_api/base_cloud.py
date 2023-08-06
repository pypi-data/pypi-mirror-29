import logging


class BaseCloud(object):

    def __init__(self):
        pass

    def get_hosts_repr(self):
        """Host info: high level"""
        result = []
        logging.warning("get_hosts_repr is not implemented")
        return result

    def get_vms_repr(self):
        """High level VM representation"""
        result = []
        logging.warning("get_vms_repr is not implemented")
        return result

    def get_vm_repr(self, vm_id):
        """High level VM info"""
        result = {}
        logging.warning("get_vm_repr is not implemented")
        return result

    def get_clusters(self):
        """Get Clusters: reordered data from Hosts"""
        result = {}
        logging.warning("get_clusters is not implemented")
        return result

    # ==========================================================================
    #     Helper Level functions
    # ==========================================================================

    def get_hosts_of_cluster(self, cluster_id):
        result = []
        logging.warning("get_hosts_of_cluster is not implemented")
        return result

    def get_pending_unscheduled(self):
        result = []
        logging.warning("get_pending_unscheduled is not implemented")
        return result

    def migrate(self):
        """Sends signal to migrate the. Important to keep track on migration
        process, since this method does not do this."""
        logging.warning("migrate function is not implemented")
        pass

    def deploy(self):
        """Sends signal to migrate the. Important to keep track on migration
        process, since this method does not do this."""
        logging.warning("deploy function is not implemented")
        pass