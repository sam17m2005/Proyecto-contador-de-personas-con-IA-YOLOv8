# Proyecto: Contador de Personas con IA (YOLOv8)

Proyecto desarrollado para la clase de **Inteligencia Artificial** en la **Universidad Jorge Tadeo Lozano**.  
El objetivo es detectar y contar personas en tiempo real utilizando **Python**, **YOLOv8**, y **Deep SORT**.

---

## Instalación y ejecución

Para ejecutar la aplicación se eben seguir los siguientes pasos: 

1. **Crear un entorno virtual**
   ```bash
   python -m venv venv
   ```

2. **Activar el entorno virtual**
     ```bash
     venv\Scripts\activate
     ```

3. **Instalar las dependencias necesarias**
   ```bash
   pip install flask ultralytics opencv-python deep-sort-realtime
   ```

4. **Ejecutar la aplicación**
   ```bash
   python appp.py
   ```

## Requisitos

- Computador con **GPU** o buen rendimiento (el modelo puede ser exigente) . 
- **Cámara conectada por USB**, que puede ser un **dispositivo móvil**, en conjunto con la cámara de su **portátil** o **PC de mesa**

## Funcionamiento

El sistema utiliza:

- **YOLOv8** para la detección de personas en tiempo real  
- **Deep SORT** para el seguimiento de cada persona y evitar contar duplicados  
- **Flask** para desplegar la interfaz y manejar el video en con las cámaras  

El resultado es un contador de personas que muestra el número total en tiempo real mientras analiza el video.

Proyecto desarrollado por **Leo Jaraba Pérez, Johan Felipe Aguilar Castillo, Samuel Alejandro González Grajales**.  
Clase de **Inteligencia Artificial**  
**Universidad Jorge Tadeo Lozano**