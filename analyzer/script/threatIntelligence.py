import json

import geoip2.database

from geoip2.errors import AddressNotFoundError
from opensearchpy import OpenSearch, helpers
from tqdm import tqdm
from zat.log_to_dataframe import LogToDataFrame
from requests_tor import RequestsTor
import opensearch_management

log_to_df = LogToDataFrame()


def greynoise(es, log_name, conn_dataframe):
    # GreyNoise
    df = conn_dataframe

    ips = df["id.orig_h"].unique()
    rt = RequestsTor(tor_ports=(9050,), tor_cport=9051, autochange_id=25)
    if not es.indices.exists(index=log_name):
        mapping = {
            "mappings": {
                "properties": {
                    "geo": {
                        "properties": {
                            "orig": {
                                "properties": {
                                    "point": {
                                        "type": "geo_point"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        es.indices.create(index=log_name, body=json.dumps(mapping))

    def generate_docs():
        print("Ip to analyze: " + str(len(ips)))
        for ip in tqdm(ips):
            query = {"size": 0,
                     "query":
                         {"match":
                             {
                                 "id.orig_h": "%s" % ip
                             }
                         }
                     }
            s = es.search(index=log_name, body=json.dumps(query))["hits"]["total"]["value"]
            if s == 0:
                while True:
                    url = "https://viz.greynoise.io:443/gn-api/greynoise/v3/internal/ip/" + ip
                    try:
                        r = rt.get(url)
                        if r.status_code != 403:
                            d = r.json()
                            if "message" not in d:
                                print("OK")
                                break
                    except:
                        pass
                    print("new Tor ID")
                    rt.new_id()

                noise_profile = {}
                if "error" not in d:
                    if d["metadata"]["noise"]["found"]:
                        noise_profile = d["noise_profile"]
                        if "tag_ids" in noise_profile:
                            noise_profile.pop("tag_ids")
                        noise_profile.pop("raw_data")
                        noise_profile.pop("sensor_metadata")
                        noise_profile.pop("spoofable")
                        noise_profile.pop("first_seen")
                        noise_profile.pop("last_seen")
                        noise_profile.pop("seen")
                        m = noise_profile.pop("metadata")
                        tor = m.pop("tor")
                        noise_profile["tor"] = tor
                        noise_profile["id.orig_h"] = noise_profile.pop("ip")
                        with geoip2.database.Reader('GeoLite2DB/GeoLite2-City.mmdb') as reader:
                            try:
                                response = reader.city(ip)
                                noise_profile["geo.orig.point"] = {"lat": response.location.latitude,
                                                                 "lon": response.location.longitude}
                                noise_profile["geo.orig.country"] = response.country.name
                            except AddressNotFoundError:
                                noise_profile["geo.orig.point"] = {"lat":0, "lon":0}
                                pass
                elif d["error"] == "ip not seen":
                    noise_profile = {"id.orig_h": ip, "classification": "blank"}
                doc = {
                    "_index": log_name,
                    "_source": noise_profile
                }
                yield doc

    res = helpers.bulk(es, generate_docs())
    opensearch_management.create_index_pattern(log_name, False)
    return res

# VirusTotal
