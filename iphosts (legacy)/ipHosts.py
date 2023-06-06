from datetime import date
from operator import truediv
import requests 



def ipHosts (context, inputs):

    niosServer = inputs["niosServer"]
    networkView = inputs["networkView"]
    usr = inputs["usr"]
    pwd = inputs["pwd"]
    requestedBy = inputs["requestedBy"]
    projectName = inputs["projectName"]
    hostName = inputs["hostName"]
    attrEnv = inputs["attrEnv"]
    attrLoc = inputs["attrLoc"]
    attrSub = inputs["attrSub"]
    netData = inputs["netData"]
    netNoc = inputs["netNoc"]
    netSoc = inputs["netSoc"]
    netBackup = inputs ["netBackup"]

    #Tratamento de Variáveis
    attrEnv = "*Ambiente="+ attrEnv
    attrLoc = "&*Localizacao="+ attrLoc
    attrSub = "&*SubAmbiente="+ attrSub

    ipData = '{{ipData}}'
    ipNoc = '{{ipNoc}}'
    ipSoc = '{{ipSoc}}'
    ipBackup = '{{ipBackup}}'

    networksData = []
    networksNOC = []
    networksSOC = []
    networksBackup = []

    #Ignora certificado caso self-signed
    requests.packages.urllib3.disable_warnings()

    #Determina Redes de Dados
    if (netData == True):
        rNet = True
        rest_url = 'https://' + niosServer + '/wapi/v2.11/network?' + attrEnv + attrLoc + attrSub + '&*Rede=Dados&*Ambiente Cloud=NAO&network_view=' + networkView
        try:
            infobloxAuth = requests.auth.HTTPBasicAuth(usr,pwd)
            r = requests.get(url=rest_url, auth=infobloxAuth, verify=False)
            r_json = r.json()
            print(r_json)
            if r.status_code == 200:
                if len(r_json) > 0:
                    for network in r_json:
                        if 'network' in network:
                            networksData.append(network['network'])
                    print('Redes Dados: ' + ','.join(map(str,networksData)))
                else:
                    print("Não foi possível encontrar uma Rede Dados com tais características")
                    rNet = False
        except ValueError:
            raise Exception(r)
        except Exception:
            raise
        
        #Pega próximo IP disponível
        if rNet == True:
            rest_url = 'https://' + niosServer + '/wapi/v2.11/network?network=' + networksData[0] + '&network_view=' + networkView
            try:
                r = requests.get(url=rest_url,auth=infobloxAuth,verify=False)
                r_json = r.json()
                if r.status_code == 200:
                    if len(r_json) > 0:
                        net_ref = r_json[0]['_ref']
                        rest_url = 'https://' + niosServer + '/wapi/v2.11/' + net_ref + '?_function=next_available_ip&num=1'
                        r = requests.post(url=rest_url, auth=infobloxAuth, verify=False)
                        r_json = r.json()
                        if r.status_code == 200:
                            ipData = r_json['ips'][0]
                            print('ipData: '+ ipData)
            except ValueError:
                raise Exception(r)
            except Exception:
                raise
            
            #Registra hostname
            rest_url = 'https://' + niosServer + '/wapi/v2.11/record:host?_return_fields=ipv4addrs'
            payload = '{"ipv4addrs": [{"configure_for_dhcp": false,"ipv4addr": "' + ipData + '"}],"name": "' + hostName + '","configure_for_dns": false,"view": "' + networkView + '"}'

            try:
                r = requests.post(url=rest_url,auth=infobloxAuth,verify=False,data=payload)
                r_json = r.json()
            except ValueError:
                raise Exception(r)
            except Exception:
                raise
        else:
            print('Erro desconhecido')

    #Determina redes NOC

    if (netNoc == True):
        rNet = True
        rest_url = 'https://' + niosServer + '/wapi/v2.11/network?' + attrEnv + attrLoc + attrSub + '&*Rede=NOC&*Ambiente Cloud=NAO&network_view=' + networkView
        try:
            infobloxAuth = requests.auth.HTTPBasicAuth(usr,pwd)
            r = requests.get(url=rest_url, auth=infobloxAuth, verify=False)
            r_json = r.json()
            if r.status_code == 200:
                if len(r_json) > 0:
                    for network in r_json:
                        if 'network' in network:
                            networksNOC.append(network['network'])
                    print('Redes NOC: ' + ','.join(map(str,networksNOC)))
                else:
                    print("Não foi possível encontrar uma Rede NOC com tais características")
                    rNet = False
        except ValueError:
            raise Exception(r)
        except Exception:
            raise

        #Pega próximo IP disponível
        if rNet == True:
            rest_url = 'https://' + niosServer + '/wapi/v2.11/network?network=' + networksNOC[0] + '&network_view=' + networkView
            try:
                r = requests.get(url=rest_url,auth=infobloxAuth,verify=False)
                r_json = r.json()
                if r.status_code == 200:
                    if len(r_json) > 0:
                        net_ref = r_json[0]['_ref']
                        rest_url = 'https://' + niosServer + '/wapi/v2.11/' + net_ref + '?_function=next_available_ip&num=1'
                        r = requests.post(url=rest_url, auth=infobloxAuth, verify=False)
                        r_json = r.json()
                        if r.status_code == 200:
                            ipNoc = r_json['ips'][0]
                            print('ipNoc: '+ ipNoc)
            except ValueError:
                raise Exception(r)
            except Exception:
                raise
            
            #Registra hostname
            rest_url = 'https://' + niosServer + '/wapi/v2.11/record:host?_return_fields=ipv4addrs'
            payload = '{"ipv4addrs": [{"configure_for_dhcp": false,"ipv4addr": "' + ipNoc + '"}],"name": "' + hostName + '","configure_for_dns": false,"view": "' + networkView + '"}'

            try:
                r = requests.post(url=rest_url,auth=infobloxAuth,verify=False,data=payload)
                r_json = r.json()
            except ValueError:
                raise Exception(r)
            except Exception:
                raise
        else:
            print('Erro desconhecido')

    #Determina redes SOC

    if (netSoc == True):
        rNet = True
        rest_url = 'https://' + niosServer + '/wapi/v2.11/network?' + attrEnv + attrLoc + attrSub + '&*Rede=SOC&*Ambiente Cloud=NAO&network_view=' + networkView
        try:
            infobloxAuth = requests.auth.HTTPBasicAuth(usr,pwd)
            r = requests.get(url=rest_url, auth=infobloxAuth, verify=False)
            r_json = r.json()
            if r.status_code == 200:
                if len(r_json) > 0:
                    for network in r_json:
                        if 'network' in network:
                            networksSOC.append(network['network'])
                    print('Redes SOC: ' + ','.join(map(str,networksSOC)))
                else:
                    print("Não foi possível encontrar uma Rede SOC com tais características")
                    rNet = False
        except ValueError:
            raise Exception(r)
        except Exception:
            raise

        #Pega próximo IP disponível
        if rNet == True:
            rest_url = 'https://' + niosServer + '/wapi/v2.11/network?network=' + networksSOC[0] + '&network_view=' + networkView
            try:
                r = requests.get(url=rest_url,auth=infobloxAuth,verify=False)
                r_json = r.json()
                if r.status_code == 200:
                    if len(r_json) > 0:
                        net_ref = r_json[0]['_ref']
                        rest_url = 'https://' + niosServer + '/wapi/v2.11/' + net_ref + '?_function=next_available_ip&num=1'
                        r = requests.post(url=rest_url, auth=infobloxAuth, verify=False)
                        r_json = r.json()
                        if r.status_code == 200:
                            ipSoc = r_json['ips'][0]
                            print('ipSoc: '+ ipSoc)
            except ValueError:
                raise Exception(r)
            except Exception:
                raise
            
            #Registra hostname
            rest_url = 'https://' + niosServer + '/wapi/v2.11/record:host?_return_fields=ipv4addrs'
            payload = '{"ipv4addrs": [{"configure_for_dhcp": false,"ipv4addr": "' + ipSoc + '"}],"name": "' + hostName + '","configure_for_dns": false,"view": "' + networkView + '"}'

            try:
                r = requests.post(url=rest_url,auth=infobloxAuth,verify=False,data=payload)
                r_json = r.json()
            except ValueError:
                raise Exception(r)
            except Exception:
                raise
        else:
            print('Erro desconhecido')

    #Determina Redes Backup

    if (netBackup == True):
        rNet = True
        rest_url = 'https://' + niosServer + '/wapi/v2.11/network?' + attrEnv + attrLoc + attrSub + '&*Rede=Backup&*Ambiente Cloud=NAO&network_view=' + networkView
        try:
            infobloxAuth = requests.auth.HTTPBasicAuth(usr,pwd)
            r = requests.get(url=rest_url, auth=infobloxAuth, verify=False)
            r_json = r.json()
            if r.status_code == 200:
                if len(r_json) > 0:
                    for network in r_json:
                        if 'network' in network:
                            networksBackup.append(network['network'])
                    print('Redes Backup: ' + ','.join(map(str,networksBackup)))
                else:
                    print("Não foi possível encontrar uma Rede Backup com tais características")
                    rNet = False
        except ValueError:
            raise Exception(r)
        except Exception:
            raise

        #Pega próximo IP disponível
        if rNet == True:
            rest_url = 'https://' + niosServer + '/wapi/v2.11/network?network=' + networksBackup[0] + '&network_view=' + networkView
            try:
                r = requests.get(url=rest_url,auth=infobloxAuth,verify=False)
                r_json = r.json()
                if r.status_code == 200:
                    if len(r_json) > 0:
                        net_ref = r_json[0]['_ref']
                        rest_url = 'https://' + niosServer + '/wapi/v2.11/' + net_ref + '?_function=next_available_ip&num=1'
                        r = requests.post(url=rest_url, auth=infobloxAuth, verify=False)
                        r_json = r.json()
                        if r.status_code == 200:
                            ipBackup = r_json['ips'][0]
                            print('ipBackup: '+ ipBackup)
            except ValueError:
                raise Exception(r)
            except Exception:
                raise
            
            #Registra hostname
            rest_url = 'https://' + niosServer + '/wapi/v2.11/record:host?_return_fields=ipv4addrs'
            payload = '{"ipv4addrs": [{"configure_for_dhcp": false,"ipv4addr": "' + ipBackup + '"}],"name": "' + hostName + '","configure_for_dns": false,"view": "' + networkView + '"}'

            try:
                r = requests.post(url=rest_url,auth=infobloxAuth,verify=False,data=payload)
                r_json = r.json()
            except ValueError:
                raise Exception(r)
            except Exception:
                raise
        else:
            print('Erro desconhecido')

    #Calcula a data atual
    currentDate = date.today().strftime("%d/%m/%Y")

    #Adiciona informações de atributos extensíveis
    paramHeaders = {'Content/Type':"application/json"}
    putPayload = {"extattrs":
        {
            "Solicitante": {
                "value": requestedBy},
            "Projeto/Juncao" : {
                "value": projectName},
            "Data_VRA": {
                "value" : currentDate},
            "Alocado por" : {
                "value" : "VRA"}
        }
    }

    if ipData is not '{{ipData}}':
        print("IpData")
        urlGet = 'https://'+ niosServer +'/wapi/v2.11/record:host?ipv4addr='+ ipData
        getRecord = requests.get(url=urlGet,auth=infobloxAuth,headers=paramHeaders,verify=False)
        refJson = getRecord.json()
        refHost = refJson[0]['_ref']
        putUrl = 'https://'+ niosServer +'/wapi/v2.11/'+ refHost
        r = requests.put(url=putUrl,auth=infobloxAuth,headers=paramHeaders,verify=False,json=putPayload)
        dataMask = networksData[0].split('/')
        ipData = ipData +'/'+ dataMask[1]
        
    if ipNoc is not '{{ipNoc}}':
        print("IpNoc")
        urlGet = 'https://'+ niosServer +'/wapi/v2.11/record:host?ipv4addr='+ ipNoc
        getRecord = requests.get(url=urlGet,auth=infobloxAuth,headers=paramHeaders,verify=False)
        refJson = getRecord.json()
        refHost = refJson[0]['_ref']
        putUrl = 'https://'+ niosServer +'/wapi/v2.11/'+ refHost
        r = requests.put(url=putUrl,auth=infobloxAuth,headers=paramHeaders,verify=False,json=putPayload)
        nocMask = networksNOC[0].split('/')
        ipNoc = ipNoc +'/'+ nocMask[1]

    if ipSoc is not '{{ipSoc}}':
        print("IpSoc")
        urlGet = 'https://'+ niosServer +'/wapi/v2.11/record:host?ipv4addr='+ ipSoc
        getRecord = requests.get(url=urlGet,auth=infobloxAuth,headers=paramHeaders,verify=False)
        refJson = getRecord.json()
        refHost = refJson[0]['_ref']
        putUrl = 'https://'+ niosServer +'/wapi/v2.11/'+ refHost
        r = requests.put(url=putUrl,auth=infobloxAuth,headers=paramHeaders,verify=False,json=putPayload)
        socMask = networksSOC[0].split('/')
        ipSoc = ipSoc +'/'+ socMask[1]

    if ipBackup is not '{{ipBackup}}':
        print("IpBackup")
        urlGet = 'https://'+ niosServer +'/wapi/v2.11/record:host?ipv4addr='+ ipBackup
        getRecord = requests.get(url=urlGet,auth=infobloxAuth,headers=paramHeaders,verify=False)
        refJson = getRecord.json()
        refHost = refJson[0]['_ref']
        putUrl = 'https://'+ niosServer +'/wapi/v2.11/'+ refHost
        r = requests.put(url=putUrl,auth=infobloxAuth,headers=paramHeaders,verify=False,json=putPayload)
        backupMask = networksBackup[0].split('/')
        ipBackup = ipBackup +'/'+ backupMask[1]


    ipAddr = []
    ipAddr = ipData +','+ ipNoc +','+ ipSoc +',' + ipBackup
    print('ipAddr: '+ ipAddr)
    return ipAddr