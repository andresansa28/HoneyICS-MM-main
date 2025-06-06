import json
# "id.orig_h": "87.120.88.59"
def extractUniqueIP():
    with open("jsons/http.json") as json_file:
        data = json.load(json_file)
        ip = []
        for row in data:
            ip.append(row["id.orig_h"])
        ip = list(set(ip))
        return ip

def extractUniqueIPs7():
    with open("jsons/s7comm.json") as json_file:
        data = json.load(json_file)
        ip = []
        for row in data:
            ip.append(row["id.orig_h"])
        ip = list(set(ip))
        return ip

def extractUniqueIPmo():
    with open("jsons/modbus.json") as json_file:
        data = json.load(json_file)
        ip = []
        for row in data:
            ip.append(row["id.orig_h"])
        ip = list(set(ip))
        return ip

s= extractUniqueIP()
a = extractUniqueIPs7()
b  = extractUniqueIPmo()

print(len(s))
print(len(a))
print(len(b))
print ("*"*20)
print (len(a)+len(b)+len(s))
