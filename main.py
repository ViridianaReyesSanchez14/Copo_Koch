from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import matplotlib.pyplot as plt
import os
import uuid
import math

app = FastAPI()

# Crear carpeta static si no existe
if not os.path.exists("static"):
    os.makedirs("static")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# -----------------------
# Curva de Koch (una línea)
# -----------------------
def koch_curve(ax, x, y, length, angle, nivel, color="#0072ff"):
    if nivel == 0:
        x2 = x + length * math.cos(angle)
        y2 = y + length * math.sin(angle)
        ax.plot([x, x2], [y, y2], color=color, linewidth=2)
        return x2, y2
    else:
        length /= 3.0
        x, y = koch_curve(ax, x, y, length, angle, nivel - 1, color)
        x, y = koch_curve(ax, x, y, length, angle + math.pi / 3, nivel - 1, color)
        x, y = koch_curve(ax, x, y, length, angle - math.pi / 3, nivel - 1, color)
        x, y = koch_curve(ax, x, y, length, angle, nivel - 1, color)
        return x, y

# -----------------------
# Dibujar curva de Koch horizontal
# -----------------------
def draw_koch_line(nivel, length=600, color="#0072ff"):
    fig, ax = plt.subplots(figsize=(10, 4))

    # Fondo blanco y sin ejes
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    x_start, y_start = 0, 0
    koch_curve(ax, x_start, y_start, length, 0, nivel, color=color)

    ax.axis("equal")
    ax.axis("off")

    filename = f"koch_{uuid.uuid4().hex}.png"
    filepath = os.path.join("static", filename)

    # Guardar imagen sin márgenes y con fondo blanco
    plt.savefig(filepath, bbox_inches="tight", facecolor='white')
    plt.close(fig)

    return filename



# -----------------------
# Ruta principal
# -----------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request, nivel: int = 3):
    filename = draw_koch_line(nivel)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "image_path": f"/static/{filename}",
        "nivel": nivel
    })
