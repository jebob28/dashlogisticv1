from Lib.library import *
from database.conection import conexaomain
from rotas.function import *

PAGE_SIZE = 11  # Define o tamanho da página
UPDATE_INTERVAL = 30  # Define o intervalo de atualização em segundos



def highlight_status(value):
    if value == 'RECEBENDO':
        return 'background-color: blue'
    elif value == 'PARCIAL':
        return 'background-color: yellow'
    elif value == 'ENCERRADA':
        return 'background-color: green'
    elif value =='CANCELADA':
        return 'background-color: Purple'
        
    else:
        return 'background-color: red'

def main():
    # Set page layout to wide-screen
    st.set_page_config(layout="wide")

    # Remover barra de rolagem horizontal
    st.markdown("""
    <style>
    .body {
        height: 100vh !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Recebimento ")
    data_atual = st.date_input('Selecione a data:', datetime.now().date())
    data_atual = data_atual.strftime('%Y-%m-%d')
    # Criando o menu lateral
    opcoes = ['TODOS', 'ENCERRADAS', 'RECEBENDO','PENDENTES','PARCIAL']

    # Widget para selecionar uma opção da lista
    opcao_selecionada = st.selectbox('Selecione uma opção:', opcoes)

    # Adicionando opções ao menu

    info_ordens_status_quatro = ordemcompra_status_quatro(data_atual)
    statusdois = ordemcompra_status_dois(data_atual)
    statusgeral = ordemcompra_geral(data_atual)
    statustre=ordemcompra_status_tres(data_atual)
    statuscinco=ordemcompra_status_cinco(data_atual)
    statusum=ordemcompra_status_um(data_atual)

    # Define o conteúdo do card
    percent_dois = (statusdois / statusgeral) * 100
    percent_tres = (statustre / statusgeral) * 100
    percent_quatro = (info_ordens_status_quatro / statusgeral) * 100
    porcent_cinco=(statuscinco / statusgeral) * 100
    porcent_um=(statusum/statusgeral)*100

    # Conteúdo dos cards
    bar_height_dois = percent_dois
    bar_height_quatro = percent_quatro
    bar_height_tres = percent_tres
    bar_height_cinco = porcent_cinco
    bar_height_um = porcent_um

    html_bar_dois = f'<div class="bar" style="width: { bar_height_dois}%;"></div>'
    html_bar_quatro = f'<div class="bar" style="width: {bar_height_quatro}%;"></div>'
    html_bar_tres = f'<div class="bar" style="width: {bar_height_tres}%;"></div>'
    html_bar_um = f'<div class="bar" style="width: {bar_height_um}%;"></div>'
    html_bar_cinco = f'<div class="bar" style="width: {bar_height_cinco}%;"></div>'

    # Conteúdo dos cards com os gráficos de barras horizontais
    conteudo_cards = f"""
    <div style="display: flex;">
        <div style="flex: 1; padding: 7px;  border-radius: 10px;">
            <p style="color: #33333;">ORDEM DE COMPRAS DO DIA</p>
            <h2 style="font-size: 40px;">{statusgeral}</h2>
        </div>
        <div style="flex: 1; padding: 7px; margin-left:-20px;    border-radius: 10px;">
            <p style="color: #33333;">ORDEM COMPRAS A RECEBER</p>
            <h2 style="font-size: 40px;">{statusdois}</h2>
            <div>{percent_dois:.2f}%</div>
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
        <div style="flex: 1; padding: 7px;margin-left:-20px background-color: #f0f0f0; border-radius: 10px;">
            <p style="color: #33333;">CADASTRADA</p>
            <h2 style="font-size: 40px;">{statusum}</h2>
            <div>{porcent_um:.2f}%</div>
            <div class="bar-chart-horizontal">{html_bar_um}</div>
        </div>
        <div style="flex: 1; padding: 7px;margin-left:-20px background-color: #f0f0f0; border-radius: 10px;">
            <p style="color: #33333;">CANCELADAS</p>
            <h2 style="font-size: 40px;">{statuscinco}</h2>
            <div>{porcent_cinco:.2f}%</div>
            <div class="bar-chart-horizontal">{html_bar_cinco}</div>
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
    </style>
    """

    # Combinar conteúdo do card e estilos CSS
    conteudo_cards += styles

    # Exibir o conteúdo HTML na interface do Streamlit
    st.markdown(conteudo_cards, unsafe_allow_html=True)

    # Calculate total number of rows

    # Determine total number of pages
    num_pages = conexaomain() // PAGE_SIZE + (1 if conexaomain() % PAGE_SIZE > 0 else 0)

    # Select page to display
    page_number = st.number_input("Enter page number:", min_value=1, max_value=num_pages, value=1)

    data_formatada = datetime.strptime(data_atual, "%Y-%m-%d").strftime("%d/%m/%Y")

    if opcao_selecionada == 'TODOS':
        offset = (page_number - 1) * PAGE_SIZE
        df = execute_sql_query(offset, PAGE_SIZE, data_formatada)
    elif opcao_selecionada == 'PENDENTES':
        df = filtro_status_dois(data_formatada)

    elif opcao_selecionada == 'ENCERRADAS':
        df = filtro_status_quatro(data_formatada)
    elif opcao_selecionada == 'RECEBENDO':
        df = filtro_status_tres(data_formatada)
    else:
        df=filtro_parcial(data_formatada)

    # Apply style to DataFrame
    styled_df = df.style.applymap(highlight_status, subset=['STATUS'])

    # Convert styled DataFrame to HTML
    styled_html = styled_df.to_html(escape=False)

    # Display the HTML using Streamlit
    st.write(styled_html, unsafe_allow_html=True)

   
      

if __name__ == "__main__":
    main()
