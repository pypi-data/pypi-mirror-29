# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from daylifact.entidades import *
from daylifact.autorizar import Autorizar_Documento

"""
TEST AUTORIZAR COMPROBANTE GUIA DE EMISION
"""

# Retorna una lista de entidades del tipo Detalle_Adicional
def Formato_Info_Adicional():
    # ETIQUETA XML: <infoAdicional>
    # Apartado info adicional (OPCIONAL)

    # Simulación de la info adicional
    info_adicional = []

    inf1 = Detalle_Adicional('TELEFONO', '098568541')
    inf2 = Detalle_Adicional('E-MAIL', 'info@organizacion.com')
    inf3 = Detalle_Adicional('SUCURSAL 03', 'Guayaquil–12 de Octubre y Universo')

    info_adicional.append(inf1)
    info_adicional.append(inf2)
    info_adicional.append(inf3)

    return info_adicional

# Retorna una lista de entidades del tipo Detalle_Adicional
def Detalle_Adicional_Dest1():
    # ETIQUETA XML: <detallesAdicionales>
    # Apartado detalles adicionales del destinatario(OPCIONAL)

    # Simulación de los detalles adicionales (En caso de tenerlos)
    detalles_adicionales_dest1 = []

    det_prod1_1 = Detalle_Adicional('Marca', 'Chevrolet')
    det_prod1_2 = Detalle_Adicional('Modelo', '2012')
    det_prod1_3 = Detalle_Adicional('Chasis', '8LDETA03V20003289')

    detalles_adicionales_dest1.append(det_prod1_1)
    detalles_adicionales_dest1.append(det_prod1_2)
    detalles_adicionales_dest1.append(det_prod1_3)

    return  detalles_adicionales_dest1

# Retorna una lista de entidades del tipo Detalle_Comprobante
def Formato_Detalle_Destinatario_1():
    # ETIQUETA XML: <detalles>
    # Apartado detalle de cada destinatario

    detalles = []

    # Simulacion del detalle
    # ------------ Detalle 1 -------------
    det1 = Detalle_Comprobante()
    det1.codigo_principal = 'AUX1' # Opcional
    det1.codigo_auxiliar = 'UAX2'  # Opcional
    det1.descripcion = 'PRUEBA'
    det1.cantidad = 1
    det1.detalles_adicionales = Detalle_Adicional_Dest1() # Opcional

    det2 = Detalle_Comprobante()
    det2.codigo_principal = '2'  # Opcional
    det2.codigo_auxiliar = '23'  # Opcional
    det2.descripcion = 'PRUEBA 2'
    det2.cantidad = 1

    detalles.append(det1)
    detalles.append(det2)

    return detalles

# Retorna una lista de entidades del tipo Destinatario
def Destinatario_1():
    # ETIQUETA XML: <destinatario>
    # Apartado destinatario

    # Simulación de los destinatarios en la guía remisión
    destinatarios = []

    des1 = Destinatario()
    des1.identificacion = '0706219029'
    des1.razon_social = 'EJEMPLO 2'
    des1.direccion = 'asd'
    des1.motivo_traslado = 'asd'
    des1.documento_aduanero_unico = '564' # Opcional
    des1.cod_establecimiento_destino = '001' # Opcional
    des1.ruta = 'asd' # Opcional
    des1.cod_doc_sustento = 'factura' # Opcional
    des1.num_doc_sustento = '002-001-000000001' # Opcional
    des1.num_autorizacion_doc_sustento = '1234567891' # Opcional
    des1.fecha_doc_sustento = '06/03/2018' # Opcional (puede ser str o datetime)
    des1.detalles = Formato_Detalle_Destinatario_1()

    destinatarios.append(des1)

    return destinatarios

# ------------------------------------------ Crear entidades -------------------------------------------

# ******************************** Empresa ********************************
emp = Empresa()
emp.razon_social = 'Distribuidora de Suministros Nacional S.A.'
emp.ruc = '0701010498001'
emp.dir_matriz = 'Enrique Guerrero Portilla OE1-34 AV. Galo Plaza Lasso'
emp.nombre_comercial = 'Empresa Importadora y Exportadora de Piezas y Partes de Equipos de Oficina' # Opcional
emp.dir_establecimiento = 'Sebastián Moreno S/N Francisco García' # Opcional
emp.contribuyente_especial = '5368' # Opcional
emp.obligado_contabilidad = 'SI' # Opcional
emp.password = '1234'  # Password en entidad empresa
emp.credencial = '223d900bf86ad5eda991dee5598891'  # Credencia en entidad empresa

# ******************************** Transportista ********************************
tran = Transportista()
tran.tipo_identificacion = 'cedula' # ruc | cedula | pasaporte | consumidor_final | identificacion_exterior | placa
tran.razon_social = 'PRUEBA'
tran.identificacion = '0706418514'
tran.rise = 'Contribuyente Regimen Simplificado RISE' # Opcional
tran.placa = 'MCL0827'

# ******************************** Guía de Remisión ********************************

# Recibe los parametros:
# El ambiente (por defecto 'pruebas')
# El tipo de documento (en este caso 'guia')

guia = Comprobante('pruebas', 'guia')  # [pruebas | produccion] , [factura | credito | debito  | guia | retencion]
guia.tipo_emision = 'normal' # normal | indisp (Indisponibilidad del sistema)
guia.estab = '001'
guia.pto_emi = '001'
guia.secuencial = '000000002'
guia.fecha_emision = '12/03/2018' #Puede ser str o datetime
guia.direccion_partida = 'machala de donde parte'
guia.fecha_inicio_transporte = '12/03/2018' #Puede ser str o datetime
guia.fecha_fin_transporte = '12/03/2018' #Puede ser str o datetime
guia.info_adicional = Formato_Info_Adicional() # Opcional

# ******************************* Destinatarios ******************************
destinatarios =  Destinatario_1()

# Construir archivo XML a partir de los datos de las entidades
# Retorna la fecha y el número de autorización

autorizar = Autorizar_Documento(emp, tran, guia, destinatarios)

if autorizar['estado']:
    print 'Autorizacion: ', autorizar['numero']
    print 'Fecha Autorizacion: ', autorizar['fecha']
else:
    print "Ha ocurrido el siguiente error: "
    print autorizar['mensaje']

