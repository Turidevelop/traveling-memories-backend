# travelling-memories-backend

> 🧱 Plantilla base para el proyecto en Python — minimalista, adaptable y extensible.

## 📌 Descripción

`travelling-memories-backend` es un proyecto desarrollado en Python. Su propósito es servir como punto de partida común para crear una API con una base limpia y bien organizada.


Un punto de partida común y personalizable para el desarrollo Python.

---

## 📁 Estructura del proyecto

```bash
travelling-memories-backend/
├── .env                     # Plantilla para variables de entorno
├── .gitignore               # Archivos ignorados por Git
├── requirements.txt         # Dependencias de Python
├── README.md                # Documentación principal del proyecto
├── main.py                  # Punto de entrada de la aplicación
│
├── core/                    # Lógica de negocio central
│   ├── config.py            # Configuración de la aplicación
│   ├── models.py            # Modelos de dominio (Pydantic)
│   └── schemas.py           # Esquemas de datos
│
├── services/                # Lógica de aplicación
│   └── example_service.py    # Servicio para operaciones con viajes
│
├── repositories/            # Acceso a datos
│   ├── base.py              # Interfaz base para repositorios
│   └── travel_repo.py       # Implementación para viajes
│
├── api/                     # Capa de presentación
│   ├── dependencies.py      # Dependencias inyectables
│   └── endpoints/           # Endpoints de la API
│       └── example.py       # Endpoints específicos para viajes
│
└── database.py              # Configuración de base de datos

