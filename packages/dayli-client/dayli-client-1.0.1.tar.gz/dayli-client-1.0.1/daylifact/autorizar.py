# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ETXML
from daylifact.utils import RUTA_ARCHIVOS
import os
import requests
import sys
from daylifact.logica import Crear_XML

def Autorizar_Documento(empresa, sujeto, documento, detalle_documento):
    try:
        # Enviar las entidades 'Empresa', 'Cliente o Proveedor', 'Documento (Factura, Retencion....)' y la lista de Entidades '(Detalle_Factura, impuests de retencion....)'
        estado = Crear_XML(empresa, sujeto, documento, detalle_documento)

        if estado[0]:
            rootWrite = estado[1]
            rootWrite.write(os.path.join(RUTA_ARCHIVOS, documento.clave_acceso + '.xml'), encoding='utf8', xml_declaration=True)

            # Envio de Informacion
            res = requests.head('http://104.236.239.181:8000/firmar/', timeout=3)

            if not res:
                # Verificar si el servicio esta disponible antes de mandar a firmar
                return {'estado': False, 'numero': None, 'fecha': None, 'mensaje': 'Servicio DAYLIFACT no disponible.'}

            ein = rootWrite.getroot()
            einvoice = ETXML.tostring(ein, encoding="utf8", method='xml')

            import base64

            r = requests.post('http://104.236.239.181:8000/firmar/', data={'credential': empresa.credencial,
                                                                       'file': base64.encodestring(einvoice),
                                                                       'password': empresa.password})
            if (r.status_code != 200):
                return {'estado': False, 'numero': None, 'fecha': None, 'mensaje': 'Servicio DAYLIFACT no disponible.'}

            __json_result = r.json()
            resultado = __json_result['result']

            if not resultado:
                return {'estado': False, 'numero': None, 'fecha': None, 'mensaje':  __json_result['message']['message']}

            autorizado = __json_result['autorizado']

            if (autorizado['estado'] == 'AUTORIZADO'):
                numero_autorizacion = autorizado['autorizacion']
                fecha_autorizacion =  autorizado['fecha']

                file_firmado = (__json_result['firmado'])
                file_autorizado = (autorizado['file'])

                if file_autorizado and file_firmado:
                    root_str = ETXML.fromstring(file_autorizado.encode("utf8"))
                    root_str_Write = ETXML.ElementTree(root_str)
                    root_str_Write.write(os.path.join(RUTA_ARCHIVOS + '/autorizados', documento.clave_acceso + '.xml'),
                                         encoding='utf8', xml_declaration=True)

                    root_str2 = ETXML.fromstring(file_firmado.encode("utf8"))
                    root_str_Write2 = ETXML.ElementTree(root_str2)
                    root_str_Write2.write(os.path.join(RUTA_ARCHIVOS + '/firmados', documento.clave_acceso + '.xml'),
                                          encoding='utf8', xml_declaration=True)

                    return {'estado': True, 'numero': numero_autorizacion, 'fecha': fecha_autorizacion, 'mensaje': 'OK'}

            return {'estado': False, 'numero': None, 'fecha': None, 'mensaje': __json_result['message']['message']}
        else:
            return {'estado': False, 'numero': None, 'fecha': None, 'mensaje': estado[1]}
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            'line': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'type': exc_type.__name__,
            'message': exc_value.message
        }

        return {'estado': False, 'numero': None, 'fecha': None, 'mensaje': traceback_details}