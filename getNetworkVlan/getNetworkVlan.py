import json
import requests

def getNetworkVlan (context, inputs):

    niosServer = inputs["niosServer"]
    networkView = inputs["networkView"]
    networkAddr = inputs["networkAddr"]
    usr = inputs["usr"]
    pwd = inputs["pwd"]

    #Ignora certificado caso self-signed
    requests.packages.urllib3.disable_warnings()

    #Variável de autenticação
    infobloxAuth = requests.auth.HTTPBasicAuth(usr,pwd)

    #Busca redes pelo VLAN ID
    restUrl = 'https://'+ niosServer +'/wapi/v2.11/network?network=' + networkAddr + '&network_view=' + networkView + '&_return_fields=vlans'
    r = requests.get(url=restUrl,auth=infobloxAuth,verify=False)

    vlanId = []

    if r.status_code == 200:
        rJson = r.json()

        if len(rJson) > 0:
            print(rJson[0])
            vlanId2 = [vlan['vlan'].split('/')[-1] for vlan in rJson[0]['vlans']]
            for id2 in vlanId2:
                print(id2)
        else:
            print('No data found for IP ' + networkAddr + ' in Network View ' + networkView)

    return vlanId