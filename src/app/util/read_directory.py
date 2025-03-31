from pandas import read_excel


def read_directory_data(cached_file):
    df = read_excel(cached_file, sheet_name="Comité")
    df.dropna(subset=["Consecutivo UIAF"], inplace=True)
    columns_filter = [
        "Consecutivo UIAF",
        "No CASO",
        "CLIENTE",
        "CC/ NIT",
        "DECISIÓN COMITÉ",
    ]
    dictionary = filter_type(df[columns_filter])
    return dictionary


def filter_type(dataframe):
    dictionary = {
        "COMISIONISTA": dataframe[
            dataframe["DECISIÓN COMITÉ"].str.contains("COMISIONISTA", na=False)
        ],
        "FIDUCIARIA": dataframe[
            dataframe["DECISIÓN COMITÉ"].str.contains("FIDUCIARIA", na=False)
        ],
        "NORMAL": dataframe[
            ~dataframe["DECISIÓN COMITÉ"].str.contains(
                "COMISIONISTA|FIDUCIARIA", na=False
            )
        ],
    }
    return dictionary
