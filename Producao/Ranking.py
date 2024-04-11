from rotas.function import ranking
from Lib.library import *


def main():
    # Importar a biblioteca FontAwesome
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        """,
        unsafe_allow_html=True
    )
    
    data = ranking()
    st.title("Ranking")
    
    
    col1, col2 = st.columns(2)
    
    
    with col1:
        st.markdown(f"<p style='text-align: center; color: white; font-size:20px'>CONFERENTE</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p style='text-align: center; color: white; font-size:20px'>QUANTIDADE DE ITENS</p>", unsafe_allow_html=True)

    for index, (nome, quantidade) in enumerate(data):
        with col1:

            if index == 0:  # Se for o primeiro lugar, adicionar uma estrela
                st.markdown(f"<p style='text-align: center; color: white; font-size:20px'><i class='fas fa-star'></i> {nome}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='text-align: center; color: white; font-size:20px'>{nome}</p>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<p style='text-align: center; color: white; font-size:20px'>{quantidade}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()