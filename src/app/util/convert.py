import re
import string
from datetime import datetime
from difflib import get_close_matches

REASON_OPTIONS = [
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
    matches = re.findall(r"\[([A-Z]),(\d+)\]", s)
    matrix = [[string.ascii_uppercase.index(letter), int(num) - 1] for letter, num in matches]
    string_list = [f"{letter}{num}" for letter, num in matches]
    return matrix, string_list


def format_date(date_str) -> str:
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")


def get_closest_reason_match(extracted_reason):
    matches = get_close_matches(extracted_reason, REASON_OPTIONS, n=1, cutoff=0.5)
    return matches[0] if matches else "Select"
