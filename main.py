from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import models
import database
from routers import admin, hod, auth, faculty, attendance

app = FastAPI(title="Kserve College Management System")

# Ensure DB tables are created
models.Base.metadata.create_all(bind=database.engine)

# Create directories for static files and templates if they don't exist
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"title": "Kserve Login"})


@app.get("/admin", response_class=HTMLResponse)
async def serve_admin(request: Request):
    return templates.TemplateResponse(request=request, name="admin.html")

@app.get("/hod", response_class=HTMLResponse)
async def serve_hod(request: Request):
    return templates.TemplateResponse(request=request, name="hod.html")

@app.get("/faculty", response_class=HTMLResponse)
async def serve_faculty(request: Request):
    return templates.TemplateResponse(request=request, name="faculty.html")

# --- Initial API Stubs ---
@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "Kserve"}

# --- Include Application Routers ---
app.include_router(admin.router)
app.include_router(hod.router)
app.include_router(auth.router)
app.include_router(faculty.router)
app.include_router(attendance.router)
