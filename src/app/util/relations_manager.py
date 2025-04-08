from openpyxl import load_workbook

# Constants
NATURAL = ["C", "E", "P", "T", "NAN"]
JURIDICAL = ["N", "NAJ"]

tipo_map_juridicas = {"N": "NIT", "NAJ": "Sociedad extranjera sin NIT en Colombia"}

tipo_map_naturales = {
    "C": "Cédula de ciudadanía",
    "E": "Cédula de extranjería",
    "P": "Pasaporte",
    "T": "Tarjeta de identidad",
    "NAN": "Documento de identificación extranjero",
}


def load_templates(tipo):
    if tipo == "NATURAL":
        return load_workbook("src/templates/Naturales.xlsx")
    elif tipo == "JURIDICA":
        return load_workbook("src/templates/Juridicas.xlsx")


def create_excel_file(filas, tipo):
    excel = load_templates(tipo)
    sheet = excel.active

    for i, fila in enumerate(filas, start=4):
        for j, value in enumerate(fila, start=1):
            sheet.cell(row=i, column=j, value=value)

    excel.save(f"output_files/{tipo}.xlsx")
    excel.close()


def procesar_juridicas(df):
    documento_counter = 0
    rl_counter = 0
    filas = []

    for i, row in df.iterrows():
        tipo = tipo_map_juridicas.get(str(row["Tipo de documento"]).upper(), "")
        documento = str(row["Documento "])

        if documento.strip() == "":
            documento = documento_counter
            documento_counter += 1

        rl_counter += 1
        nombre = row["Nombre"]
        relacion = row["Relación"]

        fila = [
            tipo,
            documento,
            nombre,
            "NA",
            "NA",
            "NA",
            "Cédula de ciudadanía",
            f"{i+1}",
            relacion,
            "NO",
        ]
        filas.append(fila)

    return filas


def procesar_naturales(df):
    documento_counter = 0
    filas = []

    for i, row in df.iterrows():
        tipo_raw = str(row["Tipo de documento"]).upper()
        tipo = tipo_map_naturales.get(tipo_raw, "DESCONOCIDO")

        documento = str(row["Documento "])
        if documento.strip() == "":
            documento = documento_counter
            documento_counter += 1

        nombre = row["Nombre"]
        relacion = row["Relación"]

        partes = str(nombre).split()

        if len(partes) >= 4:
            primer_nombre = " ".join(partes[:-3])
            primer_apellido = partes[-2]
            segundo_apellido = partes[-1]
        elif len(partes) == 3:
            primer_nombre = partes[0]
            primer_apellido = partes[1]
            segundo_apellido = partes[2]
        elif len(partes) == 2:
            primer_nombre = partes[0]
            primer_apellido = partes[1]
            segundo_apellido = ""
        else:
            primer_nombre = nombre
            primer_apellido = ""
            segundo_apellido = ""

        fila = [
            tipo,
            documento,
            primer_nombre,
            primer_apellido,
            segundo_apellido,
            relacion,
            "NO",
        ]
        filas.append(fila)

    return filas


def process_relation_df(df, tipo):
    if tipo == "NATURAL":
        valores = NATURAL
        df_filtrado = df[df["Tipo de documento"].isin(valores)]
        filas = procesar_naturales(df_filtrado)
    elif tipo == "JURIDICA":
        valores = JURIDICAL
        df_filtrado = df[df["Tipo de documento"].isin(valores)]
        filas = procesar_juridicas(df_filtrado)

    create_excel_file(filas, tipo)
