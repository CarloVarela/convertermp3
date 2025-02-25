Mi Proyecto Flask
Una aplicación web construida con Flask que incluye autenticación de usuarios y un convertidor de texto a audio con soporte para selección de idioma.

Características
Registro e inicio de sesión:
Permite a los usuarios registrarse usando su correo electrónico y una contraseña.

Convertidor de Texto a Audio:
Utiliza gTTS para convertir texto a audio y permite descargar el archivo resultante.
Además, ofrece la opción de seleccionar el idioma (por ejemplo, español o inglés) para la conversión.

Diseño inspirado en Cosmos e IA:
La interfaz cuenta con un fondo de cosmos y una sección de noticias sobre inteligencia artificial.

Tecnologías
Flask: Framework web de Python.
Flask-SQLAlchemy: ORM para interactuar con la base de datos.
Flask-Login: Manejo de autenticación de usuarios.
Flask-Migrate: Gestión de migraciones de base de datos.
gTTS: API de Google Text-to-Speech para la conversión de texto a audio.
pydub: Para postprocesar el audio (modificar el tono, etc.).