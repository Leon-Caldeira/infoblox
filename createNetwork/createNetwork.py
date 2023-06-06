import requests
import json

def creteNetwork(context, inputs):
    # URL da API do Infoblox para criar redes
    restUrl = f'https://{inputs["niosServer"]}/wapi/v2.11/network'

    # Credenciais de autenticação
    infobloxAuth = requests.auth.HTTPBasicAuth(inputs["usr"],inputs["pwd"])

    # Dados da rede a ser criada
    dados_rede = {
        'network': inputs["CIDR"],
        'network_view': inputs["netType"],
        'options': {
            'domain-name-servers' : inputs["dnsServer"],
            'Routers' : inputs["netGateway"]
        },
        'extattrs': {
            'Ambiente': inputs["netEnvironment"],
            'Subambiente': inputs["netSub"],
            'Port Group': inputs["port-Group"],
            'Gateway': inputs["netGateway"],
            'VLAN_ID': inputs["vlanId"],
            'Nome_da_VLAN': inputs["vlanName"],
            'Equipamento': inputs["netEquipment"],
            'ARP': inputs["netArp"]
        }
    }

    # Realiza a requisição POST para criar a rede
    response = requests.post(url, headers=headers, auth=(username, password), json=dados_rede)

    # Verifica o status da resposta
    if response.status_code == 201:
        print('Rede criada com sucesso!')
    else:
        print(f'Erro ao criar rede. Código de resposta: {response.status_code}')
        print(response.text)

def verificar_rede(nome):
    # URL da API do Infoblox para obter informações da rede
    url = f'https://seu_infoblox/api/network?network={nome}'

    # Credenciais de autenticação
    username = 'seu_usuario'
    password = 'sua_senha'

    # Cabeçalhos da requisição
    headers = {
        'Accept': 'application/json'
    }

    # Realiza a requisição GET para obter informações da rede
    response = requests.get(url, headers=headers, auth=(username, password))

    # Verifica o status da resposta
    if response.status_code == 200:
        data = response.json()
        redes = data.get('result', [])
        if redes:
            print('A rede já está criada.')
        else:
            print('A rede não está criada.')
    else:
        print(f'Erro ao verificar rede. Código de resposta: {response.status_code}')
        print(response.text)

# Exemplo de uso
nome = 'Minha Rede'
ambiente = 'Produção'
subambiente = 'Frontend'
tipo_rede = 'LAN'
port_group = 'GrupoA'
gateway = '192.168.0.1'
dns_server = '8.8.8.8'
vlan_id = '100'
nome_vlan = 'VLAN100'
equipamento = 'SwitchA'
arp = '192.168.0.2'
cidr = '192.168.0.0/24'

criar_rede(nome, ambiente, subambiente, tipo_rede, port_group, gateway, dns_server, vlan_id, nome_vlan
