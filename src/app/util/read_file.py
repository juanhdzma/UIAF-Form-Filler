from io import BytesIO
from app.util.error import CustomException

DATA_PATH = "./Data.xlsx"


def read_excel_file():
    try:
        with open(DATA_PATH, "rb") as f:
            cached_excel = BytesIO(f.read())
            return cached_excel
    except:
        raise CustomException("No se pudo leer el archivo base")
