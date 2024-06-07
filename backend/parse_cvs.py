import PyPDF2
from docx import Document
import json
import re

def parse_cv(file_path):
    """
    Parsea un CV en formato PDF o Word y lo convierte en un diccionario JSON estructurado.

    Args:
        file_path (str): La ruta al archivo del CV.

    Returns:
        dict: Un diccionario JSON con la información del CV.
    """

    cv_data = {}

    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            cv_data = extract_info_from_text(text)

    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        cv_data = extract_info_from_text(text)

    else:
        raise ValueError("Formato de archivo no soportado")

    return cv_data

def extract_info_from_text(text):
    cv_data = {
        "nombre": "",
        "contacto": {
            "email": "",
            "telefono": ""
        },
        "experiencia": [],
        "educacion": [],
        "habilidades": []
    }

    # Expresiones regulares para extraer información
    nombre_pattern = r"(?i)(?:Nombre|Nombre completo|Full name):\s*([\w\s]+)"
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    telefono_pattern = r"(?i)(?:Teléfono|Telefono|Celular|Phone|Mobile):\s*\(?(\d{3,4})\)?\s*(\d{6,8})"

    # Extraer nombre
    match = re.search(nombre_pattern, text)
    if match:
        cv_data["nombre"] = match.group(1).strip()

    # Extraer correo electrónico
    match = re.search(email_pattern, text)
    if match:
        cv_data["contacto"]["email"] = match.group(0)

    # Extraer número de teléfono
    match = re.search(telefono_pattern, text)
    if match:
        cv_data["contacto"]["telefono"] = match.group(1) + match.group(2)

    # ... (Aquí puedes agregar más expresiones regulares para extraer otra información)

    return cv_data
