from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
import subprocess
import json
from fastapi.middleware.cors import CORSMiddleware
import paramiko


app = FastAPI()

origins = [
    "http://172.17.0.1:4200/**",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    #ls
    result = subprocess.run(["ls", "-l"])
    return {"message": result.stdout}

@app.get("/getInfo")
def read_info():
    result = subprocess.run(["ls", "-l"])
    info =  result.stdout
    return {"message": info["delay"]}

@app.get("/getConfig", response_class=PlainTextResponse)
def read_file():
    try:
        with open("./Config.json", "r") as file:
            file_content = file.read()
        
        return file_content
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")


@app.get("/change_delay/{delay}", response_class=JSONResponse)
async def change_delay(delay: int):
    try:
        with open("./Config.json", 'r') as file:
            data = json.load(file)

        if "delay" in data:
            data["delay"] = delay

        with open("./Config.json", 'w') as file:
            json.dump(data, file, indent=2)

        return JSONResponse({"message": "Delay changed successfully"})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
@app.get("/change_key/{key}", response_class=JSONResponse)
async def change_key(key: str):
    try:
        with open("./Config.json", 'r') as file:
            data = json.load(file)

        if "MaxMind_GeoDB_Key" in data:
            data["MaxMind_GeoDB_Key"] = key

        with open("./Config.json", 'w') as file:
            json.dump(data, file, indent=2)

        return JSONResponse({"message": "MaxMind_GeoDB_Key changed successfully"})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
@app.post("/removeDeploy", response_class=JSONResponse)
async def removeDeploy(body: dict):
    try:
        with open("./Config.json", 'r') as file:
            data = json.load(file)

        for el in data["RemoteDeployments"]:
            for ip in body["ips"]:
                if el["IP"] == ip:
                    data["RemoteDeployments"].remove(el)
                    break
        

        with open("./Config.json", 'w') as file:
            json.dump(data, file, indent=2)

        return JSONResponse({"message": "Deployments removed successfully"})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
@app.post("/addDeploy", response_class=JSONResponse)
async def addDeploy(deploy: dict):
    try:
        with open("./Config.json", 'r') as file:
            data = json.load(file)

        data["RemoteDeployments"].append(deploy)

        with open("./Config.json", 'w') as file:
            json.dump(data, file, indent=2)

        return JSONResponse({"message": "Deployments added successfully"})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

def esegui_ping(host, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=username, password=password)
        comando_ping = "ping -c 4 google.com"  
        stdin, stdout, stderr = ssh.exec_command(comando_ping)
        output_ping = stdout.read().decode('utf-8')
        return output_ping
    except Exception as e:
        print(f"Errore durante la connessione SSH: {e}")
    finally:
        ssh.close()

@app.get("/checkDeployments")
async def checkDeployments():
    try:
        with open("./Config.json", 'r') as file:
            data = json.load(file)

        for el in data["RemoteDeployments"]:
            # ssh to ip and check if analyzer is running with ping command to ip with subprocess
            result = subprocess.run(["ping", "-c", "1", el["IP"]], stdout=subprocess.PIPE)

            if result.stdout != b"active\n":
                data["RemoteDeployments"].remove(el)
        
        with open("./Config.json", 'w') as file:
            json.dump(data, file, indent=2)
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/rebootAnalyzer/{ip}")
async def rebootAnalyzer(ip: str):
    try:
        with open("./Config.json", 'r') as file:
            data = json.load(file)

        for el in data["RemoteDeployments"]:
            if el["IP"] == ip:
                # ssh to ip and reboot
                result = subprocess.run(["docker-compose", "down", "analyzer", "-d"])
                break

        with open("./Config.json", 'w') as file:
            json.dump(data, file, indent=2)

        return JSONResponse({"message": "Rebooting analyzer"})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")