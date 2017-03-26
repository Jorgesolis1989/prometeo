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
from modelos_existentes.models import Departamentos, Paises,Municipios , Formatos_Definidos


def generarPdf_general(request, tipo_certificado, periodo, id_empresa_vinculada):

    #Empresa
    empresa = Empresa.objects.get(id_emprsa= id_empresa_vinculada)
    logo_empresa = Empresa_Con_Logo.objects.get(id_emprsa=id_empresa_vinculada)

    # Formato
    try:
        formato_definido = Formatos_Definidos.objects.get(id_emprsa = empresa.id_emprsa , cdgo_frmto= tipo_certificado,
                                                         actvo=1)
    except Formatos_Definidos.DoesNotExist as e:
        print("No existe" + e)

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


    ## tabla header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.fontSize = 11
    styleBH.alignment = TA_CENTER

    corporacion = Paragraph('''Corporación''', styleBH)
    planchanum = Paragraph('''# Plancha''', styleBH)
    principal = Paragraph('''Candidato Principal''', styleBH)
    suplente = Paragraph('''Candidato Suplente''', styleBH)
    numvotos = Paragraph('''# Votos''', styleBH)

    ##table
    styles = getSampleStyleSheet()
    styleBH.alignment = TA_CENTER
    styleN = styles["BodyText"]
    styleN.fontSize =8

    width, height =A4

    high = 1000

    registros = []

    #obteniendo datos

    data = []
    data.append([corporacion,planchanum,principal,suplente,numvotos])
    sendToTable(data, registros, high, C)
    registros= []
    high = high - 80

    C.showPage() #guarda pagina

    #guarda pdf
    C.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def sendToTable(data, registros, high, C):
    #data.append(registros)

    for registro in registros:

        #this_registro = [registro['Corporación'],registro['NoPlancha'],registro['CandidatoPrincipal'],registro['CandidatoSuplente'],
                        # registro['NoVotos']]

        #data.append(this_registro)

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
