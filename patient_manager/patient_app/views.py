from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
import random

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
