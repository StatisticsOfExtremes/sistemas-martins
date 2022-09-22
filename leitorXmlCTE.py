import os
import leitorDados as lD
from leitorDados import formatarIndexador
import pandas as pd



rootdir = input("Path do arquivo: ")#.replace("\\", "/")

directory = os.fsencode(rootdir)


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
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".xml"):
         xmlDados = lD.getData(os.path.join(rootdir, filename), "CTE")
         Dados['CTe'].append(str(int(xmlDados['NumDoc'])))
         Dados['Valor'].append(xmlDados['Valor'].replace(".",","))
         Dados['Tomador'].append(f"{xmlDados['Nome']} ({formatarIndexador(xmlDados['Indexador'])})")
         Dados['Origem'].append(xmlDados['Origem'])
         Dados['Destino'].append(xmlDados['Destino'])
         Dados['Data'].append(xmlDados['Data'])
         Dados['Tipo'].append(xmlDados['Tipo'].upper())
         Dados['Aliq'].append(f"{str(float(xmlDados['Aliq'])/100).replace('.', ',')}")

df = pd.DataFrame(Dados)

arquivoSaida = input("dados lidos com sucesso!\n Qual o nome de arquivo de saída?")

df.to_excel(f'./{arquivoSaida}.xlsx')
