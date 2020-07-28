from django.db import models
from login_reg_app2.models import User

# Create your models here.

class QuoteManager(models.Manager):
    def validate_quote(self, postData):
        errors = {}

        if len(postData['author'])<3:
            errors['author'] = 'Author name must be 3 or more characters'

        if len(postData['quote_text'])<10:
            errors['quote_text'] = 'Qutoe must be 10 or more characters'
        return errors


class Quote(models.Model):
    owner = models.ForeignKey(User, related_name='quotes', on_delete=models.CASCADE)
    author = models.TextField(max_length=50)
    quote_text = models.TextField(max_length= 1000)
    liked_by = models.ManyToManyField(User, related_name='liked_quotes')
    objects = QuoteManager()