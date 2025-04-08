from pandas import read_excel, DataFrame, concat
from app.util.convert import format_date
from app.util.convert import obtener_motivo_mas_parecido

# Constantes de etiquetas utilizadas en la hoja de Excel
CELDA_MOTIVO = "vii. Temática Asociada a LA/FT"
CELDA_CASE_ID = "No. Caso"
CELDA_TIPO_DOCUMENTO = "J10"
CELDA_DOCUMENTO = "L10"
CELDA_VALOR = "Valor Reporte"
COLUMNA_FECHA_INICIO = "F"
COLUMNA_FECHA_FIN = "H"
CONCLUSIONES = "5. Conclusiones del Comité"
RAZONES_FIN = "iii. Movimientos a destacar"
RAZONES_INICIO = "ii. Razones del reporte: Inusualidades encontradas"
RELACIONADOS_FIN = "v. Explicación de la operación "
RELACIONADOS_INICIO = "iv. Relacionados"

# Direcciones posibles para obtener_valor_celda
DIRECCION_DERECHA = "R"
DIRECCION_DOS_DERECHA = "RR"
DIRECCION_ABAJO = "D"


def read_user_data(cached_file, nombre_reportado):
    excel = read_excel(cached_file, sheet_name=nombre_reportado, header=None)

    texto_detalles = extraer_texto_detalles_usuario(
        excel, buscar_fila_por_etiqueta(excel, CONCLUSIONES, "B")
    )

    relacionados = extraer_relacionados(excel)
    tipo_documento = obtener_valor_celda(excel, CELDA_TIPO_DOCUMENTO)
    documento = obtener_valor_celda(excel, CELDA_DOCUMENTO)
    relacionado_reporte = {
        "Nombre": nombre_reportado,
        "Tipo de documento": tipo_documento,
        "Documento ": documento,
        "Relación": "CLIENTE",
    }

    relacionados = concat(
        [relacionados, DataFrame([relacionado_reporte])], ignore_index=True
    )

    case_id = relacionados["No. Caso"][0]

    razones = extraer_razones(excel)
    motivo = extraer_valor(excel, CELDA_MOTIVO, "C", DIRECCION_ABAJO)
    valor = extraer_valor(excel, CELDA_VALOR, "C", DIRECCION_DOS_DERECHA)
    fechas = extraer_fechas(excel)

    return {
        "case_id": case_id,
        "texto_detalles": texto_detalles,
        "relacionados": relacionados,
        "motivo": obtener_motivo_mas_parecido(motivo),
        "valor": round(valor),
        "razones": razones,
        "fecha_inicio": fechas["fecha_inicio"],
        "fecha_fin": fechas["fecha_fin"],
    }


def buscar_fila_por_etiqueta(excel, frase, columna_letra):
    col_idx = columna_excel_a_indice(columna_letra)
    matches = excel[excel[col_idx] == frase]
    return matches.index[0] + 1 if not matches.empty else None


def extraer_texto_detalles_usuario(excel, fila_final):
    rango = excel.iloc[8 : fila_final - 1, 1:14].fillna("")
    return "\n".join("\t".join(map(str, fila)) for fila in rango.values)


def extraer_tabla(excel, inicio, final, title=False):
    data = excel.iloc[inicio:final, 2:13].fillna("")
    data = DataFrame(data)
    if title:
        encabezados = excel.iloc[inicio, 2:13].tolist()
        data = data.iloc[1:]
        data.columns = encabezados
    return data.reset_index(drop=True)


def obtener_valor_celda(excel, celda, direccion=DIRECCION_DERECHA):
    col_letras = "".join(filter(str.isalpha, celda)).upper()
    fila = int("".join(filter(str.isdigit, celda))) - 1
    col = columna_excel_a_indice(col_letras)

    try:
        if direccion == DIRECCION_DERECHA:
            return excel.iloc[fila, col]
        elif direccion == DIRECCION_ABAJO:
            return excel.iloc[fila + 1, col]
        elif direccion == DIRECCION_DOS_DERECHA:
            return excel.iloc[fila, col + 2]
        else:
            raise ValueError(f"Dirección inválida: {direccion}")
    except IndexError:
        return None


def columna_excel_a_indice(col_letters):
    col_letters = col_letters.upper()
    index = 0
    for char in col_letters:
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index - 1


def extraer_relacionados(excel):
    inicio = buscar_fila_por_etiqueta(excel, RELACIONADOS_INICIO, "C")
    fin = buscar_fila_por_etiqueta(excel, RELACIONADOS_FIN, "C")
    return extraer_tabla(excel, inicio + 1, fin - 2, True)


def extraer_razones(excel):
    inicio = buscar_fila_por_etiqueta(excel, RAZONES_INICIO, "C")
    fin = buscar_fila_por_etiqueta(excel, RAZONES_FIN, "C")
    return extraer_tabla(excel, inicio, fin - 2)[2].to_list()


def extraer_valor(excel, celda, columna, direccion=None):
    index = buscar_fila_por_etiqueta(excel, celda, columna)
    value = None
    if direccion:
        value = obtener_valor_celda(excel, f"{columna}{index}", direccion)
    else:
        value = obtener_valor_celda(excel, f"{columna}{index}")
    return value


def extraer_fechas(excel):
    fila_periodo = buscar_fila_por_etiqueta(excel, "Período Analizado", "C")
    celda_fecha_inicio = f"{COLUMNA_FECHA_INICIO}{fila_periodo}"
    celda_fecha_fin = f"{COLUMNA_FECHA_FIN}{fila_periodo}"

    return {
        "fecha_inicio": format_date(
            str(obtener_valor_celda(excel, celda_fecha_inicio))
        ),
        "fecha_fin": format_date(str(obtener_valor_celda(excel, celda_fecha_fin))),
    }
