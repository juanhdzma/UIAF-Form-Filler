from pandas import read_excel


def read_directory_data(cached_file):
    df = read_excel(cached_file, sheet_name="Comité", dtype=str)
    df.dropna(subset=["Consecutivo UIAF"], inplace=True)
    selected_columns = [
        "Consecutivo UIAF",
        "No CASO",
        "CLIENTE",
        "CC/ NIT",
        "DECISIÓN COMITÉ",
        "Filial",
    ]
    dictionary = split_by_source(df[selected_columns])
    dictionary = split_by_type(dictionary)
    return dictionary


def split_by_source(dataframe):
    dictionary = {
        "Banco": dataframe[dataframe["Filial"] == "Banco"],
        "Fiduciaria": dataframe[dataframe["Filial"] == "Fiduciaria"],
        "Comisionista": dataframe[dataframe["Filial"] == "Comisionista"],
    }
    return dictionary


def split_by_type(dictionary):
    result = {}
    for key, df_branch in dictionary.items():
        result[key] = {
            "ROS": df_branch[
                ~df_branch["DECISIÓN COMITÉ"].str.contains(
                    "reputacional|tentativa de vinculación|operación intentada",
                    case=False,
                    na=False,
                )
            ],
            "Reputacional": df_branch[df_branch["DECISIÓN COMITÉ"].str.contains("reputacional", case=False, na=False)],
            "Intentadas": df_branch[df_branch["DECISIÓN COMITÉ"].str.contains("tentativa de vinculación|operación intentada", case=False, na=False)],
        }
    return result
