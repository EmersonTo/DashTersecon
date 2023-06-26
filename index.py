from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.io as pio
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from app import app
from datetime import datetime

# IMPORTAR OS DADOS E PROCESSAR DADOS
# cidades = {"Aguas Lindas": 387, "Americano do Brasil": 9, "Ap. de Goiânia": 19,
# "Caldas Novas": 45, "Catalão": 53, "Castelândia":  293, "Ceres": 60,
# "Goiatuba": 101, "Inaciolância": 295, "Ipameri": 112, "Luziânia": 145,
# "Mineiros": 153, "Morrinhos": 159, "Cidade Ocidental": 283, "Pirenópolis": 195,
# "Santa Helena": 212, "Valparaíso": 394, "Aurilândia": 27, "Niquelândia": 171,
# "Goianésia": 88, "Sanclerlândia": 208, "Carmo do Rio Verde": 52, }
server = app.server

cidades = {"Senador Canedo": 229, "Santo Antônio do Descoberto": 218, "Caldas Novas": 45, "Guapo": 103, "Montividiu": 158,
           "Iporá":  113, "Anápolis": 11, "Itarumã": 124, "Jataí": 139, "Fazenda Nova": 81}

template = "slate"
load_figure_template(template)

municipios = []
for cidade in cidades:
    municipios.append(cidade)
municipios.sort()

df_tcm = pd.read_csv("df_tcm.csv", sep=';')
df_tcm = df_tcm.drop(columns=['Unnamed: 0'])
print("aki")
url = "https://www.tesourotransparente.gov.br/ckan/dataset/72b5f371-0c35-4613-8076-c99c821a6410/resource/07af297a-5e59-494a-a88a-55ddfd2f4b01/download/Relatorio-Situacao-de-Varios-Entes---Municipios---UF-Todas---Abrangencia-1.csv"
print("aki")

# LAYOUT
app.layout = html.Div(children=[
    dcc.Interval(
        id='buscar_dados',
        interval=1 * 3600000

    ),
    dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.H1("Tersecon", style={
                        "font-size": "2.5vw"}),
                    html.Hr(style={"font-size": "0.4vw"}),
                    html.H3("Cidades:", style={
                        "font-size": "0.8vw"}),
                    dcc.Checklist(municipios, municipios, id="id_check_cidade", inputStyle={
                                  "margin-right": "8px", "margin-left": "10px"})

                ], style={"height": "95vh", "margin": "10px", "padding": "5px"})

            ], sm=2),

            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.H1("Gestões Atrasadas", style={
                                    "text-align": "center"}),
                            html.H1(
                                "TCM-GO", style={"text-align": "center"}),
                            html.Hr(),
                            html.H1(id="id_qtd_atrasados_tcm", style={
                                    "text-align": "center"})
                        ], style={"padding": "15px"})
                    ], sm=4),
                    dbc.Col([
                        dbc.Card([
                            html.H1("Gestões a Enviar", style={
                                    "text-align": "center"}),
                            html.H1(
                                "TCM-GO", style={"text-align": "center"}),
                            html.Hr(),
                            html.H1(id="id_qtd_enviar_tcm", style={
                                    "text-align": "center"})
                        ], style={"padding": "15px"})
                    ], sm=4),
                    dbc.Col([
                        dbc.Card([
                            html.H1("Pendências", style={
                                    "text-align": "center"}),
                            html.H1("CAUC", style={
                                    "text-align": "center"}),
                            html.Hr(),
                            html.H1(id="id_qtd_cauc", style={
                                    "text-align": "center"})
                        ], style={"padding": "15px", "margin-right": "20px"})
                    ], sm=4,),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dcc.Graph(
                                id="id_fig_barra_atrasados_enviar_por_cidade", style={'width': '90vh', 'height': '90vh'})
                        ], style={"margin-right": "20px", "padding": "10px", "height": "30vh"})
                    ])

                ]),
                dbc.Row([
                    dbc.Col([
                            dbc.Card([
                                dcc.Graph(
                                    id="id_fig_barra_pendencia_cauc_por_cidade", animate=True)
                            ], style={"margin-right": "20px", "padding": "10px"})
                            ])

                ]),
            ], sm=10)

            ])

])
# , fluid=True, olhar o que é depois
# CALLBACKS


@app.callback([
    Output('id_qtd_atrasados_tcm', 'children'),
    Output('id_qtd_enviar_tcm', 'children'),
    Output('id_qtd_cauc', 'children'),
    Output('id_fig_barra_atrasados_enviar_por_cidade', 'figure'),
    Output('id_fig_barra_pendencia_cauc_por_cidade', 'figure'),
    # Output('id_lista_atrasadas', 'children')
],
    Input('id_check_cidade', 'value'))
def update_qtd_atrasados(municipios):
    municipios.sort()
    now = datetime.now()
    if now.month == 3 and now.year == 2023:
        if now.day <= 17:
            mes_enviar = 1
        else:
            mes_enviar = 2
    elif now.month == 4 and now.year == 2023:
        if now.day <= 14:
            mes_enviar = 2
        else:
            mes_enviar = 3
    elif now.month == 5 and now.year == 2023:
        if now.day <= 15:
            mes_enviar = 3
        else:
            mes_enviar = 4
    elif now.month == 6 and now.year == 2023:
        if now.day <= 14:
            mes_enviar = 4
        else:
            mes_enviar = 5
    elif now.month == 7 and now.year == 2023:
        if now.day <= 17:
            mes_enviar = 5
        else:
            mes_enviar = 6
    elif now.month == 8 and now.year == 2023:
        if now.day <= 14:
            mes_enviar = 6
        else:
            mes_enviar = 7
    elif now.month == 9 and now.year == 2023:
        if now.day <= 14:
            mes_enviar = 7
        else:
            mes_enviar = 8
    elif now.month == 10 and now.year == 2023:
        if now.day <= 16:
            mes_enviar = 8
        else:
            mes_enviar = 9
    elif now.month == 11 and now.year == 2023:
        if now.day <= 14:
            mes_enviar = 9
        else:
            mes_enviar = 10
    elif now.month == 12 and now.year == 2023:
        if now.day <= 15:
            mes_enviar = 10
        else:
            mes_enviar = 11
    elif now.month == 1 and now.year == 2024:
        if now.day <= 16:
            mes_enviar = 11
        else:
            mes_enviar = 12
    elif now.month == 2 and now.year == 2024:
        if now.day <= 14:
            mes_enviar = 12
        else:
            mes_enviar = 1

    df_tcm_filter = df_tcm[df_tcm["cidade"].isin(municipios)]

    filterJaneiro = df_tcm_filter.loc[df_tcm_filter['1'] == 0]
    filterFevereiro = df_tcm_filter.loc[df_tcm_filter['2'] == 0]
    filterMarco = df_tcm_filter.loc[df_tcm_filter['3'] == 0]
    filterAbril = df_tcm_filter.loc[df_tcm_filter['4'] == 0]
    filterMaio = df_tcm_filter.loc[df_tcm_filter['5'] == 0]
    filterJunho = df_tcm_filter.loc[df_tcm_filter['6'] == 0]
    filterJulho = df_tcm_filter.loc[df_tcm_filter['7'] == 0]
    filterAgosto = df_tcm_filter.loc[df_tcm_filter['8'] == 0]
    filterSetembro = df_tcm_filter.loc[df_tcm_filter['9'] == 0]
    filterOutubro = df_tcm_filter.loc[df_tcm_filter['10'] == 0]
    filterNovembro = df_tcm_filter.loc[df_tcm_filter['11'] == 0]
    filterDezembro = df_tcm_filter.loc[df_tcm_filter['12'] == 0]

    # criando o grafico
    colunas = ['cidade', 'ano', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio',
               'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    df_resumo = pd.DataFrame(columns=colunas)
    for cidade in municipios:
        df_cidade = df_tcm_filter.loc[df_tcm_filter['cidade'] == cidade]
        filterJaneiroAtrasado = df_cidade.loc[df_cidade['1'] == 0]
        filterFevereiroAtrasado = df_cidade.loc[df_cidade['2'] == 0]
        filterMarcoAtrasado = df_cidade.loc[df_cidade['3'] == 0]
        filterAbrilAtrasado = df_cidade.loc[df_cidade['4'] == 0]
        filterMaioAtrasado = df_cidade.loc[df_cidade['5'] == 0]
        filterJunhoAtrasado = df_cidade.loc[df_cidade['6'] == 0]
        filterJulhoAtrasado = df_cidade.loc[df_cidade['7'] == 0]
        filterAgostoAtrasado = df_cidade.loc[df_cidade['8'] == 0]
        filterSetembroAtrasado = df_cidade.loc[df_cidade['9'] == 0]
        filterOutubroAtrasado = df_cidade.loc[df_cidade['10'] == 0]
        filterNovembroAtrasado = df_cidade.loc[df_cidade['11'] == 0]
        filterDezembroAtrasado = df_cidade.loc[df_cidade['12'] == 0]
        new_row = pd.Series({'cidade': cidade, 'ano': 2023,
                             'Janeiro': len(filterJaneiroAtrasado),
                             'Fevereiro': len(filterFevereiroAtrasado),
                             'Março': len(filterMarcoAtrasado),
                             'Abril': len(filterAbrilAtrasado),
                             'Maio': len(filterMaioAtrasado),
                             'Junho': len(filterJunhoAtrasado),
                             'Julho': len(filterJulhoAtrasado),
                             'Agosto': len(filterAgostoAtrasado),
                             'Setembro': len(filterSetembroAtrasado),
                             'Outubro': len(filterOutubroAtrasado),
                             'Novembro': len(filterNovembroAtrasado),
                             'Dezembro': len(filterDezembroAtrasado)})
        df_resumo = pd.concat(
            [df_resumo, new_row.to_frame().T], ignore_index=True)

    if mes_enviar == 1:
        atrasados = 0
        a_enviar = len(filterJaneiro)
        df_resumo['atrasado'] = 0
        df_resumo['a_enviar'] = df_resumo['Janeiro']
        COLUNAS = ['cidade', 'nome_orgao', 'ano', 'mes']
        df_tcm_mes = pd.DataFrame(columns=COLUNAS)

    elif mes_enviar == 2:
        atrasados = len(filterJaneiro)
        a_enviar = len(filterFevereiro)
        df_resumo['atrasado'] = df_resumo['Janeiro']
        df_resumo['a_enviar'] = df_resumo['Fevereiro']
        df_tcm_mes_1 = df_tcm[df_tcm['1'] == 0]

        df_tcm_mes_1['mes'] = 'Janeiro'
        df_tcm_mes = pd.concat(df_tcm_mes_1)

    elif mes_enviar == 3:
        atrasados = len(filterJaneiro) + len(filterFevereiro)
        a_enviar = len(filterMarco)
        df_resumo['atrasado'] = df_resumo['Janeiro'] + df_resumo['Fevereiro']
        df_resumo['a_enviar'] = df_resumo['Março']
        df_tcm_mes_1 = df_tcm[df_tcm['1'] == 0]
        df_tcm_mes_2 = df_tcm[df_tcm['2'] == 0]
        df_tcm_mes_1['mes'] = 'Janeiro'
        df_tcm_mes_2['mes'] = 'Fevereiro'

        df_tcm_mes = pd.concat([df_tcm_mes_1, df_tcm_mes_2])

    elif mes_enviar == 4:
        atrasados = len(filterJaneiro) + \
            len(filterFevereiro) + len(filterMarco)
        a_enviar = len(filterAbril)
        df_resumo['atrasado'] = df_resumo['Janeiro'] + \
            df_resumo['Fevereiro'] + df_resumo['Março']
        df_resumo['a_enviar'] = df_resumo['Abril']
        df_tcm_mes_1 = df_tcm[df_tcm['1'] == 0]
        df_tcm_mes_2 = df_tcm[df_tcm['2'] == 0]
        df_tcm_mes_3 = df_tcm[df_tcm['3'] == 0]

        df_tcm_mes_1['mes'] = 'Janeiro'
        df_tcm_mes_2['mes'] = 'Fevereiro'
        df_tcm_mes_3['mes'] = 'Março'

        df_tcm_mes = pd.concat([df_tcm_mes_1, df_tcm_mes_2, df_tcm_mes_3])
        df_tcm_mes = df_tcm_mes.drop(columns=[
            'codigo_municipio', 'codigo_orgao', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        df_tcm_mes = df_tcm_mes.reset_index(drop=True)

    elif mes_enviar == 5:
        atrasados = len(filterJaneiro) + len(filterFevereiro) + \
            len(filterMarco) + len(filterAbril)
        a_enviar = len(filterMaio)
        df_resumo['atrasado'] = df_resumo['Janeiro'] + \
            df_resumo['Fevereiro'] + df_resumo['Março'] + df_resumo['Abril']
        df_resumo['a_enviar'] = df_resumo['Maio']
        df_tcm_mes_1 = df_tcm[df_tcm['1'] == 0]
        df_tcm_mes_2 = df_tcm[df_tcm['2'] == 0]
        df_tcm_mes_3 = df_tcm[df_tcm['3'] == 0]
        df_tcm_mes_4 = df_tcm[df_tcm['4'] == 0]

        df_tcm_mes_1['mes'] = 'Janeiro'
        df_tcm_mes_2['mes'] = 'Fevereiro'
        df_tcm_mes_3['mes'] = 'Março'
        df_tcm_mes_4['mes'] = 'Abril'

        df_tcm_mes = pd.concat(
            [df_tcm_mes_1, df_tcm_mes_2, df_tcm_mes_3, df_tcm_mes_4])
        df_tcm_mes = df_tcm_mes.drop(columns=[
            'codigo_municipio', 'codigo_orgao', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        df_tcm_mes = df_tcm_mes.reset_index(drop=True)

    elif mes_enviar == 6:
        atrasados = len(filterJaneiro) + len(filterFevereiro) + \
            len(filterMarco) + len(filterAbril) + len(filterMaio)
        a_enviar = len(filterJunho)
        df_resumo['atrasado'] = df_resumo['Janeiro'] + df_resumo['Fevereiro'] + \
            df_resumo['Março'] + df_resumo['Abril'] + df_resumo['Maio']
        df_resumo['a_enviar'] = df_resumo['Junho']
        df_tcm_mes_1 = df_tcm[df_tcm['1'] == 0]
        df_tcm_mes_2 = df_tcm[df_tcm['2'] == 0]
        df_tcm_mes_3 = df_tcm[df_tcm['3'] == 0]
        df_tcm_mes_4 = df_tcm[df_tcm['4'] == 0]
        df_tcm_mes_5 = df_tcm[df_tcm['5'] == 0]

        df_tcm_mes_1['mes'] = 'Janeiro'
        df_tcm_mes_2['mes'] = 'Fevereiro'
        df_tcm_mes_3['mes'] = 'Março'
        df_tcm_mes_4['mes'] = 'Abril'
        df_tcm_mes_5['mes'] = 'Maio'

        df_tcm_mes = pd.concat(
            [df_tcm_mes_1, df_tcm_mes_2, df_tcm_mes_3, df_tcm_mes_4, df_tcm_mes_5])
        df_tcm_mes = df_tcm_mes.drop(columns=[
            'codigo_municipio', 'codigo_orgao', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        df_tcm_mes = df_tcm_mes.reset_index(drop=True)

    elif mes_enviar == 7:
        atrasados = len(filterJaneiro) + len(filterFevereiro) + \
            len(filterMarco) + len(filterAbril) + \
            len(filterMaio) + len(filterJunho)
        a_enviar = len(filterJulho)
        df_resumo['atrasado'] = df_resumo['Janeiro'] + df_resumo['Fevereiro'] + \
            df_resumo['Março'] + df_resumo['Abril'] + \
            df_resumo['Maio'] + df_resumo['Junho']
        df_resumo['a_enviar'] = df_resumo['Julho']
        df_tcm_mes_1 = df_tcm[df_tcm['1'] == 0]
        df_tcm_mes_2 = df_tcm[df_tcm['2'] == 0]
        df_tcm_mes_3 = df_tcm[df_tcm['3'] == 0]
        df_tcm_mes_4 = df_tcm[df_tcm['4'] == 0]
        df_tcm_mes_5 = df_tcm[df_tcm['5'] == 0]
        df_tcm_mes_6 = df_tcm[df_tcm['6'] == 0]

        df_tcm_mes_1['mes'] = 'Janeiro'
        df_tcm_mes_2['mes'] = 'Fevereiro'
        df_tcm_mes_3['mes'] = 'Março'
        df_tcm_mes_4['mes'] = 'Abril'
        df_tcm_mes_5['mes'] = 'Maio'
        df_tcm_mes_6['mes'] = 'Junho'

        df_tcm_mes = pd.concat(
            [df_tcm_mes_1, df_tcm_mes_2, df_tcm_mes_3, df_tcm_mes_4, df_tcm_mes_5, df_tcm_mes_6])
        df_tcm_mes = df_tcm_mes.drop(columns=[
            'codigo_municipio', 'codigo_orgao', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        df_tcm_mes = df_tcm_mes.reset_index(drop=True)

    elif mes_enviar == 8:
        atrasados = len(filterJaneiro) + len(filterFevereiro) + \
            len(filterMarco) + len(filterAbril) + \
            len(filterMaio) + len(filterJunho) + len(filterJulho)
        a_enviar = len(filterAgosto)
        df_resumo['atrasado'] = df_resumo['Janeiro'] + df_resumo['Fevereiro'] + df_resumo['Março'] + \
            df_resumo['Abril'] + df_resumo['Maio'] + \
            df_resumo['Junho'] + df_resumo['Julho']
        df_resumo['a_enviar'] = df_resumo['Agosto']
        df_tcm_mes_1 = df_tcm[df_tcm['1'] == 0]
        df_tcm_mes_2 = df_tcm[df_tcm['2'] == 0]
        df_tcm_mes_3 = df_tcm[df_tcm['3'] == 0]
        df_tcm_mes_4 = df_tcm[df_tcm['4'] == 0]
        df_tcm_mes_5 = df_tcm[df_tcm['5'] == 0]
        df_tcm_mes_6 = df_tcm[df_tcm['6'] == 0]
        df_tcm_mes_7 = df_tcm[df_tcm['7'] == 0]

        df_tcm_mes_1['mes'] = 'Janeiro'
        df_tcm_mes_2['mes'] = 'Fevereiro'
        df_tcm_mes_3['mes'] = 'Março'
        df_tcm_mes_4['mes'] = 'Abril'
        df_tcm_mes_5['mes'] = 'Maio'
        df_tcm_mes_6['mes'] = 'Junho'
        df_tcm_mes_7['mes'] = 'Julho'

        df_tcm_mes = pd.concat([df_tcm_mes_1, df_tcm_mes_2, df_tcm_mes_3, df_tcm_mes_4, df_tcm_mes_5, df_tcm_mes_6,
                                df_tcm_mes_7])
        df_tcm_mes = df_tcm_mes.drop(columns=[
            'codigo_municipio', 'codigo_orgao', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        df_tcm_mes = df_tcm_mes.reset_index(drop=True)

    elif mes_enviar == 9:
        atrasados = len(filterJaneiro) + len(filterFevereiro) + \
            len(filterMarco) + len(filterAbril) + len(filterMaio) + \
            len(filterJunho) + len(filterJulho) + len(filterAgosto)
        a_enviar = len(filterSetembro)
        df_resumo['atrasado'] = df_resumo['Janeiro'] + df_resumo['Fevereiro'] + df_resumo['Março'] + \
            df_resumo['Abril'] + df_resumo['Maio'] + \
            df_resumo['Junho'] + df_resumo['Julho'] + df_resumo['Agosto']
        df_resumo['a_enviar'] = df_resumo['Setembro']
        df_tcm_mes_1 = df_tcm[df_tcm['1'] == 0]
        df_tcm_mes_2 = df_tcm[df_tcm['2'] == 0]
        df_tcm_mes_3 = df_tcm[df_tcm['3'] == 0]
        df_tcm_mes_4 = df_tcm[df_tcm['4'] == 0]
        df_tcm_mes_5 = df_tcm[df_tcm['5'] == 0]
        df_tcm_mes_6 = df_tcm[df_tcm['6'] == 0]
        df_tcm_mes_7 = df_tcm[df_tcm['7'] == 0]
        df_tcm_mes_8 = df_tcm[df_tcm['8'] == 0]

        df_tcm_mes_1['mes'] = 'Janeiro'
        df_tcm_mes_2['mes'] = 'Fevereiro'
        df_tcm_mes_3['mes'] = 'Março'
        df_tcm_mes_4['mes'] = 'Abril'
        df_tcm_mes_5['mes'] = 'Maio'
        df_tcm_mes_6['mes'] = 'Junho'
        df_tcm_mes_7['mes'] = 'Julho'
        df_tcm_mes_8['mes'] = 'Agosto'

        df_tcm_mes = pd.concat([df_tcm_mes_1, df_tcm_mes_2, df_tcm_mes_3, df_tcm_mes_4, df_tcm_mes_5, df_tcm_mes_6,
                                df_tcm_mes_7, df_tcm_mes_8])
        df_tcm_mes = df_tcm_mes.drop(columns=[
            'codigo_municipio', 'codigo_orgao', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        df_tcm_mes = df_tcm_mes.reset_index(drop=True)

    elif mes_enviar == 10:
        atrasados = len(filterJaneiro) + len(filterFevereiro) + \
            len(filterMarco) + len(filterAbril) + len(filterMaio) + len(filterJunho) + \
            len(filterJulho) + len(filterAgosto) + len(filterSetembro)
        a_enviar = len(filterOutubro)
        df_resumo['atrasado'] = df_resumo['Janeiro'] + df_resumo['Fevereiro'] + df_resumo['Março'] + df_resumo['Abril'] + \
            df_resumo['Maio'] + df_resumo['Junho'] + df_resumo['Julho'] + \
            df_resumo['Agosto'] + df_resumo['Setembro']
        df_resumo['a_enviar'] = df_resumo['Outubro']
        df_tcm_mes_1 = df_tcm[df_tcm['1'] == 0]
        df_tcm_mes_2 = df_tcm[df_tcm['2'] == 0]
        df_tcm_mes_3 = df_tcm[df_tcm['3'] == 0]
        df_tcm_mes_4 = df_tcm[df_tcm['4'] == 0]
        df_tcm_mes_5 = df_tcm[df_tcm['5'] == 0]
        df_tcm_mes_6 = df_tcm[df_tcm['6'] == 0]
        df_tcm_mes_7 = df_tcm[df_tcm['7'] == 0]
        df_tcm_mes_8 = df_tcm[df_tcm['8'] == 0]
        df_tcm_mes_9 = df_tcm[df_tcm['9'] == 0]

        df_tcm_mes_1['mes'] = 'Janeiro'
        df_tcm_mes_2['mes'] = 'Fevereiro'
        df_tcm_mes_3['mes'] = 'Março'
        df_tcm_mes_4['mes'] = 'Abril'
        df_tcm_mes_5['mes'] = 'Maio'
        df_tcm_mes_6['mes'] = 'Junho'
        df_tcm_mes_7['mes'] = 'Julho'
        df_tcm_mes_8['mes'] = 'Agosto'
        df_tcm_mes_9['mes'] = 'Setembro'

        df_tcm_mes = pd.concat([df_tcm_mes_1, df_tcm_mes_2, df_tcm_mes_3, df_tcm_mes_4, df_tcm_mes_5, df_tcm_mes_6,
                                df_tcm_mes_7, df_tcm_mes_8, df_tcm_mes_9])
        df_tcm_mes = df_tcm_mes.drop(columns=[
                                     'codigo_municipio', 'codigo_orgao', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        df_tcm_mes = df_tcm_mes.reset_index(drop=True)

    elif mes_enviar == 11:
        atrasados = len(filterJaneiro) + len(filterFevereiro) + \
            len(filterMarco) + len(filterAbril) + len(filterMaio) + len(filterJunho) + \
            len(filterJulho) + len(filterAgosto) + \
            len(filterSetembro) + len(filterOutubro)
        a_enviar = len(filterNovembro)
        df_resumo['atrasado'] = df_resumo['Janeiro'] + df_resumo['Fevereiro'] + df_resumo['Março'] + df_resumo['Abril'] + \
            df_resumo['Maio'] + df_resumo['Junho'] + df_resumo['Julho'] + \
            df_resumo['Agosto'] + df_resumo['Setembro'] + df_resumo['Outubro']
        df_resumo['a_enviar'] = df_resumo['Novembro']
        df_tcm_mes_1 = df_tcm[df_tcm['1'] == 0]
        df_tcm_mes_2 = df_tcm[df_tcm['2'] == 0]
        df_tcm_mes_3 = df_tcm[df_tcm['3'] == 0]
        df_tcm_mes_4 = df_tcm[df_tcm['4'] == 0]
        df_tcm_mes_5 = df_tcm[df_tcm['5'] == 0]
        df_tcm_mes_6 = df_tcm[df_tcm['6'] == 0]
        df_tcm_mes_7 = df_tcm[df_tcm['7'] == 0]
        df_tcm_mes_8 = df_tcm[df_tcm['8'] == 0]
        df_tcm_mes_9 = df_tcm[df_tcm['9'] == 0]
        df_tcm_mes_10 = df_tcm[df_tcm['10'] == 0]

        df_tcm_mes_1['mes'] = 'Janeiro'
        df_tcm_mes_2['mes'] = 'Fevereiro'
        df_tcm_mes_3['mes'] = 'Março'
        df_tcm_mes_4['mes'] = 'Abril'
        df_tcm_mes_5['mes'] = 'Maio'
        df_tcm_mes_6['mes'] = 'Junho'
        df_tcm_mes_7['mes'] = 'Julho'
        df_tcm_mes_8['mes'] = 'Agosto'
        df_tcm_mes_9['mes'] = 'Setembro'
        df_tcm_mes_10['mes'] = 'Outubro'

        df_tcm_mes = pd.concat([df_tcm_mes_1, df_tcm_mes_2, df_tcm_mes_3, df_tcm_mes_4, df_tcm_mes_5, df_tcm_mes_6,
                                df_tcm_mes_7, df_tcm_mes_8, df_tcm_mes_9, df_tcm_mes_10])
        df_tcm_mes = df_tcm_mes.drop(columns=[
                                     'codigo_municipio', 'codigo_orgao', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        df_tcm_mes = df_tcm_mes.reset_index(drop=True)

    elif mes_enviar == 12:
        atrasados = len(filterJaneiro) + len(filterFevereiro) + \
            len(filterMarco) + len(filterAbril) + len(filterMaio) + len(filterJunho) + \
            len(filterJulho) + len(filterAgosto) + len(filterSetembro) + \
            len(filterOutubro) + len(filterNovembro)
        a_enviar = len(filterDezembro)
        df_resumo['atrasado'] = df_resumo['Janeiro'] + df_resumo['Fevereiro'] + df_resumo['Março'] + df_resumo['Abril'] + df_resumo['Maio'] + \
            df_resumo['Junho'] + df_resumo['Julho'] + df_resumo['Agosto'] + \
            df_resumo['Setembro'] + \
            df_resumo['Outubro'] + df_resumo['Novembro']
        df_resumo['a_enviar'] = df_resumo['Dezembro']
        df_tcm_mes_1 = df_tcm[df_tcm['1'] == 0]
        df_tcm_mes_2 = df_tcm[df_tcm['2'] == 0]
        df_tcm_mes_3 = df_tcm[df_tcm['3'] == 0]
        df_tcm_mes_4 = df_tcm[df_tcm['4'] == 0]
        df_tcm_mes_5 = df_tcm[df_tcm['5'] == 0]
        df_tcm_mes_6 = df_tcm[df_tcm['6'] == 0]
        df_tcm_mes_7 = df_tcm[df_tcm['7'] == 0]
        df_tcm_mes_8 = df_tcm[df_tcm['8'] == 0]
        df_tcm_mes_9 = df_tcm[df_tcm['9'] == 0]
        df_tcm_mes_10 = df_tcm[df_tcm['10'] == 0]
        df_tcm_mes_11 = df_tcm[df_tcm['11'] == 0]

        df_tcm_mes_1['mes'] = 'Janeiro'
        df_tcm_mes_2['mes'] = 'Fevereiro'
        df_tcm_mes_3['mes'] = 'Março'
        df_tcm_mes_4['mes'] = 'Abril'
        df_tcm_mes_5['mes'] = 'Maio'
        df_tcm_mes_6['mes'] = 'Junho'
        df_tcm_mes_7['mes'] = 'Julho'
        df_tcm_mes_8['mes'] = 'Agosto'
        df_tcm_mes_9['mes'] = 'Setembro'
        df_tcm_mes_10['mes'] = 'Outubro'
        df_tcm_mes_11['mes'] = 'Novembro'

        df_tcm_mes = pd.concat([df_tcm_mes_1, df_tcm_mes_2, df_tcm_mes_3, df_tcm_mes_4, df_tcm_mes_5, df_tcm_mes_6,
                                df_tcm_mes_7, df_tcm_mes_8, df_tcm_mes_9, df_tcm_mes_10, df_tcm_mes_11])
        df_tcm_mes = df_tcm_mes.drop(columns=[
            'codigo_municipio', 'codigo_orgao', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        df_tcm_mes = df_tcm_mes.reset_index(drop=True)

    data = df_tcm_mes.to_dict('records')
    columns = [{"name": i, "id": i, } for i in (df_tcm_mes.columns)]

    fig_grafico1 = go.Figure()
    fig_grafico1.add_trace(go.Bar(name="Atrasados",
                                  x=df_resumo['cidade'], y=df_resumo['atrasado']))
    fig_grafico1.add_trace(
        go.Bar(name="A Enviar", x=df_resumo['cidade'], y=df_resumo['a_enviar']))

    fig_grafico1.update_layout(margin=dict(l=0, r=0, t=0, b=0), autosize=True,
                               legend=dict(
                                   orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=0.21),
                               xaxis_title='Cidade', yaxis_title="Qtde a Enviar",
                               title=dict(text='<b>TCM-GO</b>', y=1, x=0.5, xanchor='center',
                                          yanchor='top', font=dict(size=20)))

    df_cauc = pd.read_csv(url, sep=';', encoding='latin-1', skiprows=[0, 1, 2, 5572, 5573, 5574, 5575, 5576, 5577, 5578, 5579, 5580, 5581, 5582,
                          5583, 5584, 5585, 5586, 5587, 5588, 5589, 5590, 5591, 5592, 5593, 5594, 5595, 5596, 5597, 5598, 5599, 5600, 5601, 5602, 5603, 5604, 5605])

    # cidades_cauc = {"Aguas Lindas": 5200258, "Americano do Brasil": 5200852, "Ap. de Goiânia": 5201405, "Caldas Novas": 5204508, "Catalão": 5205109, "Castelândia":  5205059, "Ceres": 5205406, "Goiatuba": 5209101, "Inaciolância": 5209937, "Ipameri": 5210109, "Luziânia": 5212501,
    # "Mineiros": 5213103, "Morrinhos": 5213806, "Cidade Ocidental": 5205497, "Pirenópolis": 5217302, "Santa Helena": 5219308, "Valparaíso": 5221858, "Aurilândia": 5202601, "Niquelândia": 5214606, "Goianésia": 5208608, "Sanclerlândia": 5219001, "Carmo do Rio Verde": 5205000, }

    cidades_cauc = {"Senador Canedo": 5220454, "Santo Antônio do Descoberto": 5219753, "Caldas Novas": 5204508,  "Guapo": 5209200,
                    "Montividiu": 5213756, "Iporá":  5210208, "Anápolis": 5201108, "Itarumã": 5211305, "Jataí": 5211909, "Fazenda Nova": 5207600}
    codigo = []
    for key, value in cidades_cauc.items():
        codigo.append(value)

    df_cauc_filter = df_cauc.loc[df_cauc["Código IBGE"].isin(codigo)]
    df_cauc_filter = df_cauc_filter.reset_index(drop=True)

    for key, value in cidades_cauc.items():
        df_cauc_filter.loc[df_cauc_filter["Código IBGE"]
                           == value, 'cidade'] = key
    pendencia = {}

    for indeces, row in df_cauc_filter.iterrows():
        lista_pendencia = []
        # print(row['cidade'], row['1.1'], row['1.3'],row['1.4'],row['1.5'],row['2.1.1'],row['2.1.2'],row['3.1.1'],
        #     row['3.1.2'],row['3.2.1'],row['3.2.2'], row['3.2.3'],row['3.2.4'], row['3.3'], row['3.4.1'], row['3.4.2'],
        #      row['3.5'],  row['4.1'], row['4.2'], row['5.1'], row['5.2'], row['5.3'], row['5.4'])
        if row['1.1'] == '!':
            lista_pendencia.append('1.1')

        if row['1.3'] == '!':
            lista_pendencia.append('1.3')

        if row['1.4'] == '!':
            lista_pendencia.append('1.4')

        if row['1.5'] == '!':
            lista_pendencia.append('1.5')

        if row['2.1.1'] == '!':
            lista_pendencia.append('2.1.1')

        if row['2.1.2'] == '!':
            lista_pendencia.append('2.1.2')

        if row['3.1.1'] == '!':
            lista_pendencia.append('3.1.1')

        if row['3.1.2'] == '!':
            lista_pendencia.append('3.1.2')

        if row['3.2.1'] == '!':
            lista_pendencia.append('3.2.1')

        if row['3.2.2'] == '!':
            lista_pendencia.append('3.2.2')

        if row['3.2.3'] == '!':
            lista_pendencia.append('3.2.3')

        if row['3.2.4'] == '!':
            lista_pendencia.append('3.2.4')

        if row['3.3'] == '!':
            lista_pendencia.append('3.3')

        if row['3.4.1'] == '!':
            lista_pendencia.append('3.4.1')

        if row['3.4.2'] == '!':
            lista_pendencia.append('3.4.2')

        if row['3.5'] == '!':
            lista_pendencia.append('3.5')

        if row['4.1'] == '!':
            lista_pendencia.append('4.1')

        if row['4.2'] == '!':
            lista_pendencia.append('4.2')

        if row['5.1'] == '!':
            lista_pendencia.append('5.1')

        if row['5.2'] == '!':
            lista_pendencia.append('5.2')

        if row['5.3'] == '!':
            lista_pendencia.append('5.3')

        if row['5.4'] == '!':
            lista_pendencia.append('5.4')
        pendencia[row['cidade']] = lista_pendencia

    colunas_cauc = ['cidade', 'Qtde']
    df_cauc_fig = pd.DataFrame(columns=colunas_cauc)
    for key, value in cidades.items():
        new_row = pd.Series({'cidade': key, 'Qtde': len(pendencia[key])})

        df_cauc_fig = pd.concat(
            [df_cauc_fig, new_row.to_frame().T], ignore_index=True)

    df_cauc_fig_filter = df_cauc_fig.loc[df_cauc_fig["cidade"].isin(
        municipios)]

    df_cauc_fig_filter = df_cauc_fig_filter.sort_values('cidade')
    df_cauc_fig_filter = df_cauc_fig_filter.reset_index(drop=True)
    qtde_cauc = df_cauc_fig_filter['Qtde'].sum()

    fig_grafico2 = go.Figure()
    fig_grafico2.add_trace(
        go.Bar(x=df_cauc_fig_filter['cidade'], y=df_cauc_fig_filter['Qtde']))

    fig_grafico2.update_layout(margin=dict(l=0, r=0, t=25, b=0),
                               legend=dict(
                                   orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=0.21),
                               xaxis_title='Cidade', yaxis_title="Qtde de Pendências",
                               title=dict(text='<b>CAUC</b>', y=1, x=0.5, xanchor='center',
                                          yanchor='top', font=dict(size=20)))
    # fig_grafico2.update_layout(template=template)

    # dash_table.DataTable(data=data, columns=columns, page_size=6)
    return atrasados, a_enviar, qtde_cauc, fig_grafico1, fig_grafico2


# @app.callback([Output('teste_atualizar', 'children')],
# [Input('buscar_dados', 'n_intervals')])
# def update_timestamp(interval):
# data_e_hora_atuais = datetime.now()
# print("*-*-*-*-*-*-*-*-*-*-*-*")
# print(data_e_hora_atuais)
# print("*-*-*-*-*-*-*-*-*-*-*-*")
# data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
# return [f"Última Atualização: {data_e_hora_em_texto}"]


if __name__ == '__main__':
    app.run_server(debug=True)
