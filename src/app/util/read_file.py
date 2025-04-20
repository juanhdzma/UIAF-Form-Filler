from io import BytesIO
from app.util.error import CustomException

DATA_PATH = "./Data2.xlsx"


def load_excel_file():
    try:
        with open(DATA_PATH, "rb") as file:
            excel_buffer = BytesIO(file.read())
            return excel_buffer
    except:
        raise CustomException("No se pudo leer el archivo base")
