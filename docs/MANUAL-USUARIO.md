# Manual de usuario — EcoGame: El pato furioso (Beta)

## 1. ¿De qué trata?

Eres el guardián del **Parque Alba**. Recoge los 12 residuos tirados en el parque y deposítalos en el contenedor correcto. Al terminar aparece **Don Mugrón**, un pato gigante que quiere volver a ensuciarlo: derrótalo usando lo que reciclaste.

## 2. Requisitos

- Computadora con un navegador actual (Chrome, Edge o Firefox).
- Python 3 para el lanzador `Jugar.cmd` (opcional si se abre en Construct 2).
- Teclado.

## 3. Cómo iniciar

1. Descomprime `EcoGame-beta.zip`.
2. Haz doble clic en **Jugar.cmd**. Se abrirá el juego en el navegador.
3. Mantén abierta la ventana negra mientras juegas; ciérrala para terminar.

Alternativa: abre `EcoGame.capx` en Construct 2 y pulsa **F5**.

## 4. Controles

| Acción | Tecla |
|---|---|
| Caminar | W A S D o flechas |
| Recoger un residuo | Caminar sobre él |
| Entregar / disparar | **E** o **Espacio**, junto al contenedor |
| Pausa | **P** o **Esc** (o botón II) |
| Guía de separación | **H** |
| Silenciar / activar sonido | **M** |
| Comenzar / continuar / reintentar | **Enter** |

## 5. Pantalla (HUD)

- **Arriba:** puntaje, residuos limpiados (x / 12), tiempo restante y vidas.
- **Arriba a la izquierda:** consejos.
- **Mochila:** muestra el residuo que llevas; una flecha señala su contenedor.

## 6. Fase 1 — Limpieza

- Tienes **3 minutos y 3 vidas**. Solo cargas **un residuo** a la vez.
- Contenedores: **orgánicos** (verde), **envases** (amarillo) y **papel** (azul).
- Acierto: +100 puntos, +10 por cada acierto seguido.
- Error: pierdes una vida; el juego te dice la categoría correcta y conservas el residuo.
- Pierdes si se acaba el tiempo o las vidas.

## 7. Fase 2 — Don Mugrón

- Recuperas 3 vidas y tienes **90 segundos**. El pato tiene **6 puntos de vida**.
- **Zona roja:** muévete, ahí caerá un ataque. Tocar al pato también duele.
- Espera el aviso **ABERTURA** en su barra.
- Ve al contenedor del **color de su escudo** y pulsa **E**: lanzas una carga reciclada.
- Necesitas 2 impactos de cada color. A media vida se enfurece: lanza 3 residuos y embiste (sigue la línea naranja).
- Victoria: +500, +2 por segundo restante, +50 por vida.

## 8. Problemas frecuentes

| Problema | Solución |
|---|---|
| Pantalla negra al abrir `index.html` con doble clic | Usa `Jugar.cmd`; el navegador bloquea archivos locales. |
| “Puerto 8765 ocupado” | Ya hay un juego abierto: visita http://127.0.0.1:8765/export/html5/ o cierra la otra ventana. |
| No se oye nada | Pulsa **M** o haz clic en el juego (el navegador exige interacción). |
| `Jugar.cmd` pide Python | Instala Python 3 desde python.org. |

## 9. Reportar un error (Beta)

Indica: qué hacías, qué esperabas, qué pasó, navegador y, si puedes, una captura. Entrégalo al equipo o abre un *issue* en el repositorio.
