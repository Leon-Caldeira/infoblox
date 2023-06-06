from datetime import date
import json
import requests

def ipVlanIdRecord (context, inputs):

    niosServer = inputs["niosServer"]
    networkView = inputs["networkView"]
    hostName = inputs["hostName"]
    vlanID = inputs["vlanID"]
    usr = inputs["usr"]
    pwd = inputs["pwd"]
    attrEnv = inputs["attrEnv"]
    requestedBy = inputs["requestedBy"]
    projectName = inputs["projectName"]

    #Ignora certificado caso self-signed
    requests.packages.urllib3.disable_warnings()

    #Variável de autenticação
    infobloxAuth = requests.auth.HTTPBasicAuth(usr,pwd)

    #Calcula a data atual
    currentDate = date.today().strftime("%d/%m/%Y")

    #Parâmetro de Headers
    paramHeaders = {'Content-Type':"application/json"}

    #Busca redes pelo VLAN ID
    restUrl = 'https://'+ niosServer +'/wapi/v2.11/vlan?id='+ vlanID +'&_return_fields=assigned_to'
    r = requests.get(url=restUrl,auth=infobloxAuth,verify=False)
    rJson = r.json()
    mainCIDR = []

    for i in range(0,len(rJson)):
        if 'assigned_to' in rJson[i]:
            secondaryCIDR = rJson[i]['assigned_to'][0].split(':')
            secondaryCIDR = secondaryCIDR[1].split('/')
            del secondaryCIDR[-1]
            mainCIDR.append(secondaryCIDR[0] +'/'+ secondaryCIDR[1])

    #Busca nas redes o atributo de Ambiente

    for i in range(0,len(mainCIDR)):
        restUrl = 'https://'+ niosServer +'/wapi/v2.11/network?network='+ mainCIDR[i] +'&_return_fields=extattrs'
        r = requests.get(url=restUrl,auth=infobloxAuth,verify=False)
        rJson = r.json()
        print(rJson)

        if attrEnv in rJson[0]['extattrs']['Ambiente']['value']:
            networkGet = mainCIDR[i]
            print(networkGet)
            break

    #Pega próximo IP disponível
    restUrl = 'https://' + niosServer + '/wapi/v2.11/network?network=' + networkGet + '&network_view=' + networkView
    try:
        r = requests.get(url=restUrl,auth=infobloxAuth,verify=False)
        rJson = r.json()
        if r.status_code == 200:
            if len(rJson) > 0:
                netRef = rJson[0]['_ref']
                restUrl = 'https://' + niosServer + '/wapi/v2.11/' + netRef + '?_function=next_available_ip&num=1'
                r = requests.post(url=restUrl, auth=infobloxAuth, verify=False)
                rJson = r.json()
                if r.status_code == 200:
                    ipAddr = rJson['ips'][0]
    except ValueError:
        raise Exception(r)
    except Exception:
        raise
            
    #Registra hostname
    restUrl = 'https://' + niosServer + '/wapi/v2.11/record:host?_return_fields=ipv4addrs'
    dataPayload = '{"ipv4addrs": [{"configure_for_dhcp": false,"ipv4addr": "'+ ipAddr +'"}],"name": "'+ hostName +'","configure_for_dns": false,"view": "'+ networkView +'"}'

    r = requests.post(url=restUrl,auth=infobloxAuth,verify=False,data=dataPayload)
    
    #Adiciona informações de atributos extensíveis
    urlGet = 'https://'+ niosServer +'/wapi/v2.11/record:host?ipv4addr='+ ipAddr
    getRecord = requests.get(url=urlGet,auth=infobloxAuth,headers=paramHeaders,verify=False)
    refJson = getRecord.json()
    refHost = refJson[0]['_ref']
    print(refHost)
    putUrl = 'https://'+ niosServer +'/wapi/v2.11/'+ refHost

    putPayload = {"extattrs":
        {
        "Solicitante": {
            "value": requestedBy},
        "Projeto/Juncao" : {
            "value": projectName},
        "Data_VRA": {
            "value" : currentDate},
        "Alocado por" : {"value" : "VRA"}
        }
    }

    r = requests.put(url=putUrl,auth=infobloxAuth,headers=paramHeaders,verify=False,json=putPayload)
    print(r.status_code)
    print(r.json())

    
    networkMask = networkGet.split('/')
    ipAddr = ipAddr +'/'+ networkMask[1]
    print('ipAddr: '+ ipAddr)
    return ipAddr