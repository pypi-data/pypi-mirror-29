from pprint import pprint as pp
from dateutil import parser

from influxdb import InfluxDBClient


def init_handler(config_dict):
    return InfluxHandler(config_dict)


def get_united_columns_values(columns, values):
    return [dict([(columns[index], row[index]) for index in range(len(columns))]) for row in values]


def get_listOfDict_without_none(listOfDict):
    return [x for x in listOfDict if x['value'] is not None]


def get_time_value_dict(listOfDict):
    result = {}
    for elem in listOfDict:
        result[elem['time']] = elem['value']
    return result


def set_value_names(listOfDict):
    for elem in listOfDict:
        attr_name = elem['metric'].split('_')[0] if '_' in elem['metric'] else elem['metric']
        elem[attr_name] = elem.pop('value', None)


def convert_data_type(listOfDict, key, converter):
    for elem in listOfDict:
        elem[key] = converter(elem[key])


def get_datetime_from_string(strTime):
    return parser.parse(strTime).replace(second=0, microsecond=0)


def get_shrinked_list(listOfDict, primary_key):
    result = {}
    for elem in listOfDict:
        if elem[primary_key] not in result:
            result[elem[primary_key]] = elem
        else:
            result[elem[primary_key]].update(elem)
    result = [dict(result[key].items()) for key in result]
    result.sort(key=lambda x: x[primary_key])
    return result


class InfluxHandler(object):

    required_params = {
        'host': str,
        'port': int,
        'dbname': str,
        'user': str,
        'password': str,
        'ssl': bool,
        'verify_ssl': bool
    }

    def is_config_ok(self, config):
        for param in self.required_params:
            if param not in config:
                pp(param + ' param is missing')
                return False
        return True

    def __init__(self, config_dict):
        self.client = InfluxDBClient(host=config_dict['host'], port=int(config_dict['port']),
                                     username=config_dict['user'], password=config_dict['password'],
                                     database=config_dict['dbname'],
                                     ssl=True if config_dict['ssl'] == 'True' else False,
                                     verify_ssl=True if config_dict['verify_ssl'] == 'True' else False)

    def get_ovz_vm(self, vm_id, metrics, limit=100):
        result = []

        deploy_id = vm_id + 1000
        metrics_filter = ["metric=\'"+metric+"_"+str(deploy_id)+"\'" for metric in metrics]
        metrics_filter = ' OR '.join(metrics_filter)

        query = "SELECT hostname, metric, value FROM check_openvz_vm_perf WHERE %s ORDER BY time DESC LIMIT %s" % (metrics_filter, str(limit), )
        data = self.client.query(query).raw

        if data != {}:
            series = data['series'][0]
            data = get_united_columns_values(series['columns'], series['values'])
            set_value_names(data)
            convert_data_type(data, 'time', get_datetime_from_string)
            result = get_shrinked_list(data, 'time')
        return result

    def get_host_vms(self, hostname):
        vms = {}
        query = "SELECT last(value) FROM check_openvz_vm_perf WHERE hostname='%s' AND metric =~ /cpu_\d+/ AND time > now() - 3m GROUP BY metric" % hostname
        data = self.client.query(query).raw
        if data != {}:
            for row in data['series']:
                metric = row['tags']['metric'].split('_')
                vms[int(metric[-1]) - 1000] = {str(metric[0]): float(row['values'][0][1])}

        query = "SELECT last(value) FROM check_openvz_vm_perf WHERE hostname='%s' AND metric =~ /mem_b_\d+/ AND time > now() - 3m GROUP BY metric" % hostname
        data = self.client.query(query).raw
        if data != {}:
            for row in data['series']:
                metric = row['tags']['metric'].split('_')
                vms[int(metric[-1]) - 1000][str(metric[0])] = float(row['values'][0][1])
        return vms

    def get_host_load(self, hostname, metric, period='1d', group_by='1h', aggregation='max'):
        query = "SELECT {_aggregation}(value) as value, metric FROM check_openvz_vm_perf WHERE hostname='{_hostname}'  AND metric='{_metric}' AND time > now() - {_period} group by time({_group_by})".format(
            _aggregation=aggregation,
            _hostname=hostname,
            _metric=metric,
            _period=period,
            _group_by=group_by
        )
        data = self.client.query(query).raw
        if data != {}:
            series = data['series'][0]
            data = get_united_columns_values(series['columns'], series['values'])
            data = get_listOfDict_without_none(data)
            convert_data_type(data, 'time', get_datetime_from_string)
            result = get_time_value_dict(data)
            return result
        return {}
