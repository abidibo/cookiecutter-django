from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

load_dotenv()
application = get_asgi_application()
