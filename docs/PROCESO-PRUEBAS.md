# Gestión del proceso de desarrollo y pruebas — EcoGame

Apartado 1 de la consigna integradora: **automatización de pruebas** y **proceso de pruebas enfocado en videojuegos con entrega Beta**.

## 1. Flujo de trabajo

| Elemento | Definición |
|---|---|
| Control de versiones | Git + GitHub. Ramas: `main` (estable), `develop` (integración), `feature/<nombre>` (cada cambio). |
| Integración | Pull request hacia `develop`; solo se fusiona si el pipeline está en verde. |
| Versionado | SemVer con etiqueta de fase: `v4.0.0-beta.1`, `v4.0.0-rc.1`, `v4.0.0`. |
| Entrega | Al etiquetar `v*`, el pipeline publica un *pre-release* con el paquete Beta. |
| Seguimiento de defectos | GitHub Issues con etiquetas de severidad (sección 4). |

## 2. Herramientas de pruebas automatizadas

| Nivel | Herramienta | Qué valida | Archivo |
|---|---|---|---|
| Análisis estático | **Ruff** | Errores de sintaxis, nombres indefinidos, imports sin uso en los scripts Python | `ruff.toml` |
| Unitarias | **unittest** (Python) | Servidor local: rutas permitidas, rechazo de JSON/PNG inválidos y cuerpos vacíos. Integridad del CAPX (ZIP sano, XML bien formado, 4 capas, variables globales) y de la exportación HTML5 (data.js, manifest, iconos, 10 audios OGG, sprites PNG) | `tests/test_servidor.py`, `tests/test_entrega.py` |
| Integración / aceptación | **Playwright** + Chromium headless | Ejecuta `docs/qa.html`: 38 pruebas sobre los eventos reales del motor Construct (movimiento, colisiones, puntaje, vidas, pausa, jefe, victoria/derrota, audio) | `tests/integracion_qa.py` |

> Construct 2 no permite probar la hoja de eventos de forma aislada; por eso la lógica del juego se valida en el nivel de integración, controlando el runtime exportado (`cr_getC2Runtime`).

### Pipeline CI/CD (`.github/workflows/ci.yml`)

```
push / pull request
   │
   ├─ calidad ──────── ruff check  →  unittest (15 pruebas)
   │
   ├─ integracion ──── Playwright: 38 pruebas en Chromium headless
   │                   artefacto: pruebas-resultados.json + capturas
   │
   └─ beta ─────────── EcoGame-beta.zip (HTML5 + CAPX + manual + reporte)
                       con etiqueta v* → GitHub Release (pre-release)
```

Cada etapa depende de la anterior: un fallo detiene la entrega.

### Ejecución local

```bash
pip install ruff playwright
python -m playwright install chromium
ruff check tools tests
python -m unittest discover -s tests -v
python tests/integracion_qa.py
```

## 3. Proceso de pruebas enfocado en videojuegos

| Fase | Tipo de prueba | Responsable | Criterio de salida |
|---|---|---|---|
| Alfa (interna) | Funcional automatizada (unitarias + integración) | Equipo | 100 % de pruebas automatizadas aprobadas |
| Alfa | Exploratoria / *smoke test* manual: abrir CAPX, F5, recorrer el nivel completo | Equipo | Sin defectos críticos ni altos |
| Beta (cerrada) | **Jugabilidad**: dificultad, curva, tiempo, claridad de objetivos | Testers externos (5–10) | Cuestionario respondido por todos |
| Beta | **Usabilidad / UX**: comprensión del HUD, controles y guía de separación | Testers | ≥ 80 % completa la fase 1 sin ayuda |
| Beta | **Compatibilidad**: Chrome, Edge, Firefox; Windows y móvil (navegador) | Testers / equipo | Funciona en ≥ 2 navegadores |
| Beta | **Rendimiento**: FPS estable (≥ 50) y tiempo de carga < 5 s en local | Equipo | Medido con las DevTools del navegador |
| Beta | **Audio**: música en bucle, efectos sincronizados, silencio con M | Testers | Sin desincronización reportada |
| Beta | **Educativa**: el jugador identifica correctamente la categoría de residuos | Testers | Mejora entre pre y post cuestionario |
| Release candidate | Regresión: pipeline completo tras corregir los defectos de la Beta | CI | Pipeline en verde |

### Procedimiento de una sesión de beta testing

1. Entregar `EcoGame-beta.zip` y el `MANUAL-USUARIO.md`.
2. Pre-cuestionario: clasificar los 6 residuos del juego (cáscara de plátano, corazón de manzana, botella PET, lata, hoja de papel, caja de cartón).
3. El tester juega sin ayuda hasta ganar o perder (máx. 2 intentos). El observador anota tiempo, errores y dudas.
4. Post-cuestionario: el mismo de clasificación + encuesta de experiencia (escala 1–5).
5. Registrar los defectos encontrados como issues con severidad y pasos para reproducirlos.
6. Consolidar en `BETA-REPORTE.md`.

## 4. Clasificación de defectos

| Severidad | Definición | Ejemplo | Acción |
|---|---|---|---|
| Crítica | Bloquea el juego o impide terminar el nivel | El jefe no aparece tras 12 entregas | Corrige antes de cualquier entrega |
| Alta | Rompe una regla del juego | Un error no resta vida | Corrige antes de la versión final |
| Media | Afecta la experiencia, existe alternativa | Texto del HUD se solapa | Planificar |
| Baja | Cosmético | Color de un destello | Opcional |
