import json
import requests

def addExtAttr (context, inputs):
    print("Versão 20")
    
    niosServer = inputs["niosServer"]
    usr = inputs["usr"]
    pwd = inputs["pwd"]

    ipAddr = inputs["ipAddr"]

    #Ignora certificado caso self-signed
    requests.packages.urllib3.disable_warnings()

    #Variável de autenticação
    infobloxAuth = requests.auth.HTTPBasicAuth(usr,pwd)

    #Parâmetros iniciais
    paramHeaders = {'Content-Type':"application/json"}

    #Busca _ref
    restUrl = 'https://'+ niosServer +'/wapi/v2.11/record:host?ipv4addr='+ ipAddr
    r = requests.get(url=restUrl,headers=paramHeaders,auth=infobloxAuth,verify=False)
    recordRef = r.json()[0]['_ref']

    print(recordRef)

    #Dados de gravação

    dataPayload = {"extattrs":{
        "Alocado por":{
            "value":"VRA"},
        "Data_VRA":{
            "value": "30-01-2023"},
        "Projeto/Juncao":{
            "value":"projeto teste"},
        "Solicitante":{
            "value":"solicitante teste"}
        }
    }

    #Insere atributos extensíveis

    putUrl = 'https://'+ niosServer +'/wapi/v2.11/'+ recordRef
    r = requests.put(url=putUrl,auth=infobloxAuth,json=dataPayload,headers=paramHeaders,verify=False)
    
    print(r.json())
    print(r.status_code)