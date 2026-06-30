# Punto de restauración — Pre-Taller

## Checkpoint actual (vigente)
Fecha: 2026-06-30
- Commit: `1d642d8` — "Merge PR #3: Frontend Josep - dark theme botiquin + path fixes"
- Incluye el merge del PR de José (tema oscuro en botiquín, fixes de rutas de imágenes en grimorio, link /taller en index.html)
- Base de datos: `backups/salud_natura_checkpoint_post_pr3.db`
  - 36 plantas en el grimorio (`base_conocimiento_salud`)
  - 29 dolencias en el botiquín (25 vinculadas por FK `id_remedio` al grimorio)

### Restaurar el código a este punto
```bash
git fetch origin
git reset --hard 1d642d8
git push origin main --force   # solo si ya se pusheó algo roto a producción
```

### Restaurar la base de datos a este punto
```bash
cp backups/salud_natura_checkpoint_post_pr3.db data/salud_natura.db
```

## Checkpoint anterior (previo al merge de PR #3)
- Commit: `e23671b` — "Clarify required Python version (3.11) in taller instructions"
- Tag de git: `checkpoint-pre-taller` (pusheado a GitHub)
- Base de datos: `backups/salud_natura_checkpoint_pre_taller.db`

### Restaurar el código a este punto anterior
```bash
git fetch --tags
git reset --hard checkpoint-pre-taller
git push origin main --force   # solo si ya se pusheó algo roto a producción
```

### Restaurar la base de datos a este punto anterior
```bash
cp backups/salud_natura_checkpoint_pre_taller.db data/salud_natura.db
```

## Requisitos para correr local
- Python 3.11 (no 3.12/3.13/3.14 — `pydantic-core` no es compatible)
- Entorno virtual: `.venv/`
- Levantar servidor: `.venv/Scripts/python.exe -m uvicorn app.main:app --port 8000`
