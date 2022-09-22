from fileinput import close
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta

load_dotenv()

CNPJ = os.environ.get("CNPJ")
CPF = os.environ.get("CPF")
IE = os.environ.get("IE")
SENHA = os.environ.get("SENHA")


headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

raw_path = "https://sistemasmartins.com.br/"

acess_path = raw_path + "Acesso/"


"""
curl --verbose --data-urlencode "txt_cnpj=35.079.122/0001-08&txt_ie=&txt_cpf=048.905.593-74&txt_senha=trans2019" https://sistemasmartins.com.br/Acesso 
--next --data-urlencode "mes=9
&ano=2022
&tipo_nota=3
&tipo_cliente=0
&cpf_cnpj=
&dia_inicial=1
&dia_final=31" https://sistemasmartins.com.br/Relatorio_Cte/BuscaListaCte 



--next "https://sistemasmartins.com.br//Relatorio_Cte/Baixar_XML?mes=9&ano=2022&tipo_nota=3&tipo_cliente=0&cpf_cnpj=&dia_inicial=1&dia_final=31" --output notas.zip
"""

form_acesso = {
    "txt_cnpj": CNPJ,
    "txt_ie":IE,
    "txt_cpf": CPF,
    "txt_senha": SENHA
}

rAcesso = requests.post(acess_path, data = form_acesso)

print(f"Status {rAcesso.status_code} - Para o acesso")


#Dados para pegar as notas
HOJE = datetime.now()

TIPO_DE_NOTA = 3
TIPO_CLIENTE = 0
CPF_CNPJ = ''
DIA_INICIAL = 1
DIA_FINAL = (datetime(HOJE.year, HOJE.month, 1) + relativedelta(months=1, days=-1)).day
ANO = HOJE.year
MES = HOJE.month

form_buscar_cte = {
    'mes': MES,
    'ano': ANO,
    'tipo_nota': TIPO_DE_NOTA,
    'tipo_cliente':TIPO_CLIENTE,
    'cpf_cnpj': CPF_CNPJ,
    'dia_inicial': DIA_INICIAL,
    'dia_final':DIA_FINAL
}


path_buscar_cte =  'Relatorio_Cte/BuscaListaCte' 

reqBuscarCte = requests.post(raw_path + path_buscar_cte, data = form_buscar_cte )

print(reqBuscarCte.status_code)

path_baixar_cte = 'Relatorio_Cte/Baixar_XML'

reqBaixarCte = requests.get(raw_path + path_baixar_cte, params= form_buscar_cte, stream = True)

print(reqBaixarCte.status_code)

with open('notas.zip', 'wb') as fd:
    for chunk in reqBaixarCte.iter_content(chunk_size = 8124):
        fd.write(chunk)
