from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page
import random
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# Create your views here.

# Lista de nombres y apellidos ficticios para generar datos aleatorios
nombres = ["Juan", "María", "Carlos", "Ana", "Pedro", "Sofía", "Luis", "Laura"]
apellidos = ["García", "López", "Martínez", "Rodríguez", "Fernández", "González", "Pérez", "Sánchez"]

# Función para generar un paciente aleatorio
def generar_paciente(patient_id):
    return {
        "id": patient_id,
        "nombre": random.choice(nombres),
        "apellido": random.choice(apellidos),
        "edad": random.randint(18, 90),
        "fecha_ingreso": f"2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "estado": random.choice(["Estable", "Crítico", "En observación", "Recuperándose"]),
        "habitacion": f"{random.randint(1, 5)}{random.choice(['A', 'B', 'C'])}",
    }

# Vista para obtener datos de un paciente específico
# Cachear las respuestas durante 60 segundos (1 minuto)
@cache_page(60)
def get_patient(request, patient_id):
    # En un sistema real, aquí consultaríamos la base de datos
    # Para este ejemplo, generamos datos ficticios
    patient_data = generar_paciente(patient_id)
    
    # Añadimos un timestamp para verificar cuando se genera nueva data vs caché
    patient_data["timestamp"] = random.randint(1000000, 9999999)
    
    return JsonResponse(patient_data)

# Vista para generar PDF con información del paciente
def generate_patient_pdf(request, patient_id):
    # Obtenemos los datos del paciente
    patient_data = generar_paciente(patient_id)
    
    # Creamos un buffer para el PDF
    buffer = io.BytesIO()
    
    # Creamos el documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Estilos para el documento
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    
    # Título del documento
    elements.append(Paragraph(f"Informe del Paciente #{patient_id}", title_style))
    
    # Datos del paciente en formato tabla
    data = [
        ["Campo", "Valor"],
        ["ID", str(patient_data["id"])],
        ["Nombre", f"{patient_data['nombre']} {patient_data['apellido']}"],
        ["Edad", str(patient_data["edad"])],
        ["Fecha de Ingreso", patient_data["fecha_ingreso"]],
        ["Estado", patient_data["estado"]],
        ["Habitación", patient_data["habitacion"]],
    ]
    
    # Estilo para la tabla
    table = Table(data, colWidths=[200, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (0, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    
    # Generamos el PDF
    doc.build(elements)
    
    # Obtenemos el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Creamos la respuesta HTTP con el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="paciente_{patient_id}.pdf"'
    response.write(pdf)
    
    return response


