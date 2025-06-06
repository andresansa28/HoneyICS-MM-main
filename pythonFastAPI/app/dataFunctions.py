from geoip2.errors import AddressNotFoundError
from opensearchpy import OpenSearch, helpers
import csv
import json
import geoip2.database


def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []

    # read csv file
    with open(csvFilePath, encoding='utf-8') as csvf:
        # load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf)

        # convert each csv row into python dict
        for row in csvReader:
            # add this python dict to json array
            jsonArray.append(row)

    # convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)


def create_new_index(es, index_name, mapping):
    res = es.indices.create(index=index_name, body=mapping)
    return res


def upload_bulk_data(es, index_name, data):
    csv_to_json("../code/app/" + data, "../code/app/dataset1.json")

    def generate_docs():
        with open("../code/app/dataset1.json") as fi:
            reader = json.load(fi)
            for row in reader:
                with geoip2.database.Reader('../code/app/GeoLite2DB/GeoLite2.mmdb') as reader:
                    try:
                        response = reader.city(row["src_ip"])
                        row["src_ip_point"] = {"lat": response.location.latitude,
                                               "lon": response.location.longitude}
                        row["src_ip_country"] = response.country.name
                    except AddressNotFoundError:
                        row["point"] = [0, 0]
                        pass

                    doc = {
                        "_index": index_name,
                        "_source": row
                    }
                    yield doc

    res = helpers.bulk(es, generate_docs())
    return res
