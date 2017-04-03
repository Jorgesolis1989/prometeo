import psycopg2
import base64
from modelos_existentes.models import Empresa
from PROMETEO.settings import STATICFILES_DIRS

def cargar_logo_empresa():
  conn_string = "host='localhost' dbname='prometeo' user='postgres' password='postgres'"
  conn = psycopg2.connect(conn_string)

  # Leer la imagen
  cursor = conn.cursor()
  cursor.execute("SET SCHEMA 'sql_soluciones';")


  empresas = Empresa.objects.filter(actvo=True)

  for empresa in empresas:

      cursor.execute("SELECT (lgtpo_emprsa) FROM emprsas WHERE id_emprsa="+ str(empresa.id_emprsa) + ";")
      mypic2 = cursor.fetchone()
      if mypic2[0] is not None:
          b64data = str(base64.b64encode(mypic2[0]))
          substrx = b64data[1:]
          picdata = base64.b64decode(substrx)
          f = open(STATICFILES_DIRS[0] +'/images/logosEmpresas/'+str(empresa.id_emprsa)+ '.bmp', 'wb')
          f.write(picdata)
          f.close()


  cursor.close()
  conn.close()


