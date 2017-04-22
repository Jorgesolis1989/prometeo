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
from modelos_existentes.models import Usuario_Web , Certificado_Retencion, Formatos_Definidos_Enc_Pie
from modelos_existentes.models import Departamentos, Paises,Municipios , Formatos_Definidos, Documentos_Correo
import datetime
from django.shortcuts import render, redirect
from empresas.views import cargar_empresas_vinculadas, cargar_carpetas
from PROMETEO.settings import STATICFILES_DIRS
from certificados.models import Documentos

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.template.loader import get_template
from django.template import Context
#import pdfkit
from reportlab.lib.enums import TA_LEFT, TA_CENTER

from empresas.forms import FormularioVincularEmpresas
from reportlab.lib.units import inch

posicion_x = 0
posicion_y = 0

def seleccion_concepto(request, id_emprsa=None):
    # POST
    if request.POST and "btnGenerer" in request.POST:
        form = FormularioEscogerCertificado(request.POST)
        if form.is_valid():
            tipo_certificado = form.cleaned_data["tipo_certificado"]
            periodo = form.cleaned_data["periodo"]

            #return  seleccion_other()
            return generarPdf_general(request,tipo_certificado, periodo,id_emprsa )
            #return example(request)
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
    C = canvas.Canvas(buffer, pagesize=A4,  )
    C.setTitle("Certificado de- "+str(formato_definido.nmbre_frmto))

    """Encabezado"""

    #******************************************************************************************************
    # ***********************************Logo de la empresa   *********************************************
    #******************************************************************************************************
    C.setLineWidth(.3)
    posicion_x = 200
    posicion_y =  730


    try:
        C.drawImage(STATICFILES_DIRS[0]+"/images/logosEmpresas/"+str(empresa.id_emprsa)+".bmp", posicion_x, posicion_y, 70, 70)
    except OSError as e:
        C.drawImage(STATICFILES_DIRS[0]+"/images/logosEmpresas/logo-empresa-df.png", posicion_x, posicion_y, 70, 70)


    C.setFont('Helvetica', 14)

    #******************************************************************************************************
    # ***********************************Datos  de la empresa *********************************************
    #******************************************************************************************************
    distancia = 15
    posicion_x = 280
    posicion_y = 780
    C.drawString(posicion_x,posicion_y,empresa.nmbre_rzon_scial)
    C.drawString(posicion_x,posicion_y - distancia, "NIT "+str(empresa.id_emprsa))
    C.setFont('Helvetica', 11)
    C.drawString(posicion_x , posicion_y - (distancia * 2),empresa.drccion)


    departamento = Departamentos.objects.filter(cdgo_pais = empresa.cdgo_pais, cdgo_dpto= empresa.cdgo_dpto)

    municipio = Municipios.objects.filter(cdgo_pais = empresa.cdgo_pais,
                                          cdgo_dpto= empresa.cdgo_dpto,
                                          cdgo_mncpio= empresa.cdgo_mncpio , actvo=1)
    # En caso que sea colombia
    if municipio is not None:
        C.drawString(posicion_x , posicion_y - (distancia * 3),
                     municipio[0].nmbre_mncpio + ", " + departamento[0].nmbre_dpto )

    #start X, height end y, height
    #C.line(30,1125,560,1125)

    posicion_y = 713

    #******************************************************************************************************
    # ***********************************Nombre del formayo *********************************************
    #******************************************************************************************************


    C.setFont('Helvetica-Bold', 16)
    #print(60 - (len(formato_definido.nmbre_frmto)))
    C.drawString(310 - ( ( int(len(formato_definido.nmbre_frmto) /2 ) + 1 )* 10)  ,posicion_y,formato_definido.nmbre_frmto)

    #******************************************************************************************************
    # ***********************************Año gravable *********************************************
    #******************************************************************************************************
    posicion_x = 100
    C.setFont('Helvetica-Bold', 13)
    C.drawString(posicion_x + 140, posicion_y - 13,"Año Gravable "+ str(periodo))


    #******************************************************************************************************
    # ***********************************Fecha de emision     *********************************************
    #******************************************************************************************************

    C.setFont('Helvetica', 12)
    C.drawString(posicion_x + 120   , posicion_y - 30,"Fecha de emisión: "+ str(datetime.datetime.today().date()))


    #******************************************************************************************************
    # ***********************************Encabezado    *********************************************
    #******************************************************************************************************

    C.setFont('Helvetica', 11)
    descripcion_datos_encabezado = Formatos_Definidos_Enc_Pie.objects.filter(id_emprsa= empresa.id_emprsa,
                                                            cdgo_frmto = formato_definido.cdgo_frmto ,
                                                            tpo_rgstro = 1).order_by('nmro_scncial')

    descripcion = ""

    if descripcion_datos_encabezado:
        for descripcion_data in descripcion_datos_encabezado:
            descripcion += descripcion_data.dscrpcion_cmpo +  " "
    else:
        descripcion = ""
    #print(descripcion)
    posicion_y = poner_parrafo(C, 59 , posicion_y - 40  , descripcion , 81)


    #******************************************************************************************************
    # ***********************************Retencion practicada a   *****************************************
    #******************************************************************************************************
    posicion_y -= 45
    C.setFont('Helvetica-Bold', 13)
    C.drawString(posicion_x - 40, posicion_y,"RETENCIÓN PRACTICADA A: ")

    #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
    #cabecera(pdf)
    posicion_y -= 40
    tabla_datos(usuario_Web, C, posicion_y)

    #******************************************************************************************************
    # ***********************************Por conceptos   **************************************************
    #******************************************************************************************************
    posicion_y -= 30
    C.setFont('Helvetica', 11)
    C.drawString(posicion_x - 40, posicion_y,"Por los conceptos que se detallan acontinuación: ")


    #******************************************************************************************************
    # ***********************************Por conceptos   **************************************************
    #******************************************************************************************************
    numero_a_retener = str(usuario_Web.nit_tcro_ascdo)
    for i in range(13 - len(usuario_Web.nit_tcro_ascdo)):
        numero_a_retener += ' '

    #print(numero_a_retener,"#")

    consulta = "SELECT row_number() OVER (ORDER BY cd.nmbre_cncpto) AS id , cd.nmbre_cncpto as nmbre_cncpto, cdp.prcntje_aplccion as tasa, mfc.vlor_grvble AS retencion, (mfc.vlor_grvble/(cdp.prcntje_aplccion/100)) AS base \
        FROM mvmnto_frmto_cncpto AS mfc INNER JOIN cncptos_dfndos_prmtros AS cdp ON mfc.cdgo_cncpto = cdp.cdgo_cncpto AND mfc.cnta_cntble = cdp.cnta_cntble \
        INNER JOIN cncptos_dfndos AS cd ON mfc.cdgo_cncpto=cd.cdgo_cncpto AND mfc.id_emprsa=cd.id_emprsa  WHERE " \
        "mfc.id_emprsa = %s AND mfc.id_trcro = '%s' and mfc.ano_mes_fnal= '%s' ;"%(str(empresa.id_emprsa) , numero_a_retener ,  periodo.ano_mes_fnal)



    tabla_concepto(C, posicion_y - 100, formato_definido , consulta)


    #******************************************************************************************************
    # ***********************************Pie de pagina   **************************************************
    #******************************************************************************************************

    descripcion_datos_pie = Formatos_Definidos_Enc_Pie.objects.filter(id_emprsa= empresa.id_emprsa,
                                                    cdgo_frmto = formato_definido.cdgo_frmto ,
                                                    tpo_rgstro = 2).order_by('nmro_scncial')

    descripcion = ""

    if descripcion_datos_pie:
        for descripcion_data in descripcion_datos_pie:
            descripcion += descripcion_data.dscrpcion_cmpo +  " "
    else:
        descripcion = ""


    C.setFont('Helvetica', 11)
    poner_parrafo(C, 60 , posicion_y -200 , descripcion, 95)


    C.showPage() #guarda pagina

    #guarda pdf
    C.save()


    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  """""""""""""""""""""""""""""""
                Aca se guarda el correo en la tabla usrios_web_mnjo_flders_det
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" """""""""""""""""""""""""""""""
    documento_correo = Documentos_Correo()
    documento_correo.email_usrio = usuario_Web.email_usrio
    documento_correo.asnto_dcmnto = "Generado " + formato_definido.nmbre_frmto
    documento_correo.nmro_flder = 0
    try:
        ultimo_registro = Documentos_Correo.objects.latest('id_dcmnto').id_dcmnto
    except Documentos_Correo.DoesNotExist as e:
        ultimo_registro = 0

    documento_correo.id_dcmnto = ultimo_registro + 1
    documento_correo.fcha_dcmnto = datetime.datetime.now()

    try:
        documento_correo.save()
    except Exception as e:
        print("No guardo " + e)


    documento = Documentos()
    documento.id_dcmnto = documento_correo.id_dcmnto

    try:
        documento.save()
    except Exception as e:
        print(e)

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

        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 60,y)


def tabla_concepto(pdf,y, formato_definido, consulta):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Concepto', 'Tasa %', 'Base', 'Retención')

        #Creamos una lista de tuplas que van a contener los datos
        #consulta = "select * from frmtos_dfndos_view"

        #print(consulta)
        retenciones = Certificado_Retencion.objects.raw(consulta)

        #print("retenciones : " , retenciones)
        datos = []
        base_total = 0
        retencion_total = 0
        contador =0
        for retencion in retenciones:
            contador += 1
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
        datos.drawOn(pdf, 60,y - (contador * 10))

def poner_parrafo(C, x , y , parrafo , limite):

    var_x = x
    var_y = y
    separador = 15
    #print("len " , int(len(parrafo) / limite))
    tamanio = int(len(parrafo) / limite) + 1
    #print("tamanio " , tamanio , len(parrafo))
    for i in range(tamanio):

        var_y  -= separador
        if len(parrafo) > (i + 1 )      * limite:
            sub_parrafo = parrafo[(i* limite):(i + 1 )* limite]
            #mayusculas = len([c for c in sub_parrafo if c.isupper()])

            C.drawString(var_x, var_y-separador ,sub_parrafo )
            #C.drawString(var_x, var_y-separador ,"de sin firma autógrafa de acuerdo con el artículo 10 del decreto 836 de 1991 y concepto dian 10kk")
            #print(str(len(parrafo[(i* limite):(i + 1 )* limite])))
            #C.drawString(540 , var_y-separador, '-')
        else:
            C.drawString(var_x, var_y-separador , parrafo[(i* limite):len(parrafo)])

    #print("car y " , var_y)

    return  var_y




def example(request):
    # Generate PDF from a web URL (maybe only from your project)
    #pdfkit.from_url('http://google.com', 'out.pdf')
    # Generate PDF from a html file.
    #pdfkit.from_file('file.html', 'out.pdf')
    # Generate PDF from a plain html string.
    pdf = pdfkit.from_string('<h1>Hello</h1>!', 'out.pdf')

        # Generate download
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="hola.pdf"'

    return response
