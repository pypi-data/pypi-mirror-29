# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from daylifact.entidades import *
from daylifact.autorizar import Autorizar_Documento

"""
TEST AUTORIZAR UNA NOTA DE DEBITO
"""

# Retorna una lista de entidades del tipo Impuesto
def Formato_Impuestos():
    # ETIQUETA XML: <impuestos>
    # Apartado impuestos

    # Simulación de los impuestos
    total_con_impuestos = []

    # 'codigo': Nombre del impuesto: iva (IVA 0% e IVA 12%) | ice (ICE %) | irbpnr
    # 'codigo_porcentaje': Porcentaje de IVA únicamente (0, 12, 14...) ** la tarifa ICE tiene sus propios códigos (VER TABLA 19 SRI) *** la tarifa IRBPNR tiene sus propios códigos

    imp1 = Impuesto()
    imp1.codigo = 'iva'
    imp1.codigo_porcentaje = 12 #Puede ser int o str
    imp1.tarifa = 12
    imp1.base_imponible = 12
    imp1.valor = 1.44

    total_con_impuestos.append(imp1)

    return total_con_impuestos

# Retorna una lista de entidades del tipo Pago
def Formato_Pagos():
    # ETIQUETA XML: <pagos>
    # Apartado forma de pago de la nota de débito

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
    pag1.forma_pago = 'credito' # FORMAS DE PAGO VALIDAS
    pag1.total = 10
    pag1.plazo = 2
    pag1.unidad_tiempo = 'meses'

    pag2 = Pago()
    pag2.forma_pago = 'efectivo'  # FORMAS DE PAGO VALIDAS
    pag2.total = 2

    pagos.append(pag1)
    pagos.append(pag2)

    return pagos

# Retorna una lista de entidades del tipo Detalle_Adicional
def Formato_Info_Adicional():
    # ETIQUETA XML: <infoAdicional>
    # Apartado info adicional (OPCIONAL)

    # Simulación de la info adicional
    info_adicional = []

    inf1 = Detalle_Adicional('Dirección', 'AMAZONAS S/N ROCA')
    inf2 = Detalle_Adicional('Emial', 'prueba@sri.gob.e')
    inf3 = Detalle_Adicional('Teléfono', '0222222222222 ext. 3322')

    info_adicional.append(inf1)
    info_adicional.append(inf2)
    info_adicional.append(inf3)

    return info_adicional

# Retorna una lista de entidades del tipo Detalle_Comprobante
def Formato_Motivos():
    # ETIQUETA XML: <motivos>
    # Apartado motivos de la nota de débito

    mitivos = []

    # Simulacion de los motivos
    # ------------ Motivo 1 -------------
    mot1 = Motivo('Interés por mora', 12)
    mitivos.append(mot1)

    return mitivos

# ------------------------------------------ Crear entidades -------------------------------------------

# ******************************** Empresa ********************************
emp = Empresa()
emp.razon_social = 'PRUEBA'
emp.ruc = '0701010498001'
emp.dir_matriz = 'SALINAS'
emp.nombre_comercial = 'PRUEBA 2' # Opcional
emp.dir_establecimiento = 'PÁEZ' # Opcional
emp.contribuyente_especial = '12345' # Opcional
emp.obligado_contabilidad = 'SI' # Opcional
emp.password = '1234'  # Password en entidad empresa
emp.credencial = '223d900bf86ad5eda991dee5598891'  # Credencia en entidad empresa

# ******************************** Cliente ********************************
cli = Cliente()
cli.tipo_identificacion_comprador = 'ruc' # ruc | cedula | pasaporte | consumidor_final | identificacion_exterior | placa
cli.razon_social_comprador = 'PRUEBA SRI'
cli.identificacion_comprador = '1713328506001'

# ******************************** Nota de débito ********************************

# Recibe los parametros:
# El ambiente (por defecto 'pruebas')
# El tipo de documento (en este caso 'debito')

deb = Comprobante('pruebas', 'debito')  # [pruebas | produccion] , [factura | credito | debito  | guia | retencion]
deb.tipo_emision = 'normal' # normal | indisp (Indisponibilidad del sistema)
deb.estab = '001'
deb.pto_emi = '001'
deb.secuencial = '000000002'
deb.fecha_emision = '12/03/2018' #Puede ser str o datetime
deb.cod_doc_sustento = 'factura'
deb.num_doc_sustento = '001-001-000000001'
deb.fecha_doc_sustento = '28/02/2018'
deb.total_sin_impuestos = 12
deb.total_con_impuestos = Formato_Impuestos()
deb.importe_total = 13.44
deb.pagos = Formato_Pagos()
deb.info_adicional = Formato_Info_Adicional() # Opcional

# ******************************* Detalle Factura ******************************
motivos =  Formato_Motivos()

# Construir archivo XML a partir de los datos de las entidades
# Retorna la fecha y el número de autorización

autorizar = Autorizar_Documento(emp, cli, deb, motivos)

if autorizar['estado']:
    print 'Autorizacion: ', autorizar['numero']
    print 'Fecha Autorizacion: ', autorizar['fecha']
else:
    print "Ha ocurrido el siguiente error: "
    print autorizar['mensaje']

