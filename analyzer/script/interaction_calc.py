import json

import numpy as np
from opensearchpy import OpenSearch, helpers
import opensearch_management
import pandas as pd
from tqdm import tqdm
import uuid

bounds = {'http': 30 * 60, 'modbus': 1, 's7comm': 1, 'http_plc': 5}
protocols = ["http", "s7comm", "ssh", "rdp", "modbus", "kerberos"]

def support_index(es, deploy, df1, protocol):
    r = ""
    if protocol == "http":
        for (container_name), group in df1.groupby("container_name"):
            if "HMI_PLC" in container_name:
                time_delta = pd.Timedelta(seconds=5)
                r = split_sessions_start_time(es, deploy, protocol, group, time_delta)
            else:
                time_delta = pd.Timedelta(seconds=bounds[protocol])
                r = split_sessions_start_time(es, deploy, protocol, group, time_delta)
    else:
        time_delta = pd.Timedelta(seconds=bounds[protocol])
        r = split_sessions_start_time(es, deploy, protocol, df1, time_delta)
    # upload_requests_to_index(es, deploy, protocol, dataframe)
    return r

def split_sessions_start_time(es, deploy, protocol, frame, time_delta):
    # Sort the DataFrame
    frame.sort_values(['id.orig_h', 'id.resp_h', 'id.orig_p', 'id.resp_p', 'ts'], inplace=True)

    sessions = []

    # Group by source and destination
    for (src, dst, srcp, dstp), group in tqdm(frame.groupby(['id.orig_h', 'id.resp_h', 'id.orig_p', 'id.resp_p']), leave=False):
        if group.empty:
            continue

        session = []
        last_time = group.iloc[0]['ts']

        for _, row in group.iterrows():

            intel = get_ip_intel(es, deploy, row["id.orig_h"])
            # intel = get_ip_intel(es, "deploy1", row["id.orig_h"])
            if intel is not None and "classification" in intel:
                row["classification"] = intel["classification"]
                if "actor" in intel:
                    row["actor"] = intel["actor"]
                else:
                    row["actor"] = "unknown"
                if "geo.orig.point" in intel:
                    row["geo.orig.point"] = intel["geo.orig.point"]
            row["service"] = protocol

            if row['ts'] > last_time + time_delta:
                sessions.append(pd.DataFrame(session))
                session = []

            last_time = row['ts']
            session.append(row)

        if session:
            sessions.append(pd.DataFrame(session))

    r = upload_sessions_to_index2(es, deploy, sessions)
    return r

def get_ip_intel(es, deploy, ip):
    query = {
        "query":
            {"match":
                {
                    "id.orig_h": "%s" % ip
                }
            }
    }
    s = es.search(index="deploy1" + "_intel", body=json.dumps(query))["hits"]["hits"]
    if len(s) != 0:
        return s[0]["_source"]
    else:
        return None


def upload_sessions_to_index2(es, deploy, sessions):
    r = {}

    def generate_docs():
        for session in sessions:
            uid = uuid.uuid4()
            s = {}
            # session.sort_values(['id.orig_h', 'id.resp_h', 'id.orig_p', 'id.resp_p', 'ts'], inplace=True)
            f = session.iloc[0]
            # r[f["uid"]] = uid
            s["ts"] = f["ts"]
            s["id.orig_h"] = f["id.orig_h"]
            s["id.orig_p"] = f["id.orig_p"]
            s["id.resp_h"] = f["id.resp_h"]
            s["id.resp_p"] = f["id.resp_p"]
            if "service" in f:
                s["service"] = f["service"]
            else:
                s["service"] = None

            if "container_name" in f:
                s["container_name"] = f["container_name"]
            else:
                s["container_name"] = None

            if "classification" in f:
                s["classification"] = f["classification"]
            else:
                s["classification"] = "unknown"

            if "actor" in f:
                s["actor"] = f["actor"]
            else:
                s["actor"] = "unknown"

            if "geo.orig.point" in f:
                s["geo.orig.point"] = f["geo.orig.point"]
            else:
                s["geo.orig.point"] = None

            if "geo.orig.country" in f:
                s["geo.orig.country"] = f["geo.orig.country"]
            else:
                s["geo.orig.country"] = None

            s["request_id"] = uid
            s["session_complexity"] = len(session.index)
            s["session_duration"] = str(session.iloc[-1]["ts"] - session.iloc[0]["ts"])
            doc = {
                "_index": deploy + "_interactions",
                "_source": s
            }
            yield doc

    helpers.bulk(es, generate_docs())
    opensearch_management.create_index_pattern(deploy + "_interactions", True)
    return r


def upload_requests_to_index(es, deploy, service, data):
    def generate_docs():
        for idx, row in data.iterrows():
            new_row = {}
            row = row.replace(np.nan, None)
            row = row.to_dict()
            if "uid" in row:
                new_row["uid"] = row["uid"]
            else:
                new_row["uid"] = None
            new_row["id.orig_h"] = row["id.orig_h"]
            new_row["id.resp_h"] = row["id.resp_h"]
            new_row["id.orig_p"] = row["id.orig_p"]
            new_row["id.resp_p"] = row["id.resp_p"]
            new_row["container_name"] = row["container_name"]
            new_row["service"] = service
            new_row["ts"] = row["ts"]
            doc = {
                "_index": deploy + "_requests",
                "_source": new_row
            }
            yield doc

    res = helpers.bulk(es, generate_docs())
    opensearch_management.create_index_pattern(deploy + "_requests", False)
