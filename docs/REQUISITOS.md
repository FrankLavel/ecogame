# Alcance del videojuego

La consigna integra tres materias. Este trabajo desarrolla el apartado **Creación de Videojuegos (Enfoque 2D en Construct)**. La aplicación móvil, la autenticación, los servicios en la nube y el proceso CI/CD corresponden a las otras actividades.

| Requisito del apartado 3 | Implementación |
|---|---|
| Motor Construct | Proyecto nativo de Construct 2 r213 en CAPROJ y CAPX; exportación HTML5 realizada desde el editor |
| Escenas/layouts, capas y eventos | Un layout de 1280 × 720, cuatro capas y hoja de eventos comentada; las pantallas se controlan por estados y cuadros del sprite Overlay |
| Movimiento del personaje | Comportamiento 8 Direction, controles WASD/flechas; 16 cuadros de caminata y orientación persistente al parar |
| Comportamientos y colisiones | Solid para estanque, bancas y límites; colisión con residuos para recolectar |
| Mecánica ambiental educativa | 12 residuos, seis ilustraciones y tres categorías; mochila de capacidad uno y entrega por proximidad |
| Sistema de puntaje | Puntos por acierto, racha y bonificación final por tiempo y vidas |
| Vidas/intentos | Tres vidas, explicación al equivocarse, derrota y reinicio completo |
| Un nivel funcional completo | Inicio, exploración, recolección y clasificación; después, introducción y pelea contra Don Mugrón, victoria y derrota |
| Escenario y sprites | Pixel art original: parque, senderos, vegetación, estanque, bancas, personaje y contenedores; reflejos, hojas y destellos animados |
| HUD | Puntaje, progreso, tiempo, vidas y mochila compactos; consejos arriba a la izquierda; controles y sonido en pausa |
| Efectos y música | Música en bucle y efectos para recoger, acertar, equivocarse, ganar y perder; control de silencio |

## Concepto y estructura

El jugador es guardián del Parque Alba. La limpieza se observa al desaparecer cada residuo y aumentar el contador. Cada entrega carga un contenedor. Después de separar todo, Don Mugrón aparece y el jugador reutiliza esas cargas para defender el parque. El diseño usa etiquetas, números y color para identificar los contenedores.

La variable `State` representa las pantallas: 0 inicio, 1 juego activo, 2 pausa, 3 guía, 4 victoria, 5 derrota y 6 introducción del jefe. `Stage` distingue recolección (0) y combate (1). `Cmd` recibe las acciones del teclado o los botones. `Carry` conserva la categoría y `ItemName` el nombre del residuo transportado. `Clean`, `Score`, `Lives`, `TimeLeft` y `Combo` controlan el progreso. `BossHP`, `Shield`, `BossClock`, `Cooldown` e `Invuln` controlan la pelea. `Facing`, `AnimClock` y `BossHurt` sincronizan los cuadros de animación con las acciones. Cada contenedor tiene una variable de instancia `Stock`.

El nivel usa 38 tipos de objeto, cuatro capas y 72 bloques de eventos, más 22 declaraciones de variables globales: el editor cuenta 94 eventos. Se mantiene dentro de las restricciones de la edición gratuita instalada. La pelea y la estética pixel son ampliaciones creativas solicitadas por el usuario. Se configura muestreo Linear y sprites de mayor resolución para mejorar la lectura.

## Entrega sugerida

Entregar `EcoGame.capx`, la carpeta `export/html5`, el manual `README.md` y el registro técnico de pruebas. Agregar los nombres de los integrantes y cualquier portada requerida por el docente. No se ha inventado información de participantes ni resultados de pruebas con alumnos.

La versión 4 añade proyectiles visibles de lata y tierra, una triple descarga en furia y embestida anunciada al perder media vida. La ventana de contraataque se reduce durante esta fase.
