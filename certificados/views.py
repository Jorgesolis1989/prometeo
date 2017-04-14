from certificados.forms import FormularioEscogerCertificado
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, cm, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from modelos_existentes.models import Empresa
from modelos_existentes.models import Usuario_Web , Certificado_Retencion
from modelos_existentes.models import Departamentos, Paises,Municipios , Formatos_Definidos
import datetime
from django.shortcuts import render, redirect
from empresas.views import cargar_empresas_vinculadas, cargar_carpetas
from PROMETEO.settings import STATICFILES_DIRS
#import pdfkit
from django.template.loader import get_template
from django.template import Context
#import pdfkit
from reportlab.lib.enums import TA_LEFT, TA_CENTER

from empresas.forms import FormularioVincularEmpresas
from reportlab.lib.units import inch


def seleccion_concepto(request, id_emprsa=None):
    # POST
    if request.POST and "btnGenerer" in request.POST:
        form = FormularioEscogerCertificado(request.POST)
        if form.is_valid():
            tipo_certificado = form.cleaned_data["tipo_certificado"]
            periodo = form.cleaned_data["periodo"]

            #return  seleccion_other()
            return generarPdf_general(request,tipo_certificado, periodo,id_emprsa )
            #return example()
        else:
            print("no valido")


    formatos = Formatos_Definidos.objects.filter(actvo=1, id_emprsa=id_emprsa)

    """tupla_formatos = []
    for formato in formatos:
        tupla_formatos.append((formato.cdgo_frmto , formato.nmbre_frmto))
    """
    form = FormularioEscogerCertificado()

    form.fields['tipo_certificado'].queryset = formatos

    #Empresa que practica retención
    empresa = Empresa.objects.get(id_emprsa= id_emprsa)

    return render(request, 'seleccion-concepto.html', {'empresa':empresa,'empresas_vinculadas': cargar_empresas_vinculadas(request) ,
                                                        'carpetas': cargar_carpetas(request) ,  'FormularioEscogerCertificado': form
                                                        })




def generarPdf_general(request, formato_definido, periodo, id_empresa_vinculada):

    #Empresa que practica retención
    empresa = Empresa.objects.get(id_emprsa= id_empresa_vinculada)


    # Usuario de la empresa que descarga el certificado
    try:
        usuario_Web = Usuario_Web.objects.get(email_usrio=request.user.email , actvo=1)
    except Exception as e:
        print(e)


    #crea la cabezera HttpResponse con PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=certificado-de-'+ str(empresa.nmbre_rzon_scial )+'.pdf'
    #Crea el objeto pdf, usando el objeto BytesIO
    buffer = BytesIO()
    #size = landscape(A4)
    C = canvas.Canvas(buffer, pagesize=A4)
    C.setTitle("Certificado de- "+str(formato_definido.nmbre_frmto))

    """Encabezado"""

    #Logo de la empresa
    C.setLineWidth(.3)
    try:
        C.drawImage(STATICFILES_DIRS[0]+"/images/logosEmpresas/"+str(empresa.id_emprsa)+".bmp", 180, 730, 70, 70)
    except OSError as e:
        C.drawImage(STATICFILES_DIRS[0]+"/images/logosEmpresas/logo-empresa-df.png", 180, 730, 70, 100)


    C.setFont('Helvetica', 14)

    # Titulo de la empresa
    distancia = 15
    posicion_x_titulo = 260
    posicion_y_titulo = 780
    C.drawString(posicion_x_titulo,posicion_y_titulo,empresa.nmbre_rzon_scial)
    C.drawString(posicion_x_titulo,posicion_y_titulo - distancia, "NIT "+str(empresa.id_emprsa))
    C.setFont('Helvetica', 11)
    C.drawString(posicion_x_titulo , posicion_y_titulo - (distancia * 2),empresa.drccion)


    departamento = Departamentos.objects.filter(cdgo_pais = empresa.cdgo_pais, cdgo_dpto= empresa.cdgo_dpto)

    municipio = Municipios.objects.filter(cdgo_pais = empresa.cdgo_pais,
                                          cdgo_dpto= empresa.cdgo_dpto,
                                          cdgo_mncpio= empresa.cdgo_mncpio , actvo=1)
    # En caso que sea colombia
    if municipio is not None:
        C.drawString(posicion_x_titulo , posicion_y_titulo - (distancia * 3),
                     municipio[0].nmbre_mncpio + ", " + departamento[0].nmbre_dpto )

    #start X, height end y, height
    C.line(30,1125,560,1125)
    C.setFont('Helvetica-Bold', 16)
    C.drawString(100,713,formato_definido.nmbre_frmto)
    #print(len(formato_definido.nmbre_frmto))
    C.setFont('Helvetica-Bold', 13)
    C.drawString(220, 698,"Año Gravable "+ str(periodo))

    C.setFont('Helvetica', 13)
    C.drawString(180, 670,"Fecha de emisión: "+ str(datetime.datetime.today().date()))


    C.setFont('Helvetica-Bold', 13)
    C.drawString(60, 640,"RETENCIÓN PRACTICADA A: ")

    #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
    #cabecera(pdf)
    y = 600
    tabla_datos(usuario_Web, C, y)

    C.setFont('Helvetica', 13)
    C.drawString(60, y - 30,"Por los conceptos que se detallan a continuación:" )


    numero_a_retener = '' + usuario_Web.nit_tcro_ascdo
    for i in range(13 - len(usuario_Web.nit_tcro_ascdo)):
        numero_a_retener += ' '

    #print(numero_a_retener,"#")

    consulta = "SELECT row_number() OVER (ORDER BY cd.nmbre_cncpto) AS id , cd.nmbre_cncpto as nmbre_cncpto, cdp.prcntje_aplccion as tasa, mfc.vlor_grvble AS retencion, (mfc.vlor_grvble/(cdp.prcntje_aplccion/100)) AS base \
        FROM mvmnto_frmto_cncpto AS mfc INNER JOIN cncptos_dfndos_prmtros AS cdp ON mfc.cdgo_cncpto = cdp.cdgo_cncpto AND mfc.cnta_cntble = cdp.cnta_cntble \
        INNER JOIN cncptos_dfndos AS cd ON mfc.cdgo_cncpto=cd.cdgo_cncpto AND mfc.id_emprsa=cd.id_emprsa  WHERE " \
        "mfc.id_emprsa = %s AND mfc.id_trcro = '%s' and mfc.ano_mes_fnal= '%s' ;"%(str(empresa.id_emprsa) , numero_a_retener ,  periodo.ano_mes_fnal)



    tabla_concepto(C, y - 190, formato_definido , consulta)

    C.setFont('Helvetica', 11)

    #p = Paragraph('some text. ' * 30, styles['default']),

    #p.wrapOn(C, 100, 100)
    #p.drawOn(C, 60 , y - 200)




    C.drawString(60, y- 220,"La retención efectuada fue debidamente consignada en la Dirección de Impuestos y Aduanas ")
    C.drawString(60, y -240,"Nacionales de la ciudad de Medellin . El presente certificado emitido el 13/12/2013, se expide en")
    C.drawString(60, y -260,"concordancia con las disposiciones legales contenidas en el artículo 381 del Estatuto Tributario.")
    C.drawString(60, y -280,"NOTA: Se expide sin firma autógrafa de acuerdo con el art.10 del DC.836 de 1991, y concepto")
    C.drawString(60, y -300,"DIAN 105489 de Dic de 2007.")

    C.showPage() #guarda pagina

    #guarda pdf
    C.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def tabla_datos(usuarioWeb, pdf,y):
        #Creamos una tupla de encabezados para neustra tabla
        #encabezados = ('DNI', 'Nombre', 'Apellido Paterno', 'Apellido Materno')
        #Creamos una lista de tuplas que van a contener a las personas


        nombreEmpresa_filter = Empresa.objects.filter(id_emprsa= usuarioWeb.nit_tcro_ascdo,actvo=1)

        if nombreEmpresa_filter:
            nombreEmpresa = nombreEmpresa_filter[0].nmbre_rzon_scial
        else:
            nombreEmpresa = "NO INSCRITA"


        detalles =[["NOMBRE DE LA EMPRESA" , nombreEmpresa],
                   ["NIT" , usuarioWeb.nit_tcro_ascdo ]]


        #detalles = [(empresa.cdgo_dpto, empresa.cdgo_mncpio, empresa.cdgo_pais, empresa.nmbre_rzon_scial) for empresa in Empresa.objects.all()]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table( detalles, colWidths=[8 * cm, 9 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle([
        ('BACKGROUND',(1,1),(-2,-2),colors.black),
        ('TEXTCOLOR',(0,0),(1,-1),colors.black),
        ('GRID', (0, 0), (1, 1), 1, colors.darkgray),
        ('FONTSIZE', (0, 0), (-1, -1), 10),

        ]))

        """
        detalle_orden.setStyle(TableStyle(
        [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'LEFT'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10)
                ]
        ))
        """
        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 60,y)


def tabla_concepto(pdf,y, formato_definido, consulta):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Concepto', 'Tasa %', 'Base', 'Retención')

        #Creamos una lista de tuplas que van a contener los datos

        #Consulta


        """
        consulta = "SELECT row_number() OVER (ORDER BY cd.nmbre_cncpto) AS id , cd.nmbre_cncpto as nmbre_cncpto, cdp.prcntje_aplccion as tasa, mfc.vlor_grvble AS retencion, (mfc.vlor_grvble/(cdp.prcntje_aplccion/100)) AS base \
        FROM mvmnto_frmto_cncpto AS mfc INNER JOIN cncptos_dfndos_prmtros AS cdp ON mfc.cdgo_cncpto = cdp.cdgo_cncpto AND mfc.cnta_cntble = cdp.cnta_cntble \
        INNER JOIN cncptos_dfndos AS cd ON mfc.cdgo_cncpto=cd.cdgo_cncpto AND mfc.id_emprsa=cd.id_emprsa  WHERE " \
        "mfc.id_emprsa = %s AND mfc.id_trcro = '%s' "%('890300005' , '67020646     ')
        """
        #consulta = "select * from frmtos_dfndos_view"

        #print(consulta)
        retenciones = Certificado_Retencion.objects.raw(consulta)

        #print("retenciones : " , retenciones)
        datos = []
        base_total = 0
        retencion_total = 0
        for retencion in retenciones:
            datos.append((retencion.nmbre_cncpto , retencion.tasa, int(retencion.base), retencion.retencion))
            base_total += retencion.base
            retencion_total += retencion.retencion
            #print(retencion[0] ,  retencion[1] , retencion[2] ,retencion[3] , retencion[4])
            #print(retencion.id, retencion.nmbre_cncpto)



        #print(len(datos))
        cantidad_filas = len(datos)

        total = ('Total','', int(base_total), retencion_total)
        #Establecemos el tamaño de cada una de las columnas de la tabla
        datos = Table([encabezados] + datos + [total], colWidths=[8 * cm, 3 * cm, 3 * cm, 3 * cm] )
        #Aplicamos estilos a las celdas de la tabla


        datos.setStyle(TableStyle(
        [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),

                ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                #fin caracteristicas encabezado

                #caracteristicas para el centro
                #Primera columna
                ('ALIGN',(0,1),(0,cantidad_filas),'LEFT'),
                ('ALIGN',(1,1),(3,cantidad_filas),'RIGHT'),
                ('VALIGN',(1,-2),(-1,-1),'MIDDLE'),


                #Caracteristicas para primera columna tercera fila
                ('FONTSIZE', (0, (cantidad_filas + 1)), (-1, (cantidad_filas + 1)), 10),
                ('FONT', (0, (cantidad_filas + 1)), (-1, (cantidad_filas + 1)), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN',(0,(cantidad_filas + 1)),(-1,(cantidad_filas + 1)),'RIGHT'),
                ('VALIGN',(0,(cantidad_filas + 1)),(-1,(cantidad_filas + 1)),'MIDDLE'),
                ('SPAN',(0, (cantidad_filas + 1) ),(1,(cantidad_filas + 1))),
        ]

        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla
        datos.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        datos.drawOn(pdf, 60,y)

"""
def example():

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
        # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_string('MicroPyramid', 'salida.pdf', options=options)
    response = HttpResponse(pdf ,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="salida.pdf"'

    return response
"""