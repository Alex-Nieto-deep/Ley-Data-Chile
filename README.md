# Proyecto: Extracción de Datos y API con FastAPI

Este proyecto realiza web scraping para extraer datos sobre las leyes de Chile, los almacena en archivos CSV y proporciona una API con FastAPI para consultar estos datos.

---

## Tabla de Contenidos

1. [Requisitos](#requisitos)
2. [Configuración del Entorno](#configuración-del-entorno)
3. [Instalación de Dependencias](#instalación-de-dependencias)
4. [Ejecución del Proyecto](#ejecución-del-proyecto)
5. [Pruebas de la API](#pruebas-de-la-api)
6. [Notas Adicionales](#notas-adicionales)

---

## Requisitos

- Python 3.9 o superior.

---

## Configuración del Entorno

### Opción 1: Usar Conda (recomendado)

1. **Crear un entorno Conda**:
   Si tienes Conda instalado, crea un entorno con el siguiente comando:

   ```bash
   conda create -n leyes-chile
   ```

### Opción 2: Usando venv (Si no tienes Conda)\*\*:

```bash
 python -m venv venv
 source venv/bin/activate  # En Linux
 venv\Scripts\activate  # En Windows
```

## instalación-de-dependencias

2. **Instalar dependencias**:
   Ejecuta el siguiente comando para instalar todas las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el Web Scraping**:
   Este proyecto fue desarrollado en un entorno Linux, por lo que si usas Windows, algunos paths pueden generar errores.

   Para ejecutar el web scraping y generar los archivos .csv, usa:

   ```bash
   python main.py
   ```

4. **Iniciar la API**:

   ```bash
   cd app/
   python app.py
   ```

5. **Pruebas de la API**:

   ```bash
   copie este link en el navegador: http://localhost:5000/docs
   ```
