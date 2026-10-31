# Ficha técnica · Módulo `cmr_sale`

**CMR - Ventas**

| Dato | Valor |
|---|---|
| Nombre técnico | `cmr_sale` |
| Versión | 20.0.1.0.0 |
| Odoo compatible | 20.0 (Community y Enterprise) |
| Dependencias | `sale_crm`, `sale_management`, `cmr_crm` |
| Licencia | LGPL-3 · Autor: Cili |
| Estado | Probado en Odoo 20 local (15/15). Pendiente: `cmr-test` y producción |
| Plan de trabajo | Fase 4, punto 10 (numeración por opción) · CILI-07 (#968) |

Es el módulo de Ventas de CMR. Esta primera versión trae el número de cotización. Las versiones siguientes agregarán el formato PDF FT-CTZ-01 y los hitos de pago.

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
- **Revisión de una opción enviada:** por ahora se hace como opción nueva (pregunta 17 a CMR).
- **Nombre escrito a mano** al crear la cotización: se respeta.
- Los números no tienen huecos (secuencia `no_gap`) y se bloquea la oportunidad al asignar, para que dos cotizaciones simultáneas no tomen el mismo número.

## 2. Ajuste para CMR

*Ventas → Configuración → Ajustes → Cotizaciones y órdenes → **Número de cotización CMR** → Siguiente número de proyecto.*

Es el número que tomará el próximo proyecto del año en curso. Al instalar arranca en 1, así que **hay que poner el que les toca** (pregunta 26 a CMR). El 1 de enero vuelve a 1 solo.

## 3. Dónde se ve

- **Oportunidad:** pestaña Especificaciones Técnicas → "Nº de proyecto" y "Año del proyecto", visibles después de la primera cotización.
- **Cotización:** el nombre (`283- 12-26`) y, en *Otra información*, "Nº de proyecto" y "Opción".

## 4. Instalación

**Primero en `cmr-test`:**

```bash
cd /opt/odoo-cmr-test
unzip -q cmr_sale.zip -d addons/ && chmod -R 755 addons
./scripts/modulo.sh instalar cmr_sale
```

**Después en producción** (con respaldo previo):

```bash
/opt/respaldos-cmr/respaldo.sh
cd /opt/odoo-cmr
unzip -q /ruta/cmr_sale.zip -d addons/ && chmod -R 755 addons
docker compose exec odoo odoo -d cmr_db -i cmr_sale --stop-after-init --no-http
docker compose restart odoo
```

Luego hay que ir al **ajuste del punto 2** y poner el siguiente número de proyecto.

Las cotizaciones que ya existían conservan su número anterior (por ejemplo, S00001). Si una oportunidad ya tenía cotizaciones, la siguiente que se haga empieza en la opción 01.

## 5. Pruebas (local 15/15)

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

## 6. Pendientes de CMR

- **Pregunta 25:** año del sufijo cuando una opción se hace en un año distinto al del proyecto. Hoy se usa el año del proyecto.
- **Pregunta 26:** siguiente número de proyecto para 2026.
- **Pregunta 17:** revisión contra opción nueva.

## 7. Historial

| Versión | Fecha | Cambios |
|---|---|---|
| 20.0.1.0.0 | 30-oct-2026 | Número de cotización proyecto-opción-año con ajuste del siguiente número de proyecto |
