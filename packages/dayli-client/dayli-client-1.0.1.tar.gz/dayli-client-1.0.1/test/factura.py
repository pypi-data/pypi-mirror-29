# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from daylifact.entidades import *
from daylifact.autorizar import Autorizar_Documento

"""
TEST AUTORIZAR UNA FACTURA DE VENTA
"""

# Retorna una lista de entidades del tipo Impuesto
def Formato_Total_Con_Impuestos():
    # ETIQUETA XML: <totalConImpuestos>
    # Apartado Total con impuestos (Por toda la factura)

    # Simulación de los impuestos en la factura
    total_con_impuestos = []

    # 'codigo': Nombre del impuesto: iva (IVA 0% e IVA 12%) | ice (ICE %) | irbpnr
    # 'codigo_porcentaje': Porcentaje de IVA únicamente (0, 12, 14...) ** la tarifa ICE tiene sus propios códigos (VER TABLA 19 SRI) *** la tarifa IRBPNR tiene sus propios códigos
    # 'descuento_adicional': Opcional solo aplica para codigo iva

    imp1 = Impuesto()
    imp1.codigo = 'iva'
    imp1.codigo_porcentaje = 'noiva' #Puede ser int o str
    imp1.descuento_adicional = None # Opcional solo aplica para código iva.
    imp1.base_imponible = 15
    imp1.valor = 0

    imp2 = Impuesto()
    imp2.codigo = 'iva'
    imp2.codigo_porcentaje = 'excento' #Puede ser int o str
    imp2.descuento_adicional = None  # Opcional solo aplica para código iva.
    imp2.base_imponible = 4
    imp2.valor = 0

    imp3 = Impuesto()
    imp3.codigo = 'ice'
    imp3.codigo_porcentaje = 3011 #Puede ser int o str
    imp3.base_imponible = 14
    imp3.valor = 5

    imp4 = Impuesto()
    imp4.codigo = 'irbpnr'
    imp4.codigo_porcentaje = 5001 #Puede ser int o str
    imp4.base_imponible = 0
    imp4.valor = 4

    total_con_impuestos.append(imp1)
    total_con_impuestos.append(imp2)
    total_con_impuestos.append(imp3)
    total_con_impuestos.append(imp4)

    return total_con_impuestos

# Retorna una lista de entidades del tipo Detalle_Adicional
def Formato_Info_Adicional():
    # ETIQUETA XML: <infoAdicional>
    # Apartado info adicional (OPCIONAL)

    # Simulación de la info adicional
    info_adicional = []

    inf1 = Detalle_Adicional('Direccion', 'NADA')
    inf2 = Detalle_Adicional('Email', 'asdas@gmail.com')

    info_adicional.append(inf1)
    info_adicional.append(inf2)

    return info_adicional

# Retorna una lista de entidades del tipo Detalle_Adicional
def Detalle_Adicional_Prod1():
    # ETIQUETA XML: <detallesAdicionales>
    # Apartado detalles adicionales del producto(OPCIONAL)

    # Simulación de los detalles adicionales (En caso de tenerlos)
    detalles_adicionales_prod1 = []

    det_prod1_1 = Detalle_Adicional('Marca Chevrolet', 'Chevrolet')
    det_prod1_2 = Detalle_Adicional('Modelo', '2012')

    detalles_adicionales_prod1.append(det_prod1_1)
    detalles_adicionales_prod1.append(det_prod1_2)

    return  detalles_adicionales_prod1

# Retorna una lista de entidades del tipo Impuesto
def Impuestos_Prod1():
    # ETIQUETA XML: <impuestos>
    # Apartado impuestos (Por cada producto en el detalle de la factura)

    # Simulación de los impuestos en el detalle
    impuestos = []

    # 'codigo': Nombre del impuesto: iva (IVA 0% e IVA 12%) | ice (ICE %) | irbpnr
    # 'codigo_porcentaje': Porcentaje de IVA únicamente (0, 12, 14...) ** la tarifa ICE tiene sus propios códigos (VER TABLA 19 SRI) *** la tarifa IRBPNR tiene sus propios códigos

    imp1 = Impuesto()
    imp1.codigo = 'ice'
    imp1.codigo_porcentaje = 3011 #Puede ser int o str
    imp1.tarifa = 0
    imp1.base_imponible = 2
    imp1.valor = 2

    imp2 = Impuesto()
    imp2.codigo = 'iva'
    imp2.codigo_porcentaje = 'excento' #Puede ser int o str
    imp2.tarifa = 0
    imp2.base_imponible = 4
    imp2.valor = 0

    imp3 = Impuesto()
    imp3.codigo = 'irbpnr'
    imp3.codigo_porcentaje = 5001 #Puede ser int o str
    imp3.tarifa = 0
    imp3.base_imponible = 0
    imp3.valor = 1

    impuestos.append(imp1)
    impuestos.append(imp2)
    impuestos.append(imp3)

    return impuestos

# Retorna una lista de entidades del tipo Impuesto
def Impuestos_Prod2():
    # ETIQUETA XML: <impuestos>
    # Apartado impuestos (Por cada producto en el detalle de la factura)

    # Simulación de los impuestos en el detalle
    impuestos = []

    # 'codigo': Nombre del impuesto: iva (IVA 0% e IVA 12%) | ice (ICE %) | irbpnr
    # 'codigo_porcentaje': Porcentaje de IVA únicamente (0, 12, 14...) ** la tarifa ICE tiene sus propios códigos (VER TABLA 19 SRI) *** la tarifa IRBPNR tiene sus propios códigos

    imp1 = Impuesto()
    imp1.codigo = 'iva'
    imp1.codigo_porcentaje = 'noiva' #Puede ser int o str
    imp1.tarifa = 0
    imp1.base_imponible = 15
    imp1.valor = 0

    imp2 = Impuesto()
    imp2.codigo = 'ice'
    imp2.codigo_porcentaje = 3011 #Puede ser int o str
    imp2.tarifa = 0
    imp2.base_imponible = 12
    imp2.valor = 3

    imp3 = Impuesto()
    imp3.codigo = 'irbpnr'
    imp3.codigo_porcentaje = 5001 #Puede ser int o str
    imp3.tarifa = 0
    imp3.base_imponible = 0
    imp3.valor = 3

    impuestos.append(imp1)
    impuestos.append(imp2)
    impuestos.append(imp3)

    return impuestos

# Retorna una lista de entidades del tipo Detalle_Comprobante
def Formato_Detalle_Factura():
    # ETIQUETA XML: <detalles>
    # Apartado detalle de cada producto

    productos = []

    # Simulacion de productos en el detalle
    # ------------ Producto 1 -------------
    prod1 = Detalle_Comprobante()
    prod1.codigo_principal = 'AUX1'
    prod1.codigo_auxiliar = 'UAX2'  # Opcional
    prod1.descripcion = 'Prueba 3333'
    prod1.cantidad =  1
    prod1.precio_unitario = 2
    prod1.descuento = 0
    prod1.precio_total_sin_impuesto = 2
    #prod1.detalles_adicionales = Detalle_Adicional_Prod1() # Opcional
    prod1.impuestos = Impuestos_Prod1()

    # ------------ Producto 2 -------------
    prod2 = Detalle_Comprobante()
    prod2.codigo_principal = '2'
    prod2.codigo_auxiliar = '23'  # Opcional
    prod2.descripcion = 'PRUEBA 2'
    prod2.cantidad = 1
    prod2.precio_unitario = 12
    prod2.descuento = 0
    prod2.precio_total_sin_impuesto = 12
    prod2.impuestos = Impuestos_Prod2()

    productos.append(prod1)
    productos.append(prod2)

    return productos

# Retorna una lista de entidades del tipo Pago
def Formato_Pagos():
    # ETIQUETA XML: <pagos>
    # Apartado forma de pago de la factura

    pagos = []

    # Simulacion de formas de pago

    # ------ FORMAS DE PAGO VALIDAS ------
    # 'efectivo': SIN UTILIZACION DEL SISTEMA FINANCIERO
    # 'deudas': COMPENSACIÓN DE DEUDAS
    # 'debito': TARJETA DE DÉBITO
    # 'electronico': DINERO ELECTRÓNICO
    # 'prepago': TARJETA PREPAGO
    # 'credito': TARJETA DE CRÉDITO
    # 'otros': OTROS CON UTILIZACION DEL SISTEMA FINANCIERO
    # 'endoso': ENDOSO DE TÍTULOS

    pag1 = Pago()
    pag1.forma_pago = 'efectivo' # FORMAS DE PAGO VALIDAS
    pag1.total = 23
    pag1.plazo = None
    pag1.unidad_tiempo = None

    pagos.append(pag1)

    return pagos

# ------------------------------------------ Crear entidades -------------------------------------------

# ******************************** Empresa ********************************
emp = Empresa()
emp.razon_social = 'NOBLECILLA CASTRO RAUL NICOLAS'
emp.ruc = '0701010498001'
emp.dir_matriz = 'BOLIVAR Y MACHALA ñ'
emp.nombre_comercial = 'FINCA PIEDAD áé' # Opcional
emp.dir_establecimiento = None # Opcional
emp.contribuyente_especial = None # Opcional
emp.obligado_contabilidad = 'SI' # Opcional
emp.password = '1234'  # Password en entidad empresa
emp.credencial = '223d900bf86ad5eda991dee5598891'  # Credencia en entidad empresa

# ******************************** Cliente ********************************
cli = Cliente()
cli.tipo_identificacion_comprador = 'ruc' # ruc | cedula | pasaporte | consumidor_final | identificacion_exterior | placa
cli.razon_social_comprador = 'JENNIFER'
cli.identificacion_comprador = '0706418514001'
cli.direccion_comprador = 'NADA' # Opcional

# ******************************** Factura ********************************

# Recibe los parametros:
# El ambiente (por defecto 'pruebas')
# El tipo de documento (en este caso 'factura')

fac = Comprobante('pruebas', 'factura')  # [pruebas | produccion] , [factura | credito | debito  | guia | retencion]
fac.tipo_emision = 'normal' # normal | indisp (Indisponibilidad del sistema)
fac.estab = '001'
fac.pto_emi = '001'
fac.secuencial = '000000016'
fac.fecha_emision = '22/02/2018' #Puede ser str o datetime
fac.guia_remision = None # Opcional
fac.total_sin_impuestos = 14
fac.total_descuento = 0
fac.total_con_impuestos = Formato_Total_Con_Impuestos()
fac.propina = 0
fac.importe_total = 23
fac.pagos = Formato_Pagos()
fac.valor_ret_iva = None # Opcional
fac.valor_ret_renta = None # Opcional
fac.info_adicional = Formato_Info_Adicional() # Opcional

# ******************************* Detalle Factura ******************************
detalle =  Formato_Detalle_Factura()

# Construir archivo XML a partir de los datos de las entidades
# Retorna la fecha y el número de autorización

autorizar = Autorizar_Documento(emp, cli, fac, detalle)

if autorizar['estado']:
    print 'Autorizacion: ', autorizar['numero']
    print 'Fecha Autorizacion: ',autorizar['fecha']
else:
    print "Ha ocurrido el siguiente error: "
    print autorizar['mensaje']

