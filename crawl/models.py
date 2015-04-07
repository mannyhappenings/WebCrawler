from django.db import models

class Page(models.Model):
    #url = models.URLField(primmary_key=True)
    url = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    #title_stem = models.CharField(max_length=128,db_index=True)
    content = models.CharField(max_length=256)
    #content_stem = models.CharField(max_length=256,db_index=True)
    name = models.CharField(max_length=128)
    #name_stem = models.CharField(max_length=128,db_index=True)

    def __unicode__(self):
        return self.url
    
    def __str__(self):
        return self.url
    
   #save function
   
class UrlDb(models.Model):
    url = models.CharField(max_length=128, db_index=True)
    pass
        