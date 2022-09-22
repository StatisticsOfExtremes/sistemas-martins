import os
import leitorDados as lD
from leitorDados import formatarIndexador
import pandas as pd




rootdir = 'C:\\Users\\novol\\Downloads\\XML_AUTORIZADAS'

directory = os.fsencode(rootdir)


Dados = {
    'NFS': [],
    'Valor' : [],
    'Tomador': [],
    'Status': []
}



"""
Itera sobre os arquivos do [root] com final ".xml", retorna os dados importantes do XML
"""
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".xml"):
         xmlDados = lD.getData(os.path.join(rootdir, filename), "NFS")

         [Dados['NFS'].append(f"NFS-e {num}") for num in xmlDados['NumNFS']]

         [Dados['Valor'].append(valor.replace(".",",")) for valor in xmlDados['Valor']]

         [Dados['Tomador'].append(f"{nome} ({formatarIndexador(index)})") for nome, index in zip(xmlDados['Tomador'],xmlDados['Indexador'])]
        
         [Dados['Status'].append(status) for status in xmlDados['Status']]

df = pd.DataFrame(Dados)

df = df[df['Status'] == "NORMAL"]

df.to_excel('./nfs.xlsx')


#root = tree.getroot()
