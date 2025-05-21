from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path


app = FastAPI()

# Ruta base del frontend
frontend_path = Path(__file__).resolve().parent.parent / "frontend"

# Montar carpetas estáticas
app.mount("/styles", StaticFiles(directory=frontend_path / "styles"), name="styles")
app.mount("/JS", StaticFiles(directory=frontend_path / "JS"), name="js")
app.mount("/IMG", StaticFiles(directory=frontend_path / "IMG"), name="img")

# Montar favicon como archivo estático
@app.get("/favicon.ico")
async def get_favicon():
    favicon_path = frontend_path / "IMG" / "favicon.ico"
    if favicon_path.exists():
        return FileResponse(favicon_path)
    raise HTTPException(status_code=404, detail="Favicon no encontrado")

# Página Principal
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    file_path = frontend_path / "HTML" / "index.html"
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Página principal no encontrada")

# Rutas dinámicas para otras páginas HTML
@app.get("/{page_name}", response_class=HTMLResponse)
async def serve_page(page_name: str):
    # Validar que el archivo termine en .html para mayor seguridad
    if not page_name.endswith(".html"):
        raise HTTPException(status_code=400, detail="Archivo no válido")
    
    file_path = frontend_path / "HTML" / page_name
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    
    raise HTTPException(status_code=404, detail="Página no encontrada")

""" 
# Formulario

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Form
import databases
import sqlalchemy

# Configuración DB SQLite
DATABASE_URL = "sqlite:///./contactos.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

contacto = sqlalchemy.Table(
    "contacto",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("nombre", sqlalchemy.String),
    sqlalchemy.Column("telefono", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("mensaje", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

# FastAPI
app = FastAPI()

# CORS opcional para pruebas locales
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/enviar_formulario")
async def enviar_formulario(
    nombre: str = Form(...),
    telefono: str = Form(None),
    email: str = Form(...),
    mensaje: str = Form(...)
):
    query = contacto.insert().values(
        nombre=nombre,
        telefono=telefono,
        email=email,
        mensaje=mensaje
    )
    await database.execute(query)
    return {"mensaje": "Datos recibidos correctamente"}

"""











