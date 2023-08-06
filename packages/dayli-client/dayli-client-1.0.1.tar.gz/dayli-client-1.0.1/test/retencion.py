# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from daylifact.entidades import *
from daylifact.autorizar import Autorizar_Documento

"""
TEST AUTORIZAR COMPROBANTE DE RETENCIÓN
"""

# Retorna una lista de entidades del tipo Detalle_Adicional
def Formato_Info_Adicional():
    # ETIQUETA XML: <infoAdicional>
    # Apartado info adicional (OPCIONAL)

    # Simulación de la info adicional
    info_adicional = []

    inf1 = Detalle_Adicional('ConvenioDobleTributacion', 'MA123456')
    inf2 = Detalle_Adicional('documentoIFIS', 'BP2010-01-0014')

    info_adicional.append(inf1)
    info_adicional.append(inf2)

    return info_adicional

# Retorna una lista de entidades del tipo Impuesto
def Impuestos_1():
    # ETIQUETA XML: <impuestos>
    # Apartado impuestos del comprobante de retención

    # Simulación de los impuestos
    impuestos = []

    # 'codigo': Nombre del impuesto a retener: renta | iva | isd
    # 'codigo_porcentaje':
    # Retención de IVA: 10%, 20%, 30%, 50%, 70%, 100%, 0% Retención en 0, 0% No procede retención (VER TABLA 21 SRI-Apartado retención de IVA)
    # Retención de ISD: 5% (VER TABLA 21 SRI-Apartado retención de ISD)
    # Retención de Renta: (VER TABLA 21 SRI-Apartado retención de Renta)

    imp1 = Impuesto()
    imp1.codigo = 'isd'
    imp1.codigo_porcentaje = 5 #Puede ser int o str
    imp1.base_imponible = 2000
    imp1.porcentaje_retener = 5
    imp1.valor = 100

    imp2 = Impuesto()
    imp2.codigo = 'iva'
    imp2.codigo_porcentaje = 30 #Puede ser int o str
    imp2.base_imponible = 101.94
    imp2.porcentaje_retener = 30
    imp2.valor = 30.58

    imp3 = Impuesto()
    imp3.codigo = 'renta'
    imp3.codigo_porcentaje = '323B1' #Puede ser int o str
    imp3.base_imponible = 10904.50
    imp3.porcentaje_retener = 2
    imp3.valor = 218.09

    impuestos.append(imp2)
    impuestos.append(imp3)
    impuestos.append(imp1)


    return impuestos

# ------------------------------------------ Crear entidades -------------------------------------------

# ******************************** Empresa ********************************
emp = Empresa()
emp.razon_social = 'Daylisoft Cia Ltda'
emp.ruc = '0701010498001'
emp.dir_matriz = 'Cantón Machala'
emp.nombre_comercial = None # Opcional
emp.dir_establecimiento = None # Opcional
emp.contribuyente_especial = '5138' # Opcional
emp.obligado_contabilidad = 'NO' # Opcional
emp.password = '1234'  # Password en entidad empresa
emp.credencial = '223d900bf86ad5eda991dee5598891'  # Credencia en entidad empresa

# ******************************** Provedor ********************************
prov = Proveedor()
prov.tipo_identificacion = 'ruc' # ruc | cedula | pasaporte | consumidor_final | identificacion_exterior | placa
prov.razon_social = 'Daylisoft'
prov.identificacion = '0999999999001'

# ******************************** Retención ********************************

# Recibe los parametros:
# El ambiente (por defecto 'pruebas')
# El tipo de documento (en este caso 'retencion')

ret = Comprobante('pruebas', 'retencion')  # [pruebas | produccion] , [factura | credito | debito  | guia | retencion]
ret.tipo_emision = 'normal' # normal | indisp (Indisponibilidad del sistema)
ret.estab = '001'
ret.pto_emi = '001'
ret.secuencial = '000000004'
ret.fecha_emision = '07/03/2018' #Puede ser str o datetime
ret.periodo_fiscal = '03/2018'
ret.cod_doc_sustento = 'factura' # Nombre del documento 'factura', 'debito', 'ifis', ...
ret.num_doc_sustento = '001001000000001' # Opcional
ret.fecha_doc_sustento = '08/01/2018' # Opcional (Puede ser str o datetime)
ret.info_adicional = Formato_Info_Adicional() # Opcional

# ******************************* Impuestos ******************************
impuestos =  Impuestos_1()

# Construir archivo XML a partir de los datos de las entidades
# Retorna la fecha y el número de autorización

autorizar = Autorizar_Documento(emp, prov, ret, impuestos)

if autorizar['estado']:
    print 'Autorizacion: ', autorizar['numero']
    print 'Fecha Autorizacion: ', autorizar['fecha']
else:
    print "Ha ocurrido el siguiente error: "
    print autorizar['mensaje']

