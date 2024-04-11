from Lib.library import pyodbc,os,load_dotenv,pd

load_dotenv()

DATABASE=os.getenv('DATABASE')
USER=os.getenv('USER')
PW=os.getenv('PASSWD')
SERVER=os.getenv('SERVER')
DRIVER=os.getenv('DRIVER')


def conexao(query):
    conn = pyodbc.connect(driver=DRIVER,
                          server=SERVER,
                          database=DATABASE,
                          uid=USER,
                          pwd=PW)

    cursor = conn.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    rows=cursor.fetchall()
    # Feche o cursor e a conexão
    cursor.close()
    conn.close()
    
    data=[tuple(row) for row in rows]
    df = pd.DataFrame(data, columns=columns)
    df['DATA RECEBIMENTO'] = pd.to_datetime(df['DATA RECEBIMENTO'], errors='coerce')

    # Format 'DATA RECEBIMENTO' column to 'dd-mm-yyyy'
    df['DATA RECEBIMENTO'] = df['DATA RECEBIMENTO'].dt.strftime('%d-%m-%Y')

    return df

def conexao_padrao(query):
    conn = pyodbc.connect(driver=DRIVER,
                          server=SERVER,
                          database=DATABASE,
                          uid=USER,
                          pwd=PW)

    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    total_count = result[0]

    cursor.close()
    conn.close()

    return total_count
    
def conexaomain():
    conn = pyodbc.connect(driver=DRIVER,
                          server=SERVER,
                          database=DATABASE,
                          uid=USER,
                          pwd=PW)

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM CP_ORDENSCOMPRAITENS WHERE TIPOMOVIMENTACAO NOT IN (23, 90);")
    total_rows = cursor.fetchone()[0]
    conn.close()
    return total_rows
   
   
       
def conexaoteste(query):
    conn = pyodbc.connect(driver=DRIVER,
                          server=SERVER,
                          database=DATABASE,
                          uid=USER,
                          pwd=PW)

    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Obter os nomes das colunas
    columns = [column[0] for column in cursor.description]
    
    # Criar um DataFrame com os resultados e os nomes das colunas
    df = pd.DataFrame.from_records(results, columns=columns)

    cursor.close()
    conn.close()

    return df


def conexaoraking(query):
    conn = pyodbc.connect(driver=DRIVER,
                          server=SERVER,
                          database=DATABASE,
                          uid=USER,
                          pwd=PW)

    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall() 
    total_count = results

    cursor.close()
    conn.close()

    return total_count