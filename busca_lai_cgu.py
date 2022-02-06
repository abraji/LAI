# -*- coding: utf-8
# Abraji (https://www.abraji.org.br)
# Reinaldo Chaves (reinaldo@abraji.org.br)
# Programa acessar os pedidos da LAI registrados no ESIC federal
# Faz estudos com palavras nas Respostas e Decisoes
#


import xml.etree.ElementTree as ET
from lxml import etree
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import wget
import os
from zipfile import ZipFile

import plotly          
import plotly.express as px
import plotly.io as pio


# Mostra diretório atual
print(os.getcwd())
# Seta diretório para gravar arquivos
os.chdir('D:\\Code\\lai_cgu\\repo\\dados_usados')


# Origem dos dados da LAI do ESic federal
# http://www.consultaesic.cgu.gov.br/busca/_layouts/15/DownloadPedidos/DownloadDados.aspx

# Faz o download do arquivo de 2020 
wget.download("https://dadosabertos-download.cgu.gov.br/FalaBR/Arquivos_FalaBR_Filtrado/Arquivos_xml_2020.zip")
# 2021
wget.download("https://dadosabertos-download.cgu.gov.br/FalaBR/Arquivos_FalaBR_Filtrado/Arquivos_xml_2021.zip")
# 2022 - 6/fev/2022
wget.download("https://dadosabertos-download.cgu.gov.br/FalaBR/Arquivos_FalaBR_Filtrado/Arquivos_xml_2022.zip")


# Descompacta
with ZipFile('Arquivos_xml_2020.zip', 'r') as zipObj:
    listOfFileNames = zipObj.namelist()
    for fileName in listOfFileNames:
        if fileName.endswith('Pedidos_xml_2020.xml'):
            arquivo = fileName           
            zipObj.extract(fileName, 'temp_csv')

with ZipFile('Arquivos_xml_2021.zip', 'r') as zipObj:
    listOfFileNames = zipObj.namelist()
    for fileName in listOfFileNames:
        if fileName.endswith('Pedidos_xml_2021.xml'):
            arquivo = fileName           
            zipObj.extract(fileName, 'temp_csv')

with ZipFile('Arquivos_xml_2022.zip', 'r') as zipObj:
    listOfFileNames = zipObj.namelist()
    for fileName in listOfFileNames:
        if fileName.endswith('Pedidos_xml_2022.xml'):
            arquivo = fileName           
            zipObj.extract(fileName, 'temp_csv')


os.chdir('D:\\Code\\lai_cgu\\repo\\dados_usados\\temp_csv')


##########################################################################
# Cria dataframe de 2020
f = open('20220206_Pedidos_xml_2020.xml','r',encoding='utf-16')
xml_data = f.read()
xml_data = xml_data.replace('&','')

root = ET.XML(xml_data)
pedidos = []
for obj in list(root):
    pedidos.append(obj.attrib)
    
df_2020 = pd.DataFrame(pedidos)
df_2020['id_ano']= df_2020['IdPedido']+'_2020'

df_2020 = df_2020[['IdPedido', 
                   'ProtocoloPedido', 
                   'Esfera',
                   'Orgaodestinatario',
                   'Situacao',
                   'DataRegistro',
                   'ResumoSolicitacao',
                   'DetalhamentoSolicitacao',
                   'PrazoAtendimento',
                   'FoiProrrogado',
                   'FoiReencaminhado',
                   'FormaResposta',
                   'OrigemSolicitacao',
                   'IdSolicitante',
                   'AssuntoPedido',
                   'SubAssuntoPedido',
                   'Tag',
                   'DataResposta',
                   'Resposta',
                   'Decisao',
                   'EspecificacaoDecisao',
                   'id_ano']]


df_2020.info()


##########################################################################
# Cria dataframe de 2021
f = open('20220206_Pedidos_xml_2021.xml','r',encoding='utf-16')
xml_data = f.read()
xml_data = xml_data.replace('&','')

root = ET.XML(xml_data)
pedidos = []
for obj in list(root):
    pedidos.append(obj.attrib)
    
df_2021 = pd.DataFrame(pedidos)
df_2021['id_ano']= df_2021['IdPedido']+'_2021'

df_2021 = df_2021[['IdPedido', 
                   'ProtocoloPedido', 
                   'Esfera',
                   'Orgaodestinatario',
                   'Situacao',
                   'DataRegistro',
                   'ResumoSolicitacao',
                   'DetalhamentoSolicitacao',
                   'PrazoAtendimento',
                   'FoiProrrogado',
                   'FoiReencaminhado',
                   'FormaResposta',
                   'OrigemSolicitacao',
                   'IdSolicitante',
                   'AssuntoPedido',
                   'SubAssuntoPedido',
                   'Tag',
                   'DataResposta',
                   'Resposta',
                   'Decisao',
                   'EspecificacaoDecisao',
                   'id_ano']]


df_2021.info()


##########################################################################
# Cria dataframe de 2022
f = open('20220206_Pedidos_xml_2022.xml','r',encoding='utf-16')
xml_data = f.read()
xml_data = xml_data.replace('&','')

root = ET.XML(xml_data)
pedidos = []
for obj in list(root):
    pedidos.append(obj.attrib)
    
df_2022 = pd.DataFrame(pedidos)
df_2022['id_ano']= df_2022['IdPedido']+'_2022'

df_2022 = df_2022[['IdPedido', 
                   'ProtocoloPedido', 
                   'Esfera',
                   'Orgaodestinatario',
                   'Situacao',
                   'DataRegistro',
                   'ResumoSolicitacao',
                   'DetalhamentoSolicitacao',
                   'PrazoAtendimento',
                   'FoiProrrogado',
                   'FoiReencaminhado',
                   'FormaResposta',
                   'OrigemSolicitacao',
                   'IdSolicitante',
                   'AssuntoPedido',
                   'SubAssuntoPedido',
                   'Tag',
                   'DataResposta',
                   'Resposta',
                   'Decisao',
                   'EspecificacaoDecisao',
                   'id_ano']]


df_2022.info()

##########################################################################


# Une dataframes
frames = [df_2020, df_2021, df_2022]
df_todos = pd.concat(frames)
df_todos.info()

# Tipos de Decisao
df_todos['Decisao'].unique()

df_todos.to_csv('resultados/pedidos_lai_todos_6_fev_2022.csv', index=False)



# Procura por pedidos que tenham na Resposta termos da LGPD
palavras = df_todos[pd.notnull(df_todos['Resposta'])].copy()
palavras.shape

palavras["resposta_upper"] = palavras['Resposta'].str.upper()
#search_list = ['PEDIDO GENÉRICO', 'DESARRAZOADO', 'FISHING' 'FISHING EXPEDITION', 'DESPROPORCIONAL', 'SEGURANÇA NACIONAL', 'SIGILOSOS', 'PROCESSO DECISÓRIO EM CURSO', 'EXIGE TRABALHOS ADICIONAIS', 'LGPD', 'LEI GERAL DE PROTEÇÃO DE DADOS', 'LEI Nº 13.709/2018']
search_list = ['LGPD', 'LEI GERAL DE PROTEÇÃO DE DADOS', 'LEI Nº 13.709/2018', '13.709/2018']
mask = palavras['resposta_upper'].str.contains('|'.join(search_list))
seleciona = palavras[mask]

seleciona.info()

os.chdir('D:\\Code\\lai_cgu\\repo')

seleciona.to_csv('resultados/pedidos_lai_com_LGPD_6_fev_2022.csv', index=False)
seleciona.to_excel('resultados/pedidos_lai_com_LGPD_6_fev_2022.xlsx',sheet_name='Sheet1', index=False)

# Conta quantos pedidos existem em cada tipo de Decisao
seleciona.groupby(['Decisao']).size().sort_values(ascending=False).reset_index()

# Plota gráfico 
conta1 = seleciona.groupby(['Decisao']).size().sort_values(ascending=False).reset_index()
conta1.columns = ['tipos_respostas', 'contagem']

barchart = px.bar(
    data_frame=conta1,
    x="tipos_respostas",
    y="contagem",
    text='contagem', # Mostra valores na barra
    color="tipos_respostas",               # differentiate color of marks
    opacity=0.9,                  # set opacity of markers (from 0 to 1)
    orientation="v",              # 'v','h': orientation of the marks
    barmode='relative', 
    labels={"tipos_respostas": "Categorias de respostas na LAI",
    "contagem":"Quantidade de cada tipo de resposta"},           # map the labels of the figure
    title='Respostas a pedidos na LAI com termos ligados a LGPD - 2020, 2021, 2022', # figure title
    width=1400,                   # figure width in pixels
    height=720,                   # figure height in pixels
    template='plotly_dark'
    )

pio.show(barchart)





# Procura por pedidos que NÃO tenham na Resposta termos da LGPD
search_list = ['LGPD', 'LEI GERAL DE PROTEÇÃO DE DADOS', 'LEI Nº 13.709/2018', '13.709/2018']
mask = ~palavras['resposta_upper'].str.contains('|'.join(search_list))
seleciona = palavras[mask]

seleciona.info()

# Conta quantos pedidos existem em cada tipo de Decisao
seleciona.groupby(['Decisao']).size().sort_values(ascending=False).reset_index()

# Plota gráfico 
conta2 = seleciona.groupby(['Decisao']).size().sort_values(ascending=False).reset_index()
conta2.columns = ['tipos_respostas', 'contagem']

barchart = px.bar(
    data_frame=conta2,
    x="tipos_respostas",
    y="contagem",
    text='contagem', # Mostra valores na barra
    color="tipos_respostas",               # differentiate color of marks
    opacity=0.9,                  # set opacity of markers (from 0 to 1)
    orientation="v",              # 'v','h': orientation of the marks
    barmode='relative', 
    labels={"tipos_respostas": "Categorias de respostas na LAI",
    "contagem":"Quantidade de cada tipo de resposta"},           # map the labels of the figure
    title='Respostas a pedidos na LAI SEM termos ligados a LGPD - 2020, 2021, 2022', # figure title
    width=1400,                   # figure width in pixels
    height=720,                   # figure height in pixels
    template='plotly_dark'
    )

pio.show(barchart)