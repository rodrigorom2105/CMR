# Ficha técnica · Módulo `cmr_crm`

**CMR - CRM Pipeline Comercial**

| Dato | Valor |
|---|---|
| Nombre técnico | `cmr_crm` |
| Versión | 20.0.2.1.0 |
| Odoo compatible | 20.0 (Community y Enterprise) |
| Categoría | Sales/CRM |
| Dependencias | `crm`, `sale_crm`, `sale_management` |
| Licencia | LGPL-3 |
| Autor | Cili |
| Tipo | Extensión (no aparece como aplicación principal) |
| Estado | 20.0.2.1.0 **instalada en producción** (base `cmr_db`) el 29-oct-2026, actualizada desde 1.0.0 sin errores. Probada antes en Odoo 20 local y en `cmr-test` |
| Acciones de la minuta | CILI-01 (ESP-TEC en la oportunidad) y CILI-02 (etapas y validaciones de avance). Ambas dependen de CMR-04 |

---

## 1. Propósito

Adapta el CRM de Odoo al proceso comercial de CMR (moldes y cimbras de aluminio):

- Pipeline con las 7 etapas comerciales de CMR.
- Pestaña **Especificaciones Técnicas** con todas las secciones del formato **ESP-TEC** (`ET-COT-01-1-24`, hoja *Formato unico*), consultable en todo el flujo.
- **Documentos y planos con estado:** Faltante, Recibido · revisión pendiente, Revisado o No aplica.
- **Requisitos de avance configurables** por etapa y por tipo de cotización, sin tocar código (reemplaza el gate fijo de 4 planos).
- **Tipos de cotización = las 5 plantillas de CMR**: cada tipo puede ligarse a su plantilla, que se carga al crear la cotización desde la oportunidad.
- Plan de actividades opcional al entrar a cada etapa (responsables y plazos).
- m² ponderados por probabilidad y motivos de pérdida estandarizados.

---

## 2. Estructura de archivos

```
cmr_crm/
├── __manifest__.py
├── models/
│   ├── cmr_catalogos.py        # Tipos de cotización (con plantilla), de producto y de documento
│   ├── cmr_requisito.py        # Requisitos por etapa y su evaluación
│   ├── crm_lead.py             # Campos ESP-TEC, validación de avance, etiqueta, plan, contexto de cotización
│   ├── crm_lead_documento.py   # Documentos de la oportunidad
│   └── crm_stage.py            # Requisitos y plan de actividades por etapa
├── data/                       # Etapas, etiqueta, motivos, catálogos y requisitos (noupdate)
├── security/ir.access.csv      # Formato de permisos de Odoo 20 (ir.access)
├── views/                      # Pestaña, búsqueda, etapa y menús de configuración
└── migrations/
    ├── 20.0.2.0.0/post-migrate.py   # Desde 1.0.0: casillas → documentos, tipos, etiqueta
    └── 20.0.2.1.0/post-migrate.py   # Desde 2.0.0: tipos alineados a las plantillas de CMR
```

**Nota Odoo 20:** los permisos van en `ir.access.csv` (`model_id` = nombre del modelo, `operation` = subconjunto de `crud`). `ir.model.access` ya no existe.

---

## 3. Modelos nuevos

| Modelo | Uso | Permisos |
|---|---|---|
| `cmr.tipo.cotizacion` | Los 5 tipos de cotización de CMR. Define qué secciones del ESP-TEC se muestran y qué plantilla de cotización se carga | Vendedor: leer · Gerente: todo |
| `cmr.tipo.producto` | Basic Forms 5.4, Robust Forms 8.0, Malasia 6.4, Alum PVC (por revisar con CMR, ver sección 10) | Vendedor: leer · Gerente: todo |
| `cmr.tipo.documento` | Catálogo de planos/documentos que se agregan a cada oportunidad | Vendedor: leer · Gerente: todo |
| `cmr.requisito.etapa` | Qué documento o dato se exige desde qué etapa y para qué tipos | Vendedor: leer · Gerente: todo |
| `crm.lead.documento` | Documentos de cada oportunidad, con estado, enlace, versión y revisión | Vendedor: todo |

Configuración: **CRM → Configuración → Especificaciones técnicas** (Requisitos por etapa, Tipos de cotización, Documentos y planos, Tipos de producto).

---

## 4. Mapeo ESP-TEC → Odoo

**Reutilizados (nativos):** Asesor comercial = `user_id`; Cliente = `partner_id`/`partner_name`; Nombre del contacto = `contact_name`; Cargo = `function`; Correo = `email_from`; Teléfono = `phone`; Dirección/Ciudad/País = `street`/`city`/`country_id`.

| Filas | Sección | Campos `crm.lead` |
|---|---|---|
| 1-4 | Encabezado | `cmr_esptec_fecha`, `cmr_num_cotizacion`, `cmr_esptec_formato` (ET-COT-01-1-24), `cmr_esptec_enlace` (Excel en SharePoint) |
| 11 | Término de negociación | `cmr_termino_negociacion` (DDP / EXWORK) |
| 13-15 | Datos del proyecto | `cmr_tipo_cotizacion_id`, `cmr_obra_nombre`, `cmr_obra_ciudad`, `cmr_cant_equipos`, `cmr_cant_adaptaciones`, `cmr_cant_viviendas`, `cmr_tipo_producto_id` |
| 17-19 | Planos | Líneas `cmr_documento_ids`: Planos de plantas, Planta baja, Planta alta, Primer nivel, Piso tipo, Azotea, Cortes y fachadas, Urbanístico (+ Plano estructural) |
| 20 | Datos de planos | `cmr_planos_fecha_act`, `cmr_planos_version`, `cmr_planos_formato` (CAD/PDF/IFC/RVT/BIM), `cmr_clave_bim` (visible solo con BIM) |
| 22-26 | Información técnica (cm) | `cmr_altura_libre`, `cmr_tipo_union`, `cmr_espesor_muro`, `cmr_espesor_losa`, `cmr_enrase_puertas`, `cmr_enrase_ventanas`, `cmr_juegos_losa_puntal`, `cmr_juegos_reapuntalamiento`, `cmr_config_equipo` (210/240/270), `cmr_alto_eql`, `cmr_alto_cap`, `cmr_alineacion_vertical` |
| 27-30 | Sistema de seguridad | `cmr_sistema_seguridad`, `cmr_seguridad_cantidad`, `cmr_mensulas`, `cmr_plataformas`, `cmr_guarda_cuerpo`, `cmr_requiere_puntales`, `cmr_seguridad_vaciado`, `cmr_linea_vida`, `cmr_juegos_adic_reapuntalamiento`, `cmr_alineacion_horizontal` |
| 32-38 | Detalles arquitectónicos | 20 campos (`cmr_muros_texturados` … `cmr_gotero_bordes_losa`) con las listas del formato |
| 40-43 | Punto fijo | `cmr_cotizar_punto_fijo`, `cmr_punto_fijo_alcance`, `cmr_cuarto_maquinas`, `cmr_cotizar_escaleras`, `cmr_tipo_escalera`, `cmr_cant_escaleras`, `cmr_losa_cubre_escaleras`, `cmr_escalera_posicion`, `cmr_proceso_constructivo` |
| 45-47 | Detalles constructivos | `cmr_forma_construccion`, `cmr_juntas_dilatacion`, `cmr_espesor_junta`, `cmr_desnivel_viviendas`, `cmr_altura_desnivel`, `cmr_retroceso_viviendas` |
| A49-A55 | Textos | `cmr_alcance_cotizacion`, `cmr_caracteristicas`, `cmr_secuencia_vaciados`, `cmr_notas_generales` |

- Las listas desplegables reproducen las validaciones de datos del Excel (N/A/SI/NO y listas específicas).
- **Alto EQL** = altura libre − configuración − espesor de losa (N26). **Alto CAP** = altura libre − configuración + espesor de losa (Z26). Calculados y almacenados.
- Se conservan del prototipo: `cmr_alcance_molde` (ahora "Complejidad del molde"), `cmr_m2_cotizados`, `cmr_m2_ponderados`.

---

## 5. Reglas de negocio

### 5.1 Estados de documento

| Estado | Significado | Automático |
|---|---|---|
| Faltante | No se ha recibido | Estado inicial de cada documento |
| Recibido · revisión pendiente | Llegó, falta revisarlo | Fecha de recepción |
| Revisado | Revisado por CMR | Revisado por y fecha de revisión |
| No aplica | El caso se cotiza sin ese documento | — |

Cada cambio de estado queda en el historial (chatter) de la oportunidad. Cada oportunidad nueva recibe los documentos marcados como "Agregar a oportunidades nuevas".

### 5.2 Requisitos de avance (reemplaza el gate de 1.0.0)

- Un requisito exige uno de dos:
  - un **documento**, en estado mínimo Recibido o Revisado, y opcionalmente aceptando "No aplica";
  - un **dato** de la ficha (cualquier campo almacenado de la oportunidad).
- Se exige **al entrar a su etapa y a todas las posteriores** (orden del pipeline), solo para los tipos de cotización indicados (vacío = todos).
- Aplica al arrastrar en kanban, al cambiar etapa en el formulario, al crear en una etapa y al botón **Ganado**. No aplica a Perdido ni a registros tipo lead.
- Mensaje de bloqueo: "*'Oportunidad' no puede pasar a la etapa X. Falta: - Planos de plantas: faltante - Plano de cortes y fachadas: recibido, revisión pendiente …*". Distingue documento faltante de revisión pendiente.
- La pestaña muestra arriba un aviso con lo que falta para la **siguiente** etapa.

**Requisitos iniciales cargados (propuesta, a validar en CMR-04):**

| Desde etapa | Requisito | Tipos |
|---|---|---|
| Volumetría Preliminar | Tipo de cotización capturado | Todos |
| Volumetría Preliminar | Planos de plantas recibido (No aplica no cuenta) | Molde por niveles, Molde vivienda PB + planta alta, Adaptación / repotenciación |
| Volumetría Preliminar | Cortes y fachadas recibido (acepta No aplica) | Los mismos tres |
| Cotización | m² cotizados capturados | Los mismos tres |

El plano estructural y la azotea ya **no** son obligatorios. Solicitud Recibida y Revisión y Specs no tienen requisitos: la ficha se puede capturar progresivamente.

### 5.3 Etiqueta "Pendientes para avanzar"

Antes "Falta documentación". Se pone cuando la oportunidad tiene requisitos pendientes para su **siguiente** etapa y se quita al cumplirlos. Se recalcula al cambiar etapa, tipo de cotización, documentos o cualquier dato usado en un requisito.

### 5.4 Tipos de cotización y secciones

Los tipos corresponden a las 5 plantillas de cotización que envió CMR el 29-oct-2026.

| Tipo | Planos | Técnica y seguridad | Arquitectónicos | Punto fijo | Constructivos |
|---|---|---|---|---|---|
| Molde por niveles | ✔ | ✔ | ✔ | ✔ | ✔ |
| Molde vivienda PB + planta alta | ✔ | ✔ | ✔ | ✔ | ✔ |
| Adaptación / repotenciación | ✔ | ✔ | ✔ | ✔ | ✔ |
| Fabricación por listado / reparación | ✔ | ✔ | — | — | — |
| Venta de accesorios | — | ✔ | — | — | — |

Sin tipo se muestran todas las secciones. Ficha, datos del proyecto, volumetría y textos se muestran siempre. Propuesta a validar en CMR-04.

### 5.5 Plantilla de cotización por tipo

- Cada tipo de cotización tiene el campo **Plantilla de cotización** (`plantilla_id`).
- Al pulsar **Nueva cotización** en una oportunidad cuyo tipo tiene plantilla, la cotización nace con esa plantilla, con sus secciones y líneas cargadas y ligada a la oportunidad.
- Sin tipo, o con un tipo sin plantilla, la cotización nace vacía, como siempre.
- Las plantillas se importan con los archivos de CMR (CILI-07). Después se ligan en *Tipos de cotización*.

### 5.6 Plan de actividades por etapa

- Campo opcional en la etapa: **Plan de actividades al entrar** (planes nativos de Odoo para CRM).
- Al entrar una oportunidad, se programan las actividades del plan con su responsable y plazo. Las "a definir" se asignan al vendedor.
- Si el plan falla, se deja una nota y la oportunidad avanza igual.
- Es la base para CILI-05.

---

## 6. Migraciones (automáticas al actualizar)

### 6.1 Desde 20.0.1.0.0

- Casillas Plantas / Cortes / Estructural / Azotea marcadas → documento **Recibido** con nota "Migrado de la versión anterior"; el resto de documentos queda Faltante.
- Tipo de proyecto Equipo nuevo → **Molde por niveles**; Adaptación → **Adaptación / repotenciación**.
- Fecha de la ficha = fecha de creación de la oportunidad.
- Etiqueta renombrada a "Pendientes para avanzar" y recalculada.
- `cmr_requiere_gate` desaparece de las etapas. Al terminar la actualización, Odoo **borra los campos y columnas viejos** (`cmr_tipo_proyecto`, `cmr_plantas_arq`, `cmr_cortes_fachadas`, `cmr_plano_estructural`, `cmr_plano_azotea`, `cmr_gate_completo`, `cmr_requiere_gate`). La migración copia sus datos antes, y los valores originales solo quedan en el respaldo previo a la actualización.

Al actualizar producción de 1.0.0 a 2.1.0, Odoo corre las dos migraciones en orden.

### 6.2 Desde 20.0.2.0.0 (`cmr-test`)

- Renombra Molde completo → Molde por niveles, Adaptación → Adaptación / repotenciación, Listado → Fabricación por listado / reparación y Accesorios → Venta de accesorios. Solo los renombra si conservan su nombre original, así que no pisa cambios hechos a mano.
- Crea el tipo **Molde vivienda PB + planta alta** y lo agrega a los requisitos que aplicaban a Molde completo.

---

## 7. Instalación / actualización

**Dependencias nuevas en 2.1.0:**
- `sale_crm`: ya instalado en producción (botón *Nueva cotización*).
- `sale_management`: plantillas de cotización. Se instala solo al actualizar `cmr_crm`; CMR ya había pedido activarlo.

Odoo puede instalar con él módulos automáticos de Ventas (por ejemplo, el constructor de PDF de cotizaciones). Es normal.

### 7.1 `cmr-test`

```bash
cd /opt/odoo-cmr-test
mv addons/cmr_crm /root/cmr_crm_respaldo_$(date +%F)
unzip -q cmr_crm.zip -d addons/ && chmod -R 755 addons
./scripts/modulo.sh actualizar cmr_crm
docker compose logs odoo --tail 80 | grep -i "cmr_crm\|error\|traceback"
```

Debe aparecer `Running upgrade [20.0.2.1.0>] post-migrate` y los 4 renombres de tipos.

### 7.2 Producción (respaldo previo)

```bash
# 1. Respaldo manual antes de tocar nada
/opt/respaldos-cmr/respaldo.sh                      # revisar que termine en "Listo"

# 2. Reemplazar el módulo
cd /opt/odoo-cmr
mv addons/cmr_crm /root/cmr_crm_v1_$(date +%F)       # fuera de addons
unzip -q /ruta/cmr_crm.zip -d addons/ && chmod -R 755 addons
grep version addons/cmr_crm/__manifest__.py          # 20.0.2.1.0

# 3. Actualizar
docker compose exec odoo odoo -d NOMBRE_BD -u cmr_crm --stop-after-init --no-http 2>&1 | tee /root/upgrade_cmr_crm.log
grep -i "cmr_crm:\|Running upgrade\|error\|traceback" /root/upgrade_cmr_crm.log
docker compose restart odoo
```

En el log deben aparecer las dos migraciones (`20.0.2.0.0` y `20.0.2.1.0`) y las líneas "oportunidades con tipo…" y "líneas de documento creadas…".

**Si falla:** el comando `-u` no deja cambios a medias; Odoo revierte la transacción. Se regresa la carpeta anterior a `addons/` y se reinicia. Si algo quedó mal después de reiniciar, se restaura el respaldo del paso 1 (ver `respaldos_cmr.md`, 4.1).

**Importante:** copiar la carpeta y reiniciar no basta. Sin el `-u`, Odoo carga el código nuevo sobre la base sin actualizar y el CRM falla con un error de servidor en `crm.lead`. Pasó en producción el 29-oct antes de correr el paso 3; se resolvió al correrlo.

Las etapas por defecto de Odoo (Nuevo, Calificado, Propuesta, Ganado) deben estar eliminadas: si existen, se intercalan en el orden del pipeline y afectan el cálculo de "siguiente etapa".

---

## 8. Configuración posterior

| Ajuste | Dónde |
|---|---|
| Requisitos de paso | CRM → Configuración → Especificaciones técnicas → Requisitos por etapa (o dentro de cada etapa) |
| Secciones y plantilla por tipo de cotización | … → Tipos de cotización (columna *Plantilla de cotización*) |
| Documentos que se agregan a cada oportunidad | … → Documentos y planos |
| Tipos de producto | … → Tipos de producto |
| Plan de actividades por etapa | CRM → Configuración → Etapas → *Plan de actividades al entrar* |

---

## 9. Pruebas de aceptación

| # | Prueba | Resultado esperado | Local | cmr-test |
|---|---|---|---|---|
| 1 | Actualizar desde 1.0.0 | Documentos y tipos migrados, etiqueta recalculada | ✔ | ✔ |
| 2 | Crear oportunidad | 9 documentos en Faltante; sin etiqueta en Solicitud Recibida | ✔ | ✔ |
| 3 | Pasar a Revisión y Specs | Etiqueta y aviso: falta plantas y cortes | ✔ | ✔ |
| 4 | Arrastrar a Volumetría sin planos | Bloqueo con plantas y cortes faltantes; no menciona estructural | ✔ | ✔ |
| 5 | Plantas Recibido + Cortes No aplica | Avanza a Volumetría | ✔ | ✔ |
| 6 | Pasar a Cotización sin m² | Bloqueo "m² Cotizados: sin capturar" | ✔ | ✔ |
| 7 | Requisito en nivel Revisado con plano Recibido | Bloqueo "recibido, revisión pendiente" | ✔ | ✔ |
| 8 | Marcar Revisado | Registra quién y cuándo; queda en el chatter | ✔ | ✔ |
| 9 | Tipo Venta de accesorios | Avanza sin planos; sección de planos oculta | ✔ | ✔ |
| 10 | Sin tipo de cotización → Volumetría | Bloqueo "Tipo de cotización: sin capturar" | ✔ | ✔ |
| 11 | Botón Ganado sin requisitos / con requisitos | Bloquea / pasa a Ganada | ✔ | ✔ |
| 12 | Convertir lead / duplicar oportunidad | Con documentos / copia documentos | ✔ | ✔ |
| 13 | Altura 250, config 240, losa 10 | EQL 0, CAP 20 | ✔ | ✔ |
| 14 | Plan en Volumetría | Al entrar se programa la actividad del plan | ✔ | ✔ |
| 15 | Actualizar a 2.1.0 | 5 tipos con los nombres de las plantillas de CMR; requisitos incluyen Molde vivienda | ✔ | ☐ |
| 16 | Ligar una plantilla a un tipo y pulsar *Nueva cotización* | La cotización nace con la plantilla y sus líneas, ligada a la oportunidad | ✔ | ☐ |
| 17 | *Nueva cotización* con tipo sin plantilla | Cotización vacía, como antes | ✔ | ☐ |

Pruebas 1 a 14 en `cmr-test` hechas con 2.0.0 el 29-oct-2026.

---

## 10. Pendientes de CMR que afectan este módulo (CMR-04 / CMR-06)

Todos se resuelven por configuración, salvo donde se indica.

1. **Requisitos de paso definitivos** por etapa y tipo (sección 5.2) y quién puede marcar un documento como Revisado o No aplica.
2. **Secciones y campos por tipo de cotización** (5.4), en especial Fabricación por listado y Venta de accesorios.
3. **"Metros ponderados"**: hoy es m² × probabilidad; confirmar significado antes de usarlo en reportes. *(Puede requerir código.)*
4. **Versión vigente del formato**: confirmar que `ET-COT-01-1-24` es el compartido por Arlex el 26-oct 16:57.
5. **Observaciones del Excel:**
   - "Junta de control en antepechos" aparece dos veces (AF34 y AF37); se dejó un solo campo.
   - "Cantidad de punto fijo" tiene opciones Completo/Medio (no es una cantidad).
   - "Base de tinco" se tomó como "Base de tinaco".
   - El plano estructural no está en el formato; se conserva como documento opcional.
   - **Tipo de producto:** el catálogo de CMR (29-oct) solo maneja RobustForm con platina 5.4/6.5 cm y vida útil 500/1,000 usos. Propuesta: sustituir el campo por "Platina" y "Vida útil". *(Requiere código; pregunta 10 a CMR.)*
6. **Congelamiento** de la especificación (CMR-06 / CILI-08): hoy se puede editar en cualquier etapa. *(Requiere código.)*

---

## 11. Consideraciones

- **Desinstalar borra los campos** y los documentos capturados. Respaldar antes.
- **Los estados de documento son declarativos:** no validan que el archivo exista; el enlace es opcional (base para CILI-09 SharePoint).
- **Requisitos con datos numéricos:** un valor 0 cuenta como "sin capturar".
- **Etiquetas en la cotización:** Odoo copia las etiquetas de la oportunidad a la cotización, incluida "Pendientes para avanzar". Es comportamiento estándar de `sale_crm`.
- **Opciones, revisiones, PDF FT-CTZ-01 e hitos de pago** (CILI-07) no van en este módulo; se harán en un módulo nuevo `cmr_sale`.

---

## 12. Fuera del alcance

| Componente | Cómo se cubre |
|---|---|
| Catálogo, listas de precios y plantillas de cotización (CILI-07) | Importación de los archivos de CMR del 29-oct (con correcciones) |
| PDF FT-CTZ-01, opciones / revisiones, hitos de pago | Módulo nuevo `cmr_sale` (pendiente) |
| Resumen de volumetría y áreas (CILI-06) | Pendiente (CMR-05: columna "Programa / % aumentado") |
| Permisos por rol y ocultar importes a Ingeniería (CILI-03) | Pendiente (CMR-03) |
| Traspaso a Proyectos de Ingeniería (CILI-04) | Fase 5 del plan de trabajo |
| Congelamiento y versión aprobada (CILI-08) | Pendiente (CMR-06) |
| Moneda USD/MXN, tipo de cambio DOF y CFDI | Subtarea nueva por crear |
| Reloj de SLA, dashboard de KPIs | Pendiente |

---

## 13. Historial de versiones

| Versión | Fecha | Cambios |
|---|---|---|
| 20.0.1.0.0 | 24-oct-2026 | Versión inicial para Odoo 20: 7 etapas, pestaña con 4 casillas de planos, gate por etapa, m² ponderados, motivos de pérdida. |
| 20.0.2.0.0 | 29-oct-2026 | Minuta Reunión 2 (CILI-01, CILI-02): ESP-TEC completo en la pestaña; tipos de cotización con secciones condicionales; documentos con estado (distingue faltante de revisión pendiente); requisitos de avance configurables por etapa y tipo, en lugar del gate fijo de 4 planos; plano estructural deja de ser obligatorio; etiqueta "Pendientes para avanzar"; plan de actividades por etapa; migración automática desde 1.0.0. |
| 20.0.2.1.0 | 29-oct-2026 | Respuesta de CMR del 29-oct: los tipos de cotización pasan a ser las 5 plantillas de CMR (se agrega Molde vivienda PB + planta alta); cada tipo se liga a su plantilla, que se carga al crear la cotización desde la oportunidad; nuevas dependencias `sale_crm` y `sale_management`; migración desde 2.0.0. |
