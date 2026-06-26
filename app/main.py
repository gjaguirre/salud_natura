from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from typing import Optional

from app.config import settings
from app.database import init_db, get_db
from app.models import RemedioIn, UsuarioIn


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def home(request: Request):
    conn = get_db()
    remedios = conn.execute("SELECT * FROM base_conocimiento_salud").fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "settings": settings,
        "remedios": remedios,
    })


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/remedios")
async def listar_remedios():
    conn = get_db()
    remedios = [dict(r) for r in conn.execute("SELECT * FROM base_conocimiento_salud").fetchall()]
    conn.close()
    return {"ok": True, "data": remedios}


@app.get("/api/remedios/{id_remedio}")
async def obtener_remedio(id_remedio: int):
    conn = get_db()
    remedio = conn.execute("SELECT * FROM base_conocimiento_salud WHERE id_remedio = ?", (id_remedio,)).fetchone()
    conn.close()
    if not remedio:
        return {"ok": False, "error": "Remedio no encontrado"}
    return {"ok": True, "data": dict(remedio)}


@app.post("/api/remedios")
async def crear_remedio(remedio: RemedioIn):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO base_conocimiento_salud (nombre_remedio, planta_base, propiedades, contraindicaciones, dosificacion, link_articulo_web) VALUES (?, ?, ?, ?, ?, ?)",
        (remedio.nombre_remedio, remedio.planta_base, remedio.propiedades, remedio.contraindicaciones, remedio.dosificacion, remedio.link_articulo_web),
    )
    conn.commit()
    id_nuevo = cursor.lastrowid
    conn.close()
    return {"ok": True, "id_remedio": id_nuevo}


@app.post("/api/usuarios")
async def registrar_usuario(usuario: UsuarioIn):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO usuarios_y_clientes (nombre_completo, celular, email, direccion_completa, ciudad_prov_pais, latitud, longitud) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (usuario.nombre_completo, usuario.celular, usuario.email, usuario.direccion_completa, usuario.ciudad_prov_pais, usuario.latitud, usuario.longitud),
    )
    conn.commit()
    id_nuevo = cursor.lastrowid
    conn.close()
    return {"ok": True, "id_usuario": id_nuevo}


# ── Admin ──

@app.get("/admin")
async def admin_inicio(request: Request):
    conn = get_db()
    total_remedios = conn.execute("SELECT COUNT(*) FROM base_conocimiento_salud").fetchone()[0]
    total_usuarios = conn.execute("SELECT COUNT(*) FROM usuarios_y_clientes").fetchone()[0]
    conn.close()
    return templates.TemplateResponse("admin_inicio.html", {
        "request": request, "settings": settings, "seccion": "inicio",
        "total_remedios": total_remedios, "total_usuarios": total_usuarios,
    })


@app.get("/admin/remedios")
async def admin_remedios(request: Request, mensaje: Optional[str] = None):
    conn = get_db()
    remedios = conn.execute("SELECT * FROM base_conocimiento_salud ORDER BY id_remedio DESC").fetchall()
    conn.close()
    return templates.TemplateResponse("admin_remedios.html", {
        "request": request, "settings": settings, "seccion": "remedios",
        "remedios": remedios, "mensaje": mensaje,
    })


@app.post("/admin/remedios/guardar")
async def admin_remedios_guardar(
    nombre_remedio: str = Form(...),
    planta_base: str = Form(""),
    propiedades: str = Form(""),
    contraindicaciones: str = Form(""),
    dosificacion: str = Form(""),
    link_articulo_web: str = Form(""),
    id_remedio: str = Form(""),
):
    conn = get_db()
    if id_remedio:
        conn.execute(
            "UPDATE base_conocimiento_salud SET nombre_remedio=?, planta_base=?, propiedades=?, contraindicaciones=?, dosificacion=?, link_articulo_web=? WHERE id_remedio=?",
            (nombre_remedio, planta_base or None, propiedades or None, contraindicaciones or None, dosificacion or None, link_articulo_web or None, int(id_remedio)),
        )
        mensaje = "Remedio actualizado"
    else:
        conn.execute(
            "INSERT INTO base_conocimiento_salud (nombre_remedio, planta_base, propiedades, contraindicaciones, dosificacion, link_articulo_web) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre_remedio, planta_base or None, propiedades or None, contraindicaciones or None, dosificacion or None, link_articulo_web or None),
        )
        mensaje = "Remedio creado"
    conn.commit()
    conn.close()
    return RedirectResponse(f"/admin/remedios?mensaje={mensaje}", status_code=303)


@app.post("/admin/remedios/{id_remedio}/eliminar")
async def admin_remedios_eliminar(id_remedio: int):
    conn = get_db()
    conn.execute("DELETE FROM base_conocimiento_salud WHERE id_remedio=?", (id_remedio,))
    conn.commit()
    conn.close()
    return RedirectResponse("/admin/remedios?mensaje=Remedio eliminado", status_code=303)


@app.get("/admin/usuarios")
async def admin_usuarios(request: Request, mensaje: Optional[str] = None):
    conn = get_db()
    usuarios = conn.execute("SELECT * FROM usuarios_y_clientes ORDER BY id_usuario DESC").fetchall()
    conn.close()
    return templates.TemplateResponse("admin_usuarios.html", {
        "request": request, "settings": settings, "seccion": "usuarios",
        "usuarios": usuarios, "mensaje": mensaje,
    })


@app.post("/admin/usuarios/guardar")
async def admin_usuarios_guardar(
    nombre_completo: str = Form(...),
    celular: str = Form(""),
    email: str = Form(""),
    direccion_completa: str = Form(""),
    ciudad_prov_pais: str = Form(""),
    latitud: str = Form(""),
    longitud: str = Form(""),
    id_usuario: str = Form(""),
):
    lat = float(latitud) if latitud else None
    lon = float(longitud) if longitud else None
    conn = get_db()
    if id_usuario:
        conn.execute(
            "UPDATE usuarios_y_clientes SET nombre_completo=?, celular=?, email=?, direccion_completa=?, ciudad_prov_pais=?, latitud=?, longitud=? WHERE id_usuario=?",
            (nombre_completo, celular or None, email or None, direccion_completa or None, ciudad_prov_pais or None, lat, lon, int(id_usuario)),
        )
        mensaje = "Usuario actualizado"
    else:
        conn.execute(
            "INSERT INTO usuarios_y_clientes (nombre_completo, celular, email, direccion_completa, ciudad_prov_pais, latitud, longitud) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (nombre_completo, celular or None, email or None, direccion_completa or None, ciudad_prov_pais or None, lat, lon),
        )
        mensaje = "Usuario creado"
    conn.commit()
    conn.close()
    return RedirectResponse(f"/admin/usuarios?mensaje={mensaje}", status_code=303)


@app.post("/admin/usuarios/{id_usuario}/eliminar")
async def admin_usuarios_eliminar(id_usuario: int):
    conn = get_db()
    conn.execute("DELETE FROM usuarios_y_clientes WHERE id_usuario=?", (id_usuario,))
    conn.commit()
    conn.close()
    return RedirectResponse("/admin/usuarios?mensaje=Usuario eliminado", status_code=303)
