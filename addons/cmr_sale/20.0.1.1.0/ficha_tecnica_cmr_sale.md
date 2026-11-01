# Ficha técnica · Módulo `cmr_sale`

**CMR - Ventas**

| Dato | Valor |
|---|---|
| Nombre técnico | `cmr_sale` |
| Versión | 20.0.1.1.0 |
| Odoo compatible | 20.0 (Community y Enterprise) |
| Dependencias | `sale_crm`, `sale_management`, `cmr_crm` |
| Licencia | LGPL-3 · Autor: Cili |
| Estado | 20.0.1.0.0 **instalado en producción** (`cmr_db`) el 30-oct-2026. **20.0.1.1.0 (formato FT-CTZ-01) por probar en `cmr-test`**: revisada de forma estática contra el código de Odoo 20 y con vista previa en wkhtmltopdf usando los datos de la CTZ 283-1; sin ejecutar en Odoo todavía |
| Plan de trabajo | Fase 4 (numeración) y Fase 6, pasos 13 a 16 (formato, memoria gráfica, hitos y plazos) · CILI-07 (#968) |

Es el módulo de Ventas de CMR: el número de cotización y el formato PDF **FT-CTZ-01**, el código del formato de cotización de CMR (título de sus Excel). Las versiones siguientes agregarán la facturación por hito de pago.

---

## 1. Número de cotización `283- 12-26`

| Parte | Significado | Regla |
|---|---|---|
| `283` | Proyecto = oportunidad del CRM | Contador anual de 3 dígitos que vuelve a 001 el 1 de enero. Se asigna con la **primera cotización** de la oportunidad y queda guardado en ella |
| `12` | Opción de cotización del proyecto | 01, 02, 03… Cada cotización nueva o duplicada de la oportunidad toma la siguiente. Las canceladas cuentan |
| `26` | Año | Año del proyecto: una opción hecha en enero de 2027 para un proyecto de 2026 sigue terminando en `-26` |

- El espacio después del primer guion es parte del formato de CMR.
- **Cotización sin oportunidad** (por ejemplo, venta de accesorios): toma un número de proyecto propio y opción 01.
- **Al confirmarse** como pedido conserva el mismo número.
- **Opción contra revisión:** en la reunión 3 CMR confirmó que son distintas. Corregir una opción enviada se hace por ahora como opción nueva (pregunta 17).
- **Nombre escrito a mano** al crear la cotización: se respeta.
- Los números no tienen huecos (secuencia `no_gap`) y se bloquea la oportunidad al asignar, para que dos cotizaciones simultáneas no tomen el mismo número.

**Ajuste:** *Ventas → Configuración → Ajustes → Cotizaciones y órdenes → Número de cotización CMR → Siguiente número de proyecto.* Hay que poner el que les toca (pregunta 26; Mónica mencionó la 290).

---

## 2. Formato PDF FT-CTZ-01 (1.1.0)

El botón **Imprimir** y el correo de la cotización usan el formato de CMR (hoja carta). La factura proforma conserva el formato estándar de Odoo.

### 2.1 Partes del PDF

| Parte del Excel de CMR | En Odoo |
|---|---|
| Encabezado en **cada página**: logo CMR, "COTIZACIÓN FT-CTZ-01", logo del cliente | Logo de la compañía. El logo del cliente es la imagen de su contacto (si no tiene, la celda queda vacía) |
| Fecha y Nº CTZ (rojo) | Fecha de la cotización y número `283- 01-26` |
| Producto cotizado, Referencia | Pestaña **Formato CMR** de la cotización |
| País / ciudad | Se llena con el país y la ciudad de la obra de la oportunidad; se puede cambiar |
| Cliente | Empresa del cliente |
| Contacto y correo/teléfono | Se llenan con el contacto y el correo (o teléfono) de la oportunidad; se pueden cambiar |
| Bloques "VALOR TOTAL EQUIPO ALUMINIO – PLANTA BAJA" | **Sección** de la cotización: renglón TOTAL MT2 / VALOR TOTAL … / SUBTOTAL |
| Tablas "COTIZACIÓN CIMBRA PARA …" | **Subsección**: título gris, columnas CANT. · UND MEDIDA · CONCEPTO · PRECIO/UNIT · PRECIO, y TOTAL MT2, TOTAL ML y SUBTOTAL |
| "VALOR TOTAL EQUIPO ALUMINIO" de todas las plantas (rojo) | Automático cuando hay **dos o más secciones con el mismo nombre base** ("Equipo de aluminio – Planta baja", "Equipo de aluminio – Primer nivel"…) |
| Complementarios, Logística, Accesorios | Sección sin subsecciones: título, líneas y VALOR TOTAL |
| "INCLUYE ACCESORIOS BÁSICOS DE SUJECIÓN…" | Nota de línea |
| Crédito con m² negativos | Línea normal con cantidad negativa; resta del total de su bloque |
| Memoria gráfica | Imágenes con leyenda (pestaña Formato CMR), dos por renglón. Solo sale si hay imágenes |
| Importe con letra ("…CON 63/100 DÓLARES AMERICANOS") | Automático a partir del total (USD: DÓLARES AMERICANOS; MXN: PESOS MEXICANOS M.N.) |
| SUB TOTAL, DESCUENTO ESPECIAL, SUB TOTAL 1, FLETE, SUB TOTAL 2, IVA, TOTAL USD | Ver 2.2 |
| TOTAL MXN | Opcional (casilla *Mostrar total en MXN*), con el tipo de cambio de la fecha de la cotización |
| Observaciones, Vigencia, Garantía | Pestaña Formato CMR. La vigencia se calcula en días con la fecha de vencimiento |
| Forma de pago (60 % anticipo, 30 % contra BL… con monto) | Tabla de **hitos** (2.3) |
| Tiempo de entrega | Tabla de **plazos** con su descripción o condición |
| Tiempo de tránsito, Incoterms | Campo de texto; Incoterm nativo + lugar ("DDP" + "PUESTO EN OBRA") |
| Firma de aprobación del cliente | Recuadro junto a las condiciones comerciales, con NOMBRE |
| Condiciones generales | **Términos y condiciones** de la cotización; cada párrafo sale en su renglón |
| Firma final | Vendedor de la cotización y razón social de la compañía |

Colores del Excel de CMR: etiquetas y encabezados de columna `#EBF1DE`, títulos de bloque `#F2F2F2`, Nº CTZ, hitos y gran total en rojo; Arial. Se ajustan con el manual de identidad (#990).

### 2.2 Totales, flete y descuento

- **Flete:** las líneas cuyo producto tiene marcada la casilla **Flete en la cotización CMR** (ficha del producto, pestaña Ventas) no salen dentro de su sección; se suman en el renglón FLETE. El script de plantillas la marca en el producto "Flete". Otros fletes, como el "Flete de recolección y entrega en obra" de Logística, siguen como línea normal de su sección, como en la CTZ 232.
- **Descuento especial:** el descuento global de Odoo (botón *Descuento* de la cotización) se muestra como "DESCUENTO ESPECIAL DE x %" y SUB TOTAL 1. Si no hay descuento, esos renglones no salen.
- **IVA:** el de los impuestos de las líneas (0 % en exportación, #993).
- SUB TOTAL 2 = base antes de impuestos de Odoo; TOTAL = total de la cotización.

### 2.3 Hitos de pago y plazos de entrega

- **Hitos** (`cmr.sale.hito`): %, hito (anticipo, contra BL, contra arribo a puerto, contra entrega en fábrica, contra entrega en obra, contra validación, finiquito, al contado, leasing, otro), detalle opcional ("por planta") y monto calculado sobre el total.
- Los hitos normales deben sumar **100 %**; si no, Odoo no deja guardar. Las formas de pago completas ("100 % leasing", "al contado") se marcan como **Alternativa** y no se suman.
- **Plazos** (`cmr.sale.entrega`): plazo ("90 a 120 días") y descripción o condición ("entrega de 1 dúplex", "una vez recibido el anticipo y firmado el Shell Plan").
- Hitos, plazos y memoria gráfica se copian al duplicar la cotización (opción nueva).
- La **facturación por hito** queda para una versión posterior (paso 17).

### 2.4 Plantillas de cotización

Para que salgan los dos niveles de totales, las plantillas se reestructuran con `scripts/reestructurar_plantillas_cmr.py` (sección 4.3):

| Plantilla | Resultado |
|---|---|
| Molde por niveles | 4 secciones "Equipo de aluminio – <planta>" (molde, punto fijo, escalera, muro de patio, pretil y tinaquera como subsecciones) + 4 "Complementarios – <planta>" (andamiaje y alineación) + Flete y servicios |
| Molde vivienda PB + planta alta | "Equipo de aluminio – Planta baja" y "– Planta alta" (pretil, escalera y reborde van en planta alta) + Complementarios + Flete y servicios |
| Adaptación / repotenciación | Igual, con "Equipo existente" (crédito) como subsección de su planta + Complementarios, Logística y Servicios |
| Fabricación por listado | Sin cambios (secciones simples) |
| Venta de accesorios | Sin cambios (secciones simples) |

Probado con las 5 plantillas del archivo `PLANTILLAS_COTIZACION_ODOO_CMR.xlsx`: conserva todas las líneas (85, 23, 38, 15 y 15).

---

## 3. Dónde se ve

- **Oportunidad:** pestaña Especificaciones Técnicas → "Nº de proyecto" y "Año del proyecto".
- **Cotización:** nombre (`283- 12-26`); *Otra información* → "Nº de proyecto" y "Opción"; pestaña nueva **Formato CMR** (encabezado, condiciones comerciales, forma de pago, tiempo de entrega y memoria gráfica).
- **Producto:** pestaña Ventas → *Flete en la cotización CMR*.

---

## 4. Instalación / actualización

### 4.1 `cmr-test`

```bash
cd /opt/odoo-cmr-test
mv addons/cmr_sale /root/cmr_sale_respaldo_$(date +%F)
unzip -q cmr_sale.zip -d addons/ && chmod -R 755 addons
grep version addons/cmr_sale/__manifest__.py          # 20.0.1.1.0
./scripts/modulo.sh actualizar cmr_sale
docker compose logs odoo --tail 80 | grep -i "cmr_sale\|error\|traceback"
```

### 4.2 Producción (respaldo previo)

```bash
/opt/respaldos-cmr/respaldo.sh                       # debe terminar en "Listo"
cd /opt/odoo-cmr
mv addons/cmr_sale /root/cmr_sale_v10_$(date +%F)     # fuera de addons
unzip -q /ruta/cmr_sale.zip -d addons/ && chmod -R 755 addons
docker compose exec odoo odoo -d cmr_db -u cmr_sale --stop-after-init --no-http 2>&1 | tee /root/upgrade_cmr_sale.log
grep -i "cmr_sale\|error\|traceback" /root/upgrade_cmr_sale.log
docker compose restart odoo
```

Como en `cmr_crm`, copiar la carpeta y reiniciar no basta: hace falta el `-u`.

### 4.3 Reestructurar las plantillas (después de actualizar)

```bash
cd /opt/odoo-cmr                                     # o /opt/odoo-cmr-test con -d cmr_test
cp addons/cmr_sale/scripts/reestructurar_plantillas_cmr.py .
# Primero en revisión: cambiar APLICAR = True por APLICAR = False al inicio del archivo
docker compose exec -T odoo odoo shell -d cmr_db --no-http < reestructurar_plantillas_cmr.py 2>&1 | tail -80
# Si la salida es la esperada, regresar APLICAR = True y correrlo otra vez
```

- Muestra por plantilla las secciones nuevas y los títulos que pasan a subsección.
- Termina en `== Cambios: N | Errores: 0` y `== Guardado.`; si hay un `ERROR`, no guarda nada.
- La segunda corrida dice "ya tiene subsecciones; sin cambios".
- Solo cambia las plantillas: las cotizaciones ya creadas se quedan como están.

---

## 5. Pruebas

### 5.1 Numeración (1.0.0, local 15/15)

| # | Prueba | Esperado |
|---|---|---|
| 1-2 | Ajuste "Siguiente número de proyecto" en 284 | Se guarda y se muestra |
| 3-4 | Dos cotizaciones desde una oportunidad | `284- 01-26`, `284- 02-26`; la oportunidad guarda proyecto 284-26 |
| 5 | Duplicar una cotización | `284- 03-26`, ligada a la misma oportunidad |
| 6 | Cotización de otra oportunidad | `285- 01-26` |
| 7 | Cotización sin oportunidad | `286- 01-26` |
| 8 | Ajuste después de usarse | Muestra 287 |
| 9 | Confirmar como pedido | Conserva `284- 02-26` |
| 10 | Nueva opción con una cancelada | `284- 04-26` |
| 11 | Proyecto nuevo en enero de 2027 | `001- 01-27` |
| 12 | Opción nueva de un proyecto de 2026, en enero de 2027 | `284- 05-26` |
| 13 | Nombre escrito a mano | Se respeta |
| 14-15 | Campos en oportunidad y ajuste en Ventas | Visibles |

### 5.2 Formato FT-CTZ-01 (1.1.0, por hacer en `cmr-test`)

| # | Prueba | Esperado | cmr-test |
|---|---|---|---|
| 16 | Actualizar a 1.1.0 | Sin errores; pestaña Formato CMR en la cotización | ☐ |
| 17 | Script de plantillas en revisión y luego aplicado | Salida como la tabla 2.4; segunda corrida sin cambios | ☐ |
| 18 | Nueva cotización desde una oportunidad tipo Molde por niveles | Plantilla con secciones por planta y subsecciones; País/ciudad y contacto llenos desde la oportunidad | ☐ |
| 19 | Imprimir | Encabezado de CMR en cada página; subsecciones con TOTAL MT2, TOTAL ML y SUBTOTAL; VALOR TOTAL por planta y VALOR TOTAL EQUIPO DE ALUMINIO en rojo | ☐ |
| 20 | Línea de Flete con precio | No sale en su sección; sale en FLETE y SUB TOTAL 2 | ☐ |
| 21 | Botón Descuento 8 % | DESCUENTO ESPECIAL DE 8 % y SUB TOTAL 1; el total coincide con Odoo | ☐ |
| 22 | Hitos 60 % + 30 % + 10 % + 100 % leasing (alternativa) | Se guarda; montos sobre el total; 60 % + 30 % solos no deja guardar | ☐ |
| 23 | Plazos y memoria gráfica (3 imágenes con leyenda) | Salen en el PDF; la tercera imagen ocupa todo el renglón | ☐ |
| 24 | Términos y condiciones con 5 párrafos | Cada párrafo en su renglón de CONDICIONES GENERALES | ☐ |
| 25 | Importe con letra de USD 347,964.63 | "TRESCIENTOS CUARENTA Y SIETE MIL NOVECIENTOS SESENTA Y CUATRO CON 63/100 DÓLARES AMERICANOS" | ☐ |
| 26 | Total MXN marcado | Renglón TOTAL MXN con el tipo de cambio de la fecha | ☐ |
| 27 | Duplicar la cotización | Opción nueva con hitos, plazos y memoria gráfica copiados | ☐ |
| 28 | Cotización de accesorios sin memoria ni descuento | No salen esos bloques; sí FLETE si tiene | ☐ |
| 29 | Enviar por correo | El adjunto usa el formato FT-CTZ-01 | ☐ |

---

## 6. Pendientes de CMR

- **Pregunta 16:** regla de la columna "Programa / % aumentado"; hoy no se imprime y la cantidad se captura final.
- **Pregunta 17:** revisión contra opción nueva.
- **Pregunta 19:** si el descuento especial se muestra como renglón (así sale hoy) o solo el total.
- **Pregunta 25:** año del sufijo cuando una opción se hace en un año distinto al del proyecto.
- **Pregunta 26:** siguiente número de proyecto para 2026.
- **Pregunta 28:** cuántas imágenes lleva la memoria gráfica y si cambian por opción.
- **Pregunta 29:** logo del cliente (hoy sale si su contacto tiene imagen).
- **Manual de identidad (#990):** colores y tipografía definitivos.

## 7. Consideraciones

- El encabezado del PDF tiene altura fija (78 mm de margen superior). Una referencia muy larga (más de 4 renglones) puede encimarse con el cuerpo; conviene resumirla.
- El formato reemplaza al estándar de Odoo para **todas** las cotizaciones de la base.
- Desinstalar el módulo borra hitos, plazos y memoria gráfica. Respaldar antes.

## 8. Historial

| Versión | Fecha | Cambios |
|---|---|---|
| 20.0.1.0.0 | 30-oct-2026 | Número de cotización proyecto-opción-año con ajuste del siguiente número de proyecto |
| 20.0.1.1.0 | 31-oct-2026 | Formato PDF FT-CTZ-01: encabezado de CMR en cada página, secciones y subsecciones con TOTAL MT2/ML y subtotales, gran total por nombre de bloque, memoria gráfica, importe con letra, flete y descuento en totales, total MXN opcional, condiciones comerciales con hitos de pago (con alternativas) y plazos de entrega, condiciones generales por párrafo y firmas. Script para reestructurar las 5 plantillas por planta |
