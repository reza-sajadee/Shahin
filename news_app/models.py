from django.db import models
from jalali_date import date2jalali 
# Create your models here.
class Categoriy(models.Model):
    
    title            = models.CharField(max_length=250 )

    
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = " دسته بندی اخبار "
        verbose_name_plural = " دسته بندی اخبار "
    
    def __str__(self):
        return self.title 
    
class News(models.Model):
    title           = models.CharField(max_length=250,verbose_name = 'عنوان خبر' ,blank=True , null=True)
    image           = models.ImageField(upload_to='images/news', verbose_name = 'عکس' ,blank=True , null=True)
    description     = models.TextField(verbose_name = 'متن خبر'  ,blank = True ,null = True)
    NewsCategoriy   = models.ForeignKey(Categoriy ,verbose_name = 'دسته بندی خبر'  , related_name='NewsCategoriy' , on_delete = models.CASCADE ,blank = True ,null = True)    
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "   اخبار "
        verbose_name_plural = "   اخبار "
    
    def __str__(self):
        return str(self.id )
    
    def get_jalali_date(self):
        return date2jalali(self.updated_at)