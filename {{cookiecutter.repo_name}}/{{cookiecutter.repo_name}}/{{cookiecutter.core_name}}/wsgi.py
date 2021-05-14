from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()
application = get_wsgi_application()
