from django.contrib.auth.models import AbstractUser


# custom user model just in case we need to add functionality
class User(AbstractUser):
    pass
