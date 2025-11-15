import os
import json
import pdfkit
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pypdf import PdfReader, PdfWriter

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

# Configurar el entorno Jinja2
env = Environment(loader=FileSystemLoader(BASE_DIR))

header_template = env.get_template("header.html")
header_rendered = header_template.render(**data)

footer_template = env.get_template("footer.html")
footer_rendered = footer_template.render(**data)

content_template = env.get_template("template.html")
content_rendered = content_template.render(**data)

temp_header_path = os.path.join(BASE_DIR, "temp_header.html")
with open(temp_header_path, "w", encoding="utf-8") as f:
    f.write(header_rendered)

temp_footer_path = os.path.join(BASE_DIR, "temp_footer.html")
with open(temp_footer_path, "w", encoding="utf-8") as f:
    f.write(footer_rendered)

temp_content_path = os.path.join(BASE_DIR, "temp.html")
with open(temp_content_path, "w", encoding="utf-8") as f:
    f.write(content_rendered)

options = {
    "page-size": "Letter",
    "orientation": "Landscape",
    "encoding": "UTF-8",
    "margin-top": "35mm",  # Espacio para el header
    "margin-bottom": "20mm",  # Espacio para el footer
    "margin-left": "15mm",
    "margin-right": "15mm",
    "header-html": temp_header_path,
    "footer-html": temp_footer_path,
    "header-spacing": 5,  # Espacio entre header y contenido
    "footer-spacing": 5,  # Espacio entre contenido y footer
    "enable-local-file-access": None,
    "dpi": 96,
    "title": "None"
}

# Salida PDF
output_pdf = os.path.join(BASE_DIR, "estado_cuenta.pdf")

if config is None:
    print("Aviso: no se encontró wkhtmltopdf en la ruta configurada. Solo se generó el HTML temporal:", temp_content_path)
else:
    # Generar PDF temporal
    temp_pdf = os.path.join(BASE_DIR, "temp_output.pdf")
    pdfkit.from_file(
        temp_content_path,
        temp_pdf,
        options=options,
        configuration=config
    )
    
    # Agregar metadatos personalizados usando PyPDF2
    reader = PdfReader(temp_pdf)
    writer = PdfWriter()
    
    # Copiar todas las páginas
    for page in reader.pages:
        writer.add_page(page)
    
    # Agregar metadatos personalizados
    writer.add_metadata({
        '/Title': 'None',
        '/Subject': 'None',
        '/Author': 'Keitel Faviana Roman Martinez',
        '/Creator': 'Microsoft Excel para Microsoft 365',
        '/Producer': 'Microsoft Excel para Microsoft 365',
        '/Keywords': 'None'
    })
    
    # Guardar el PDF final con metadatos
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)
    
    # Eliminar PDF temporal
    if os.path.exists(temp_pdf):
        os.remove(temp_pdf)
    
    print("PDF GENERADO:", output_pdf)
    print("Archivos temporales creados:")
    print("- Header:", temp_header_path)
    print("- Footer:", temp_footer_path)
    print("- Contenido:", temp_content_path)
