# Demo de cotización desde la oportunidad · CILI-10

**Subtarea:** #971 · [R2][CILI-10] Cargar productos de ejemplo y demostrar la cotización en Odoo (C07 #812)
**Fecha:** 29-oct-2026 · Para la revisión con CMR del 30-oct
**Archivo:** `productos_demo_cmr.xlsx`
**Entorno recomendado:** `cmr-test`, para no dejar productos de prueba en producción.

Probado en Odoo 20 local: la importación liga las columnas sola, crea la unidad "Lote" y los 33 productos, y la cotización se genera desde la oportunidad con secciones, notas, línea negativa de inventario y flete.

---

## 1. Qué contiene el archivo

**Hoja `1_Unidad_Lote`**: crea la unidad **Lote**. Odoo 20 ya trae m², metro lineal (m) y pieza (Unidades), pero no lote.

**Hoja `2_Productos`**: 33 productos tomados de las plantillas FT-CTZ-01 de Molde completo, Adaptación, Listado y Accesorios.

| Grupo | Unidad | Ejemplos | Precio demo (USD) |
|---|---|---|---|
| Equipo de aluminio | m² | Muros, unión muro-losa, losa y caps, caps y EQL, culatas, punto fijo, tapa de escalera, escalera, pretil, base de tinaco, reborde de fachada | 270 |
| Equipo reutilizado (crédito) | m² | Equipo adaptado de inventario existente | 270 (cantidad negativa) |
| Listado de piezas | m² | Fabricación de piezas compatibles | 240 |
| Perímetro | m | Ángulo de arrastre, andamiaje básico y completo, seguridad para colado, cuchilla | 25 – 360 |
| Juegos | Lote | Alineación, alineación horizontal, escuadras, piezas para pretil | 1,800 – 10,304 |
| Accesorios | Unidades | Pin, cuña, corbatas, puntal, cercha, plataforma, ménsula | 0.56 – 279.19 |
| Servicios | Lote | Mantenimiento, recolección, flete | Flete en 0, se captura en cada cotización |

- Todos llevan **"[DEMO]"** en el nombre y **"DEMO-"** en la referencia interna.
- Los precios salen de las plantillas y **solo sirven para la demo**; no son tarifas.
- El catálogo definitivo lo entrega CMR (CMR-01).

---

## 2. Pasos

### 2.1 Habilitar unidades de medida

*Ventas → Configuración → Ajustes → Productos* → activar **Unidades de medida** → Guardar.

### 2.2 Importar la unidad "Lote" (hoja 1)

1. *Ventas → Configuración → Unidades de medida → ⚙ → Importar registros*.
2. Subir `productos_demo_cmr.xlsx` y elegir la hoja **1_Unidad_Lote**.
3. **Probar** → **Importar**.

### 2.3 Importar los productos (hoja 2)

1. *Ventas → Productos → Productos → ⚙ → Importar registros*.
2. Subir el mismo archivo y elegir la hoja **2_Productos**.
3. **Probar** → **Importar**. Deben quedar 33 productos.

La hoja 1 va primero porque los productos por lote buscan esa unidad.

### 2.4 Crear la cotización desde la oportunidad

1. Abrir una oportunidad y pulsar **Nueva cotización**. Queda ligada sola y el botón *Cotizaciones* de la oportunidad sube a 1.
2. Armar las líneas como en la plantilla de Molde completo:

| Tipo de línea | Contenido |
|---|---|
| Sección | Cimbra planta baja al último nivel |
| Productos | Muros · Unión muro-losa · Losa y caps · Ángulo de arrastre |
| Nota | Incluye accesorios básicos de sujeción: pasadores, cuñas, corbatas, puntales para vaciado, tensores de vano y escalera para armado |
| Sección | Punto fijo |
| Productos | Losa y caps · Muros y antepechos de punto fijo · Losa tapa de escalera |
| Sección | Equipo reutilizado |
| Producto | Equipo adaptado de inventario existente, con **cantidad negativa** (ej. −93.9 m²) |
| Sección | Complementarios |
| Productos | Andamiaje básico · Seguridad para colado · Alineación horizontal |
| Producto | Flete: cantidad 1, importe en precio unitario |

3. En *Otra información*: **fecha de vencimiento** (vigencia), **términos de pago** y, en *Términos y condiciones*, las condiciones generales de la plantilla.
4. Previsualizar o imprimir el PDF.

### 2.5 Mostrar opciones

Duplicar la cotización (⚙ → Duplicar) y cambiar cantidades. Así se ve cómo una oportunidad puede tener varias alternativas, como las hojas 100-1, 100-2 y 100-3 de las plantillas.

### 2.6 Limpiar después

En *Productos*, buscar **DEMO-** en la referencia, seleccionar todo y archivar.

---

## 3. Diferencias contra las plantillas de Excel

Anotarlas en #971 y llevarlas a la revisión con CMR.

| Tema | En la plantilla | En la demo | Se resuelve en |
|---|---|---|---|
| Programa y % aumentado | Cantidad = programa × (1 + %) | Se captura la cantidad final | CMR-05 · CILI-06/07 |
| Moneda | USD | Moneda de la compañía; si es MXN, sale en pesos | Multimoneda y lista de precios USD · CILI-07 |
| Totales por bloque | Subtotal, Total MT2 y Total ML por sección | El PDF estándar no los suma igual | Personalizar reporte · CILI-07 |
| Descuento especial 8% | Se calcula pero no se aplica al total | No incluido | Confirmar con CMR |
| Importe con letra, firma de aprobación, memoria gráfica | En el formato | No vienen en el PDF estándar | Personalizar reporte |
| Opción contra revisión | Una hoja por opción/revisión | Duplicar crea alternativas, sin control de versiones | CILI-07 · CILI-08 |
| Precios | Por proyecto | Precios demo de las plantillas | Catálogo CMR-01 |

---

## 4. Siguiente paso sugerido

Crear **plantillas de cotización de Odoo**, una por tipo (Molde completo, Adaptación, Listado, Accesorios), con sus secciones, notas y condiciones precargadas, para que la demo se parezca más a los formatos de CMR. Es la base de CILI-07.
