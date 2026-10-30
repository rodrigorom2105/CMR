# -*- coding: utf-8 -*-
"""Precios en USD del catálogo de CMR (29/10/2026).

La compañía está en MXN y Odoo guarda el "precio de venta" del producto en esa moneda. Por eso los
precios en USD del catálogo se cargan en las listas de precios (que sí están en USD):

1. Precio extra por variante (hoja "Precio extra variantes"). Sirve de referencia en la ficha del producto.
2. Lista "Cliente nuevo": precio fijo en USD por cada variante = precio del catálogo + precio extra.
3. Lista "Cliente existente": toma los precios de "Cliente nuevo", salvo las reglas de la hoja
   "Listas de precios" (cuña y pasador importados).

Requisitos: catálogo importado (paso 5.2) y las dos listas en USD creadas (paso 4).
Se puede correr varias veces: actualiza precios y no duplica reglas.
Si CMR cambia un precio del catálogo: actualizar el producto y volver a correr este script.

Uso (en el servidor, carpeta de producción):
    docker compose exec -T odoo odoo shell -d cmr_db --no-http < 3_precios_extra_y_listas.py
Con APLICAR = False solo muestra lo que haría, sin guardar nada.
"""
APLICAR = True

PRECIOS_EXTRA = [  # (código, atributo, valor, precio extra USD)
    ('MOL-001', 'Vida útil', '500 usos', 0.0),
    ('MOL-001', 'Vida útil', '1000 usos', 50.0),
    ('MOL-002', 'Vida útil', '500 usos', 0.0),
    ('MOL-002', 'Vida útil', '1000 usos', 50.0),
    ('MOL-003', 'Vida útil', '500 usos', 0.0),
    ('MOL-003', 'Vida útil', '1000 usos', 50.0),
    ('MOL-004', 'Vida útil', '500 usos', 0.0),
    ('MOL-004', 'Vida útil', '1000 usos', 50.0),
    ('MOL-005', 'Vida útil', '500 usos', 0.0),
    ('MOL-005', 'Vida útil', '1000 usos', 50.0),
    ('MOL-006', 'Vida útil', '500 usos', 0.0),
    ('MOL-006', 'Vida útil', '1000 usos', 50.0),
    ('MOL-007', 'Vida útil', '500 usos', 0.0),
    ('MOL-007', 'Vida útil', '1000 usos', 50.0),
    ('MOL-008', 'Vida útil', '500 usos', 0.0),
    ('MOL-008', 'Vida útil', '1000 usos', 50.0),
    ('MOL-009', 'Vida útil', '500 usos', 0.0),
    ('MOL-009', 'Vida útil', '1000 usos', 50.0),
    ('MOL-010', 'Vida útil', '500 usos', 0.0),
    ('MOL-010', 'Vida útil', '1000 usos', 50.0),
    ('MOL-011', 'Vida útil', '500 usos', 0.0),
    ('MOL-011', 'Vida útil', '1000 usos', 50.0),
    ('MOL-012', 'Vida útil', '500 usos', 0.0),
    ('MOL-012', 'Vida útil', '1000 usos', 50.0),
    ('MOL-013', 'Vida útil', '500 usos', 0.0),
    ('MOL-013', 'Vida útil', '1000 usos', 50.0),
    ('COM-001', 'Andamiaje', 'Básico', 0.0),
    ('COM-001', 'Andamiaje', 'Solo ménsulas', 165.0),
    ('COM-001', 'Andamiaje', 'Completo – guardacuerpo doble tubo riel', 240.0),
    ('COM-001', 'Andamiaje', 'Completo – guardacuerpo mampara modular + rodapié', 275.0),
    ('COM-002', 'Tipo de equipo de seguridad', 'Básico – alineadores de cap', 0.0),
    ('COM-002', 'Tipo de equipo de seguridad', 'Completo – alineadores de cap + guardacuerpo doble tubo riel', 120.0),
    ('COM-003', 'Tipo de alineación', 'Muros 3 líneas (2 en muro + 1 en borde de cap) + escuadras', 0.0),
    ('COM-003', 'Tipo de alineación', 'Tipo rosca mariposa', 1196.0),
    ('COM-003', 'Tipo de alineación', 'Horizontal 2 líneas (ángulo de acero)', 5696.0),
    ('MOL-014', 'Vida útil', '500 usos', 0.0),
    ('MOL-014', 'Vida útil', '1000 usos', 50.0),
    ('MOL-015', 'Vida útil', '500 usos', 0.0),
    ('MOL-015', 'Vida útil', '1000 usos', 50.0),
    ('FAB-003', 'Tipo de pieza de escalera', 'Esqueletos (ángulos) – juego de 2', 0.0),
    ('FAB-003', 'Tipo de pieza de escalera', 'Peldaños (juego de 8)', 590.0),
    ('ACS-001', 'Origen y platina', 'Importado 5.4 cm', 0.0),
    ('ACS-001', 'Origen y platina', 'Importado 6.5 cm', 0.0),
    ('ACS-001', 'Origen y platina', 'Nacional 5.4 cm', 0.25),
    ('ACS-002', 'Origen y platina', 'Importado 5.4 cm', 0.0),
    ('ACS-002', 'Origen y platina', 'Importado 6.5 cm', 0.0),
    ('ACS-002', 'Origen y platina', 'Nacional 5.4 cm', 0.2),
    ('ACS-003', 'Tipo de cuña en ángulo', 'Galvanizada nacional', 0.0),
    ('ACS-003', 'Tipo de cuña en ángulo', 'Para andamiaje CMR tipo Forsa', 1.72),
    ('ACS-004', 'Medida', 'M8', 0.0),
    ('ACS-004', 'Medida', 'M10', 0.55),
    ('ACS-004', 'Medida', 'M12', 0.75),
    ('ACS-004', 'Medida', 'M15', 0.98),
    ('ACS-004', 'Medida', 'M20', 1.19),
    ('ACS-004', 'Medida', 'M25', 2.88),
    ('ACS-005', 'Medida', 'MD10 Junta 2.5 cm', 0.0),
    ('ACS-005', 'Medida', 'MD10 Junta 5 cm', 0.06),
    ('AND-001', 'Largo de cercha', '150 cm', 0.0),
    ('AND-001', 'Largo de cercha', '265 cm', 21.0),
    ('AND-001', 'Largo de cercha', '290 cm', 28.0),
    ('AND-002', 'Largo de plataforma', '80 cm', 0.0),
    ('AND-002', 'Largo de plataforma', '165 cm', 103.18),
    ('AND-002', 'Largo de plataforma', '230 cm', 182.08),
    ('AND-004', 'Tipo de alineador', 'Tipo 1.00', 0.0),
    ('AND-004', 'Tipo de alineador', 'Tipo 1.20', 0.0),
]

CATEGORIAS_CMR = ["Moldes de aluminio", "Complementarios", "Servicios", "Accesorios",
                  "Accesorios de andamiaje", "Fabricación y reparación"]

REGLAS_CLIENTE_EXISTENTE = [  # (variante, precio fijo USD)
    ('Cuña (Importado 5.4 cm)', 0.73),
    ('Cuña (Importado 6.5 cm)', 0.73),
    ('Pasador (Importado 5.4 cm)', 1.12),
    ('Pasador (Importado 6.5 cm)', 1.12),
]

Template = env["product.template"].with_context(active_test=False)
PTAV = env["product.template.attribute.value"]
errores, cambios = [], 0

print("== Precios extra por variante")
for codigo, atributo, valor, extra in PRECIOS_EXTRA:
    tmpl = Template.search([("default_code", "=", codigo)], limit=1)
    if not tmpl:
        errores.append(f"No existe el producto {codigo}"); continue
    ptav = PTAV.search([("product_tmpl_id", "=", tmpl.id),
                        ("attribute_id.name", "=", atributo),
                        ("product_attribute_value_id.name", "=", valor)], limit=1)
    if not ptav:
        errores.append(f"{codigo}: no tiene el valor '{valor}' del atributo '{atributo}'"); continue
    if round(ptav.price_extra, 4) != round(extra, 4):
        print(f"  {codigo} {tmpl.name} · {valor}: {ptav.price_extra} -> {extra}")
        ptav.price_extra = extra
        cambios += 1

Item = env["product.pricelist.item"]
Lista = env["product.pricelist"]

def regla_fija(lista, producto, precio, etiqueta):
    global cambios
    regla = lista.item_ids.filtered(lambda i: i.applied_on == "0_product_variant" and i.product_id == producto)
    vals = {"applied_on": "0_product_variant", "product_id": producto.id,
            "product_tmpl_id": producto.product_tmpl_id.id, "compute_price": "fixed", "fixed_price": precio}
    if not regla:
        Item.create(dict(vals, pricelist_id=lista.id)); cambios += 1
        print(f"  {lista.name} · {etiqueta}: creada USD {precio}")
    elif round(regla[0].fixed_price, 4) != round(precio, 4) or regla[0].compute_price != "fixed":
        regla[0].write(vals); cambios += 1
        print(f"  {lista.name} · {etiqueta}: USD {regla[0].fixed_price} -> {precio}")

nueva = Lista.search([("name", "=", "Cliente nuevo")], limit=1)
existente = Lista.search([("name", "=", "Cliente existente")], limit=1)
for nombre, lista in (("Cliente nuevo", nueva), ("Cliente existente", existente)):
    if not lista:
        errores.append(f"No existe la lista de precios '{nombre}' (paso 4)")
    elif lista.currency_id.name != "USD":
        errores.append(f"La lista '{nombre}' está en {lista.currency_id.name}, debe ser USD")

if nueva and existente:
    env.flush_all()
    print("== Lista Cliente nuevo: precio fijo en USD por variante")
    # Solo productos del catálogo de CMR: código con prefijo del catálogo y una de sus 6 categorías
    variantes = env["product.product"].search([
        ("product_tmpl_id.categ_id.name", "in", CATEGORIAS_CMR),
        ("product_tmpl_id.default_code", "=like", "___-%"),
    ])
    print(f"  {len(variantes)} variantes del catálogo")
    for producto in variantes:
        # precio del catálogo (USD) = precio base capturado + precio extra de la variante
        precio = producto.product_tmpl_id.list_price + producto.price_extra
        regla_fija(nueva, producto, round(precio, 4), producto.display_name)

    print("== Lista Cliente existente: base Cliente nuevo + reglas de CMR")
    base = existente.item_ids.filtered(lambda i: i.applied_on == "3_global")
    vals_base = {"applied_on": "3_global", "compute_price": "discount", "base": "pricelist",
                 "base_pricelist_id": nueva.id, "price_discount": 0.0}
    if not base:
        Item.create(dict(vals_base, pricelist_id=existente.id)); cambios += 1
        print("  regla general creada: precios de Cliente nuevo")
    elif base[0].base != "pricelist" or base[0].base_pricelist_id != nueva or base[0].compute_price != "discount" or base[0].price_discount:
        base[0].write(vals_base); cambios += 1
        print("  regla general actualizada: precios de Cliente nuevo")
    for variante, precio in REGLAS_CLIENTE_EXISTENTE:
        nombre, _, valor = variante.partition(" (")
        valor = valor.rstrip(")")
        producto = env["product.product"].search([
            ("product_tmpl_id.name", "=", nombre),
            ("product_template_attribute_value_ids.product_attribute_value_id.name", "=", valor)], limit=1)
        if not producto:
            errores.append(f"No existe la variante {variante}"); continue
        regla_fija(existente, producto, precio, variante)

print(f"== Cambios: {cambios} | Errores: {len(errores)}")
for e in errores:
    print("  ERROR:", e)
if APLICAR and not errores:
    env.cr.commit()
    print("== Guardado.")
else:
    env.cr.rollback()
    print("== NO se guardó nada" + (" (hay errores)" if errores else " (APLICAR = False)") + ".")
