# Registro de validación técnica

Fecha: 28 de octubre de 2026. Entorno: Windows, Construct 2 r213 Free Edition y navegador Chromium del panel local.

Resultado: **38 de 38 pruebas de aceptación aprobadas**.

## Pruebas sobre el motor exportado

El banco `docs/qa.html` carga el HTML5 generado por Construct. Prepara posiciones y variables en una instancia aislada y comprueba las transiciones de los eventos reales. Las pruebas del nivel completo reposicionan al personaje; no representan una partida manual de velocidad ni sustituyen una evaluación de dificultad con usuarios.

- Aprobada: Inicio: 12 residuos, 3 vidas, 180 segundos y puntaje cero.
- Aprobada: Comenzar cambia al estado de juego.
- Aprobada: Sprites con 16 cuadros de caminata, 6 poses del jefe y 8 cuadros de agua.
- Aprobada: El teclado selecciona animación de caminar y reposo en las cuatro direcciones.
- Aprobada: Colisión recoge un residuo y conserva categoría y nombre.
- Aprobada: La mochila muestra el icono recogido y la flecha señala ENVASES.
- Aprobada: La mochila admite un único residuo.
- Aprobada: Entregar lejos de los contenedores no resta vidas ni suma puntos.
- Aprobada: Contenedor incorrecto resta una vida, conserva residuo e indica ENVASES.
- Aprobada: Contenedor correcto suma 100 puntos y carga una unidad de defensa.
- Aprobada: Tras entregar, se ocultan el icono de mochila y la flecha.
- Aprobada: El agua y las hojas se animan durante la partida.
- Aprobada: Pausa congela el reloj, el personaje y las animaciones ambientales.
- Aprobada: La guía conserva la pausa y permite continuar.
- Aprobada: Silenciar y reactivar actualiza el estado.
- Aprobada: Tres errores activan derrota y bloquean nuevas penalizaciones.
- Aprobada: Reintentar restaura residuos, reloj, vidas, mochila y puntaje.
- Aprobada: Dos residuos superpuestos recogen solo uno y dejan el otro en el parque.
- Aprobada: Agotar el tiempo activa derrota.
- Aprobada: 12 recogidas y entregas desbloquean al jefe sin conceder victoria prematura.
- Aprobada: Confirmar la introducción inicia el combate sin reiniciar el reciclaje.
- Aprobada: La zona roja es visible durante el aviso y se oculta en la abertura.
- Aprobada: Disparar cuando el jefe está protegido no gasta cargas.
- Aprobada: Un contenedor de color incorrecto tampoco gasta cargas.
- Aprobada: Un disparo válido crea un proyectil y consume una sola carga.
- Aprobada: Pausa detiene un proyectil en vuelo, los ataques y el tiempo.
- Aprobada: Zona de impacto resta una vida y da invulnerabilidad temporal.
- Aprobada: Contacto con Don Mugrón también causa daño.
- Aprobada: El tercer acierto activa una fase de ataques más rápida.
- Aprobada: Latas y tierra visibles recorren la pantalla; tres proyectiles en furia.
- Aprobada: La embestida solo aparece a media vida y mueve al pato por su trayectoria.
- Aprobada: La pausa congela también la basura enemiga.
- Aprobada: Durante la embestida no se gastan cargas.
- Aprobada: La barra del jefe refleja visualmente su media vida.
- Aprobada: Seis impactos de los tres colores derrotan al jefe.
- Aprobada: Victoria congela el reloj y permite reiniciar las dos fases.
- Aprobada: El tiempo del combate también puede agotarse.
- Aprobada: Recursos de audio disponibles: dos músicas y ocho efectos.

## Comprobación manual

- Apertura del proyecto en Construct y ejecución de la vista previa.
- Revisión visual de menú, escenario, personaje, HUD, guía y pausa.
- Movimiento con teclado y recolección por colisión.
- Entrega incorrecta: resta una vida y conserva el residuo.
- Entrega correcta: suma puntaje y progreso.
- Derrota por vidas y reinicio mediante el botón de pantalla.
- Exportación HTML5 desde el editor de Construct.

## Integridad de la entrega

- CAPX sin errores de compresión; sus recursos y proyecto coinciden con la carpeta editable.
- 38 tipos de objeto, cuatro capas y 72 bloques de eventos; con 22 variables globales, Construct cuenta 94 eventos.
- Muestreo Linear y recursos de mayor resolución: personaje 32 × 48, jefe 112 × 112, agua 112 × 72.
- Diez archivos OGG verificados en la exportación y en los recursos internos.

## Reproducir las pruebas

Abre `Jugar.cmd`, visita http://127.0.0.1:8765/docs/qa.html y pulsa Ejecutar pruebas. El servidor local guarda el reporte JSON y dos capturas en `docs/`. La prueba es independiente del proyecto abierto en Construct.

## Límites de esta validación

No se han realizado sesiones de beta testing con alumnos ni pruebas en un teléfono físico. La carga de audio y el control de silencio fueron comprobados; queda a tu criterio ajustar su volumen y evaluar la dificultad mediante una partida. Las pruebas automatizadas preparan posiciones y variables para validar reglas y casos límite; no constituyen una partida humana completa.

El reporte verificable está en `pruebas-resultados.json`; las capturas corresponden al render real del juego durante las pruebas.

Ajuste posterior: los cuatro cuadros de caminar a la derecha reflejan los de la izquierda para conservar tamaño y proporciones. Se actualizaron el CAPX y el atlas HTML5. Por solicitud del usuario no se ejecutaron nuevas pruebas tras este ajuste visual.
