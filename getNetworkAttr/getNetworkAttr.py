import json
import requests

def checkNull(varStr):
    if varStr is None:
        return ''
    else:
        return varStr

def getNetworkAttr (context, inputs):

    niosServer = inputs["niosServer"]
    networkView = inputs["networkView"]
    networkAddr = inputs["networkAddr"]
    usr = inputs["usr"]
    pwd = inputs["pwd"]

    #Ignora certificado caso self-signed
    requests.packages.urllib3.disable_warnings()

    #Variável de autenticação
    infobloxAuth = requests.auth.HTTPBasicAuth(usr,pwd)

    if not networkAddr:
        networkAddr = ''

    #Busca redes pelo VLAN ID
    restUrl = 'https://'+ niosServer +'/wapi/v2.11/network?network=' + networkAddr + '&network_view=' + networkView + '&_return_fields=extattrs,vlans'
    r = requests.get(url=restUrl,auth=infobloxAuth,verify=False)

    extAttr = [{}]

    if r.status_code == 200:
        rJson = r.json()
        if len(rJson) > 0:
            id = ''
            if 'vlans' in rJson[0]:
                vlanId = [vlan['vlan'].split('/')[-1] for vlan in rJson[0]['vlans']]
                if vlanId:
                    id = vlanId[-1]
            extAttrDict = {}
            for key in ['Ambiente', 'Localizacao', 'Nome', 'SubAmbiente']:
                if key in rJson[0]['extattrs']:
                    extAttrDict[key] = checkNull(rJson[0]['extattrs'][key]['value'])
                else:
                    extAttrDict[key] = ''
            extAttrDict['VLAN'] = id
            extAttr[0] = extAttrDict
        else:
            extAttr.clear()
            extAttr.append(
                {'Ambiente' : '',
                 'Localizacao' : '',
                 'Nome' : '',
                 'SubAmbiente' : '',
                 'VLAN' : ''
                 })
 
    else:
        print(r.status_code)
        print(r.text)
        extAttr.clear()
        extAttr.append(
            {'Ambiente' : '',
             'Localizacao' : '',
             'Nome' : '',
             'SubAmbiente' : '',
             'VLAN' : ''
            })

    print(extAttr)
    return extAttr