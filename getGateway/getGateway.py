import requests
import ipaddress

# Desativa avisos para certificados auto-assinados
requests.packages.urllib3.disable_warnings()

def validateIp(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def getGateway(context, inputs):
    # Tratamento de variáveis
    infobloxAuth = requests.auth.HTTPBasicAuth(inputs["usr"], inputs["pwd"])
    niosServer = inputs["niosServer"]
    ipAddr = inputs["ipAddr"]
    print(ipAddr)
    networkOptions = []

    # Tratamento da variável de entrada
    for i in range(len(ipAddr)):
        ipAddr[i] = ipAddr[i].split(',')
    
    for i in range(len(ipAddr)):
        for j in range(len(ipAddr[i])):
            ipAddr[i][j] = ipAddr[i][j].split('/',1)[0]

    for ipArray in ipAddr:
        optionsForThisArray = []
        for ip in ipArray:
            if not validateIp(ip):
                optionsForThisArray.append("")  # adicionado um valor vazio se o IP não for válido
                continue
            
            hostGateway = 'Nenhum'
            dnsRecord = 'Nenhum'
            portGroup = 'Nenhum'

            # Dados do host
            restUrl = f'https://{niosServer}/wapi/v2.11/ipv4address?ip_address={ip}&network_view=REDES_LOCAIS'
            r = requests.get(url=restUrl, auth=infobloxAuth, verify=False)
            print('Dados do host')
            print(r.json()[0])
            hostNetwork = r.json()[0]['network']

            # Pega o atributo extensível Port Group
            restUrl = f'https://{niosServer}/wapi/v2.11/network?network={hostNetwork}&network_view=REDES_LOCAIS&_return_fields=network,extattrs'
            r = requests.get(url=restUrl, auth=infobloxAuth, verify=False)
            print('Port Group')
            print(r.json()[0])
            if 'Port Group' in r.json()[0]['extattrs']:
                portGroup = r.json()[0]['extattrs']['Port Group']['value']

            # Realizar a pesquisa pelo router/gateway do host
            restUrl = f'https://{niosServer}/wapi/v2.11/network?network={hostNetwork}&_return_fields=options'
            r = requests.get(url=restUrl, auth=infobloxAuth, verify=False)
            print('Pesquisa pelo Router')
            print(r.json()[0])

            for item in r.json()[0]['options']:
                if item['name'] == 'routers':
                    hostGateway = item['value']
                if item['name'] == 'domain-name-servers':
                    dnsRecord = item['value']

            print(f'O gateway padrão para o host com o IP {ip} é {hostGateway}')
            print(f'O DNS para o host com IP {ip} é {dnsRecord}')

            optionsForThisArray.append(f'<br>GW: {hostGateway}<br>DNS: {dnsRecord}<br>Port Group: {portGroup}')

        networkOptions.append(",".join(optionsForThisArray))

    print(networkOptions)
    return networkOptions
