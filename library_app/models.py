from django.db import models

# Create your models here.
def user_directory_path_library(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'library_document/{0}'.format( filename)
class fileProfile(models.Model):
    CATEGORY_STATUS  = (('all','همه'),('video','فیلم'),('article','مقاله') )
    
    title= models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True ) 
    fileUploaded= models.FileField(upload_to=(user_directory_path_library) ,blank=True, null=True)
    imageUploaded = models.FileField(upload_to=(user_directory_path_library) ,blank=True, null=True)
    category = models.CharField(max_length=100 ,choices= CATEGORY_STATUS , default='video' )
    
    
    
    
    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    class Meta:
        verbose_name = "فایل  کتابخانه"
        verbose_name_plural = "فایل  کتابخانه"
    
    def __str__(self):
        return str(self.id)  