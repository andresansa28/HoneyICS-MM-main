#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
KEYCLOAK_URL=https://172.17.0.1:8443
KEYCLOAK_ADMIN_LOGIN=admin
KEYCLOAK_ADMIN_PASSWORD=password

echo -n "Getting admin access token..."

ADMIN_TOKEN=$(curl -ks -X POST \
"$KEYCLOAK_URL/auth/realms/master/protocol/openid-connect/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=$KEYCLOAK_ADMIN_LOGIN" \
-d "password=$KEYCLOAK_ADMIN_PASSWORD" \
-d 'grant_type=password' \
-d 'client_id=admin-cli' | jq -r '.access_token')

if  [[ $ADMIN_TOKEN == "null" ]]; then
    echo -e "${RED} \u2717 Could not get admin token ${NC}"
    exit 1
else
    echo -e "${GREEN} \xE2\x9C\x94 ${NC}"
fi

echo -n "Creating new user..."

response=$(curl -ks -X POST \
  $KEYCLOAK_URL/auth/admin/realms/ICSConsole/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "username": "admin1",
    "enabled": true,
    "email": "admin1@gmail.com",
    "firstName": "admin1",
    "lastName": "admin1",
    "credentials": [
      {
        "type": "password",
        "value": "password",
        "temporary": false
      }
    ]
  }')

if [[ $response == "" ]]; then
    echo -e "${GREEN} \u2713 ${NC}"
    echo "Username: admin1"
    echo "Password: password"
else
    if [[ $response == *"User exists with same username"* ]]; then
        echo -n "User with username 'admin1' already exists"
        echo -e "${GREEN} \u2713 ${NC}"
    else
        echo -e "${RED} \u2717 ${NC}"
        #echo $response
    fi
fi

echo -n "Getting user id..."
json_data=$(curl -ks -X GET \
  "$KEYCLOAK_URL/auth/admin/realms/ICSConsole/users?username=admin1" \
  -H "Authorization: Bearer $ADMIN_TOKEN")

user_id=$(echo "$json_data" | jq -r '.[0].id')

if [[ $user_id == "" ]]; then
    echo -e "${RED} \u2717 ${NC}"
    exit 1
else
    echo -e "${GREEN} \u2713 ${NC}"
    #echo "id: $user_id"
fi

echo -n "Getting admin role id..."
response=$(curl -ks -X GET "$KEYCLOAK_URL/auth/admin/realms/ICSConsole/users/$user_id/role-mappings/realm/available?first=0&max=11" \
  -H "Authorization: Bearer $ADMIN_TOKEN")

admin_role_id=$(echo "$response" | jq '.[0].id' | tr -d '"')
admin_role_name=$(echo "$response" | jq '.[0].name' | tr -d '"')

if [[ $admin_role_id == "" ]]; then
    echo -e "${RED} \u2717 ${NC}"
    exit 1
else
    echo -e "${GREEN} \u2713 ${NC}"
    #echo "admin role id: $admin_role_id"
    #echo "admin role name: $admin_role_name"
fi

echo -n "Assigning admin role to user..."

response=$(curl -ks -X POST "$KEYCLOAK_URL/auth/admin/realms/ICSConsole/users/$user_id/role-mappings/realm" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H 'content-type: application/json' \
    --data-raw '[{"id":"f3f0003b-81cc-4520-9417-659483a5f3ef","name":"admin","description":"","composite":false,"clientRole":false,"containerId":"ICSConsole"}]')

if [[ $response == "" ]]; then
    echo -e "${GREEN} \u2713 ${NC}"
else
    echo -e "${RED} \u2717 ${NC}"
    echo $response
fi

echo -n "Verifying admin role assignment..."

json_data=$(curl -ks -X GET "$KEYCLOAK_URL/auth/admin/realms/ICSConsole/users/$user_id/role-mappings" \
    -H "Authorization: Bearer $ADMIN_TOKEN")

realm_mappings=$(echo "$json_data" | jq -r '.realmMappings')

for row in $(echo "${realm_mappings}" | jq -r '.[] | @base64'); do
    _jq() {
     echo ${row} | base64 --decode | jq -r ${1}
    }

    name=$(_jq '.name')

    if [ "$name" == "admin" ]; then
        echo -e "${GREEN} \u2713 ${NC}"
        break
    fi
done
