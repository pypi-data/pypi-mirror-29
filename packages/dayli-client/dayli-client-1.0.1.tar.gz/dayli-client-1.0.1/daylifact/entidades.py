# -*- coding: utf-8 -*-
from daylifact.utils import CODIGO_NUMERICO

class Empresa(object):
    def __init__(self, razon_social = None, ruc = None, dir_matriz = None):
        self.razon_social = razon_social
        self.ruc = ruc
        self.dir_matriz = dir_matriz
        self.nombre_comercial = None
        self.dir_establecimiento = None
        self.contribuyente_especial = None
        self.obligado_contabilidad = None
        self.credencial = None #Para firmar archivo xml
        self.password = None #Para firmar archivo xml

class Cliente(object):
    def __init__(self, tipo_identificacion_comprador = None, razon_social_comprador = None, identificacion_comprador = None):
        self.tipo_identificacion_comprador = tipo_identificacion_comprador
        self.razon_social_comprador = razon_social_comprador
        self.identificacion_comprador = identificacion_comprador
        self.direccion_comprador = None
        self.telefono = None
        self.email = None

class Proveedor(object):
    def __init__(self, tipo_identificacion=None, razon_social=None,
                 identificacion=None, rise=None):
        self.tipo_identificacion = tipo_identificacion
        self.razon_social = razon_social
        self.identificacion = identificacion
        self.rise = rise
        self.telefono = None
        self.email = None

class Transportista(object):
    def __init__(self, razon_social=None, tipo_identificacion=None,
                 identificacion=None, rise=None):
        self.razon_social = razon_social
        self.tipo_identificacion = tipo_identificacion
        self.identificacion = identificacion
        self.rise = rise
        self.placa = None
        self.email = None

class Comprobante(object):
    id = "comprobante"
    version = "1.0.0"
    moneda = "DOLAR"

    def __init__(self, ambiente = 'pruebas', cod_doc = None):
        self.ambiente = ambiente
        self.cod_doc = cod_doc
        self.tipo_emision = None
        self.clave_acceso = None
        self.estab = None
        self.pto_emi = None
        self.secuencial = None
        self.fecha_emision = None
        self.guia_remision = None
        self.total_sin_impuestos = None
        self.total_descuento = None
        self.total_con_impuestos = []
        self.propina = None
        self.importe_total = None
        self.pagos = []
        self.valor_ret_iva = None
        self.valor_ret_renta = None
        self.info_adicional = []

        # Para retenciones
        self.periodo_fiscal = None
        self.cod_doc_sustento = None
        self.num_doc_sustento = None
        self.fecha_doc_sustento = None

        # Para guia de remision
        self.direccion_partida = None
        self.fecha_inicio_transporte = None
        self.fecha_fin_transporte = None

        # Para nota de crédito
        self.valor_modificacion = None
        self.motivo = None

        # Sirve para construir la clave de acceso una vez validados todos los datos de la factura
        self.codigo_numerico = CODIGO_NUMERICO # Un código de 8 números cualquiera

class Detalle_Comprobante(object):
    def __init__(self):
        self.codigo_principal = None
        self.codigo_auxiliar = None
        self.descripcion = None
        self.cantidad = None
        self.precio_unitario = None
        self.descuento = None
        self.precio_total_sin_impuesto = None
        self.detalles_adicionales = []
        self.impuestos = []

class Impuesto(object):
    def __init__(self):
        self.codigo = None
        self.codigo_porcentaje = None
        self.tarifa = None
        self.base_imponible = None
        self.descuento_adicional = None
        self.valor = None
        self.porcentaje_retener = None # Para retención únicamente

class Motivo(object):
    def __init__(self, razon = None, valor = None):
        self.razon = razon
        self.valor = valor

class Destinatario(object):
    def __init__(self):
        self.identificacion = None
        self.razon_social = None
        self.direccion = None
        self.motivo_traslado = None
        self.documento_aduanero_unico = None
        self.cod_establecimiento_destino = None
        self.ruta = None
        self.cod_doc_sustento = None
        self.num_doc_sustento = None
        self.num_autorizacion_doc_sustento = None
        self.fecha_doc_sustento = None
        self.detalles = []

class Pago(object):
    def __init__(self):
        self.forma_pago = None
        self.total = None
        self.plazo = None
        self.unidad_tiempo = None

class Detalle_Adicional(object):
    def __init__(self, nombre = None, valor = None):
        self.nombre = nombre
        self.valor = valor