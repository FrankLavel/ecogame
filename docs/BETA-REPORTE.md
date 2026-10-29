# Reporte de Beta Testing — EcoGame 4.0 Beta

| Dato | Valor |
|---|---|
| Versión | `v4.0.0-beta.1` |
| Motor | Construct 2 r213 — exportación HTML5 |
| Fecha de corte | 28/10/2026 |
| Equipo | _(nombres de integrantes)_ |
| Paquete | `EcoGame-beta.zip` (generado por el pipeline CI) |

## 1. Resultados automatizados (verificados)

| Nivel | Herramienta | Resultado |
|---|---|---|
| Análisis estático | Ruff | 0 errores (se corrigieron 4 imports/f-strings sin uso en `tools/`) |
| Unitarias | unittest | 15 / 15 aprobadas |
| Integración | Playwright + Chromium headless | **38 / 38 aprobadas** — detalle en `pruebas-resultados.json` |

Defecto encontrado por las pruebas unitarias y corregido: el servidor local cerraba la conexión sin respuesta al recibir un reporte JSON inválido; ahora responde `400 Bad Request` (`tools/serve_game.py`).

Capturas del render real durante las pruebas: `docs/evidence/` (juego, intro, boss, embestida, pausa, victoria).

## 2. Sesiones con testers

> Completar con los datos reales de cada sesión. No llenar con valores estimados.

| # | Tester (edad / perfil) | Navegador / dispositivo | Resultado (gana/pierde, fase) | Tiempo | Errores de clasificación | Pre ✓/6 | Post ✓/6 |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |

### Encuesta de experiencia (1 = muy en desacuerdo, 5 = muy de acuerdo)

| Afirmación | Promedio |
|---|---|
| Entendí el objetivo sin leer el manual | |
| Los controles responden bien | |
| El HUD (tiempo, vidas, mochila) es claro | |
| La dificultad del jefe es justa | |
| La música y los efectos son agradables | |
| Aprendí a separar mejor los residuos | |
| Volvería a jugar | |

## 3. Defectos reportados en la Beta

| ID | Severidad | Descripción | Pasos para reproducir | Estado |
|---|---|---|---|---|
| | | | | |

## 4. Conclusiones y siguientes pasos

- _(hallazgos principales de jugabilidad y aprendizaje)_
- _(ajustes de dificultad / UX a aplicar antes de `v4.0.0`)_

## 5. Limitaciones conocidas

- La lógica de Construct se prueba a nivel de integración (runtime exportado), no con pruebas unitarias aisladas.
- Las pruebas automatizadas reposicionan al personaje y modifican variables; no sustituyen una partida humana.
- No se ha probado en un teléfono físico. La versión actual se controla con teclado.
