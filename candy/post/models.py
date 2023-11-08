from django.db import models

# Create your models here.
class Posting(models.Model):
    title=models.CharField('Title', max_length=80)
    content = models.TextField('Content')
    upload_time = models.DateTimeField('Upload Time')

    def __str__(self):
        return self.title