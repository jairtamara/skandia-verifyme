
# Prompt de estilos — Sistema VerifyMe

Pega este documento completo en el otro proyecto, como instrucción de diseño. Está escrito para
que lo lea una persona o un asistente y produzca pantallas coherentes con las de este proyecto.

Los valores **no están inventados**: salen del sistema de diseño del Portal Empresarial Skandia
(`SkCo.Portalempresarial.Corporate.Angular/DESIGN.md` y `src/styles.css`). Si el otro proyecto
también es del portal, no cambies los hex. Si es otra marca, cambia únicamente el acento y la
familia tipográfica y deja intacto todo lo demás.

---

## 1. La idea que gobierna todo

> **La superficie está en silencio; el color solo habla cuando comunica un estado.**

Fondos planos, tarjetas blancas, tipografía haciendo la jerarquía. El verde, el ámbar y el rojo
se reservan para decir en qué punto va algo. Si un color no responde a «¿en qué estado está
esto?», «¿a qué categoría pertenece este dato?» o «¿es la acción principal?», sobra.

---

## 2. Paleta

Pégala tal cual. Los tres bloques son obligatorios: el claro define **todos** los tokens, y los
dos oscuros solo los redefinen. Un color que solo exista dentro del bloque oscuro deja la página
ilegible para quien tiene el sistema en claro.

```css
:root {
  /* Lienzo y superficies */
  --canvas: #eef1f6;          /* fondo de página */
  --surface: #ffffff;         /* tarjetas, modales */
  --surface-2: #f4f6fa;       /* superficie secundaria */
  --sunken: #ececef;          /* hundido: thead, pie de paginador, esqueleto */
  --hover: rgba(0,0,0,.075);  /* fila o ítem bajo el cursor */

  /* Resplandores del lienzo (radiales, nunca 135°) */
  --glow-1: rgba(0,199,61,.17);
  --glow-2: rgba(0,153,222,.15);
  --glow-3: rgba(0,153,222,.09);

  /* Tinta — cuatro escalones, no inventes grises intermedios */
  --ink: #404040;             /* texto por defecto */
  --ink-strong: #18202a;      /* títulos y valores */
  --ink-muted: #5c6672;       /* texto secundario, metadatos */
  --ink-faint: #a5a5a5;       /* marcador de posición, detalle */

  /* Líneas */
  --line: #ededed;            /* borde de tarjeta y separador de fila */
  --line-strong: #d7dce2;     /* borde de control y de modal */

  /* Marca */
  --accent: #00c73d;          /* SOLO relleno, borde e icono. Nunca texto */
  --accent-ink: #00812c;      /* el verde cuando es texto */
  --accent-tint: #e4fbde;     /* fondo de ítem elegido */

  /* Estado — cada familia con su lavado, su línea y su tinta */
  --ok-wash: #f0fdf4;  --ok-tint: #dcfce7;  --ok-line: #bbf7d0;  --ok-ink: #166534;
  --warn-wash: #fff7ed; --warn-line: #fed7aa; --warn-ink: #c2410c;
  --danger-wash: #fdf2f2; --danger-soft: #f3a9a5; --danger-ink: #991b1b;

  /* Dato — para gráficas, nunca para estado */
  --data: #3c6ea5;
  --grid: var(--line);

  --shadow-card: 0 8px 24px rgba(31,45,79,.16);

  /* Radios */
  --r-xs: 4px;      /* barras, chips de datos */
  --r-select: 10px; /* inputs, selects, bloques */
  --r-badge: 20px;  /* pastillas de estado */
  --r-pill: 50px;   /* botones */
  --r-card: 14px;   /* tarjetas */

  /* Espaciado — una sola escala */
  --s-xs: 8px; --s-sm: 16px; --s-md: 24px; --s-lg: 36px; --s-xl: 40px;

  --page-max: 1200px;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --canvas: #0c1016;
    --surface: #121922; --surface-2: #0f151d;
    --sunken: rgba(255,255,255,.05); --hover: rgba(255,255,255,.055);
    --glow-1: rgba(34,215,92,.17);
    --glow-2: rgba(79,185,239,.15);
    --glow-3: rgba(79,185,239,.09);
    --ink: #e9eef5; --ink-strong: #f4f7fb; --ink-muted: #a3aebb;
    --ink-faint: rgba(255,255,255,.42);
    --line: rgba(255,255,255,.10); --line-strong: rgba(255,255,255,.16);
    --accent-ink: #7ef2a4; --accent-tint: rgba(34,215,92,.14);
    --ok-wash: rgba(34,215,92,.10); --ok-tint: rgba(34,215,92,.18);
    --ok-line: rgba(34,215,92,.30); --ok-ink: #7ef2a4;
    --warn-wash: rgba(245,158,11,.12); --warn-line: rgba(245,158,11,.32);
    --warn-ink: #f0b45f;
    --danger-wash: rgba(255,107,107,.10); --danger-soft: rgba(255,107,107,.35);
    --danger-ink: #ffa8a8;
    --data: #6fa3d6;
    --shadow-card: 0 12px 30px rgba(0,0,0,.55);
  }
}
/* Repite EXACTAMENTE el mismo bloque para que el interruptor gane en los dos sentidos */
:root[data-theme="dark"] { /* …idéntico al bloque de arriba… */ }
```

`--accent` se mantiene `#00c73d` en ambos temas: es el color de marca.

### Sólidos de estado para rellenos de gráfica

Cuando necesites el color pleno del estado (segmentos de barra, puntos de leyenda):
éxito `#00c73d`, advertencia `#f59e0b`, error `#d22c27`, neutro `var(--ink-faint)`.

---

## 3. Tipografía

**Dos familias, y la regla que decide cuál:**

> Si el texto es una **etiqueta, un botón, un título o un dato numérico** → Montserrat 700.
> Si es **contenido para leer** → Open Sans 400.

No las mezcles dentro del mismo rol.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Open+Sans:wght@400;600&display=swap">
```

```css
body { font: 400 14px/1.45 "Open Sans", system-ui, sans-serif; }
h1, h2, h3, .lbl, .pill, .chip, th, .btn { font-family: Montserrat, system-ui, sans-serif; }
.num { font-variant-numeric: tabular-nums; }   /* obligatorio en columnas de cifras */
code { font-family: ui-monospace, Consolas, monospace; font-size: .88em;
       background: var(--sunken); padding: 1px 5px; border-radius: var(--r-xs); }
```

| Rol | Especificación |
|---|---|
| Título de página | Montserrat 700, `clamp(26px, 2.2vw, 34px)`, interlineado 1.15, `--ink-strong`, `text-wrap: balance` |
| Título de sección | Montserrat 700, 20 px, interlineado 1.1, `--ink-strong` |
| Título de tarjeta | Montserrat 700, 14–16 px |
| Cuerpo | Open Sans 400, 14 px, interlineado 1.45. En documentos de lectura: 15 px / 1.65 |
| Etiqueta | Montserrat 700, 10–11 px, `letter-spacing: .07em`, mayúsculas, `--ink-muted` |
| Cifra grande | Montserrat 700, 24–27 px, interlineado 1, `--ink-strong` |
| Nota al pie | 12–12.5 px, `--ink-muted` |

**Medida de lectura:** los párrafos van a `max-width: 68ch`; las entradas de sección a `66ch`.
Un texto que cruza toda la pantalla no se lee.

---

## 4. Reglas de color que hay que respetar

Estas son las que evitan que el sistema se deshaga a la tercera pantalla.

1. **El verde de marca no es legible como texto.** `#00c73d` da 2,2:1. Todo verde que sea tinta
   usa `--accent-ink`. El de marca se reserva para rellenos, bordes e iconos.
2. **El color de estado está reservado.** Verde, ámbar y rojo solo dicen en qué punto va algo.
   Nunca son «la serie 3» de una gráfica ni un acento decorativo.
3. **El rojo se gana.** Solo en rechazo o error real. No para llamar la atención.
4. **Un color de dato dice a qué categoría pertenece**, no en qué estado está. Va únicamente
   dentro de una gráfica o en el punto que etiqueta su leyenda.
5. **Forma además de color.** El punto de estado es **redondo**; la marca de categoría es un
   **cuadrado redondeado** de 3 px. Dos vocabularios distintos, dos formas distintas.
6. **Ningún componente trae su propia paleta.** Si necesitas un gris nuevo, ya existe en la lista
   de arriba.
7. **Degradados de 135° solo para estado** (pastillas, barras de progreso). Nunca como fondo
   decorativo. El lienzo de página es la única excepción, y usa radiales.

---

## 5. Componentes

### Botón

```css
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px;
       height: 44px; padding: 0 26px; border: 0; border-radius: var(--r-pill);
       background: var(--accent); color: #fff; cursor: pointer;
       font: 700 13px/1 Montserrat, sans-serif; transition: filter .12s; }
.btn:hover:not(:disabled) { filter: brightness(1.06); }
.btn:disabled { opacity: .5; cursor: not-allowed; }
.btn:focus-visible { outline: 2px solid var(--accent-ink); outline-offset: 2px; }

.btn.sec     { background: var(--surface); color: var(--ink); border: 1px solid var(--line-strong); }
.btn.peligro { background: var(--surface); color: var(--danger-ink); border: 1px solid var(--danger-soft); }
```

Píldora de 44 px de alto, siempre. El primario es verde sólido; el secundario es contorno. **Nunca
degradado.** Un botón de peligro es contorno rojo, no relleno.

### Pastilla de estado

```css
.pill { display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px;
        border-radius: var(--r-badge); font: 700 11px/1.3 Montserrat, sans-serif;
        letter-spacing: .04em; border: 1px solid transparent; white-space: nowrap; }
.pill::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }

.pill.ok     { background: var(--ok-tint);     color: var(--ok-ink);     border-color: var(--ok-line); }
.pill.warn   { background: var(--warn-wash);   color: var(--warn-ink);   border-color: var(--warn-line); }
.pill.error  { background: var(--danger-wash); color: var(--danger-ink); border-color: var(--danger-soft); }
.pill.neutro { background: var(--sunken);      color: var(--ink-muted);  border-color: var(--line-strong); }
```

El punto redondo del `::before` es lo que la hace legible sin depender solo del color.

### Tarjeta

```css
.card { background: var(--surface); border: 1px solid var(--line);
        border-radius: var(--r-card); padding: var(--s-md); }
```

Sin sombra en reposo. La sombra se reserva para lo que flota: menús (`--shadow-card`) y modales.
**No todo es una tarjeta**: si un bloque no necesita separarse, va sobre el lienzo con un
separador de 1 px.

### Fila de cifras

```css
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 1px; background: var(--line); border: 1px solid var(--line);
        border-radius: var(--r-card); overflow: hidden; }
.kpi { background: var(--surface); padding: 18px 20px; }
.kpi .lbl  { font: 700 11px/1.2 Montserrat, sans-serif; letter-spacing: .07em;
             text-transform: uppercase; color: var(--ink-muted); display: block; }
.kpi-v     { display: block; margin-top: 7px; font: 700 27px/1 Montserrat, sans-serif;
             color: var(--ink-strong); }
.kpi .foot { display: block; margin-top: 6px; font-size: 12px; color: var(--ink-muted); }
```

El truco del `gap: 1px` sobre fondo `--line` da las divisiones sin dibujar bordes.

### Tabla

```css
.tbl-wrap { overflow-x: auto; border: 1px solid var(--line);
            border-radius: var(--r-card); background: var(--surface); }
table { border-collapse: collapse; width: 100%; }
thead th { background: var(--sunken); text-align: left; padding: 11px 14px;
           font: 700 11px/1.2 Montserrat, sans-serif; letter-spacing: .06em;
           text-transform: uppercase; color: var(--ink-muted);
           position: sticky; top: 0; z-index: 1; }
tbody td { padding: 10px 14px; border-top: 1px solid var(--line);
           vertical-align: top; font-size: 13px; }
tbody tr:hover { background: var(--hover); }
```

Encabezado hundido y pegajoso, filas separadas por línea superior, sin cebra.
Toda tabla va dentro de un contenedor con `overflow-x: auto`: **el cuerpo de la página nunca
hace scroll horizontal.**

### Campos y filtros

```css
select, input[type="text"] {
  font: 400 14px/1.2 "Open Sans", sans-serif; color: var(--ink);
  background: var(--surface); border: 1px solid var(--line-strong);
  border-radius: var(--r-select); padding: 12px 14px; }

.chip { border: 1px solid var(--line-strong); background: var(--surface); color: var(--ink);
        border-radius: var(--r-pill); padding: 7px 15px; font-size: 12px; font-weight: 700;
        cursor: pointer; transition: background .12s, border-color .12s, color .12s; }
.chip:hover { background: var(--hover); }
.chip[aria-pressed="true"] { background: var(--accent-tint); border-color: var(--accent);
                             color: var(--accent-ink); }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
```

El chip activo se marca con `aria-pressed`, no con una clase: el estado queda en el DOM y no solo
a la vista.

### Navegación lateral

```css
nav a { display: flex; align-items: center; gap: 11px; padding: 10px 12px;
        border-radius: var(--r-select); color: var(--ink); text-decoration: none;
        font: 600 13px/1.2 Montserrat, sans-serif; }
nav a:hover { background: var(--hover); }
nav a[aria-current="page"] { background: var(--accent-tint); color: var(--accent-ink); }
```

Iconos de 17 px, trazo de 2, sin relleno. El activo se marca con `aria-current="page"`.

### Bloque de mensaje

```css
.bloque-msg { border: 1px solid var(--line); border-left-width: 3px;
              border-radius: var(--r-select); padding: 18px 22px; background: var(--surface); }
.bloque-msg.ok    { border-left-color: #00c73d; background: var(--ok-wash); }
.bloque-msg.warn  { border-left-color: #f59e0b; background: var(--warn-wash); }
.bloque-msg.error { border-left-color: #d22c27; background: var(--danger-wash); }
```

El trazo de color a la izquierda **solo se admite cuando su valor sale de un dato de estado**.
Nunca fijo, nunca por categoría, nunca por gusto.

### Consola

```css
.consola { background: #0e141b; color: #d6dde6; border-radius: var(--r-select);
           padding: 14px 16px; overflow: auto;
           font: 12px/1.55 ui-monospace, Consolas, monospace; white-space: pre-wrap; }
.consola .ok { color: #7ee89a; } .consola .bad  { color: #ff9b96; }
.consola .warn { color: #f5c46b; } .consola .dim { color: #7b8798; }
.consola .cmd { color: #8fd0ff; }
```

Es la única superficie que se mantiene oscura en los dos temas.

---

## 6. Maquetación

- Ancho máximo **1200 px**, centrado. En documentos de lectura, **860 px**.
- Un riel lateral de 246 px es un objeto real: el contenido se centra en lo que queda a su derecha.
- Cortes: **767 px** (móvil) y **1024 px** (tableta). No inventes un tercero.
- Agrupa con `flex`/`grid` y `gap`, no con márgenes por elemento.
- Contenido ancho (tablas, código, diagramas) en su propio contenedor con `overflow-x: auto`.

```css
.page { max-width: var(--page-max); margin-inline: auto; padding: 40px 24px 96px; }
@media (max-width: 767px) { .page { padding: 28px 16px 56px; } }
```

### Lienzo de página

```css
body { margin: 0; background: var(--canvas); color: var(--ink); }
body::before {
  content: ""; position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background:
    radial-gradient(60rem 40rem at 12% -8%, var(--glow-1), transparent 62%),
    radial-gradient(52rem 36rem at 92% 4%, var(--glow-2), transparent 60%),
    radial-gradient(46rem 34rem at 50% 108%, var(--glow-3), transparent 64%);
}
```

`body` **siempre** pinta su fondo desde un token. Un `body` transparente hereda el fondo del
contenedor y rompe el tema.

---

## 7. Gráficas

- **Un solo tono de dato por gráfica** (`--data`) con etiqueta directa. La paleta categórica de
  Skandia es de croma bajo a propósito y sus pares vecinos no pasan la separación para daltonismo:
  si necesitas varias series, sepáralas en pequeños múltiplos antes que en colores.
- **Una sola escala** compartida cuando compares escenarios; así se leen de un vistazo.
- **Cortes redondos** en el eje: 0, 250, 500… Un eje con 288 y 863 no se lee.
- **Marca el objetivo** con una línea discontinua rotulada. Un número sin referencia no dice si
  está bien.
- Rejilla en `--grid`, texto de eje en `--ink-muted`. El texto nunca toma el color de la serie.
- Deja sitio en el `viewBox` para las etiquetas exteriores y dale `fill` explícito a cada forma.

---

## 8. Accesibilidad y temas

- Tres estados de tema: `data-theme="dark"`, `data-theme="light"` y **ninguno** (el del sistema).
  Los tres bloques de la sección 2 cubren los tres casos.
- Foco visible siempre: `outline: 2px solid var(--accent); outline-offset: 2px`.
- El estado nunca se comunica solo con color: pastilla con punto **y** texto.
- `@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }`
- Transiciones de 120 ms. Nada más lento se siente como retraso.

---

## 9. Qué no hacer

- Verde de marca como color de texto.
- Degradado en un botón, en un fondo de página o en una tarjeta.
- Un gris nuevo «parecido» a uno que ya existe.
- Sombra en todas las tarjetas: aplana la jerarquía en vez de crearla.
- Un radio distinto por componente. Son cinco, y cada uno tiene su rol.
- Emoji como marcador de sección.
- Números en columna sin `tabular-nums`.
- Un color definido únicamente dentro de un bloque de tema oscuro.
- Texto de lectura a todo el ancho de la pantalla.

---

## 10. Si la marca es otra

Cambia solo esto y el resto del sistema se sostiene:

1. `--accent` y su par legible `--accent-ink` (mide el contraste: el de texto necesita 4,5:1).
2. `--accent-tint`, que es el acento a ~10 % sobre superficie.
3. Las dos familias tipográficas, manteniendo la regla de las dos voces.
4. `--data`, si la marca tiene un azul de dato propio.

Los grises, los estados, los radios y la escala de espaciado sirven igual para cualquier marca.
