import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta


def download_ctes(export_path = 'notas.zip'):
    """
    Retona o nome do arquivo do download das notas dos CTES

    @param export_path<string>: caminho para o download dos arquivos.

    @return <None>
    """


    load_dotenv()

    CNPJ = os.environ.get("CNPJ")
    CPF = os.environ.get("CPF")
    IE = os.environ.get("IE")
    SENHA = os.environ.get("SENHA")


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    session = requests.Session()

    raw_path = "https://sistemasmartins.com.br/"

    acess_path = raw_path + "Acesso/Index"


    form_acesso = {
        "txt_cnpj": CNPJ,
        "txt_ie":IE,
        "txt_cpf": CPF,
        "txt_senha": SENHA,
        "manter_cookie":'on'
    }

    response_session = session.get(acess_path, data = form_acesso, allow_redirects=True)

    session_cookie = response_session.cookies.get_dict()

    rAcesso = session.post(acess_path, data = form_acesso, allow_redirects=True, cookies=session_cookie)

    print(f"Status \x1b[5;34,42m {rAcesso.status_code} \x1b[0m - Para o acesso\n")


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

    print(f"Buscando os CTE's...")

    reqBuscarCte = session.post(raw_path + path_buscar_cte, data = form_buscar_cte, cookies=session_cookie)

    path_baixar_cte = 'Relatorio_Cte/Baixar_XML/'



    print(f"CTE's encontrandos, baixando os arquivos")

    header_baixar = {
        "Content-Type": "application/zip"
    }

    reqBaixarCte = session.get(raw_path + path_baixar_cte, params= form_buscar_cte, stream = True, headers=header_baixar, cookies=session_cookie)


    with open(export_path, 'wb') as fd:
        for chunk in reqBaixarCte.iter_content(chunk_size = 8124):
            fd.write(chunk)

    print(f"Arquivos baixados!\nExtraindo os arquivos")
