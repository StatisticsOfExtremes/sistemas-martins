from codecs import decode
import os
import leitorDados as lD
from leitorDados import formatarIndexador
import pandas as pd
from getCTES import download_ctes
import zipfile

#Baixa os CTES, eles são baixados pro mesmo diretório deste arquivo.
download_ctes()

#Extrai os arquivos
with zipfile.ZipFile('notas.zip', 'r') as zip_ref:
    zip_ref.extractall('temp/')

"""
Vai ter dois diretórios:
 1. Para os arquivos não cancelados;
 2. Para os arquivos cancelados;
"""

TIPOS_CTES = ['XML_AUTORIZADAS', 'XML_CANCELADAS']

rootdir = 'temp/'


Dados = {
    'CTe': [],
    'Valor' : [],
    'Tomador': [],
    'Tipo': [],
    'Origem': [],
    'Destino': [],
    'Data': [],
    'Aliq': []
}



"""
Itera sobre os arquivos do [root] com final ".xml", retorna os dados importantes do XML
"""
for dir in os.listdir(rootdir):
    if dir in TIPOS_CTES:
            for file in os.listdir(os.path.join(rootdir, dir)):
                filename = os.fsdecode(file)
                if filename.endswith(".xml"):
                    xmlDados = lD.getData(os.path.join(rootdir + dir, filename), "CTE")
                    Dados['CTe'].append(str(int(xmlDados['NumDoc'])))
                    if dir == 'XML_AUTORIZADAS':
                        Dados['Tipo'].append(xmlDados['Tipo'].upper())
                    else:
                        Dados['Tipo'].append('CANCELADO')
                    Dados['Valor'].append(xmlDados['Valor'].replace(".",","))
                    Dados['Data'].append(xmlDados['Data'])
                    Dados['Tomador'].append(f"{xmlDados['Nome']} ({formatarIndexador(xmlDados['Indexador'])})")
                    Dados['Origem'].append(xmlDados['Origem'])
                    Dados['Destino'].append(xmlDados['Destino'])
                    Dados['Aliq'].append(f"{str(float(xmlDados['Aliq'])/100).replace('.', ',')}")

df = pd.DataFrame(Dados)

arquivoSaida = input(" Dados lidos com sucesso!\n Qual o caminho do diretório de saída? ")

df.to_excel(f'{arquivoSaida}/notas.xlsx')
