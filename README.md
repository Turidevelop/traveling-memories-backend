# traveling-memories-backend

> 🧱 Plantilla base para el proyecto en Python — minimalista, adaptable y extensible.

## 📌 Descripción

`traveling-memories-backend` es un proyecto desarrollado en Python. Su propósito es servir como punto de partida común para crear una API con una base limpia y bien organizada.

Un punto de partida común y personalizable para el desarrollo Python.

---

## 📁 Estructura del proyecto

```bash
traveling-memories-backend/
├── .env                         # Variables de entorno
├── .gitignore                   # Archivos ignorados por Git
├── requirements.txt             # Dependencias de Python
├── README.md                    # Documentación principal del proyecto
├── main.py                      # Punto de entrada de la aplicación FastAPI
├── database.py                  # Configuración y conexión a la base de datos
│
├── core/                        # Lógica de negocio central y modelos de dominio
│   ├── config.py                # Configuración de la aplicación
│   ├── models.py                # Modelos de dominio (SQLAlchemy)
│   └── schemas.py               # Esquemas de datos (Pydantic)
│
├── services/                    # Casos de uso y lógica de aplicación
│   ├── user_service.py
│   ├── trip_service.py
│   └── place_visited_service.py
│
├── repositories/                # Acceso a datos y persistencia
│   ├── base.py                  # Interfaz base para repositorios
│   ├── user_repo.py
│   ├── trip_repo.py
│   └── place_visited_repo.py
│
├── api/                         # Capa de presentación (API)
│   └── endpoints/               # Endpoints de la API REST
│       ├── user_endpoint.py
│       ├── trip_endpoint.py
│       └── place_visited_endpoint.py
│
├── test/                        # Tests automatizados
│   ├── test_user_endpoint.py
│   ├── test_trip_endpoint.py
│   └── test_place_visited_endpoint.py
│
└── DB/
    └── create_schema_travel_and_tables.sql   # Script de creación de esquema y tablas
```

---

## 🛠️ Tecnologías y herramientas

- **Python** (tipado)
- **FastAPI** (API REST)
- **SQLAlchemy** (ORM)
- **Pydantic** (validación de datos)
- **PostgreSQL** (base de datos)
- **pytest** (testing)

---

## 🧩 Principios de arquitectura

- **Clean Architecture**: Separación clara de capas (core, services, repositories, api).
- **Tipado estricto**: Uso de type hints y Pydantic en todo el proyecto.
- **Inyección de dependencias**: Uso de `Depends` de FastAPI para desacoplar componentes.
- **Async I/O**: Operaciones asíncronas en API y acceso a datos.

---

## 🚀 Cómo empezar

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Configura tu archivo `.env` con las variables necesarias.
3. Ejecuta la aplicación:
   ```bash
   uvicorn main:app --reload
   ```
4. Ejecuta los tests:
   ```bash
   pytest
   ```

---

## 📚 Documentación adicional

- Consulta los archivos en la carpeta `core/` para ver los modelos y esquemas.
- Los endpoints están en `api/endpoints/`.
- Los servicios y repositorios siguen los principios de Clean Architecture.

---

