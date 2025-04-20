from pandas import read_excel, DataFrame, concat
from app.util.convert import format_date
from app.util.convert import get_closest_reason_match

# Constantes de etiquetas utilizadas en la hoja de Excel
CELL_REASON = "vii. Temática Asociada a LA/FT"
CELL_CASE_ID = "No. Caso"
CELL_DOCUMENT_TYPE = "J10"
CELL_DOCUMENT = "L10"
CELL_AMOUNT = "Valor Reporte"
COLUMN_START_DATE = "F"
COLUMN_END_DATE = "H"
CONCLUSIONS = "5. Conclusiones del Comité"
REASONS_END = "iii. Movimientos a destacar"
REASONS_START = "ii. Razones del reporte: Inusualidades encontradas"
RELATED_END = "v. Explicación de la operación "
RELATED_START = "iv. Relacionados"

# Direcciones posibles para obtener_valor_celda
DIRECTION_RIGHT = "R"
DIRECTION_TWO_RIGHT = "RR"
DIRECTION_DOWN = "D"


def read_user_data(cached_file, reported_name):
    excel = read_excel(cached_file, sheet_name=reported_name, header=None)

    details_text = extract_user_details_text(excel, find_row_by_label(excel, CONCLUSIONS, "B"))
    related = extract_related(excel)
    document_type = get_cell_value(excel, CELL_DOCUMENT_TYPE)
    document = get_cell_value(excel, CELL_DOCUMENT)
    related_report = {
        "Name": reported_name,
        "Document type": document_type,
        "Document ": document,
        "Relation": "CLIENTE",
    }
    related = concat([related, DataFrame([related_report])], ignore_index=True)

    reasons = extract_reasons(excel)
    reason = extract_value(excel, CELL_REASON, "C", DIRECTION_DOWN)
    amount = extract_value(excel, CELL_AMOUNT, "C", DIRECTION_TWO_RIGHT)
    dates = extract_dates(excel)
    return {
        "description": details_text,
        "related": related,
        "operation_reason": get_closest_reason_match(reason),
        "transaction_amount": round(amount),
        "alert_reasons": reasons,
        "start_date": dates["start_date"],
        "end_date": dates["end_date"],
    }


def find_row_by_label(excel, phrase, column_letter):
    col_idx = excel_column_to_index(column_letter)
    matches = excel[excel[col_idx] == phrase]
    return matches.index[0] + 1 if not matches.empty else None


def extract_user_details_text(excel, final_row):
    range_data = excel.iloc[8 : final_row - 1, 1:14].fillna("")
    return "\n".join("\t".join(map(str, row)) for row in range_data.values)


def extract_table(excel, start, end, title=False):
    data = excel.iloc[start:end, 2:13].fillna("")
    data = DataFrame(data)
    if title:
        headers = excel.iloc[start, 2:13].tolist()
        data = data.iloc[1:]
        data.columns = headers
    return data.reset_index(drop=True)


def get_cell_value(excel, cell, direction=DIRECTION_RIGHT):
    col_letters = "".join(filter(str.isalpha, cell)).upper()
    row = int("".join(filter(str.isdigit, cell))) - 1
    col = excel_column_to_index(col_letters)

    try:
        if direction == DIRECTION_RIGHT:
            return excel.iloc[row, col]
        elif direction == DIRECTION_DOWN:
            return excel.iloc[row + 1, col]
        elif direction == DIRECTION_TWO_RIGHT:
            return excel.iloc[row, col + 2]
        else:
            raise ValueError(f"Invalid direction: {direction}")
    except IndexError:
        return None


def excel_column_to_index(col_letters):
    col_letters = col_letters.upper()
    index = 0
    for char in col_letters:
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index - 1


def extract_related(excel):
    start = find_row_by_label(excel, RELATED_START, "C")
    end = find_row_by_label(excel, RELATED_END, "C")
    return extract_table(excel, start + 1, end - 2, True)


def extract_reasons(excel):
    start = find_row_by_label(excel, REASONS_START, "C")
    end = find_row_by_label(excel, REASONS_END, "C")
    return extract_table(excel, start, end - 2)[2].to_list()


def extract_value(excel, cell, column, direction=None):
    index = find_row_by_label(excel, cell, column)
    value = None
    if direction:
        value = get_cell_value(excel, f"{column}{index}", direction)
    else:
        value = get_cell_value(excel, f"{column}{index}")
    return value


def extract_dates(excel):
    period_row = find_row_by_label(excel, "Período Analizado", "C")
    cell_start_date = f"{COLUMN_START_DATE}{period_row}"
    cell_end_date = f"{COLUMN_END_DATE}{period_row}"

    return {
        "start_date": format_date(str(get_cell_value(excel, cell_start_date))),
        "end_date": format_date(str(get_cell_value(excel, cell_end_date))),
    }
