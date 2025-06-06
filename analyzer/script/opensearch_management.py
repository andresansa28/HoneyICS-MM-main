import requests
from requests.auth import HTTPBasicAuth
import json
import dashboard_management

def create_index_with_mapping(es, index_name):
    mapping = {
        "mappings": {
            "properties": {
                "geo": {
                    "properties": {
                        "orig": {
                            "properties": {
                                "city": {
                                    "type": "text",
                                    "fields": {
                                        "keyword": {
                                            "type": "keyword",
                                            "ignore_above": 256
                                        }
                                    }
                                },
                                "country_code": {
                                    "type": "text",
                                    "fields": {
                                        "keyword": {
                                            "type": "keyword",
                                            "ignore_above": 256
                                        }
                                    }
                                },
                                "point": {
                                    "type": "geo_point"
                                },
                                "region": {
                                    "type": "text",
                                    "fields": {
                                        "keyword": {
                                            "type": "keyword",
                                            "ignore_above": 256
                                        }
                                    }
                                }

                            }
                        }
                    }
                }
            }
        }
    }
    es.indices.create(index=index_name, body=json.dumps(mapping))


def create_index_pattern(index_pattern_name, with_time_field):
    tenant = index_pattern_name.split("_")[0]
    headers = {'osd-xsrf': 'true',
               'securitytenant': tenant,
               'Content-Type': 'application/json'
               }
    if with_time_field:
        payload = {
            "attributes": {
                "title": "%s" % index_pattern_name,
                "timeFieldName": "ts"
            },
        }
        r = requests.post("https://172.17.0.1:5601/api/saved_objects/index-pattern/" + index_pattern_name, verify=False,
                          auth=HTTPBasicAuth('admin', 'admin'), data=json.dumps(payload), headers=headers)
    else:
        payload = {
            "attributes": {
                "title": "%s" % index_pattern_name
            },
        }
        r = requests.post("https://172.17.0.1:5601/api/saved_objects/index-pattern/" + index_pattern_name, verify=False,
                          auth=HTTPBasicAuth('admin', 'admin'), data=json.dumps(payload), headers=headers)
    return r


def opensearch_first_setup(es, vm_hosts):
    for vm in vm_hosts:
        r = requests.get("https://172.17.0.1:9200/_plugins/_security/api/tenants/" + vm["name"], verify=False,
                         auth=HTTPBasicAuth('admin', 'admin'))

        tenant = vm["name"]

        if "status" in r.json():
            # create tenant
            headers = {'osd-xsrf': 'true',
                       'Content-Type': 'application/json'}
            payload = {"description": "A tenant for the human resources team."}
            r = requests.put("https://172.17.0.1:9200/_plugins/_security/api/tenants/" + tenant, verify=False,
                             auth=HTTPBasicAuth('admin', 'admin'), headers=headers, data=json.dumps(payload))
            print(r)
            # create role for the previous tenant
            headers = {'osd-xsrf': 'true',
                       'Content-Type': 'application/json'}
            payload = {"description": "A tenant for the human resources team."}
            r = requests.put("https://172.17.0.1:9200/_plugins/_security/api/roles/" + tenant + "_user",
                             verify=False,
                             auth=HTTPBasicAuth('admin', 'admin'), headers=headers, data=json.dumps(payload))
            print(r)
            headers = {'osd-xsrf': 'true',
                       'Content-Type': 'application/json'}

            role = {'cluster_permissions': ['indices:data/read/mget*'],
                    'index_permissions': [
                        {'index_patterns': [tenant + '*'], 'dls': '', 'fls': [], 'masked_fields': [],
                         'allowed_actions': ['search']}],
                    'tenant_permissions': [
                        {'tenant_patterns': [str(tenant)], 'allowed_actions': ['kibana_all_read']}]
                    }
            r = requests.put("https://172.17.0.1:9200/_plugins/_security/api/roles/" + tenant + "_user",
                             verify=False,
                             auth=HTTPBasicAuth('admin', 'admin'), headers=headers, data=json.dumps(role))
            print(r)
            back_end_role = {
                "backend_roles": [tenant],
            }
            r = requests.put("https://172.17.0.1:9200/_plugins/_security/api/rolesmapping/" + tenant + "_user",
                             verify=False,
                             auth=HTTPBasicAuth('admin', 'admin'), headers=headers, data=json.dumps(back_end_role))
            print(r)

            #UPLOAD DASHBOARDS
            dashboard_management.upload_dashboards(es, tenant)
    
        
