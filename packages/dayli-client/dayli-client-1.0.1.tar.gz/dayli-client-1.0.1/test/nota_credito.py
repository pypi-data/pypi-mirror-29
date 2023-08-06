# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from daylifact.entidades import *
from daylifact.autorizar import Autorizar_Documento

"""
TEST AUTORIZAR UNA NOTA DE CREDITO
"""

# Retorna una lista de entidades del tipo Impuesto
def Formato_Total_Con_Impuestos():
    # ETIQUETA XML: <totalConImpuestos>
    # Apartado Total con impuestos (Por toda la nota de crédito)

    # Simulación de los impuestos en la nota de crédito
    total_con_impuestos = []

    # 'codigo': Nombre del impuesto: iva (IVA 0% e IVA 12%) | ice (ICE %) | irbpnr
    # 'codigo_porcentaje': Porcentaje de IVA únicamente (0, 12, 14...) ** la tarifa ICE tiene sus propios códigos (VER TABLA 19 SRI) *** la tarifa IRBPNR tiene sus propios códigos

    imp1 = Impuesto()
    imp1.codigo = 'iva'
    imp1.codigo_porcentaje = 'noiva' #Puede ser int o str
    imp1.base_imponible = 14
    imp1.valor = 0

    imp2 = Impuesto()
    imp2.codigo = 'iva'
    imp2.codigo_porcentaje = 'excento' #Puede ser int o str
    imp2.base_imponible = 3
    imp2.valor = 0

    imp3 = Impuesto()
    imp3.codigo = 'ice'
    imp3.codigo_porcentaje = 3011  # Puede ser int o str
    imp3.base_imponible = 14
    imp3.valor = 3

    imp4 = Impuesto()
    imp4.codigo = 'irbpnr'
    imp4.codigo_porcentaje = 5001  # Puede ser int o str
    imp4.base_imponible = 22
    imp4.valor = 12

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

    inf1 = Detalle_Adicional('E-MAIL', 'info@organizacion.com')
    info_adicional.append(inf1)

    return info_adicional

# Retorna una lista de entidades del tipo Detalle_Adicional
def Detalle_Adicional_Prod1():
    # ETIQUETA XML: <detallesAdicionales>
    # Apartado detalles adicionales del producto(OPCIONAL)

    # Simulación de los detalles adicionales (En caso de tenerlos)
    detalles_adicionales_prod1 = []

    det_prod1_1 = Detalle_Adicional('Marca', 'Chevrolet')
    detalles_adicionales_prod1.append(det_prod1_1)

    return  detalles_adicionales_prod1

# Retorna una lista de entidades del tipo Impuesto
def Impuestos_Prod1():
    # ETIQUETA XML: <impuestos>
    # Apartado impuestos (Por cada producto en el detalle de la nota de crédito)

    # Simulación de los impuestos en el detalle
    impuestos = []

    # 'codigo': Nombre del impuesto: iva (IVA 0% e IVA 12%) | ice (ICE %) | irbpnr
    # 'codigo_porcentaje': Porcentaje de IVA únicamente (0, 12, 14...) ** la tarifa ICE tiene sus propios códigos (VER TABLA 19 SRI) *** la tarifa IRBPNR tiene sus propios códigos

    imp1 = Impuesto()
    imp1.codigo = 'iva'
    imp1.codigo_porcentaje = 'excento' #Puede ser int o str
    #imp1.tarifa = 0 # Opcional
    imp1.base_imponible = 3
    imp1.valor = 0

    imp2 = Impuesto()
    imp2.codigo = 'ice'
    imp2.codigo_porcentaje = 3011 #Puede ser int o str
    #imp2.tarifa = 12 # Opcional
    imp2.base_imponible = 2
    imp2.valor = 1

    imp3 = Impuesto()
    imp3.codigo = 'irbpnr'
    imp3.codigo_porcentaje = 5001  # Puede ser int o str
    # imp3.tarifa = 12 # Opcional
    imp3.base_imponible = 12
    imp3.valor = 1

    impuestos.append(imp1)
    impuestos.append(imp2)
    impuestos.append(imp3)

    return impuestos

def Impuestos_Prod2():
    # ETIQUETA XML: <impuestos>
    # Apartado impuestos (Por cada producto en el detalle de la nota de crédito)

    # Simulación de los impuestos en el detalle
    impuestos = []

    # 'codigo': Nombre del impuesto: iva (IVA 0% e IVA 12%) | ice (ICE %) | irbpnr
    # 'codigo_porcentaje': Porcentaje de IVA únicamente (0, 12, 14...) ** la tarifa ICE tiene sus propios códigos (VER TABLA 19 SRI) *** la tarifa IRBPNR tiene sus propios códigos

    imp1 = Impuesto()
    imp1.codigo = 'iva'
    imp1.codigo_porcentaje = 'noiva' #Puede ser int o str
    #imp1.tarifa = 0 # Opcional
    imp1.base_imponible = 14
    imp1.valor = 0

    imp2 = Impuesto()
    imp2.codigo = 'ice'
    imp2.codigo_porcentaje = 3011 #Puede ser int o str
    #imp2.tarifa = 12 # Opcional
    imp2.base_imponible = 12
    imp2.valor = 2

    imp3 = Impuesto()
    imp3.codigo = 'irbpnr'
    imp3.codigo_porcentaje = 5001  # Puede ser int o str
    # imp3.tarifa = 12 # Opcional
    imp3.base_imponible = 10
    imp3.valor = 11

    impuestos.append(imp1)
    impuestos.append(imp2)
    impuestos.append(imp3)

    return impuestos

# Retorna una lista de entidades del tipo Detalle_Comprobante
def Formato_Detalle_Nota_Credito():
    # ETIQUETA XML: <detalles>
    # Apartado detalle de cada producto

    productos = []

    # Simulacion de productos en el detalle
    # ------------ Producto 1 -------------
    prod1 = Detalle_Comprobante()
    prod1.codigo_principal = '125BJC-01'
    prod1.codigo_auxiliar = '1234D56789-A'  # Opcional
    prod1.descripcion = 'CAMIONETA 4X4 DIESEL 3.7'
    prod1.cantidad = 1
    prod1.precio_unitario = 2
   # prod1.descuento = 5000
    prod1.precio_total_sin_impuesto = 2
    prod1.detalles_adicionales = Detalle_Adicional_Prod1() # Opcional
    prod1.impuestos = Impuestos_Prod1()

    # ------------ Producto 1 -------------
    prod2 = Detalle_Comprobante()
    prod2.codigo_principal = '2'
    prod2.codigo_auxiliar = '23'  # Opcional
    prod2.descripcion = 'PRUEBA 2'
    prod2.cantidad = 1
    prod2.precio_unitario = 12
    # prod2.descuento = 5000
    prod2.precio_total_sin_impuesto = 12
    prod2.impuestos = Impuestos_Prod2()

    productos.append(prod1)
    productos.append(prod2)

    return productos

# ------------------------------------------ Crear entidades -------------------------------------------

# ******************************** Empresa ********************************
emp = Empresa()
emp.razon_social = 'Distribuidora de Suministros Nacional S.A.'
emp.ruc = '0701010498001'
emp.dir_matriz = 'ENRIQUE GUERRERO PORTILLA OE1-34 AV. GALO PLAZA LASSO'
emp.nombre_comercial = 'Empresa Importadora y Exportadora de Piezas' # Opcional
emp.dir_establecimiento = 'Sebastián Moreno S/N Francisco García' # Opcional
emp.contribuyente_especial = '5368' # Opcional
emp.obligado_contabilidad = 'SI' # Opcional
emp.password = '1234'  # Password en entidad empresa
emp.credencial = '223d900bf86ad5eda991dee5598891'  # Credencia en entidad empresa

# ******************************** Cliente ********************************
prov = Proveedor()
prov.tipo_identificacion = 'ruc' # ruc | cedula | pasaporte | consumidor_final | identificacion_exterior | placa
prov.razon_social = 'PRUEBAS SERVICIO DERENTAS INTERNAS</'
prov.identificacion = '1713328506001'
prov.rise = 'Contribuyente Régimen Simplificado RISE' # Opcional

# ******************************** Nota de crédito ********************************

# Recibe los parametros:
# El ambiente (por defecto 'pruebas')
# El tipo de documento (en este caso 'credito')

cre = Comprobante('pruebas', 'credito')  # [pruebas | produccion] , [factura | credito | debito  | guia | retencion]
cre.tipo_emision = 'normal' # normal | indisp (Indisponibilidad del sistema)
cre.estab = '001'
cre.pto_emi = '001'
cre.secuencial = '000000006'
cre.fecha_emision = '22/02/2018' #Puede ser str o datetime
cre.cod_doc_sustento = 'factura'
cre.num_doc_sustento = '002-001-000000001'
cre.fecha_doc_sustento = '21/10/2011'
cre.total_sin_impuestos = 14
cre.valor_modificacion = 29
cre.total_con_impuestos = Formato_Total_Con_Impuestos()
cre.motivo = 'DEVOLUCIÓN'
cre.info_adicional = Formato_Info_Adicional() # Opcional

# ******************************* Detalle Factura ******************************
detalle =  Formato_Detalle_Nota_Credito()

# Construir archivo XML a partir de los datos de las entidades
# Retorna la fecha y el número de autorización

autorizar = Autorizar_Documento(emp, prov, cre, detalle)

if autorizar['estado']:
    print 'Autorizacion: ', autorizar['numero']
    print 'Fecha Autorizacion: ', autorizar['fecha']
else:
    print "Ha ocurrido el siguiente error: "
    print autorizar['mensaje']

