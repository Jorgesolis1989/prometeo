from certificados.forms import FormularioEscogerCertificado
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, cm, landscape, A3
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generarPdf_general(request, tipo_reporte):

    #crea la cabezera HttpResponse con PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reporte-de-elecciones'+ str()+'.pdf'
    #Crea el objeto pdf, usando el objeto BytesIO
    buffer = BytesIO()
    #size = landscape(A4)
    C = canvas.Canvas(buffer, pagesize=A3)
    C.setTitle("Certificado de- "+str())

    #Encabezado
    C.setLineWidth(.3)
    C.setFont('Helvetica-Bold', 22)
    C.drawString(30,1150,"SIVORE")
    #C.drawImage('http://http://54.200.145.159:8080/static/media/sql_soluciones.png', 730,1090, 50, 70)
    C.setFont('Helvetica', 12)
    C.drawString(30,1135,"Sistema PROMETEO")
    #start X, height end y, height
    C.line(30,1125,560,1125)
    C.setFont('Helvetica-Bold', 16)
    C.drawString(330,1100,"Reporte de Elecciones")
    C.setFont('Helvetica-Bold', 13)
    C.drawString(30,1060,"Nombre de la Jornada: "+ str())


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

    width, height =A3

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
    width, height = A3
    table = Table(data, colWidths=[12.5 * cm, 2.2 * cm, 6.0 * cm, 6.0 * cm, 1.9 * cm, 1.9 * cm])



    #stilos de la tabla
    table.setStyle(TableStyle([('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0,0),(-1,-1), 0.25, colors.black)]))
    #pdf size
    table.wrapOn(C, width, height)
    table.drawOn(C, 30, high)
