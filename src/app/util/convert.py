import re
import string


def string_to_matrix(s) -> tuple[list[list[int]], list[str]]:
    """Convierte un string [Letra, Número] en ([[pos_letra, número], ...], ["A1", "B3", ...])"""
    matches = re.findall(r"\[([A-Z]),(\d+)\]", s)

    matrix = [
        [string.ascii_uppercase.index(letter), int(num) - 1] for letter, num in matches
    ]
    string_list = [f"{letter}{num}" for letter, num in matches]

    return matrix, string_list
