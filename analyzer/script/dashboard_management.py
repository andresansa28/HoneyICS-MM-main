import json
import requests
from requests.auth import HTTPBasicAuth
from tqdm import tqdm
from opensearchpy import OpenSearch


def getDashboardID(es, tenant):
    es.transport.connection_pool.connection.headers.update(
        {'securitytenant': tenant})
    body = '''
                {
      "_source": [
        "dashboard.title"
      ],
      "query": {
       "term": {
          "dashboard.title": "dashboard"
        }
      } 
    }
'''
    print(es.search(index=".kibana", body=body)['hits']['hits'][0]['_id'].split(':')[1])


def upload_dashboards(es, tenant):
    headers = {'osd-xsrf': 'true',
               'securitytenant': tenant,
               }
    file = {
        'file': open('DashBoards/graphicdash.ndjson', 'rb')
    }
    r1 = requests.post("https://172.17.0.1:5601/api/saved_objects/_import", verify=False,
                       auth=HTTPBasicAuth('admin', 'admin'), headers=headers, files=file)
    file = {
        'file': open('DashBoards/tabulardash.ndjson', 'rb')
    }
    r2 = requests.post("https://172.17.0.1:5601/api/saved_objects/_import", verify=False,
                       auth=HTTPBasicAuth('admin', 'admin'), headers=headers, files=file)

    if r1.json()["success"] and r2.json()["success"]:
        es.transport.connection_pool.connection.headers.update({'securitytenant': tenant})
        body = {
            "_source": [
                "visualization.title"
            ],
            "size": 1000,
            "query": {
                "match_all": {}
            }
        }
        l = es.search(index=".kibana", body=json.dumps(body))['hits']['hits']

        v_id = []
        for i in l:
            if "visualization" in i["_id"]:
                v_id.append(i["_id"].split(":")[1])

            if "index-pattern" in i["_id"]:
                ids = (i["_id"].split(":")[1])
                r = requests.delete('https://172.17.0.1:5601/api/saved_objects/index-pattern/' + ids, verify=False,
                                    auth=HTTPBasicAuth('admin', 'admin'), headers=headers)

        headers = {'osd-xsrf': 'true',
                   'securitytenant': tenant,
                   'Content-Type': 'application/json'
                   }

        for id in tqdm(v_id):
            r = requests.get("https://172.17.0.1:5601/api/saved_objects/visualization/" + str(id), verify=False,
                             auth=HTTPBasicAuth('admin', 'admin'), headers=headers)
            resp = r.json()
            for r in resp["references"]:
                r["id"] = tenant + "_" + r["id"].split("_")[1]
            resp.pop("id")
            resp.pop("type")
            resp.pop("namespaces")
            resp.pop("updated_at")
            resp.pop("version")
            resp.pop("migrationVersion")
            r = requests.put("https://172.17.0.1:5601/api/saved_objects/visualization/" + str(id), verify=False,
                             auth=HTTPBasicAuth('admin', 'admin'), headers=headers, data=json.dumps(resp))
        print("Import complete")

