from typing import Any, Mapping

EMAIL_BODY: str = """Hola,  

Me llamo Victor y soy un programador con más de 10 años de experiencia en Python.  
Actualmente estoy buscando oportunidades de trabajo como desarrollador, y como buen fan de la automatización, he escrito un pequeño script para contactar con todas las empresas del ParcBit ;).  

Si te apetece echar un vistazo a cómo lo hice, el código está aquí: https://github.com/ciurana-life/bit_apply
Y para comprobar mi experiencia profesional, puedes consultar mi CV aquí: https://docs.google.com/document/d/1BYH7b1DsioU8lPT-DsBDNb24-qFMF6UuANCye3AfBpA/edit?usp=sharing 

No dudes en escribirme si surge alguna oportunidad o si quieres charlar sobre programación, automatización… o café.

¡Saludos!  
Victor"""
EMAIL_SUBJECT: str = "Busco colaborar como programador en tu equipo"

POST_URL: str = "https://www.parcbit.es/wparcbitfront/dwr/call/plaincall/FrontOffice.obtenerListaFiltradaFrontEmpresas.dwr"
FORM_PAYLOAD: Mapping[str, Any] = {
    "callCount": 1,
    "page": "/wparcbitfront/EmpresaLis.jsp",
    "scriptSessionId": "D720C0B24255whateverA057B4271DEF68",
    "c0-scriptName": "FrontOffice",
    "c0-methodName": "obtenerListaFiltradaFrontEmpresas",
    "c0-id": 0,
    "c0-e1": "string:",  # NOSONAR
    "c0-e2": "string:",
    "c0-e3": "string:",
    "c0-e4": "number:0",
    "c0-e5": "number:0",
    "c0-e6": "string:",
    "c0-e7": "null:null",
    "c0-e8": "boolean:true",
    "c0-e9": "string:",
    "c0-e10": "string:",
    "c0-param0": (
        "Object_Object:{"
        "actividad:reference:c0-e1,"
        "className:reference:c0-e2,"
        "codigoLOV:reference:c0-e3,"
        "columnaOrden:reference:c0-e4,"
        "edificioCodigo:reference:c0-e5,"
        "nombre:reference:c0-e6,"
        "numPagina:reference:c0-e7,"
        "ordenAscendente:reference:c0-e8,"
        "palabraClave:reference:c0-e9,"
        "valorLOV:reference:c0-e10"
        "}"
    ),
    "batchId": 1,
}
