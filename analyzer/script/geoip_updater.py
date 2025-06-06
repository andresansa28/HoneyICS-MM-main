import requests
import datetime
import os
import tarfile


def update_db(license_key):
    download_url = "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=" + license_key + "&suffix=tar.gz"
    old_date = int(os.path.getmtime("GeoLite2DB/GeoLite2-City.mmdb"))
    dt = datetime.datetime.now().timestamp()
    if (dt - old_date) > 604800:
        r = requests.get(download_url)
        with open("db.tar.gz", mode="wb") as file:
            file.write(r.content)
        file = tarfile.open("db.tar.gz")
        name = file.getnames()
        print(name)
        file.extract(name[0] + "/GeoLite2-City.mmdb", ".")
        os.rename(name[3], "GeoLite2DB/GeoLite2-City.mmdb")
        os.remove("db.tar.gz")
        # os.remove(name[0])
    else:
        print("GeoIP DB Already Up-To Date\n")

