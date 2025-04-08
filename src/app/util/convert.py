import re
import string
from datetime import datetime
from difflib import get_close_matches

OPCIONES_MOTIVO = [
    "Concierto para delinquir",
    "Contrabando",
    "Seleccionar",
    "Contrabando hidrocarburos",
    "Corrupción",
    "Delitos contra el sistema financiero",
    "Delitos contra la administración pública",
    "Enriquecimiento ilicito",
    "Exportaciones ficticias",
    "Extorsión",
    "Financiamiento de terrorismo",
    "Fraude aduanero",
    "Importaciones ficticias",
    "Minería ilegal",
    "Operaciones con activos virtuales",
    "Secuestro extorsivo",
    "Tráfico de emigrantes",
    "Tráfico de estupefacientes",
    "Tráfico de menores",
    "Tráfico de personas",
]


def string_to_matrix(s) -> tuple[list[list[int]], list[str]]:
    """Convierte un string [Letra, Número] en ([[pos_letra, número], ...], ["A1", "B3", ...])"""
    matches = re.findall(r"\[([A-Z]),(\d+)\]", s)

    matrix = [
        [string.ascii_uppercase.index(letter), int(num) - 1] for letter, num in matches
    ]
    string_list = [f"{letter}{num}" for letter, num in matches]

    return matrix, string_list


def format_date(fecha_str):
    return datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")


def obtener_motivo_mas_parecido(motivo_extraido):
    coincidencias = get_close_matches(motivo_extraido, OPCIONES_MOTIVO, n=1, cutoff=0.5)
    return coincidencias[0] if coincidencias else "Seleccionar"
