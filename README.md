# blueprint-empty

> 🧱 Plantilla base para proyectos en Python — minimalista, adaptable y extensible.

## 📌 Descripción

`blueprint-empty` es una **plantilla vacía y estructurada** para proyectos desarrollados en Python. Su propósito es servir como punto de partida común para crear aplicaciones o sistemas con una base limpia y bien organizada.

Esta plantilla **no impone una arquitectura específica**, sino que proporciona una estructura mínima que puede adaptarse a cualquier necesidad **vertical** (según el dominio del proyecto, ya sea web, CLI, ciencia de datos, automatización, APIs, etc.).

Ideal para equipos o desarrolladores que buscan un punto de partida común y personalizable para sus desarrollos Python.

---

## 📁 Estructura del proyecto

```bash
blueprint-empty/
├── src/                  # Código fuente del proyecto
│   └── main.py
│   └──resources/
│      └──application/
│      └──domain/
│      └──infrastructure/
├── users/
│
├── tests/                # Pruebas automatizadas
│   └── __init__.py
├── .gitignore            # Archivos y carpetas ignorados por git
├── pyproject.toml        # Configuración del proyecto y dependencias (PEP 621)
├── README.md             # Documentación principal del proyecto
