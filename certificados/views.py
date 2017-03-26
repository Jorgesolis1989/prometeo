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
from empresas.models import Empresa_Con_Logo
from modelos_existentes.models import Usuario_Web , Usuario_Web_Vinculacion_Empresa
from modelos_existentes.models import Departamentos, Paises,Municipios , Formatos_Definidos
import datetime
from django.shortcuts import render, redirect
from empresas.views import cargar_empresas_vinculadas, cargar_logos_empresas, cargar_carpetas

from empresas.forms import FormularioVincularEmpresas
from reportlab.lib.units import inch


def seleccion_concepto(request, id_emprsa=None):
    # POST
    if request.POST and "btnGenerer" in request.POST:
        form = FormularioEscogerCertificado(request.POST)
        print(form)
        if form.is_valid():
            tipo_certificado = form.cleaned_data["tipo_certificado"]
            print(tipo_certificado)
            periodo = form.cleaned_data["periodo"]
            return generarPdf_general(request,tipo_certificado, periodo,id_emprsa )
        else:
            print("no valido")

    try:
        empresa_logo = Empresa_Con_Logo.objects.get(id_emprsa=id_emprsa)
    except Exception:
        return redirect('login_user')

    logo_empresa = empresa_logo.lgtpo_emprsa

    formatos = Formatos_Definidos.objects.filter(actvo=1, id_emprsa=id_emprsa)

    """tupla_formatos = []
    for formato in formatos:
        tupla_formatos.append((formato.cdgo_frmto , formato.nmbre_frmto))
    """
    form = FormularioEscogerCertificado()

    form.fields['tipo_certificado'].queryset = formatos

    return render(request, 'seleccion-concepto.html', {'empresas_vinculadas': cargar_empresas_vinculadas(request) ,
                                                       'logos_empresas': cargar_logos_empresas(request),
                                                       'logo_empresa':logo_empresa , 'carpetas': cargar_carpetas(request) ,
                                                        'FormularioEscogerCertificado': form
                                                        })


def generarPdf_general( request, formato_definido, periodo, id_empresa_vinculada):

    #Empresa que practica retención
    empresa = Empresa.objects.get(id_emprsa= id_empresa_vinculada)
    logo_empresa = Empresa_Con_Logo.objects.get(id_emprsa=id_empresa_vinculada)

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
    C.drawImage(logo_empresa.lgtpo_emprsa.url, 120, 730, 200, 100)
    C.setFont('Helvetica', 14)

    # Titulo de la empresa
    distancia = 15
    posicion_x_titulo = 330
    posicion_y_titulo = 780
    C.drawString(posicion_x_titulo,posicion_y_titulo,empresa.nmbre_rzon_scial)
    C.drawString(posicion_x_titulo,posicion_y_titulo - distancia, "NIT "+str(empresa.id_emprsa))
    C.setFont('Helvetica', 11   )
    C.drawString(posicion_x_titulo , posicion_y_titulo - (distancia * 2),empresa.drccion)


    departamento = Departamentos.objects.filter(cdgo_pais = empresa.cdgo_pais, cdgo_dpto= empresa.cdgo_dpto)

    municipio = Municipios.objects.filter(cdgo_pais = empresa.cdgo_pais,
                                          cdgo_dpto= empresa.cdgo_dpto,
                                          cdgo_mncpio= empresa.cdgo_mncpio , actvo=1)
    # En caso que sea colombia
    if municipio is not None:
        C.drawString(posicion_x_titulo , posicion_y_titulo - (distancia * 3),
                     municipio[0].nmbre_mncpio + ", " + departamento[0].nmbre_dpto )

    C.setFont('Helvetica-Bold', 16)
    C.drawString(180,715,formato_definido.nmbre_frmto)
    C.setFont('Helvetica-Bold', 13)
    C.drawString(220, 700,"Año Gravable "+ periodo)

    C.setFont('Helvetica', 13)
    C.drawString(180, 670,"Fecha de emisión: "+ str(datetime.datetime.today().date()))


    C.setFont('Helvetica-Bold', 13)
    C.drawString(60, 620,"RETENCIÓN PRACTICADA A: ")

    #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
    #cabecera(pdf)
    y = 580
    tabla_datos(usuario_Web, C, y)


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
        print(nombreEmpresa_filter)

        if nombreEmpresa_filter:
            print("entre")
            nombreEmpresa = nombreEmpresa_filter[0].nmbre_rzon_scial
        else:
            nombreEmpresa = "NO INSCRITA"


        detalles =[["NOMBRE DE LA EMPRESA" , nombreEmpresa],
                   ["NIT" , usuarioWeb.nit_tcro_ascdo ]]
        print(detalles)

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

def sendToTable(data, registros, high, C):
    data.append(registros)

    for registro in registros:

        this_registro = [registro['Corporación'],registro['NoPlancha'],registro['CandidatoPrincipal'],registro['CandidatoSuplente'],
                        registro['NoVotos']]

        data.append(this_registro)

        high = high - 18


    #table size
    width, height = A4
    table = Table(data, colWidths=[12.5 * cm, 2.2 * cm, 6.0 * cm, 6.0 * cm, 1.9 * cm, 1.9 * cm])



    #stilos de la tabla
    table.setStyle(TableStyle([('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0,0),(-1,-1), 0.25, colors.black)]))
    #pdf size
    table.wrapOn(C, width, height)
    table.drawOn(C, 30, high)
