# JuegosGB Backend

Backend del sistema JuegosGB - Una plataforma de juegos interactivos desarrollada en Django REST Framework.

## Descripción del Proyecto

JuegosGB es un sistema de entretenimiento que incluye múltiples juegos interactivos diseñados para brindar diversión y entretenimiento. El backend proporciona APIs REST para gestionar diferentes tipos de juegos y sus funcionalidades.

## Juegos Disponibles

### 🎵 Adivina la Canción
- Juego musical donde los equipos deben adivinar canciones
- Gestión de géneros musicales, artistas y canciones
- Soporte para archivos de audio
- Sistema de puntuación por equipos

### 🧠 Cien Mexicanos Dijeron
- Juego de preguntas y respuestas estilo encuesta familiar
- Sistema de categorías y tipos de preguntas
- Respuestas con calificaciones
- Gestión de rondas y equipos competidores

### 🎤 Karaoke
- Sistema de karaoke con gestión de canciones
- Base de datos de canciones disponibles para karaoke

### 💪 Juegos de Fuerza
- Juegos que requieren interacción física o habilidades específicas

### 📚 Primaria
- Juegos educativos orientados a nivel primario

## Tecnologías Utilizadas

- **Framework**: Django 5.1.7
- **API**: Django REST Framework
- **Base de Datos**: PostgreSQL (psycopg2)
- **Autenticación**: JWT (djangorestframework-simplejwt)
- **CORS**: django-cors-headers
- **Archivos Estáticos**: WhiteNoise
- **Procesamiento de Datos**: pandas, openpyxl
- **Comunicación Serial**: pyserial (para integración con arduino)

## Estructura del Proyecto

```
├── apps/                          # Aplicaciones Django
│   ├── adivinacancion/           # Juego de adivinar canciones
│   ├── cienmexicanos/            # Juego estilo "100 mexicanos dijeron"
│   ├── juegosfuerza/             # Juegos de fuerza
│   ├── karaoke/                  # Sistema de karaoke
│   ├── primaria/                 # Juegos educativos
│   └── users/                    # Gestión de usuarios
├── juegosgb/                     # Configuración principal del proyecto
├── templates/                    # Plantillas HTML
├── media/                        # Archivos multimedia
├── static/                       # Archivos estáticos
└── manage.py                     # Script de gestión de Django
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.12+
- PostgreSQL
- Git

### Pasos de Instalación

1. **Ingresar a la carpeta del proyecto**
   ```bash
   cd backend-juegosgb
   ```

2. **Crear y activar entorno virtual**
   ```bash
   python -m venv env
   source env/bin/activate  # En Linux/Mac
   # env\Scripts\activate  # En Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**

   Crear un archivo `.env` en la raíz del proyecto:
   ```env
   DEBUG=True
   ARDUINO_PORT=/dev/ttyUSB0  # Puerto para comunicación serial
   WEBSOCKET_URL=ws://localhost:8000/ws/
   ```

5. **Configurar base de datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crear superusuario (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

## Uso de la API

El backend expone APIs REST para cada juego. Algunos endpoints principales:

- `/admin/` - Panel de administración de Django
- `/api/adivinacancion/` - APIs del juego de adivinar canciones
- `/api/cienmexicanos/` - APIs del juego de 100 mexicanos
- `/api/karaoke/` - APIs del sistema de karaoke
- `/api/users/` - Gestión de usuarios

## Características Especiales

- **Integración con Hardware**: Soporte para comunicación serial con dispositivos Arduino
- **WebSockets**: Comunicación en tiempo real para juegos interactivos
- **Gestión Multimedia**: Soporte para archivos de audio y otros medios
- **Sistema de Equipos**: Funcionalidad para juegos competitivos entre equipos
- **APIs RESTful**: Arquitectura bien estructurada para integración con frontend
