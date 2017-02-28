# Clase para conectar el backend de la clase USUARIO y el user de Django.
from django.contrib.auth.models import User, check_password

class BackendUsuarios(object):
	def authenticate(self, username=None, password=None):

		try:
			#Obtenga el usuario
			usuario = User.objects.get(email=username)
			if usuario is not None:
				if check_password(password, usuario.password):
					return usuario
				# Si el password es incorrecto
				else:
					return None
			# Si el usuario esta vacio
			else:
				return None
		# Error en el acceso a la BD
		except User.DoesNotExist:
			return None


	def get_user(self, user_id):
		try:
			return User.objects.get(id=user_id)
		except User.DoesNotExist:
			return None