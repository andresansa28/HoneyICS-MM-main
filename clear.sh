#!/bin/bash
GREEN='\033[0;32m'
NC='\033[0m'

docker compose down

CONTAINERS=$(docker ps -a --format '{{.Names}}' | grep -E '^(honey|dashboard|os|keyclock)') #containers con nomi "plc...", "simulations...", "scada-lts...", "mysql..."
NETWORKS=$(docker network ls --format '{{.Name}}' | grep -E '^(honey)') #reti con nomi "control_net..., supervisory_net..., scada-lts..."

#ferma e rimuove tutti i container con nomi "plc...", "simulations...", etc.
for c in $CONTAINERS; do
  docker stop "$c" > /dev/null 2>&1
  docker rm "$c" > /dev/null 2>&1
  echo -e " ${GREEN}✔${NC} Container $c ${GREEN}Stopped${NC} and ${GREEN}Removed${NC}"
done

#docker compose down
#docker rmi simulpy

for n in $NETWORKS; do  #rimuove tutte le reti docker "control_net...", etc.
  docker network rm "$n" > /dev/null 2>&1
  echo -e " ${GREEN}✔${NC} Network $n ${GREEN}Removed${NC}"
done

#sudo ip link delete macvlan-shim

#Pulisci le regole iptables
#sudo iptables -t nat -D PREROUTING -p tcp --dport 102 -j REDIRECT --to-port 1102
#sudo iptables -t nat -D POSTROUTING -p tcp -d 172.25.0.4 --dport 102 -j SNAT --to-source 172.25.0.6

