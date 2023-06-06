import requests

def getVlanIdAttr (context, inputs):

    niosServer = inputs["niosServer"]
    vlanID = inputs["vlanID"]

    # Ignora certificado caso self-signed
    requests.packages.urllib3.disable_warnings()

    # Variável de autenticação
    infobloxAuth = requests.auth.HTTPBasicAuth(inputs["usr"],inputs["pwd"])

    # Busca redes pelo VLAN ID
    restUrl = 'https://'+ niosServer +'/wapi/v2.11/vlan?id='+ vlanID +'&_return_fields=assigned_to'
    r = requests.get(url=restUrl,auth=infobloxAuth,verify=False)
    rJson = r.json()
    mainCIDR = []
    extAttr = []

    # Testa funcionalidade    
    if r.status_code == 200:
        rJson = r.json()

        # Encontra cada rede específica
        for i in range(len(rJson)):
            if 'assigned_to' in rJson[i]:
                secondaryCIDR = rJson[i]['assigned_to'][0].split(':')
                secondaryCIDR = secondaryCIDR[1].split('/')
                del secondaryCIDR[-1]
                mainCIDR.append(secondaryCIDR[0] +'/'+ secondaryCIDR[1])

        #Gera Array de informações

        if len(rJson) > 0:

            for i in range(len(mainCIDR)):
                restUrl = 'https://'+ niosServer +'/wapi/v2.11/network?network='+ mainCIDR[i] +'&_return_fields=extattrs'
                r = requests.get(url=restUrl,auth=infobloxAuth,verify=False)
                rJson = r.json()

                # Adiciona atributos extensíveis ou vazio
                extAttr.append({
                    'Ambiente': rJson[0]['extattrs']['Ambiente']['value'] if 'Ambiente' in rJson[0]['extattrs'] else '',
                    'Localizacao': rJson[0]['extattrs']['Localizacao']['value'] if 'Localizacao' in rJson[0]['extattrs'] else '',
                    'Nome': rJson[0]['extattrs']['Nome']['value'] if 'Nome' in rJson[0]['extattrs'] else '',
                    'Rede': mainCIDR[i] + '(' + rJson[0]['extattrs']['Rede']['value'] + ')' if 'Rede' in rJson[0]['extattrs'] else '',
                    'SubAmbiente': rJson[0]['extattrs']['SubAmbiente']['value'] if 'SubAmbiente' in rJson[0]['extattrs'] else ''
                    })                
        else: # Erro de encontrar dados
            print('Dados não encontrados para' + vlanID)
            extAttr.append(
                {'Ambiente' : '',
                 'Localizacao' : '',
                 'Nome' : '',
                 'Rede' : '',
                 'SubAmbiente' : ''
                 })
    else: # Erro de encontrar VLAN
        print(r.status_code)
        print(r.text)
        extAttr.append(
            {'Ambiente' : '',
             'Localizacao' : '',
             'Nome' : '',
             'Rede' : '',
             'SubAmbiente' : ''
             })

    print(extAttr)
    return extAttr