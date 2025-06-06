import datetime


def read_root(es,sf):
    query = {
            "bool": {
                "must": [
                    {"match": {"container_id": sf}}
                ]
            }
        }

    minmax = es.search(index="data",
                       size=0,
                       query={
                           "match_all": {}
                       }, aggs={
            "min": {
                "min": {
                    "field": "timestamp"
                }
            },
            "max": {
                "max": {
                    "field": "timestamp"
                }
            }
        })

    occurrences = es.search(index="data",
                            size=0,
                            query={
                                "match": {
                                    "container_id": sf
                                }
                            },
                            aggs={
                                "byDay": {
                                    "date_histogram": {
                                        "field": "timestamp",
                                        "calendar_interval": "1d"
                                    }
                                }
                            }
                            )

    for val in occurrences['aggregations']['byDay']['buckets']:
        val['key'] = datetime.datetime.fromtimestamp(val['key'] / 1000).strftime('%Y-%m-%d')

    return {"min": minmax['aggregations']['min']['value'],
            "max": minmax['aggregations']['max']['value'],
            "searchfor": sf,
            "agg": occurrences['aggregations']['byDay']
            }