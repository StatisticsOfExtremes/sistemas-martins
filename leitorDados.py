import xml.etree.ElementTree as ET



"""
@path: string contendo o caminho do arquivo "*.xml"
@TipoNota: string ["CTE","NFS"] que determina quais são os tipos das notas.

[return]:  Dicionário com os dados [numDoc, valor, Nome, Indexador] nescessários.
"""
def getData(path, TipoNota):
    data = {
        'NumDoc' : '',
        "Valor" : '',
        'Nome' : '',
        'Indexador' : ''
    }

    if TipoNota == "CTE":
        data = getCTE(path)
    else:
        data = getNFS(path)
    return data


def getCTE(path):
    data = {
        'NumDoc' : '',
        "Valor" : '',
        'Nome' : '',
        'Indexador' : '',
        'Tipo': ''
    }


    tomador = {
        '0': 'rem',
        '3': 'dest',
        '2': 'receb',
        '4': 'ide/cte:toma4'
    }

    tipoCte = {
        '0' : 'normal',
        '1' : 'complementar',
        '2' : 'anulação',
        '3' : 'substituição'
    }
    
    tree = ET.parse(path)
    
    root = tree.getroot()

    namespace = {
        'cte' :'http://www.portalfiscal.inf.br/cte',
        'outro' : 'http://wwww.w3.org/2000/09/xmldsig#'
    }

    #Pega o número do CTE
    cteNum = root.findall('.//cte:ide/cte:cCT', namespace)[0]

    origem = root.findall('.//cte:rem/cte:enderReme/cte:UF', namespace)[0]

    destino = root.findall('.//cte:dest/cte:enderDest/cte:UF', namespace)[0]

    emissao = root.findall('.//cte:ide/cte:dhEmi', namespace)[0]

    aliquota = root.findall('.//cte:imp/cte:ICMS/cte:ICMS00/cte:pICMS', namespace)[0]
    
    #Tenta pegar o valor do frete
    try:
        valorFrete = root.findall('.//cte:vPrest/cte:Comp/cte:vComp', namespace)[0]
    
    #Caso dê erro, significa que o cte é provavelmente complementar, e o valor deve ser este:
    except:
        valorFrete = root.findall('.//cte:vPrest/cte:vTPrest', namespace)[0]


    try:
        tipoTomador = root.findall('.//cte:ide/cte:toma3/cte:toma', namespace)[0].text
    except:
        tipoTomador = root.findall('.//cte:ide/cte:toma4/cte:toma', namespace)[0].text

    tomadorNome = root.findall(f'.//cte:{tomador[tipoTomador]}/cte:xNome', namespace)[0]


    if tipoTomador == '4':
        tomadorIndexador = root.findall(f'.//cte:{tomador[tipoTomador]}/*', namespace)[1]   
    else:
        tomadorIndexador = root.findall(f'.//cte:{tomador[tipoTomador]}/*', namespace)[0]


    #Tipo do CTe
    
    tipo = root.findall(f'.//cte:ide/cte:tpCTe', namespace)[0].text
    
    data['Indexador'] = tomadorIndexador.text
    data['Nome'] = tomadorNome.text
    data['NumDoc'] = cteNum.text
    data['Valor'] = valorFrete.text
    data['Origem'] = origem.text
    data['Destino'] = destino.text
    data['Tipo'] = tipoCte[tipo]
    data['Data'] = emissao.text
    data['Aliq'] = aliquota.text
    return(data)



def formatarIndexador(indexador:str):
    if len(indexador) == 14:
        return indexador[0:2]+"."+indexador[2:5]+"."+indexador[5:8]+"/"+indexador[8:12]+"-"+indexador[12:14]
    else:
        return indexador[0:3]+"."+indexador[3:6]+"."+indexador[6:9]+'-'+indexador[9:11]



"""
@path: Caminho do arquivo da NFS

Diferente do arquivo do CT-e, a NFS vem em bulk
dessa forma nos temos que retornar uma lista de informações.
"""
def getNFS(path):
    data = {
        "NumNFS" : [],
        "Valor": [],
        "Tomador": [],
        "Indexador": [],
        "Status": []
    }

    tree = ET.parse(path)

    root = tree.getroot()

    namespace = {
        "ns2" : 'http://www.w3.org/2000/09/xmldsig#',
        'xsi' : 'http://www.w3.org/2001/XMLSchema-instance',
        'gin' : 'http://www.ginfes.com.br/tipos'       
    }

    #Tenta achar uma tag de Cancelamento, caso não consiga, adiciona um "NORMAL",
    #Caso contrário adiciona "CANCELADO"
    for k in root.findall('./ns2:Nfse', namespace):
        if k.find('gin:Cancelamento', namespace):
            data['Status'].append("CANCELADO")
        else:
            data['Status'].append('NORMAL')

    [data['NumNFS'].append(i.text) for i in root.findall('./ns2:Nfse/gin:Nfse/gin:IdentificacaoNfse/gin:Numero', namespaces=namespace)]
    [data['Tomador'].append(i.text) for i in root.findall('./ns2:Nfse/gin:Nfse/gin:TomadorServico/gin:RazaoSocial', namespace)]
    [data['Valor'].append(i.text) for i in root.findall('./ns2:Nfse/gin:Nfse/gin:Servico/gin:Valores/gin:ValorServicos', namespace)]
    [data['Indexador'].append(i.text) for i in root.findall('./ns2:Nfse/gin:Nfse/gin:TomadorServico/gin:IdentificacaoTomador/gin:CpfCnpj/gin:Cnpj', namespace)]
        
    return(data)
