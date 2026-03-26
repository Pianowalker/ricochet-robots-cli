# Ricochet Robots — Distribución

Este directorio contiene el ejecutable standalone de la versión GUI de Ricochet Robots.

---

## Ejecutar el juego

Hacé doble clic en `ricochet-gui.exe`. No requiere tener Python instalado.

---

## Generar el ejecutable

Desde la raíz del proyecto, con Python y PyInstaller instalados:

```
pip install pyinstaller
pyinstaller ricochet_gui.spec
```

El `.exe` resultante queda en esta carpeta (`dist/ricochet-gui.exe`).

---

## Detalles técnicos

**Empaquetado:** PyInstaller en modo `--onefile`. Todo el intérprete de Python, las dependencias y el código fuente quedan comprimidos dentro del `.exe`.

**Dependencias incluidas:**
- Python 3.10+
- pygame 2.1+

**Sin assets externos:** los gráficos se dibujan con primitivas de pygame y los sonidos se generan programáticamente. El ejecutable no necesita ninguna carpeta de recursos adicional.

**Arranque:** al ejecutarse por primera vez puede tardar unos segundos mientras PyInstaller descomprime el contenido en un directorio temporal del sistema. Esto es normal.

**Consola:** el ejecutable está compilado en modo `console=False`, por lo que no abre una ventana de consola al iniciarse.

**Entrada del programa:** `run_gui.py` (en la raíz del proyecto) actúa como punto de entrada para evitar conflictos de imports relativos al empaquetar como script independiente.

---

## Compatibilidad

Generado para **Windows 64-bit**. Para distribuir en otras plataformas es necesario compilar el `.exe` desde esa plataforma con el mismo comando.
