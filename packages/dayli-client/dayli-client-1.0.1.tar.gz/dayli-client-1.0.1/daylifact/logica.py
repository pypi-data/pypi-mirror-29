# -*- coding: utf-8 -*-

import utils
import xml.etree.cElementTree as ETXML
import sys
from daylifact.entidades import *

def Validar_Numeros_Impuesto(lista, validar_codigos=False):
    nuevo_detalle = []
    for d in lista:
        if validar_codigos:
            if (d.codigo in utils.CODIGOS_IMPUESTO) == False:
                return {'result': "El campo código en impuestos debe tener los valores: 'iva', 'ice' o 'irbpnr'. Se ha encontrado '" + str(d.codigo) + "'"}

            if d.codigo == 'iva' and (str(d.codigo_porcentaje) in utils.TARIFA_IMPUESTOS) == False:
                return {'result': "El campo código porcentaje en impuestos debe tener los valores: '0', '12', '14', 'noiva' o 'excento'. Se ha encontrado '" + str(d.codigo_porcentaje) + "'"}

            d.codigo_porcentaje = str(d.codigo_porcentaje)

        det = utils.Numerico(d)

        if det[0]:
            nuevo_detalle.append(det[1])
        else:
            return {'result': det[1]}

    return {'valores': nuevo_detalle, 'result': "OK"}

def Validar_Impuestos_Retencion(lista):
    nuevo_detalle = []
    for d in lista:
        if (d.codigo in utils.IMPUESTO_A_RETENER) == False:
            return {'result': "El campo código en impuestos debe tener los valores: 'renta', 'iva' o 'isd'. Se ha encontrado '" + str(d.codigo) + "'"}

        if d.codigo == 'iva' and (str(d.codigo_porcentaje) in utils.RETENCION_IVA) == False:
            return {'result': "El campo código de retención IVA debe tener los valores: '0a', '0b', '10', '20', '30', '50', '70' o '100'. Se ha encontrado '" + str(d.codigo_porcentaje) + "'"}

        if d.codigo == 'isd' and (str(d.codigo_porcentaje) in utils.RETENCION_ISD) == False:
            return {
                'result': "El campo código de retención ISD debe tener el valor: '5'. Se ha encontrado '" + str(d.codigo_porcentaje) + "'"}

        d.codigo_porcentaje = str(d.codigo_porcentaje)
        d.porcentaje_retener = str(d.porcentaje_retener)

        det = utils.Numerico(d)

        if det[0]:
            nuevo_detalle.append(det[1])
        else:
            return {'result': det[1]}

    return {'valores': nuevo_detalle, 'result': "OK"}

def Validar_Empresa(empresa):
    razon_social = utils.Longitud("razón social", empresa.razon_social, 300)
    if not razon_social[0]:
        return {'result': razon_social[1]}

    nombre_comercial = utils.Longitud("nombre comercial", empresa.nombre_comercial, 300, obligatorio=False, cortar=True)
    if nombre_comercial[0]:
        empresa.nombre_comercial = nombre_comercial[1]
    else:
        return {'result': nombre_comercial[1]}

    ruc = utils.Longitud_Identificacion(empresa.ruc, "ruc")
    if not ruc[0]:
        return {'result': ruc[1]}

    dir_matriz = utils.Longitud("dirección de matriz", empresa.dir_matriz, 300)
    if not dir_matriz[0]:
        return {'result': dir_matriz[1]}

    dir_establec = utils.Longitud("dirección de establecimiento", empresa.dir_establecimiento, 300, obligatorio=False,
                                  cortar=True)
    if dir_establec[0]:
        empresa.dir_establecimiento = dir_establec[1]
    else:
        return {'result': dir_establec[1]}

    contribuyente = utils.Longitud("contribuyente especial", empresa.contribuyente_especial, 13, obligatorio=False)
    if not contribuyente[0]:
        return {'result': contribuyente[1]}

    if empresa.obligado_contabilidad:
        if empresa.obligado_contabilidad.upper() in ("SI", "NO"):
            empresa.obligado_contabilidad = empresa.obligado_contabilidad.upper()
        else:
            return {'result': "El campo obligado a llevar contabilidad, debe tener los valores SI o NO"}

    return {'empresa': empresa, 'result': "OK"}

def Validar_Cliente(cliente):
    tipo = utils.Longitud_Identificacion(cliente.identificacion_comprador, cliente.tipo_identificacion_comprador)
    if not tipo[0]:
        return {'result': tipo[1]}

    razon = utils.Longitud("razón social", cliente.razon_social_comprador, maximo=300)
    if not razon[0]:
        return {'result': razon[1]}

    direccion = utils.Longitud("dirección", cliente.direccion_comprador, maximo=300, obligatorio=False, cortar=True)
    if not direccion[0]:
        return {'result': direccion[1]}
    else:
        cliente.direccion_comprador = direccion[1]

    return {'cliente': cliente, 'result': "OK"}

def Validar_Proveedor(proveedor):
    tipo = utils.Longitud_Identificacion(proveedor.identificacion, proveedor.tipo_identificacion)
    if not tipo[0]:
        return {'result': tipo[1]}

    razon = utils.Longitud("razón social", proveedor.razon_social, maximo=300)
    if not razon[0]:
        return {'result': razon[1]}

    rise = utils.Longitud("rise", proveedor.rise, maximo=40, obligatorio=False)
    if not rise[0]:
        return {'result': rise[1]}

    return {'result': "OK"}

def Validar_Transportista(transportista):
    tipo = utils.Longitud_Identificacion(transportista.identificacion, transportista.tipo_identificacion)
    if not tipo[0]:
        return {'result': tipo[1]}

    razon = utils.Longitud("razón social", transportista.razon_social, maximo=300)
    if not razon[0]:
        return {'result': razon[1]}

    rise = utils.Longitud("rise", transportista.rise, maximo=40, obligatorio=False)
    if not rise[0]:
        return {'result': rise[1]}

    placa = utils.Longitud("placa", transportista.placa, maximo=20)
    if not placa[0]:
        return {'result': placa[1]}

    return {'result': "OK"}

def Validar_Comprobante(documento):
    if (documento.ambiente in utils.TIPO_AMBIENTE) == False:
        return {'result': "El campo ambiente debe tener los valores: 'pruebas' o 'produccion'. Se ha encontrado '" + str(documento.ambiente) + "'"}

    if (documento.cod_doc in utils.TIPO_COMPROBANTE) == False:
        return {'result': "El campo tipo de comprobante debe tener los valores: 'factura', 'credito', 'debito', 'guia' o 'retencion'. Se ha encontrado '" + str(documento.cod_doc) + "'"}

    if (documento.tipo_emision in utils.TIPO_EMISION) == False:
        return {'result': "El campo tipo de emisión debe tener los valores: 'normal' o 'indisp'. Se ha encontrado '" + str(documento.tipo_emision) + "'"}

    if documento.estab.isdigit():
        estab = utils.Longitud("establecimiento", documento.estab, maximo=3, minimo=3)
        if not estab[0]:
            return {'result': estab[1]}
    else:
        return {'result': "El campo establecimiento debe tener valores numéricos. Se ha encontrado " + str(documento.estab)}

    if documento.pto_emi.isdigit():
        pto = utils.Longitud("punto de emisión", documento.pto_emi, maximo=3, minimo=3)
        if not pto[0]:
            return {'result': pto[1]}
    else:
        return {'result': "El campo punto de emisión debe tener valores numéricos. Se ha encontrado " + str(documento.pto_emi)}

    if documento.secuencial.isdigit():
        sec = utils.Longitud("secuencial", documento.secuencial, maximo=9, minimo=9)
        if not sec[0]:
            return {'result': sec[1]}
    else:
        return {'result': "El campo secuencial debe tener valores numéricos. Se ha encontrado " + str(documento.secuencial)}

    fecha = utils.Formato_Fecha(documento.fecha_emision)
    if fecha[0]:
        documento.fecha_emision = fecha[1]
    else:
        return {'result': fecha[1]}

    # Parte de comprobante Factura o Nota de crédito
    if documento.cod_doc == 'factura' or documento.cod_doc == 'credito' or documento.cod_doc == 'debito':
        # Formato x.xx en valores numéricos de la factura o nota de crédito o nota de débito
        val_factura = utils.Numerico(documento)
        if val_factura[0]:
            documento = val_factura[1]
        else:
            return {'result': val_factura[1]}

        # Formato x.xx en totalImpuesto de la factura o nota de crédito o nota de débito
        if not documento.total_con_impuestos:
            return {'result': "La lista de impuestos de la factura no debe estar vacía"}
        else:
            val_impuesto = Validar_Numeros_Impuesto(documento.total_con_impuestos, True)
            if val_impuesto['result'] != "OK":
                return {'result': val_impuesto['result']}
            else:
                documento.total_con_impuestos = val_impuesto['valores']

        if documento.cod_doc == 'factura':
            guia = utils.Longitud("guía de remisión", documento.guia_remision, maximo=15, minimo=15, obligatorio=False)
            if not guia[0]:
                return {'result': guia[1]}

            # Formas de pago
            if not documento.pagos:
                return {'result': "La lista de pagos de la factura no debe estar vacía"}
            else:
                for pag in documento.pagos:
                    if (pag.forma_pago in utils.FORMAS_PAGO) == False:
                        return {
                            'result': "El campo forma de pago debe tener los valores: 'efectivo', 'deudas', 'debito', 'electronico', 'prepago', 'credito', 'otros' o 'endoso'. Se ha encontrado '" + str(
                                pag.forma_pago) + "'"}

                    if type(pag.total) is not int and type(pag.total) is not float:
                        return {'result': "El campo total de forma de pago debe ser un valor numérico. " + str(
                            pag.total) + " es de tipo " + str(type(pag.total).__name__)}

                    if pag.plazo:
                        if type(pag.plazo) is not int and type(pag.plazo) is not float:
                            return {'result': "El campo plazo en forma de pago debe ser un valor numérico. " + str(
                                pag.plazo) + " es de tipo " + str(type(pag.plazo).__name__)}

                    unidad_tiempo = utils.Longitud("unidad de tiempo", pag.unidad_tiempo, maximo=10, obligatorio=False)
                    if not unidad_tiempo[0]:
                        return {'result': unidad_tiempo[1]}

    # Parte de comprobante Retención y/o Nota de crédito y/o Nota de débito
    if documento.cod_doc == 'retencion' or documento.cod_doc == 'credito' or documento.cod_doc == 'debito':
        if documento.cod_doc == 'retencion':
            if len(documento.periodo_fiscal) != 7:
                return {'result': 'EL formato del campo periodo fiscal debe ser: mm/aaaa, usted ingresó ' + documento.periodo_fiscal}

        if documento.fecha_doc_sustento:
            fecha_doc_sustento = utils.Formato_Fecha(documento.fecha_doc_sustento)
            if fecha_doc_sustento[0]:
                documento.fecha_doc_sustento = fecha_doc_sustento[1]
            else:
                return {'result': fecha_doc_sustento[1]}

        num_cod_sustento = utils.Longitud("número documento sustento", documento.num_doc_sustento, maximo=17, minimo=15, obligatorio=False)
        if not num_cod_sustento[0]:
            return {'result': num_cod_sustento[1]}

        if documento.cod_doc_sustento:
            if (documento.cod_doc_sustento in utils.TIPO_COMPROBANTE) == False:
                return {'result': "El campo código documento sustento debe tener los valores: 'factura', 'debito', 'guia', 'credito' o 'ifis'. Se ha encontrado '" + str(documento.cod_doc_sustento) + "'"}

    # Parte de comprobante Guía de Remisión
    if documento.cod_doc == 'guia':
        dir_partida = utils.Longitud("dirección de partida", documento.direccion_partida, maximo=300, cortar=True)
        if not dir_partida[0]:
            return {'result': dir_partida[1]}
        else:
            documento.direccion_partida = dir_partida[1]

        fecha_ini = utils.Formato_Fecha(documento.fecha_inicio_transporte)
        if fecha_ini[0]:
            documento.fecha_inicio_transporte = fecha_ini[1]
        else:
            return {'result': fecha_ini[1]}

        fecha_fin = utils.Formato_Fecha(documento.fecha_fin_transporte)
        if fecha_fin[0]:
            documento.fecha_fin_transporte = fecha_fin[1]
        else:
            return {'result': fecha_fin[1]}

    if documento.cod_doc == 'credito':
        if not documento.valor_modificacion:
            return {'result': 'El valor de modificación debe ser un valor numérico'}

        motivo = utils.Longitud("motivo", documento.motivo, maximo=300)
        if not motivo[0]:
            return {'result': motivo[1]}

    if documento.cod_doc == 'debito':
        if not documento.importe_total:
            return {'result': 'El valor total debe ser un valor numérico'}

    return {'documento': documento, 'result': "OK"}

def Validar_Detalle_Factura(detalle_factura):
    val_detalle = Validar_Numeros_Impuesto(detalle_factura)
    if val_detalle['result'] != "OK":
        return {'result': val_detalle['result']}
    else:
        detalle_factura = val_detalle['valores']

    # Formato x.xx en impuestos
    for i in detalle_factura:
        val_impuesto = Validar_Numeros_Impuesto(i.impuestos, True)
        if val_impuesto['result'] != "OK":
            return {'result': val_impuesto['result']}
        else:
            i.impuestos = val_impuesto['valores']

    return {'detalle_factura': detalle_factura, 'result': "OK"}

def Validar_Detalle_Retencion(detalle_retencion):
    # Formato x.xx en impuestos
    val_detalle = Validar_Impuestos_Retencion(detalle_retencion)

    if val_detalle['result'] != "OK":
        return {'result': val_detalle['result']}
    else:
        detalle_retencion = val_detalle['valores']

    return {'detalle_retencion': detalle_retencion, 'result': "OK"}

def Validar_Detalle_Destinatario(detalle_destinatario):
    for dd in detalle_destinatario:
        identificacion = utils.Longitud("identificación del destinatario", dd.identificacion, maximo=20, minimo=3)
        if not identificacion[0]:
            return {'result': identificacion[1]}

        razon = utils.Longitud("razón social del destinatario", dd.razon_social, maximo=300)
        if not razon[0]:
            return {'result': razon[1]}

        direccion = utils.Longitud("dirección del destinatario", dd.direccion, maximo=300)
        if not direccion[0]:
            return {'result': direccion[1]}

        motivo = utils.Longitud("motivo del traslado", dd.motivo_traslado, maximo=300)
        if not motivo[0]:
            return {'result': motivo[1]}

        doc_aduanero = utils.Longitud("documento aduanero único", dd.documento_aduanero_unico, maximo=20, obligatorio=False)
        if not doc_aduanero[0]:
            return {'result': doc_aduanero[1]}

        cod_establ = utils.Longitud("código de establecimiento", dd.cod_establecimiento_destino, maximo=3, minimo=3, obligatorio=False)
        if not cod_establ[0]:
            return {'result': cod_establ[1]}

        ruta = utils.Longitud("ruta del traslado", dd.ruta, maximo=300, obligatorio=False)
        if not ruta[0]:
            return {'result': ruta[1]}

        if dd.cod_doc_sustento:
            if (dd.cod_doc_sustento in utils.TIPO_COMPROBANTE) == False:
                return {'result': "El campo código documento sustento debe tener los valores: 'factura', 'debito', 'retencion', 'credito' o 'ifis'. Se ha encontrado '" + str(dd.cod_doc_sustento) + "'"}

        if dd.fecha_doc_sustento:
            fecha_doc_sustento = utils.Formato_Fecha(dd.fecha_doc_sustento)
            if fecha_doc_sustento[0]:
                dd.fecha_doc_sustento = fecha_doc_sustento[1]
            else:
                return {'result': fecha_doc_sustento[1]}

        num_cod_sustento = utils.Longitud("número documento sustento", dd.num_doc_sustento, maximo=17, minimo=15, obligatorio=False)
        if not num_cod_sustento[0]:
            return {'result': num_cod_sustento[1]}

        aut_cod_sustento = utils.Longitud("número de autorización del documento sustento", dd.num_autorizacion_doc_sustento, maximo=49, minimo=10, obligatorio=False)
        if not aut_cod_sustento[0]:
            return {'result': aut_cod_sustento[1]}

        # Detalles
        for i in dd.detalles:
            cod_interno = utils.Longitud("código interno del detalle", i.codigo_principal, maximo=25, obligatorio=False)
            if not cod_interno[0]:
                return {'result': cod_interno[1]}

            cod_adicional = utils.Longitud("código adicional del detalle", i.codigo_auxiliar, maximo=25, obligatorio=False)
            if not cod_adicional[0]:
                return {'result': cod_adicional[1]}

            descripcion = utils.Longitud("descripción del detalle", i.descripcion, maximo=300)
            if not descripcion[0]:
                return {'result': descripcion[1]}

            if i.cantidad is not None and str(i.cantidad).isdigit():
                i.cantidad = str("%.2f" % i.cantidad)
            else:
                return {'result': 'La cantidad del detalle debe ser un valor numérico'}

    return {'destinatarios': detalle_destinatario, 'result': "OK"}

def Validar_Motivos_Pagos(detalle_motivos, detalle_pagos):
    # Motivos
    for mot in detalle_motivos:
        razon = utils.Longitud("razón del motivo", mot.razon, maximo=300)
        if not razon[0]:
            return {'result': razon[1]}

        if type(mot.valor) is str:
            valor = utils.Longitud("valor del motivo", mot.valor, maximo=300)
            if not valor[0]:
                return {'result': valor[1]}
        else:
            if mot.valor is not None:
                mot.valor = str("%.2f" % mot.valor)
            else:
                return {'result': 'El valor del motivo no debe estar vacío'}

    # Pagos
    if not detalle_pagos:
        return {'result': "La lista de pagos de la nota de débito no debe estar vacía"}
    else:
        for pag in detalle_pagos:
            if (pag.forma_pago in utils.FORMAS_PAGO) == False:
                return {'result': "El campo forma de pago debe tener los valores: 'efectivo', 'deudas', 'debito', 'electronico', 'prepago', 'credito', 'otros' o 'endoso'. Se ha encontrado '" + str(
                        pag.forma_pago) + "'"}

            if type(pag.total) is not int and type(pag.total) is not float:
                return {'result': "El campo total de forma de pago debe ser un valor numérico. " + str(
                    pag.total) + " es de tipo " + str(type(pag.total).__name__)}

            if pag.plazo:
                if type(pag.plazo) is not int and type(pag.plazo) is not float:
                    return {'result': "El campo plazo en forma de pago debe ser un valor numérico. " + str(
                        pag.plazo) + " es de tipo " + str(type(pag.plazo).__name__)}

            unidad_tiempo = utils.Longitud("unidad de tiempo", pag.unidad_tiempo, maximo=10, obligatorio=False)
            if not unidad_tiempo[0]:
                return {'result': unidad_tiempo[1]}

    return {'motivos': detalle_motivos, 'result': "OK"}

def Validar_Datos(empresa, sujeto, documento, detalle_documento):
    # Empresa
    val_empresa = Validar_Empresa(empresa)
    if val_empresa['result'] != "OK":
        return {'result': val_empresa['result']}
    else:
        empresa = val_empresa['empresa']

    # Documento
    val_documento = Validar_Comprobante(documento)
    if val_documento['result'] != "OK":
        return {'result': val_documento['result']}
    else:
        documento = val_documento['documento']

        # Generar clave de acceso. Enviar la entidad documento y el ruc de la empresa
        documento.clave_acceso = utils.Generar_Clave_Acceso(documento, empresa.ruc)
        clave = utils.Longitud("clave de accesso", documento.clave_acceso, maximo=49, minimo=49)

        if not clave[0]:
            return {'result': clave[1]}

    # Por cada tipo de sujeto
    if type(sujeto) is Cliente:
        # Cliente
        val_cliente = Validar_Cliente(sujeto)
        if val_cliente['result'] != "OK":
            return {'result': val_cliente['result']}
        else:
            sujeto = val_cliente['cliente']

    if type(sujeto) is Proveedor:
        # Proveedor
        val_proveedor = Validar_Proveedor(sujeto)
        if val_proveedor['result'] != "OK":
            return {'result': val_proveedor['result']}

    if type(sujeto) is Transportista:
        # Transportista
        val_transportista = Validar_Transportista(sujeto)
        if val_transportista['result'] != "OK":
            return {'result': val_transportista['result']}

    # Por cada tipo de documento (validar el detalle)
    if all(isinstance(det, Detalle_Comprobante) for det in detalle_documento):
        # Detalle factura o detalle nota de crédito
        val_detalle = Validar_Detalle_Factura(detalle_documento)
        if val_detalle['result'] != "OK":
            return {'result': val_detalle['result']}
        else:
            detalle_documento = val_detalle['detalle_factura']

    if documento.cod_doc == 'retencion':
        # Detalle retencion
        val_detalle = Validar_Detalle_Retencion(detalle_documento)
        if val_detalle['result'] != "OK":
            return {'result': val_detalle['result']}
        else:
            detalle_documento = val_detalle['detalle_retencion']

    if documento.cod_doc == 'guia':
        # Detalle destinatarios
        val_destinatarios = Validar_Detalle_Destinatario(detalle_documento)
        if val_destinatarios['result'] != "OK":
            return {'result': val_destinatarios['result']}
        else:
            detalle_documento = val_destinatarios['destinatarios']

    if documento.cod_doc == 'debito':
        # Motivos y pagos
        val_motivos = Validar_Motivos_Pagos(detalle_documento, documento.pagos)
        if val_motivos['result'] != "OK":
            return {'result': val_motivos['result']}
        else:
            detalle_documento = val_motivos['motivos']

    dic = {
        'empresa': empresa,
        'sujeto': sujeto,
        'documento': documento,
        'detalle_documento': detalle_documento,
        'result': "OK"
    }
    return dic

def Crear_XML(empresa, sujeto, documento, detalle_documento):
    # Crear XML de los documentos electrónicos
    if not detalle_documento:
        return False, "El detalle del comprobante no debe estar vacío"

    if documento.cod_doc == 'factura':
        factura = Crear_XML_Factura(empresa, sujeto, documento, detalle_documento)
        return factura
    elif documento.cod_doc == 'retencion':
        retencion = Crear_XML_Retencion(empresa, sujeto, documento, detalle_documento)
        return retencion
    elif documento.cod_doc == 'guia':
        guia_remision = Crear_XML_Guia_Remision(empresa, sujeto, documento, detalle_documento)
        return guia_remision
    elif documento.cod_doc == 'credito':
        nota_credito = Crear_XML_Nota_Credito(empresa, sujeto, documento, detalle_documento)
        return nota_credito
    elif documento.cod_doc == 'debito':
        nota_debito = Crear_XML_Nota_Debito(empresa, sujeto, documento, detalle_documento)
        return nota_debito
    else:
        return False, "No se encontró el documento con el nombre '" + documento.cod_doc + "'. Los nombres válidos son: 'factura', 'credito', 'debito', 'guia' o 'retencion'."

def Crear_XML_Factura(empresa, cliente, factura, detalle_factura):
    try:
        validaciones = Validar_Datos(empresa, cliente, factura, detalle_factura)

        if(validaciones['result'] == "OK"):
            empresa = validaciones['empresa']
            cliente = validaciones['sujeto']
            factura = validaciones['documento']
            detalle_factura = validaciones['detalle_documento']

            # <factura id="comprobante" version="1.0.0">
            head = ETXML.Element("factura", id=factura.id, version=factura.version)

            # <infoTributaria>
            infoTributaria = ETXML.SubElement(head, "infoTributaria")
            ETXML.SubElement(infoTributaria, "ambiente").text = utils.TIPO_AMBIENTE[factura.ambiente]
            ETXML.SubElement(infoTributaria, "tipoEmision").text = utils.TIPO_EMISION[factura.tipo_emision]
            ETXML.SubElement(infoTributaria, "razonSocial").text = empresa.razon_social.decode("utf8")

            if empresa.nombre_comercial:
                ETXML.SubElement(infoTributaria, "nombreComercial").text = empresa.nombre_comercial.decode("utf8")

            ETXML.SubElement(infoTributaria, "ruc").text = empresa.ruc
            ETXML.SubElement(infoTributaria, "claveAcceso").text = factura.clave_acceso
            ETXML.SubElement(infoTributaria, "codDoc").text = utils.TIPO_COMPROBANTE[factura.cod_doc]
            ETXML.SubElement(infoTributaria, "estab").text = factura.estab
            ETXML.SubElement(infoTributaria, "ptoEmi").text = factura.pto_emi
            ETXML.SubElement(infoTributaria, "secuencial").text = factura.secuencial
            ETXML.SubElement(infoTributaria, "dirMatriz").text = empresa.dir_matriz.decode("utf8")
            # </infoTributaria>

            # <infoFactura>
            infoFactura = ETXML.SubElement(head, "infoFactura")
            ETXML.SubElement(infoFactura, "fechaEmision").text = factura.fecha_emision

            if empresa.dir_establecimiento:
                ETXML.SubElement(infoFactura, "dirEstablecimiento").text = empresa.dir_establecimiento.decode("utf8")
            if empresa.contribuyente_especial:
                ETXML.SubElement(infoFactura, "contribuyenteEspecial").text = empresa.contribuyente_especial
            if empresa.obligado_contabilidad:
                ETXML.SubElement(infoFactura, "obligadoContabilidad").text = empresa.obligado_contabilidad

            ETXML.SubElement(infoFactura, "tipoIdentificacionComprador").text = utils.TIPO_IDENTIFICACION[cliente.tipo_identificacion_comprador]

            if factura.guia_remision:
                ETXML.SubElement(infoFactura, "guiaRemision").text = factura.guia_remision

            ETXML.SubElement(infoFactura, "razonSocialComprador").text = cliente.razon_social_comprador.decode("utf8")
            ETXML.SubElement(infoFactura, "identificacionComprador").text = cliente.identificacion_comprador.replace("-", "")

            if cliente.direccion_comprador:
                ETXML.SubElement(infoFactura, "direccionComprador").text = cliente.direccion_comprador.decode("utf8")

            ETXML.SubElement(infoFactura, "totalSinImpuestos").text = factura.total_sin_impuestos
            ETXML.SubElement(infoFactura, "totalDescuento").text = factura.total_descuento

            # <totalConImpuestos>
            totalConImpuestos = ETXML.SubElement(infoFactura, "totalConImpuestos")

            # <totalImpuesto>
            for i in factura.total_con_impuestos:
                totalImpuesto = ETXML.SubElement(totalConImpuestos, "totalImpuesto")
                ETXML.SubElement(totalImpuesto, "codigo").text = utils.CODIGOS_IMPUESTO[i.codigo]

                if utils.CODIGOS_IMPUESTO[i.codigo] == '2':
                    ETXML.SubElement(totalImpuesto, "codigoPorcentaje").text = utils.TARIFA_IMPUESTOS[str(i.codigo_porcentaje)]
                else:
                    ETXML.SubElement(totalImpuesto, "codigoPorcentaje").text = i.codigo_porcentaje

                if i.descuento_adicional is not None:
                    ETXML.SubElement(totalImpuesto, "descuentoAdicional").text = i.descuento_adicional

                ETXML.SubElement(totalImpuesto, "baseImponible").text = i.base_imponible
                ETXML.SubElement(totalImpuesto, "valor").text = i.valor
            # </totalImpuesto>
            # </totalConImpuestos>

            ETXML.SubElement(infoFactura, "propina").text = factura.propina
            ETXML.SubElement(infoFactura, "importeTotal").text = factura.importe_total
            ETXML.SubElement(infoFactura, "moneda").text = factura.moneda

            # <pagos>
            pagos = ETXML.SubElement(infoFactura, "pagos")

            # <pago>
            for p in factura.pagos:
                pago = ETXML.SubElement(pagos, "pago")

                ETXML.SubElement(pago, "formaPago").text = utils.FORMAS_PAGO[p.forma_pago]
                ETXML.SubElement(pago, "total").text = "%.2f" % p.total

                if p.plazo is not None:
                    ETXML.SubElement(pago, "plazo").text = str(p.plazo)

                if p.unidad_tiempo:
                    ETXML.SubElement(pago, "unidadTiempo").text = p.unidad_tiempo.decode("utf8")
            # </pago>
            # </pagos>

            if factura.valor_ret_iva is not None:
                ETXML.SubElement(infoFactura, "valorRetIva").text = factura.valor_ret_iva

            if factura.valor_ret_renta is not None:
                ETXML.SubElement(infoFactura, "valorRetRenta").text = factura.valor_ret_renta
            # </infoFactura>

            # <detalles>
            detalles = ETXML.SubElement(head, "detalles")

            # <detalle>
            for d in detalle_factura:
                detalle = ETXML.SubElement(detalles, "detalle")
                ETXML.SubElement(detalle, "codigoPrincipal").text = str(d.codigo_principal)

                if d.codigo_auxiliar:
                    ETXML.SubElement(detalle, "codigoAuxiliar").text = str(d.codigo_auxiliar)

                ETXML.SubElement(detalle, "descripcion").text = d.descripcion.decode("utf8")
                ETXML.SubElement(detalle, "cantidad").text = d.cantidad
                ETXML.SubElement(detalle, "precioUnitario").text = d.precio_unitario
                ETXML.SubElement(detalle, "descuento").text = d.descuento
                ETXML.SubElement(detalle, "precioTotalSinImpuesto").text = d.precio_total_sin_impuesto

                # <detallesAdicionales>
                if d.detalles_adicionales:
                    detallesAdicionales = ETXML.SubElement(detalle, "detallesAdicionales")
                    for da in d.detalles_adicionales:
                        ETXML.SubElement(detallesAdicionales, "detAdicional", nombre=da.nombre.decode("utf8"), valor=da.valor.decode("utf8"))
                # </detallesAdicionales>

                # <impuestos>
                impuestos = ETXML.SubElement(detalle, "impuestos")

                # <impuesto>
                for im in d.impuestos:
                    impuesto = ETXML.SubElement(impuestos, "impuesto")
                    ETXML.SubElement(impuesto, "codigo").text = utils.CODIGOS_IMPUESTO[im.codigo]

                    if utils.CODIGOS_IMPUESTO[im.codigo] == '2':
                        ETXML.SubElement(impuesto, "codigoPorcentaje").text = utils.TARIFA_IMPUESTOS[str(im.codigo_porcentaje)]
                    else:
                        ETXML.SubElement(impuesto, "codigoPorcentaje").text = im.codigo_porcentaje

                    ETXML.SubElement(impuesto, "tarifa").text = im.tarifa
                    ETXML.SubElement(impuesto, "baseImponible").text = im.base_imponible
                    ETXML.SubElement(impuesto, "valor").text = im.valor
                # </impuesto>
                # </impuestos>
            # </detalle>
            # </detalles>

            # <infoAdicional>
            if factura.info_adicional:
                infoAdicional = ETXML.SubElement(head, "infoAdicional")
                for ia in factura.info_adicional:
                    ETXML.SubElement(infoAdicional, "campoAdicional", nombre=ia.nombre.decode("utf8")).text = ia.valor.decode("utf8")
            # </infoAdicional>
            # </factura>

            estructura = ETXML.ElementTree(head)
            return True, estructura
        else:
            return False, validaciones
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            'line': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'type': exc_type.__name__,
            'message': exc_value.message,  # or see traceback._some_str()
        }

        print (traceback_details)
        return False, 'No se ha podido crear el archivo XML. Error: ' + ex.message

def Crear_XML_Retencion(empresa, proveedor, retencion, detalle_retencion):
    try:
        validaciones = Validar_Datos(empresa, proveedor, retencion, detalle_retencion)

        if(validaciones['result'] == "OK"):
            empresa = validaciones['empresa']
            retencion = validaciones['documento']
            detalle_retencion = validaciones['detalle_documento']

            # <comprobanteRetencion id="comprobante" version="1.0.0">
            head = ETXML.Element("comprobanteRetencion", id=retencion.id, version=retencion.version)

            # <infoTributaria>
            infoTributaria = ETXML.SubElement(head, "infoTributaria")
            ETXML.SubElement(infoTributaria, "ambiente").text = utils.TIPO_AMBIENTE[retencion.ambiente]
            ETXML.SubElement(infoTributaria, "tipoEmision").text = utils.TIPO_EMISION[retencion.tipo_emision]
            ETXML.SubElement(infoTributaria, "razonSocial").text = empresa.razon_social.decode("utf8")

            if empresa.nombre_comercial:
                ETXML.SubElement(infoTributaria, "nombreComercial").text = empresa.nombre_comercial.decode("utf8")

            ETXML.SubElement(infoTributaria, "ruc").text = empresa.ruc
            ETXML.SubElement(infoTributaria, "claveAcceso").text = retencion.clave_acceso
            ETXML.SubElement(infoTributaria, "codDoc").text = utils.TIPO_COMPROBANTE[retencion.cod_doc]
            ETXML.SubElement(infoTributaria, "estab").text = retencion.estab
            ETXML.SubElement(infoTributaria, "ptoEmi").text = retencion.pto_emi
            ETXML.SubElement(infoTributaria, "secuencial").text = retencion.secuencial
            ETXML.SubElement(infoTributaria, "dirMatriz").text = empresa.dir_matriz.decode("utf8")
            # </infoTributaria>

            # <infoCompRetencion>
            infoCompRetencion = ETXML.SubElement(head, "infoCompRetencion")
            ETXML.SubElement(infoCompRetencion, "fechaEmision").text = retencion.fecha_emision

            if empresa.dir_establecimiento:
                ETXML.SubElement(infoCompRetencion, "dirEstablecimiento").text = empresa.dir_establecimiento.decode("utf8")
            if empresa.contribuyente_especial:
                ETXML.SubElement(infoCompRetencion, "contribuyenteEspecial").text = empresa.contribuyente_especial
            if empresa.obligado_contabilidad:
                ETXML.SubElement(infoCompRetencion, "obligadoContabilidad").text = empresa.obligado_contabilidad

            ETXML.SubElement(infoCompRetencion, "tipoIdentificacionSujetoRetenido").text = utils.TIPO_IDENTIFICACION[proveedor.tipo_identificacion]
            ETXML.SubElement(infoCompRetencion, "razonSocialSujetoRetenido").text = proveedor.razon_social.decode("utf8")
            ETXML.SubElement(infoCompRetencion, "identificacionSujetoRetenido").text = proveedor.identificacion.replace("-", "")
            ETXML.SubElement(infoCompRetencion, "periodoFiscal").text = retencion.periodo_fiscal
            # </infoCompRetencion>

            # <impuestos>
            impuestos = ETXML.SubElement(head, "impuestos")

            # <impuesto>
            for im in detalle_retencion:
                impuesto = ETXML.SubElement(impuestos, "impuesto")
                ETXML.SubElement(impuesto, "codigo").text = utils.IMPUESTO_A_RETENER[im.codigo]

                if utils.IMPUESTO_A_RETENER[im.codigo] == '2':
                    ETXML.SubElement(impuesto, "codigoRetencion").text = utils.RETENCION_IVA[str(im.codigo_porcentaje)]
                elif utils.IMPUESTO_A_RETENER[im.codigo] == '6':
                    ETXML.SubElement(impuesto, "codigoRetencion").text = utils.RETENCION_ISD[str(im.codigo_porcentaje)]
                else:
                    ETXML.SubElement(impuesto, "codigoRetencion").text = im.codigo_porcentaje

                ETXML.SubElement(impuesto, "baseImponible").text = str(im.base_imponible)
                ETXML.SubElement(impuesto, "porcentajeRetener").text = str(im.porcentaje_retener)
                ETXML.SubElement(impuesto, "valorRetenido").text = str(im.valor)
                ETXML.SubElement(impuesto, "codDocSustento").text = utils.TIPO_COMPROBANTE[retencion.cod_doc_sustento]

                if retencion.num_doc_sustento:
                    ETXML.SubElement(impuesto, "numDocSustento").text = retencion.num_doc_sustento

                if retencion.fecha_doc_sustento:
                    ETXML.SubElement(impuesto, "fechaEmisionDocSustento").text = retencion.fecha_doc_sustento
            # </impuesto>
            # </impuestos>

            # <infoAdicional>
            if retencion.info_adicional:
                infoAdicional = ETXML.SubElement(head, "infoAdicional")
                for ia in retencion.info_adicional:
                    ETXML.SubElement(infoAdicional, "campoAdicional", nombre=ia.nombre.decode("utf8")).text = ia.valor.decode("utf8")
            # </infoAdicional>
            # </comprobanteRetencion>

            estructura = ETXML.ElementTree(head)
            return True, estructura
        else:
            return False, validaciones
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            'line': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'type': exc_type.__name__,
            'message': exc_value.message,
        }

        print (traceback_details)
        return False, 'No se ha podido crear el archivo XML. Error: ' + ex.message

def Crear_XML_Guia_Remision(empresa, transportista, guia, detalle_destinatarios):
    try:
        validaciones = Validar_Datos(empresa, transportista, guia, detalle_destinatarios)

        if(validaciones['result'] == "OK"):
            empresa = validaciones['empresa']
            guia = validaciones['documento']
            detalle_destinatarios = validaciones['detalle_documento']

            # <guiaRemision id="comprobante" version="1.0.0">
            head = ETXML.Element("guiaRemision", id=guia.id, version=guia.version)

            # <infoTributaria>
            infoTributaria = ETXML.SubElement(head, "infoTributaria")
            ETXML.SubElement(infoTributaria, "ambiente").text = utils.TIPO_AMBIENTE[guia.ambiente]
            ETXML.SubElement(infoTributaria, "tipoEmision").text = utils.TIPO_EMISION[guia.tipo_emision]
            ETXML.SubElement(infoTributaria, "razonSocial").text = empresa.razon_social.decode("utf8")

            if empresa.nombre_comercial:
                ETXML.SubElement(infoTributaria, "nombreComercial").text = empresa.nombre_comercial.decode("utf8")

            ETXML.SubElement(infoTributaria, "ruc").text = empresa.ruc
            ETXML.SubElement(infoTributaria, "claveAcceso").text = guia.clave_acceso
            ETXML.SubElement(infoTributaria, "codDoc").text = utils.TIPO_COMPROBANTE[guia.cod_doc]
            ETXML.SubElement(infoTributaria, "estab").text = guia.estab
            ETXML.SubElement(infoTributaria, "ptoEmi").text = guia.pto_emi
            ETXML.SubElement(infoTributaria, "secuencial").text = guia.secuencial
            ETXML.SubElement(infoTributaria, "dirMatriz").text = empresa.dir_matriz.decode("utf8")
            # </infoTributaria>

            # <infoGuiaRemision>
            infoGuiaRemision = ETXML.SubElement(head, "infoGuiaRemision")

            if empresa.dir_establecimiento:
                ETXML.SubElement(infoGuiaRemision, "dirEstablecimiento").text = empresa.dir_establecimiento.decode("utf8")

            ETXML.SubElement(infoGuiaRemision, "dirPartida").text = guia.direccion_partida.decode("utf8")
            ETXML.SubElement(infoGuiaRemision, "razonSocialTransportista").text = transportista.razon_social.decode("utf8")
            ETXML.SubElement(infoGuiaRemision, "tipoIdentificacionTransportista").text = utils.TIPO_IDENTIFICACION[transportista.tipo_identificacion]
            ETXML.SubElement(infoGuiaRemision, "rucTransportista").text = transportista.identificacion.replace("-", "")

            if transportista.rise:
                ETXML.SubElement(infoGuiaRemision, "rise").text = transportista.rise
            if empresa.obligado_contabilidad:
                ETXML.SubElement(infoGuiaRemision, "obligadoContabilidad").text = empresa.obligado_contabilidad
            if empresa.contribuyente_especial:
                ETXML.SubElement(infoGuiaRemision, "contribuyenteEspecial").text = empresa.contribuyente_especial

            ETXML.SubElement(infoGuiaRemision, "fechaIniTransporte").text = guia.fecha_inicio_transporte
            ETXML.SubElement(infoGuiaRemision, "fechaFinTransporte").text = guia.fecha_fin_transporte
            ETXML.SubElement(infoGuiaRemision, "placa").text = transportista.placa
            # </infoGuiaRemision>

            # <destinatarios>
            destinatarios = ETXML.SubElement(head, "destinatarios")

            # <destinatario>
            for de in detalle_destinatarios:
                destinatario = ETXML.SubElement(destinatarios, "destinatario")
                ETXML.SubElement(destinatario, "identificacionDestinatario").text = de.identificacion
                ETXML.SubElement(destinatario, "razonSocialDestinatario").text = de.razon_social.decode("utf8")
                ETXML.SubElement(destinatario, "dirDestinatario").text = de.direccion.decode("utf8")
                ETXML.SubElement(destinatario, "motivoTraslado").text = de.motivo_traslado.decode("utf8")

                if de.documento_aduanero_unico:
                    ETXML.SubElement(destinatario, "docAduaneroUnico").text = de.documento_aduanero_unico
                if de.cod_establecimiento_destino:
                    ETXML.SubElement(destinatario, "codEstabDestino").text = de.cod_establecimiento_destino
                if de.ruta:
                    ETXML.SubElement(destinatario, "ruta").text = de.ruta
                if de.cod_doc_sustento:
                    ETXML.SubElement(destinatario, "codDocSustento").text = utils.TIPO_COMPROBANTE[de.cod_doc_sustento]
                if de.num_doc_sustento:
                    ETXML.SubElement(destinatario, "numDocSustento").text = de.num_doc_sustento
                if de.num_autorizacion_doc_sustento:
                    ETXML.SubElement(destinatario, "numAutDocSustento").text = de.num_autorizacion_doc_sustento
                if de.fecha_doc_sustento:
                    ETXML.SubElement(destinatario, "fechaEmisionDocSustento").text = de.fecha_doc_sustento

                # <detalles>
                detalles = ETXML.SubElement(destinatario, "detalles")

                # <detalle>
                for x in de.detalles:
                    detalle = ETXML.SubElement(detalles, "detalle")

                    if x.codigo_principal:
                        ETXML.SubElement(detalle, "codigoInterno").text = x.codigo_principal
                    if x.codigo_auxiliar:
                        ETXML.SubElement(detalle, "codigoAdicional").text = x.codigo_auxiliar

                    ETXML.SubElement(detalle, "descripcion").text = x.descripcion
                    ETXML.SubElement(detalle, "cantidad").text = x.cantidad

                    # <detallesAdicionales>
                    if x.detalles_adicionales:
                        detallesAdicionales = ETXML.SubElement(detalle, "detallesAdicionales")
                        for da in x.detalles_adicionales:
                            ETXML.SubElement(detallesAdicionales, "detAdicional", nombre=da.nombre.decode("utf8"), valor=da.valor.decode("utf8"))
                    # </detallesAdicionales>
                # </detalle>
                # </detalles>
            # </destinatario>
            # </destinatarios>

            # <infoAdicional>
            if guia.info_adicional:
                infoAdicional = ETXML.SubElement(head, "infoAdicional")
                for ia in guia.info_adicional:
                    ETXML.SubElement(infoAdicional, "campoAdicional", nombre=ia.nombre.decode("utf8")).text = ia.valor.decode("utf8")
            # </infoAdicional>
            # </guiaRemision>

            estructura = ETXML.ElementTree(head)
            return True, estructura
        else:
            return False, validaciones['result']
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            'line': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'type': exc_type.__name__,
            'message': exc_value.message,
        }

        print (traceback_details)
        return False, 'No se ha podido crear el archivo XML. Error: ' + ex.message

def Crear_XML_Nota_Credito(empresa, proveedor, nota, detalle_nota):
    try:
        validaciones = Validar_Datos(empresa, proveedor, nota, detalle_nota)

        if(validaciones['result'] == "OK"):
            empresa = validaciones['empresa']
            proveedor = validaciones['sujeto']
            nota = validaciones['documento']
            detalle_nota = validaciones['detalle_documento']

            # <notaCredito id="comprobante" version="1.0.0">
            head = ETXML.Element("notaCredito", id=nota.id, version=nota.version)

            # <infoTributaria>
            infoTributaria = ETXML.SubElement(head, "infoTributaria")
            ETXML.SubElement(infoTributaria, "ambiente").text = utils.TIPO_AMBIENTE[nota.ambiente]
            ETXML.SubElement(infoTributaria, "tipoEmision").text = utils.TIPO_EMISION[nota.tipo_emision]
            ETXML.SubElement(infoTributaria, "razonSocial").text = empresa.razon_social.decode("utf8")

            if empresa.nombre_comercial:
                ETXML.SubElement(infoTributaria, "nombreComercial").text = empresa.nombre_comercial.decode("utf8")

            ETXML.SubElement(infoTributaria, "ruc").text = empresa.ruc
            ETXML.SubElement(infoTributaria, "claveAcceso").text = nota.clave_acceso
            ETXML.SubElement(infoTributaria, "codDoc").text = utils.TIPO_COMPROBANTE[nota.cod_doc]
            ETXML.SubElement(infoTributaria, "estab").text = nota.estab
            ETXML.SubElement(infoTributaria, "ptoEmi").text = nota.pto_emi
            ETXML.SubElement(infoTributaria, "secuencial").text = nota.secuencial
            ETXML.SubElement(infoTributaria, "dirMatriz").text = empresa.dir_matriz.decode("utf8")
            # </infoTributaria>

            # <infoNotaCredito>
            infoNotaCredito = ETXML.SubElement(head, "infoNotaCredito")
            ETXML.SubElement(infoNotaCredito, "fechaEmision").text = nota.fecha_emision

            if empresa.dir_establecimiento:
                ETXML.SubElement(infoNotaCredito, "dirEstablecimiento").text = empresa.dir_establecimiento.decode("utf8")

            ETXML.SubElement(infoNotaCredito, "tipoIdentificacionComprador").text = utils.TIPO_IDENTIFICACION[proveedor.tipo_identificacion]
            ETXML.SubElement(infoNotaCredito, "razonSocialComprador").text = proveedor.razon_social.decode("utf8")
            ETXML.SubElement(infoNotaCredito, "identificacionComprador").text = proveedor.identificacion.replace("-", "")

            if empresa.contribuyente_especial:
                ETXML.SubElement(infoNotaCredito, "contribuyenteEspecial").text = empresa.contribuyente_especial
            if empresa.obligado_contabilidad:
                ETXML.SubElement(infoNotaCredito, "obligadoContabilidad").text = empresa.obligado_contabilidad

            if proveedor.rise:
                ETXML.SubElement(infoNotaCredito, "rise").text = proveedor.rise

            ETXML.SubElement(infoNotaCredito, "codDocModificado").text = utils.TIPO_COMPROBANTE[nota.cod_doc_sustento]
            ETXML.SubElement(infoNotaCredito, "numDocModificado").text = nota.num_doc_sustento
            ETXML.SubElement(infoNotaCredito, "fechaEmisionDocSustento").text = nota.fecha_doc_sustento
            ETXML.SubElement(infoNotaCredito, "totalSinImpuestos").text = nota.total_sin_impuestos
            ETXML.SubElement(infoNotaCredito, "valorModificacion").text = nota.valor_modificacion
            ETXML.SubElement(infoNotaCredito, "moneda").text = nota.moneda

            # <totalConImpuestos>
            totalConImpuestos = ETXML.SubElement(infoNotaCredito, "totalConImpuestos")

            # <totalImpuesto>
            for i in nota.total_con_impuestos:
                totalImpuesto = ETXML.SubElement(totalConImpuestos, "totalImpuesto")
                ETXML.SubElement(totalImpuesto, "codigo").text = utils.CODIGOS_IMPUESTO[i.codigo]

                if utils.CODIGOS_IMPUESTO[i.codigo] == '2':
                    ETXML.SubElement(totalImpuesto, "codigoPorcentaje").text = utils.TARIFA_IMPUESTOS[str(i.codigo_porcentaje)]
                else:
                    ETXML.SubElement(totalImpuesto, "codigoPorcentaje").text = i.codigo_porcentaje

                ETXML.SubElement(totalImpuesto, "baseImponible").text = i.base_imponible
                ETXML.SubElement(totalImpuesto, "valor").text = i.valor
            # </totalImpuesto>
            # </totalConImpuestos>

            ETXML.SubElement(infoNotaCredito, "motivo").text = nota.motivo
            # </infoNotaCredito>

            # <detalles>
            detalles = ETXML.SubElement(head, "detalles")

            # <detalle>
            for d in detalle_nota:
                detalle = ETXML.SubElement(detalles, "detalle")
                ETXML.SubElement(detalle, "codigoInterno").text = str(d.codigo_principal)

                if d.codigo_auxiliar:
                    ETXML.SubElement(detalle, "codigoAdicional").text = str(d.codigo_auxiliar)

                ETXML.SubElement(detalle, "descripcion").text = d.descripcion.decode("utf8")
                ETXML.SubElement(detalle, "cantidad").text = d.cantidad
                ETXML.SubElement(detalle, "precioUnitario").text = d.precio_unitario

                if d.descuento is None:
                    d.descuento = '0.00'

                ETXML.SubElement(detalle, "descuento").text = d.descuento
                ETXML.SubElement(detalle, "precioTotalSinImpuesto").text = d.precio_total_sin_impuesto

                # <detallesAdicionales>
                if d.detalles_adicionales:
                    detallesAdicionales = ETXML.SubElement(detalle, "detallesAdicionales")
                    for da in d.detalles_adicionales:
                        ETXML.SubElement(detallesAdicionales, "detAdicional", nombre=da.nombre.decode("utf8"), valor=da.valor.decode("utf8"))
                # </detallesAdicionales>

                # <impuestos>
                impuestos = ETXML.SubElement(detalle, "impuestos")

                # <impuesto>
                for im in d.impuestos:
                    impuesto = ETXML.SubElement(impuestos, "impuesto")
                    ETXML.SubElement(impuesto, "codigo").text = utils.CODIGOS_IMPUESTO[im.codigo]

                    if utils.CODIGOS_IMPUESTO[im.codigo] == '2':
                        ETXML.SubElement(impuesto, "codigoPorcentaje").text = utils.TARIFA_IMPUESTOS[str(im.codigo_porcentaje)]
                    else:
                        ETXML.SubElement(impuesto, "codigoPorcentaje").text = im.codigo_porcentaje

                    if im.tarifa is None:
                        im.tarifa = '0.00'

                    ETXML.SubElement(impuesto, "tarifa").text = im.tarifa
                    ETXML.SubElement(impuesto, "baseImponible").text = im.base_imponible
                    ETXML.SubElement(impuesto, "valor").text = im.valor
                # </impuesto>
                # </impuestos>
            # </detalle>
            # </detalles>

            # <infoAdicional>
            if nota.info_adicional:
                infoAdicional = ETXML.SubElement(head, "infoAdicional")
                for ia in nota.info_adicional:
                    ETXML.SubElement(infoAdicional, "campoAdicional", nombre=ia.nombre.decode("utf8")).text = ia.valor.decode("utf8")
            # </infoAdicional>
            # </notaCredito>

            estructura = ETXML.ElementTree(head)
            return True, estructura
        else:
            return False, validaciones
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            'line': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'type': exc_type.__name__,
            'message': exc_value.message
        }

        print (traceback_details)
        return False, 'No se ha podido crear el archivo XML. Error: ' + ex.message

def Crear_XML_Nota_Debito(empresa, cliente, nota, detalle_nota):
    try:
        validaciones = Validar_Datos(empresa, cliente, nota, detalle_nota)

        if(validaciones['result'] == "OK"):
            empresa = validaciones['empresa']
            cliente = validaciones['sujeto']
            nota = validaciones['documento']
            detalle_nota = validaciones['detalle_documento']

            # <notaDebito id="comprobante" version="1.0.0">
            head = ETXML.Element("notaDebito", id=nota.id, version=nota.version)

            # <infoTributaria>
            infoTributaria = ETXML.SubElement(head, "infoTributaria")
            ETXML.SubElement(infoTributaria, "ambiente").text = utils.TIPO_AMBIENTE[nota.ambiente]
            ETXML.SubElement(infoTributaria, "tipoEmision").text = utils.TIPO_EMISION[nota.tipo_emision]
            ETXML.SubElement(infoTributaria, "razonSocial").text = empresa.razon_social.decode("utf8")

            if empresa.nombre_comercial:
                ETXML.SubElement(infoTributaria, "nombreComercial").text = empresa.nombre_comercial.decode("utf8")

            ETXML.SubElement(infoTributaria, "ruc").text = empresa.ruc
            ETXML.SubElement(infoTributaria, "claveAcceso").text = nota.clave_acceso
            ETXML.SubElement(infoTributaria, "codDoc").text = utils.TIPO_COMPROBANTE[nota.cod_doc]
            ETXML.SubElement(infoTributaria, "estab").text = nota.estab
            ETXML.SubElement(infoTributaria, "ptoEmi").text = nota.pto_emi
            ETXML.SubElement(infoTributaria, "secuencial").text = nota.secuencial
            ETXML.SubElement(infoTributaria, "dirMatriz").text = empresa.dir_matriz.decode("utf8")
            # </infoTributaria>

            # <infoNotaDebito>
            infoNotaDebito = ETXML.SubElement(head, "infoNotaDebito")
            ETXML.SubElement(infoNotaDebito, "fechaEmision").text = nota.fecha_emision

            if empresa.dir_establecimiento:
                ETXML.SubElement(infoNotaDebito, "dirEstablecimiento").text = empresa.dir_establecimiento.decode("utf8")

            ETXML.SubElement(infoNotaDebito, "tipoIdentificacionComprador").text = utils.TIPO_IDENTIFICACION[cliente.tipo_identificacion_comprador]
            ETXML.SubElement(infoNotaDebito, "razonSocialComprador").text = cliente.razon_social_comprador.decode("utf8")
            ETXML.SubElement(infoNotaDebito, "identificacionComprador").text = cliente.identificacion_comprador.replace("-", "")

            if empresa.contribuyente_especial:
                ETXML.SubElement(infoNotaDebito, "contribuyenteEspecial").text = empresa.contribuyente_especial
            if empresa.obligado_contabilidad:
                ETXML.SubElement(infoNotaDebito, "obligadoContabilidad").text = empresa.obligado_contabilidad

            ETXML.SubElement(infoNotaDebito, "codDocModificado").text = utils.TIPO_COMPROBANTE[nota.cod_doc_sustento]
            ETXML.SubElement(infoNotaDebito, "numDocModificado").text = nota.num_doc_sustento
            ETXML.SubElement(infoNotaDebito, "fechaEmisionDocSustento").text = nota.fecha_doc_sustento
            ETXML.SubElement(infoNotaDebito, "totalSinImpuestos").text = nota.total_sin_impuestos

            # <impuestos>
            impuestos = ETXML.SubElement(infoNotaDebito, "impuestos")

            # <impuesto>
            for im in nota.total_con_impuestos:
                impuesto = ETXML.SubElement(impuestos, "impuesto")
                ETXML.SubElement(impuesto, "codigo").text = utils.CODIGOS_IMPUESTO[im.codigo]

                if utils.CODIGOS_IMPUESTO[im.codigo] == '2':
                    ETXML.SubElement(impuesto, "codigoPorcentaje").text = utils.TARIFA_IMPUESTOS[str(im.codigo_porcentaje)]
                else:
                    ETXML.SubElement(impuesto, "codigoPorcentaje").text = im.codigo_porcentaje

                ETXML.SubElement(impuesto, "tarifa").text = im.tarifa
                ETXML.SubElement(impuesto, "baseImponible").text = im.base_imponible
                ETXML.SubElement(impuesto, "valor").text = im.valor
            # </impuesto>
            # </impuestos>

            ETXML.SubElement(infoNotaDebito, "valorTotal").text = nota.importe_total

            # <pagos>
            pagos = ETXML.SubElement(infoNotaDebito, "pagos")

            # <pago>
            for p in nota.pagos:
                pago = ETXML.SubElement(pagos, "pago")

                ETXML.SubElement(pago, "formaPago").text = utils.FORMAS_PAGO[p.forma_pago]
                ETXML.SubElement(pago, "total").text = "%.2f" % p.total

                if p.plazo is not None:
                    ETXML.SubElement(pago, "plazo").text = str(p.plazo)

                if p.unidad_tiempo:
                    ETXML.SubElement(pago, "unidadTiempo").text = p.unidad_tiempo.decode("utf8")
            # </pago>
            # </pagos>
            # </infoNotaDebito>

            # <motivos>
            motivos = ETXML.SubElement(head, "motivos")

            # <motivo>
            for dn in detalle_nota:
                motivo = ETXML.SubElement(motivos, "motivo")
                ETXML.SubElement(motivo, "razon").text = dn.razon.decode("utf8")
                ETXML.SubElement(motivo, "valor").text = dn.valor
            # </motivo>
            # </motivos>

            # <infoAdicional>
            if nota.info_adicional:
                infoAdicional = ETXML.SubElement(head, "infoAdicional")
                for ia in nota.info_adicional:
                    ETXML.SubElement(infoAdicional, "campoAdicional", nombre=ia.nombre.decode("utf8")).text = ia.valor.decode("utf8")
            # </infoAdicional>
            # </notaDebito>

            estructura = ETXML.ElementTree(head)
            return True, estructura
        else:
            return False, validaciones
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            'line': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'type': exc_type.__name__,
            'message': exc_value.message
        }

        print (traceback_details)
        return False, 'No se ha podido crear el archivo XML. Error: ' + ex.message