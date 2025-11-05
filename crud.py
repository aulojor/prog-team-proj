import pandas as pd
import parser

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)

def read_ids(df):
    # Lista de IDs únicos no DataFrame
    return sorted(set(df["ID"]))

def read_header(df, event_id):
    # Informações do header do evento
    row = df[df["ID"] == event_id].iloc[0]
    cols = list(df.columns)
    headerCols = ["DateTime", "Distance Indicator", "Event ID", "Lat", "Long", "Depth", "Agency", "Magnitudes"]
    # end = cols.index("ID") - 1
    # header_cols = cols[:end]
    # Para selecionar todas as colunas em vez de só algumas
    info = []
    for (i, col) in enumerate(headerCols):
        info.append(f"{i+1} {col}: {row[col]}")
    infoString = f"Event {event_id} header:\n" + "\n".join(info) 
    return infoString


def get_table(df, event_id):
    # retorna a tabela de dados do evento
    rows = df[df["ID"] == event_id]
    cols = list(df.columns)
    start = cols.index("ID") + 1
    table = rows[cols[start:]].iloc[1:]
    return table

def read_table_row(df, event_id, row_number):
    # retorna uma linha específica da tabela
    table = get_table(df, event_id)
    if row_number < 0 or row_number >= len(table):
        return f"Linha {row_number} não pertence ao evento {event_id}."
    row = table.iloc[row_number]
    cols = list(df.columns)
    start = cols.index("STAT")
    tableCols = cols[start:]
    info = []
    for (i, col) in enumerate(tableCols):
        info.append(f"{i+1} {col}: {row[col]}")
        # TODO corrigir numeros acima de 10 arruinando o alinhamento
    infoString = f"Event {event_id}, row {row_number} header:\n" + "\n".join(info) 
    return infoString


# teste temporário enquanto não temnos menu
if __name__ == "__main__":
    df = parser.parse()
    first_id = read_ids(df)[0]
    print(read_ids(df))
    print("\n")
    print(read_header(df, first_id))
    print("\n")
    print(get_table(df, first_id))
    print("\n")
    print(read_table_row(df, first_id, 2))
