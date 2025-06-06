import json
import os
import sys
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi_keycloak import FastAPIKeycloak, KeycloakError, OIDCUser
from opensearchpy import OpenSearch, helpers
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

sys.path.append(os.path.abspath("../code/app/"))
import sslpatch, osQueryFile, dataFunctions

with sslpatch.no_ssl_verification():
    idp = FastAPIKeycloak(
        server_url="https://172.17.0.1:8443/auth",
        client_id="fastAPI",
        client_secret="secret",
        admin_client_secret="secret",
        realm="ICSConsole",
        callback_uri="http://localhost:5000/callback"
    )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth = ('admin', 'admin')  # For testing only. Don't store credentials in code.
ca_certs_path = '../code/app/ca/admin.pem'  # Provide a CA bundle if you use intermediate CAs with your root CA.

es = OpenSearch(
    [{'host': '172.17.0.1', 'port': 9200}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    ca_certs=ca_certs_path,
)


def checkTokenValidity(token):
    with sslpatch.no_ssl_verification():
        if not idp.token_is_valid(token):
            raise "credential_exception"


def checkTokenAndRoleValidity(token, role):
    with sslpatch.no_ssl_verification():
        if not idp.token_is_valid(token):
            raise "credential_exception"
        else:
            if not idp.get_user_roles(token) == role:
                raise "role_exception"


app = FastAPI()
idp.add_swagger_config(app)

origins = [
    "http://localhost",
    "http://localhost:5002",
    "http://172.17.0.1:5002"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return es.info()

@app.get("/test")
def user_roles(token: Annotated[str, Depends(oauth2_scheme)]):
    return idp._decode_token(token)


class User(BaseModel):
    username: str
    last_name: str
    first_name: str
    email: str
    password: str


class UserGroup(BaseModel):
    user_id: str
    group_name: str


@app.get("/users", tags=["user-management"])
def get_users(user: OIDCUser = Depends(idp.get_current_user(required_roles=["admin"]))):
    with sslpatch.no_ssl_verification():
        return idp.get_all_users()


@app.get("/groups", tags=["user-groups"])
def get_groups():
    with sslpatch.no_ssl_verification():
        return idp.get_all_groups()


@app.get("/user/group/", tags=["user-groups"])
def get_user_group(user_id: str):
    with sslpatch.no_ssl_verification():
        return idp.get_user_groups(user_id)


@app.post("/user/group/add/", tags=["user-groups"])
def add_group_to_user(item: UserGroup):
    with sslpatch.no_ssl_verification():
        group_id = idp.get_groups([item.group_name])[0].id
        return idp.add_user_group(user_id=item.user_id, group_id=group_id)


@app.post("/user/create/", tags=["user-management"])
def create_user(item: User, user: OIDCUser = Depends(idp.get_current_user(required_roles=["admin"]))):
    with sslpatch.no_ssl_verification():
        return idp.create_user(username=item.username, first_name=item.first_name, last_name=item.last_name,
                               email=item.email, password=item.password, send_email_verification=False)


@app.delete("/user/delete/", tags=["user-management"])
def delete_user(user_id: str, user: OIDCUser = Depends(idp.get_current_user(required_roles=["admin"]))):
    with sslpatch.no_ssl_verification():
        return idp.delete_user(user_id=user_id)


@app.exception_handler(KeycloakError)
async def keycloak_exception_handler(request: Request, exc: KeycloakError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.reason},
    )
