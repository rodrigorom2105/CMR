# Paso 5 · Importar catálogo, precios y plantillas de CMR

**Plan de trabajo:** Fase 3, paso 5 · CILI-07 (#968)
**Fuente:** archivos enviados por CMR el 29-oct-2026 (atributos, catálogo, plantillas)
**Requisito:** paso 4 terminado (variantes, listas de precios, unidades de medida, unidad Lote, 5 categorías, USD con tasa y listas "Cliente nuevo" y "Cliente existente" en USD).

Probado en Odoo 20 local, en una copia configurada como producción. La cadena completa da 11 atributos, 57 productos con 95 variantes, 135 precios y reglas, y 5 plantillas. Una cotización creada desde la oportunidad sale con la plantilla y los precios en USD del catálogo.

---

## Archivos

| Archivo | Qué es | Cambios respecto al de CMR |
|---|---|---|
| `1_ATRIBUTOS_CMR.xlsx` | 11 atributos con sus valores | Sin la coma en "Esqueletos (ángulos) – juego de 2". Cuña en ángulo: "Para andamiaje CMR tipo Forsa" (provisional, pregunta 14) |
| `2_CATALOGO_CMR.xlsx` | 57 productos | Solo la hoja de importación. Categorías sin "Todos /". Sin la columna `uom_po_id`, que no existe en Odoo 20 |
| `3_precios_extra_y_listas.py` | Script de precios | Nuevo: carga los precios en USD a las listas (ver 5.3) |
| `4_PLANTILLAS_CMR.xlsx` | 5 plantillas de cotización | Solo la hoja de importación, sin cambios |

---

## Antes de empezar

- **Tu usuario debe estar en español** (Preferencias → Idioma). Odoo busca "Unidades" y "Servicios" con el nombre en el idioma de quien importa.
- **Respaldo manual:** `/opt/respaldos-cmr/respaldo.sh` (debe terminar en "Listo").
- Importa **en este orden**. Cada archivo usa lo que creó el anterior.

---

## 5.1 Atributos

1. *Ventas → Productos → Atributos → ⚙ → Importar registros*.
2. Sube `1_ATRIBUTOS_CMR.xlsx`.
3. Revisa que las 4 columnas aparezcan ligadas → **Probar** → **Importar**.
4. **Esperado:** 11 atributos (Vida útil, Andamiaje, Medida, etc.).

## 5.2 Catálogo

1. *Ventas → Productos → Productos → ⚙ → Importar registros*.
2. Sube `2_CATALOGO_CMR.xlsx`. Las 11 columnas deben aparecer ligadas.
3. **Probar** → **Importar**.
4. **Esperado:** 57 productos y 95 variantes. Por ejemplo, "Equipo para muros (paneles estándar)" tiene las variantes 500 usos y 1000 usos.

## 5.3 Precios en USD (script)

**Por qué hace falta:** la compañía está en MXN y Odoo guarda el "precio de venta" del producto en esa moneda. Si se dejara así, la cuña de USD 1.32 se cotizaría como 1.32 **pesos** convertidos a dólares (USD 0.07). En Odoo, los precios en otra moneda van en la lista de precios. El script hace tres cosas:

1. Pone el **precio extra** de cada variante (hoja "Precio extra variantes" de CMR), como referencia.
2. En **Cliente nuevo**, carga un precio fijo en USD por cada una de las 95 variantes: precio del catálogo más el precio extra.
3. En **Cliente existente**, crea una regla general que toma los precios de "Cliente nuevo", más las 4 reglas de CMR (cuña y pasador importados a 0.73 y 1.12).

**Cómo correrlo** en el servidor:

```bash
cd /opt/odoo-cmr
# subir el script a esta carpeta, luego:
docker compose exec -T odoo odoo shell -d cmr_db --no-http < 3_precios_extra_y_listas.py 2>&1 | tail -20
```

**Esperado** al final:
```
== Cambios: 135 | Errores: 0
== Guardado.
```

- Si aparece algún `ERROR`, **no guarda nada**. Mándame la salida.
- Se puede correr varias veces: la segunda vez debe decir `Cambios: 0`.
- Para ver lo que haría sin guardar, cambia `APLICAR = True` por `APLICAR = False` al inicio del script.

## 5.4 Plantillas de cotización

1. *Ventas → Configuración → Plantillas de cotización → ⚙ → Importar registros*.
2. Sube `4_PLANTILLAS_CMR.xlsx`.
3. **Probar**. Van a salir unos 87 **avisos** del tipo "Se encontraron varias coincidencias". Es normal: el producto tiene variantes y Odoo toma la primera (500 usos, andamiaje básico, importado 5.4 cm). No son errores.
4. **Importar**. **Esperado:** 5 plantillas "CMR – …".

---

## Paso 6 · Ligar cada tipo de cotización con su plantilla

*CRM → Configuración → Especificaciones técnicas → Tipos de cotización*. En la columna **Plantilla de cotización**:

| Tipo de cotización | Plantilla |
|---|---|
| Molde por niveles | CMR – Molde por niveles (PB, 1er, 2do y último nivel) |
| Molde vivienda PB + planta alta | CMR – Molde vivienda PB + planta alta |
| Adaptación / repotenciación | CMR – Adaptación / repotenciación de molde |
| Fabricación por listado / reparación | CMR – Fabricación de piezas por listado / reparación |
| Venta de accesorios | CMR – Venta de accesorios |

---

## Comprobación

1. Abre una oportunidad, ponle tipo **Molde por niveles** y pulsa **Nueva cotización**.
   - Debe abrir con la plantilla cargada (23 secciones), lista **Cliente nuevo** y moneda **USD**.
   - "Equipo para muros (paneles estándar) (500 usos)" debe salir en **USD 220**. Al cambiar la variante a 1000 usos, debe salir en **USD 270**.
2. Con un cliente que tenga la lista **Cliente existente**, la cuña importada 5.4 cm debe salir en **USD 0.73**; con "Cliente nuevo", en **USD 1.32**.

---

## Para saber

- **El "Precio de venta" en la ficha del producto aparece en MXN** (por ejemplo, $220.00). Es solo la referencia del catálogo. **El precio real en USD lo da la lista de precios.** Conviene explicárselo a CMR.
- **Si CMR cambia un precio:** se actualiza el precio de venta o el precio extra del producto y se vuelve a correr el script. También se puede editar la regla directamente en la lista "Cliente nuevo".
- **Producto nuevo:** después de importarlo o crearlo, hay que volver a correr el script. Si no, su precio en USD sale mal, convertido desde pesos.
- **Clientes existentes:** todos los clientes usan "Cliente nuevo" por defecto. A los que ya compraron molde hay que asignarles "Cliente existente" en su contacto (*Ventas y compras → Lista de precios*). CMR debe indicar cuáles son.
- **Cuña en ángulo:** si CMR confirma "Para andamiaje CMR 5.4", se renombra el valor en *Atributos → Tipo de cuña en ángulo*. No afecta productos, precios ni cotizaciones.
- **Precios por confirmar en el catálogo de CMR:** varios servicios en 0 (mantenimiento, adaptación, limpieza), flete sin precio y alineadores de caps en 0. Se capturan en cada cotización hasta que CMR los defina.
