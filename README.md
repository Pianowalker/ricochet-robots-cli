# Ricochet Robots

Implementación web del juego de mesa Ricochet Robots, con frontend en HTML/JS y backend en Python + FastAPI.

---

## Estructura del proyecto

```
ricochet/
├── frontend/                  # Cliente web (HTML + CSS + JS, sin build toolchain)
│   ├── index.html             # Juego principal (modos práctica y partida)
│   └── editor.html            # Herramienta interna para crear puzzles de tutorial
│
├── src/                       # Paquete Python (convención src-layout)
│   └── ricochet/
│       ├── domain/            # Lógica del juego, independiente del framework
│       │   ├── game.py        # Clase Game: tablero, movimiento de robots, física
│       │   ├── quadrant.py    # Clase Quadrant: cuadrante 8x8, rotación
│       │   ├── maps.py        # 16 definiciones de cuadrantes + ensamblado de tablero
│       │   ├── models.py      # Clases Robot, Target, Bumper
│       │   └── sessions/      # Sesiones de juego (práctica y partida)
│       │
│       └── backend/
│           └── app/
│               ├── main.py              # FastAPI app, middlewares, registro de routers
│               ├── store.py             # Almacenamiento en memoria de sesiones activas
│               ├── api/routes/          # Endpoints REST
│               │   ├── practice.py      # POST /practice, POST /practice/{id}/move
│               │   ├── game.py          # POST /game, /round/start, /declare, /move
│               │   └── editor.py        # GET /editor/quadrants, POST /editor/puzzle
│               ├── services/            # Lógica de aplicación
│               │   ├── game_service.py
│               │   ├── practice_service.py
│               │   └── serializer.py    # Convierte objetos de dominio a JSON
│               ├── schemas/             # Modelos Pydantic para requests
│               └── data/
│                   └── puzzles/
│                       └── tutorial/    # Puzzles creados con el editor (JSON)
│
├── tests/                     # Tests del dominio
├── pyproject.toml             # Configuración del paquete Python
└── README.md
```

### Nota sobre la estructura

El frontend (`frontend/`) y el backend (`src/ricochet/backend/`) están en lugares distintos del árbol porque siguen convenciones diferentes. El frontend es un archivo HTML estático que no requiere compilación. El backend sigue la convención `src-layout` estándar de Python, que evita conflictos de imports y es compatible con herramientas como `pytest` y `setuptools`.

---

## Correr en local

**Instalar dependencias:**
```bash
pip install -e .
```

**Backend:**
```bash
uvicorn ricochet.backend.app.main:app --reload
```

**Frontend:**
```bash
cd frontend
python -m http.server 3000
```
Luego abrí `http://localhost:3000` en el navegador.

**Editor de puzzles** (herramienta interna, requiere backend corriendo):
```
http://localhost:3000/editor.html
```
