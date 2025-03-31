from pandas import read_excel

CONCLUSIONES = "5. Conclusiones del Comité"


def read_user_data(cached_file, nombre_reportado):
    df = read_excel(cached_file, sheet_name=nombre_reportado)
    fila = detect_copy_range(df, CONCLUSIONES)
    print(f"Fila de inicio: {fila}")
    texto = copy_user_data(df, fila)
    print(texto)


def detect_copy_range(df, frase):
    return (
        df[df[df.columns[1]] == frase].index.tolist()[0]
        if not df[df[df.columns[1]] == frase].empty
        else None
    )


def copy_user_data(df, fila):
    rango = df.iloc[8:fila, 1:14]
    rango = rango.dropna(how="all").fillna("")
    texto = "\n".join("\t".join(map(str, fila)) for fila in rango.values)
    return texto
