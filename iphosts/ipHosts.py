from datetime import date
import requests

# Desativa avisos para certificados auto-assinados
requests.packages.urllib3.disable_warnings()

def ipHosts(context, inputs):

    # Tratamento de variáveis
    infobloxAuth = requests.auth.HTTPBasicAuth(inputs["usr"], inputs["pwd"])
    niosServer = inputs["niosServer"]
    networkView = inputs["networkView"]
    hostName = inputs["hostName"]
    attrs = ["*Ambiente="+ inputs["attrEnv"], "*Localizacao="+ inputs["attrLoc"], "*SubAmbiente="+ inputs["attrSub"]]
    networks = ["Dados", "NOC", "SOC", "Backup"]
    nets = [inputs["netData"], inputs["netNoc"], inputs["netSoc"], inputs["netBackup"]]
    ips = ['{{ipData}}', '{{ipNoc}}', '{{ipSoc}}', '{{ipBackup}}']
    ipAddr = []

    # Repetidor de adição para cada tipo de Rede
    for net, network, ip in zip(nets, networks, ips):
        if net:
            restUrl = f'https://{niosServer}/wapi/v2.11/network?{"&".join(attrs)}&*Rede={network}&*Ambiente Cloud=NAO&network_view={networkView}'
            r = requests.get(url=restUrl, auth=infobloxAuth, verify=False)
            r.raise_for_status()
            rJson = r.json()
            if rJson:
                networkRef = rJson[0]['_ref']
                netMask = networkRef.split('/')
                if networkRef:
                    
                    #Gera o próximo IP disponível
                    ip = getNextIp(infobloxAuth, niosServer, networkRef)
                    
                    #Registra o Hostname
                    registerHostname(infobloxAuth, niosServer, networkView, hostName, ip)

                    # Determina a máscara do IP registrado
                    ipMask = f'{ip}/{netMask[-2]}'
                    ipAddr.append(ipMask)

                    # Calcula a data atual
                    currentDate = date.today().strftime("%d/%m/%Y")

                    # Adiciona a informação de atributos extensíveis
                    addExtendedAttributes(infobloxAuth, niosServer, inputs["requestedBy"], inputs["projectName"], currentDate, ip)
            else:
                print(f"Não foi possível encontrar uma Rede {network} com tais características")

                # Adiciona um valor exemplo caso não exista endereço de IP disponível
                if network in networks:
                    index = networks.index(network)
                    if index < len(ips):
                        ip = ips[index]
                ipAddr.append(ip)

    ipAddr = ','.join(ipAddr)
    print(f'IPs Finais: {ipAddr}')
    return ipAddr

def getNextIp(infobloxAuth, niosServer, networkRef):
    restUrl = f'https://{niosServer}/wapi/v2.11/{networkRef}?_function=next_available_ip&num=1'
    r = requests.post(url=restUrl, auth=infobloxAuth, verify=False)
    return r.json()['ips'][0]

def registerHostname(infobloxAuth, niosServer, networkView, hostName, ip):
    restUrl = f'https://{niosServer}/wapi/v2.11/record:host?_return_fields=ipv4addrs'
    payload = '{"ipv4addrs": [{"configure_for_dhcp": false,"ipv4addr": "' + ip + '"}],"name": "' + hostName + '","configure_for_dns": false,"view": "' + networkView + '"}'
    r = requests.post(url=restUrl, auth=infobloxAuth, verify=False, data=payload)

def addExtendedAttributes(infobloxAuth, niosServer, requestedBy, projectName, currentDate, ip):
    paramHeaders = {'Content/Type':"application/json"}
    putPayload = {"extattrs": {"Solicitante": {"value": requestedBy},
                               "Projeto": {"value": projectName},
                                "Data da Solicitação": {"value": currentDate}}}
    urlGet = f'https://{niosServer}/wapi/v2.11/record:host?ipv4addr={ip}'
    getRecord = requests.get(url=urlGet,auth=infobloxAuth,headers=paramHeaders,verify=False)
    refHost = getRecord.json()[0]['_ref']
    putUrl = f'https://{niosServer}/wapi/v2.11/{refHost}'
    r = requests.put(url=putUrl, auth=infobloxAuth, headers=paramHeaders, json=putPayload, verify=False)