# EcoGame 4: El pato furioso

Juego educativo 2D desarrollado en **Construct 2 r213**, compatible con su edición gratuita. Recupera el Parque Alba separando 12 residuos y defiéndelo de un pato gigante con los contenedores que cargaste. La edición actual mantiene el ambiente retro con una interfaz legible y un combate más exigente.

## Vista y combate

Interfaz compacta: consejos arriba a la izquierda, mochila pequeña y una franja superior de estado. Los controles, la guía y el botón de sonido están en pausa (P, Esc o II). Esta versión se juega con teclado; se retiraron la cruceta y el botón de acción permanentes.

Se conservan las 16 animaciones del personaje, seis poses del pato, agua, hojas y destellos. El escenario usa detalle completo, suavizado y letras Arial grandes.

Don Mugrón lanza una lata visible en arco hacia la zona roja. Con tres puntos de vida o menos lanza tres residuos (lata y tierra), reduce el aviso a 0,75 segundos y añade una embestida. La trayectoria naranja se anuncia durante 0,75 segundos; después carga en 0,6 segundos y regresa. Solo queda una abertura de 1,2 segundos por ciclo para usar los contenedores. La pausa congela también estos ataques.

## Jugar

- En esta computadora: abre **Jugar.cmd**. Se inicia un servidor accesible únicamente desde esta computadora y se abre el juego en el navegador. Mantén su ventana abierta mientras juegas.
- Desde Construct: abre **EcoGame.capx** y pulsa **F5**. El archivo incluye los gráficos, sonidos y eventos.
- Para editar la carpeta actual: abre **EcoGame.caproj** y conserva sus subcarpetas.
- Para alojamiento web: publica el contenido de **export/html5/** en un servidor HTTP/HTTPS. Abrir `index.html` con doble clic puede bloquear la carga de recursos del motor.

El lanzador necesita Python 3. Busca primero `py`, después el Python incluido con Codex en esta computadora y finalmente `python`. Si el puerto 8765 ya está ocupado por otra instancia del juego, visita http://127.0.0.1:8765/export/html5/ o cierra esa instancia.

## Controles

| Acción | Teclado | Pantalla / ratón |
|---|---|---|
| Caminar | WASD o flechas | Teclado |
| Recoger | Caminar sobre un residuo | Igual |
| Entregar / disparar | E o espacio, cerca de un contenedor | E o espacio |
| Pausa | P o Esc | Botón II |
| Guía de separación | H | GUÍA, dentro de pausa |
| Silenciar / activar audio | M | Botón de sonido, dentro de pausa |
| Comenzar / continuar / reintentar | Enter | Botón de la pantalla correspondiente |

## Reglas

Tienes **3 minutos y 3 vidas**. La mochila admite un residuo. Deposítalo en el contenedor indicado por su etiqueta: orgánicos, envases o papel. Un error consume una vida, explica la categoría correcta y conserva el residuo para que puedas intentarlo de nuevo. No se puede entregar desde lejos.

Cada acierto suma 100 puntos más 10 por cada acierto consecutivo anterior. Un error rompe esa racha. Al completar las 12 entregas aparece **Don Mugrón**: un pato gigante con corona de lata y cinturón de neumático que quiere volver a ensuciar el parque. La pantalla de introducción explica la pelea y espera tu confirmación.

## Jefe final

Recuperas las tres vidas y tienes **90 segundos**. Cada contenedor conserva cuatro cargas gracias a los residuos entregados. Don Mugrón tiene seis puntos de vida.

1. Muévete cuando marque una zona roja: después caerá un ataque sobre ella. El contacto con el pato también causa daño.
2. Espera a que aparezca **ABERTURA** en su barra.
3. Acércate al contenedor del color de su escudo y pulsa **E** o **espacio**. La carga reciclada sale como un proyectil y le quita un punto de vida al impactar.
4. Tras cada impacto cambia de color: verde, amarillo y azul. Necesitas dos impactos de cada categoría.

Un intento con el color incorrecto o fuera de la abertura no consume munición. Cada disparo válido consume una carga, con un breve tiempo de recarga. Tras recibir daño, el guardián parpadea y queda protegido temporalmente. A media vida, el pato acorta los avisos, acelera sus ataques y amplía las zonas de impacto.

Cada impacto al jefe suma 250 puntos. Al vencerlo recibes 500 puntos extra, 2 por segundo restante entero y 50 por vida conservada. **La victoria requiere completar ambas fases.** La pausa y la guía congelan también los ataques y los proyectiles.

Los colores corresponden a la convención de este juego; las reglas reales de recolección pueden variar según la localidad.

## Archivos

| Archivo / carpeta | Contenido |
|---|---|
| EcoGame.capx | Proyecto portátil para abrir y entregar en Construct |
| EcoGame.caproj | Proyecto editable en esta carpeta |
| Layouts/Layout 1.xml | Nivel y cuatro capas: Fondo, Parque, Interfaz, Pantallas |
| Event sheets/Event sheet 1.xml | Lógica nativa y comentarios en español |
| Animations/ | Parque, personaje, residuos, contenedores, HUD y pantallas |
| Files/ | Recursos internos, incluyendo el audio que usa Construct |
| AudioSource/ | Música y efectos originales en WAV |
| export/html5/ | Juego exportado por Construct |
| tools/build_v4.py | Generador de vista compacta, pausa y nuevos ataques |
| tools/build_v3.py | Generador de la edición pixel, sobre la lógica de las versiones anteriores |
| art-source/v3/ | Originales pixel y prompts de producción |
| art-source/v2/ | Ilustraciones anteriores, usadas por el generador de base |
| archive/v1/ y archive/v2/ | Copias de las entregas anteriores |
| docs/REQUISITOS.md | Correspondencia con el apartado de videojuegos |
| docs/PRUEBAS.md | Validación técnica y sus límites |
| docs/qa.html | Pruebas de aceptación sobre el motor exportado |
| docs/PROCESO-PRUEBAS.md | Gestión del proceso: herramientas de prueba, pipeline CI/CD y proceso Beta |
| docs/BETA-REPORTE.md · docs/MANUAL-USUARIO.md | Reporte de beta testing y manual de usuario |
| tests/ · ruff.toml · .github/workflows/ci.yml | Pruebas unitarias, de integración, análisis estático y pipeline |

El escenario, el pato, el personaje, los contenedores y los residuos fueron creados con la herramienta integrada de generación de imágenes. Los atlas se separan en cuadros con mayor resolución y bordes suavizados. La interfaz, las señales, los reflejos, las hojas y los destellos se dibujan con código. El audio fue sintetizado para este proyecto. No requiere descargar assets ni instalar plugins de Construct. El motor y las bibliotecas de la exportación pertenecen a sus respectivos autores.

Para regenerar la versión actual, ejecuta `tools/build_v3.py` y después `tools/build_v4.py` con Python, Pillow y los codificadores incluidos en la instalación local de Construct 2. **Regenerar sobrescribe los layouts y eventos**: si los editas manualmente, conserva una copia antes. Después vuelve a exportar desde Construct para actualizar la versión HTML5. Los generadores anteriores se conservan como bases; ejecutarlos por separado restaura sus versiones previas.
