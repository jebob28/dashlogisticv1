import streamlit as st
import pandas as pd
import pyodbc
import time
from Lib.library import *
from database.conection import conexaomain
from rotas.function import *





PAGE_SIZE = 8 # Define o tamanho da página
UPDATE_INTERVAL = 10 
MIN_ROWS = 2 # Define o intervalo de atualização em segundos



def main_principal():
    
    df = teste()
    df2 = receptor()
    
    # Remover duplicatas de df2
    df2_unique = df2.groupby('FORNECEDOR').first().reset_index()

    # Criar um dicionário com os fornecedores e seus respectivos nomes
    fornecedores_nomes = dict(zip(df2_unique['FORNECEDOR'], df2_unique['Nomes']))

    # Mapear os nomes correspondentes no DataFrame df usando o dicionário
    df['Nomes'] = df['FORNECEDOR'].map(fornecedores_nomes)

    # Criar a coluna 'Conferente' com base no status
    df['Conferente'] = df.apply(lambda x: x['Nomes'].upper() if x['STATUS'] in ['ENCERRADA', 'RECEBENDO','PARCIAL'] else '', axis=1)

    # Reorganizar as colunas para colocar 'Conferente' após 'Falta Receber'
    columns = df.columns.tolist()
    columns.insert(columns.index('FALTA RECEBER') + 1, columns.pop(columns.index('Conferente')))
    df = df[columns]

    # Remover a coluna 'Nomes' do DataFrame final
    df.drop(columns=['Nomes'], inplace=True)
    df.drop(columns=['FORNECEDOR'], inplace=True)
    df.rename(columns={'Conferente': 'CONFERENTE'}, inplace=True)
    df.rename(columns={'NUMERO': 'NUMERO  OC'}, inplace=True)
    df.rename(columns={'nome do produto': 'PRODUTO'}, inplace=True)
    df['QTD SOLICITADA'] = df['QTD SOLICITADA'].astype(int)
    df['QTD RECEBIDA'] = df['QTD RECEBIDA'].astype(int)
    df['FALTA RECEBER'] = df['FALTA RECEBER'].astype(int)
    
    # Exibir a tabela com os dados e a coluna 'Conferente' após 'Falta Receber'
    
    return df



def ordemcompra_geral():
    conn = pyodbc.connect(driver='{SQL Server}',
                          server='192.168.1.50',
                          database='CORP_CAISP',
                          uid='sa',
                          pwd='H0rt@1!ca5')

    cursor = conn.cursor()

    query = """ SELECT COUNT(DISTINCT NUMERO) AS ORDEM_DE_COMPRA
                FROM CP_ORDENSCOMPRA WITH (NOLOCK)
                WHERE CONVERT(date, CP_ORDENSCOMPRA.K_DATADOPEDIDO) = CONVERT(date, GETDATE());"""
    cursor.execute(query)
    result = cursor.fetchone()
    total_count = result[0]

    cursor.close()
    conn.close()

    return total_count

def ordemcompra_status_dois():
    conn = pyodbc.connect(driver='{SQL Server}',
                          server='192.168.1.50',
                          database='CORP_CAISP',
                          uid='sa',
                          pwd='H0rt@1!ca5')

    cursor = conn.cursor()

    query = """ SELECT COUNT(NUMERO) AS Total_Count
                FROM CP_ORDENSCOMPRA WITH (NOLOCK)
                WHERE STATUS = 2
                AND CONVERT(date, CP_ORDENSCOMPRA.K_DATADOPEDIDO) = CONVERT(date, GETDATE());"""
    cursor.execute(query)
    result = cursor.fetchone()
    total_count = result[0]

    cursor.close()
    conn.close()

    return total_count

def ordemcompra_status_quatro():
    conn = pyodbc.connect(driver='{SQL Server}',
                          server='192.168.1.50',
                          database='CORP_CAISP',
                          uid='sa',
                          pwd='H0rt@1!ca5')

    cursor = conn.cursor()

    query = """ SELECT COUNT(NUMERO) AS Total_Count
                FROM CP_ORDENSCOMPRA WITH (NOLOCK)
                WHERE STATUS = 4
                AND CONVERT(date, CP_ORDENSCOMPRA.K_DATADOPEDIDO) = CONVERT(date, GETDATE());"""
    cursor.execute(query)
    result = cursor.fetchone()
    total_count = result[0]

    cursor.close()
    conn.close()

    return total_count

def ordemcompra_status_tres():
    conn = pyodbc.connect(driver='{SQL Server}',
                          server='192.168.1.50',
                          database='CORP_CAISP',
                          uid='sa',
                          pwd='H0rt@1!ca5')

    cursor = conn.cursor()

    query = """ SELECT COUNT(NUMERO) AS Total_Count
                FROM CP_ORDENSCOMPRA WITH (NOLOCK)
                WHERE STATUS = 3
                AND CONVERT(date, CP_ORDENSCOMPRA.K_DATADOPEDIDO) = CONVERT(date, GETDATE());"""
    cursor.execute(query)
    result = cursor.fetchone()
    total_count = result[0]

    cursor.close()
    conn.close()

    return total_count

def highlight_status(value):
    if value == 'RECEBENDO':
        return 'background-color: blue'
    elif value == 'PARCIAL':
        return 'background-color: yellow'
    elif value == 'ENCERRADA':
        return 'background-color: green'
        
    else:
        return 'background-color: red'


def truck_icon(status):
    if status == 'PENDENTE':
        return '<i class="fas fa-truck  pendente-icon" style="color: red; font-size: 24px;"></i>'   # Ícone de caminhão para status PENDENTE virado para a esquerda
    elif status == 'ENCERRADA':
        return '<i class="fas fa-truck truck-icon right" style="color: green; font-size: 24px;"></i>'  # Ícone de caminhão para status ENCERRADA
    elif status == 'PARCIAL':
        return '<i class="fas fa-truck truck-icon" style="color: yellow; font-size: 24px;"></i>'  # Ícone de caminhão para status PARCIAL
    elif status == 'RECEBENDO':
        return '<i class="fas fa-truck-loading " style="color: blue; font-size: 24px;"></i>'  # Ícone de caminhão para status RECEBENDO
    else:
        return ''








def slideshow_tabela(velocidade, offset):
    tabela = st.empty()  # Elemento vazio para atualizar a tabela
    
    while True:
        df = main_principal()

        # Limita o DataFrame apenas às primeiras 10 linhas
        df_slice = df.iloc[offset:offset + PAGE_SIZE]
        
        if len(df_slice) < MIN_ROWS:
            offset = 0  # Retorna ao início se houver menos de MIN_ROWS linhas
        
        df_slice['STATUS CAMINHAO'] = df_slice['STATUS'].apply(truck_icon)
        # Aplica o estilo ao DataFrame
        styled_df = df_slice.style.applymap(highlight_status, subset=['STATUS'])
        # Converte o DataFrame estilizado para HTML
        styled_html = styled_df.to_html(escape=False)
        
        # Exibe o HTML usando Streamlit
        tabela.write(styled_html, unsafe_allow_html=True)
        
        # Incrementa o offset para a próxima página
        offset += PAGE_SIZE
        
        # Aguarda o intervalo de tempo antes de exibir a próxima página
        time.sleep(velocidade)

    
    
def main():
 
    # Set page layout to wide-screen
    st.set_page_config(layout="wide")

    st.markdown(
    """
    <style>
    .stApp {
        margin-top: -110px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    with open("animation.css", "r") as f:
        css_content = f.read()

    # Adiciona o conteúdo do CSS ao aplicativo Streamlit
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    
    
    st.title("Recebimento ")

    
    info_ordens_status_quatro = ordemcompra_status_quatro()
    statusdois = ordemcompra_status_dois()
    statusgeral = ordemcompra_geral()
    statustre=ordemcompra_status_tres()

    # Define o conteúdo do card
    percent_dois = (statusdois / statusgeral) * 100
    percent_tres = (statustre / statusgeral) * 100
    percent_quatro = (info_ordens_status_quatro / statusgeral) * 100

    if percent_dois > 100:
        percent_dois = 100
    
    
    # Conteúdo dos cards
    bar_height_dois = percent_dois
    bar_height_quatro = percent_quatro
    bar_height_tres = percent_tres

    html_bar_dois = f'<div class="bar_red" style="width: { bar_height_dois}%;"></div>'
    html_bar_quatro = f'<div class="bar_green" style="width: {bar_height_quatro}%;"></div>'
    html_bar_tres = f'<div class="bar" style="width: {bar_height_tres}%;"></div>'

    # Conteúdo dos cards com os gráficos de barras horizontais
    conteudo_cards = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">'
    <div style="display: flex;">
        <div style="flex: 1; padding: 7px;  border-radius: 10px;">
            <p style="color: #33333;">ORDEM DE COMPRAS DO DIA</p>
            <h2 style="font-size: 40px;">{statusgeral}</h2>
        </div>
        <div style="flex: 1; padding: 7px; margin-left:-20px;    border-radius: 10px;">
            <p style="color: #33333;">ORDEM COMPRAS A RECEBER</p>
            <h2 style="font-size: 40px;">{statusdois}</h2>
            <div>{percent_dois:.0f}%</div>
            <div class="bar-chart-horizontal">{html_bar_dois}</div>
        </div>
        <div style="flex: 1; padding: 7px;margin-left:-20px background-color: #f0f0f0; border-radius: 10px;">
            <p style="color: #33333;">ORDEM COMPRAS RECEBIDAS</p>
            <h2 style="font-size: 40px;">{info_ordens_status_quatro}</h2>
            <div>{percent_quatro:.2f}%</div>
            <div class="bar-chart-horizontal">{html_bar_quatro}</div>
        </div>
        <div style="flex: 1; padding: 7px;margin-left:-20px background-color: #f0f0f0; border-radius: 10px;">
            <p style="color: #33333;">EM RECEBIMENTO</p>
            <h2 style="font-size: 40px;">{statustre}</h2>
            <div>{percent_tres:.2f}%</div>
            <div class="bar-chart-horizontal">{html_bar_tres}</div>
        </div>
    </div>
    """

    # Estilos CSS para os gráficos de barras horizontais
    styles = """
    <style>
        .bar-chart-horizontal {
            height: 30px;
            width: 100%;
            background-color: #f0f0f0;
            border-radius: 5px;
            overflow: hidden;
        }

        .bar {
            height: 100%;
            background-color: #007bff;
            transition: width 0.5s;
        }
        .bar_red {
            height: 100%;
            background-color: #cc0000;
            transition: width 0.5s;
        }
        .bar_green {
            height: 100%;
            background-color: #059629;
            transition: width 0.5s;
        }

        @keyframes moveTruck {
            0% {
                transform: translateX(-100%);
            }
            100% {
                transform: translateX(100%);
            }
        }

        .truck-icon {
            font-size: 50px;
            animation: moveTruck 5s linear infinite; /* Altere a duração da animação conforme necessário */
        }
    </style>
    """

    # Combinar conteúdo do card e estilos CSS
    conteudo_cards += styles

    # Exibir o conteúdo HTML na interface do Streamlit
    st.markdown(conteudo_cards, unsafe_allow_html=True)

    # Calculate total number of rows
    conn = pyodbc.connect(driver='{SQL Server}',
                        server='192.168.1.50',
                        database='CORP_CAISP',
                        uid='sa',
                        pwd='H0rt@1!ca5')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM CP_ORDENSCOMPRAITENS WHERE TIPOMOVIMENTACAO NOT IN (23, 90);")
    total_rows = cursor.fetchone()[0]
    conn.close()

    # Determine total number of pages
    

    # Select page to display
    offset = 0

    # Velocidade de exibição do slideshow
    velocidade = 10

    # Exibir o slideshow da tabela
    slideshow_tabela(velocidade, offset)

    st.experimental_autorefresh(interval=60000) # Atualiza a página a cada 60 segundos

        
            

if __name__ == "__main__":
 
    main()