import os
import json
import pdfkit
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Base directory (carpeta donde está este script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta correcta del wkhtmltopdf en tu PC (ajusta si es necesario)
path_wkhtmltopdf = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
if not os.path.exists(path_wkhtmltopdf):
    config = None
else:
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Cargar datos (desde la misma carpeta del script)
datos_path = os.path.join(BASE_DIR, "datos.json")
with open(datos_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Fecha actual
data["fecha_creacion"] = datetime.now().strftime("%d/%m/%Y - %I:%M %p")

# Renderizar HTML (plantilla desde la misma carpeta)
env = Environment(loader=FileSystemLoader(BASE_DIR))
template = env.get_template("template.html")
html_rendered = template.render(**data)

# Guardar HTML temporal en la misma carpeta
temp_html_path = os.path.join(BASE_DIR, "temp.html")
with open(temp_html_path, "w", encoding="utf-8") as f:
    f.write(html_rendered)

# Opciones PDF
options = {
    "page-size": "Letter",
    "encoding": "UTF-8",
    "margin-top": "20mm",
    "margin-bottom": "20mm",
    "margin-left": "10mm",
    "margin-right": "10mm",
    "enable-local-file-access": None
}

# Salida PDF
output_pdf = os.path.join(BASE_DIR, "estado_cuenta.pdf")

if config is None:
    print("Aviso: no se encontró wkhtmltopdf en la ruta configurada. Solo se generó el HTML temporal:", temp_html_path)
else:
    # Generar PDF
    pdfkit.from_file(
        temp_html_path,
        output_pdf,
        options=options,
        configuration=config
    )
    print("PDF GENERADO:", output_pdf)
