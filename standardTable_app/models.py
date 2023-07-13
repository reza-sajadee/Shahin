from django.db import models
from django.db.models.fields.related import ForeignKey , ManyToManyField

from organization_app.models import Vahed
#جدول لیست پرسنلی
class StandardList(models.Model):
    pass

language_choices = (
    ("فارسی", "فارسی"),
    ("انگلیسی", "انگلیسی")
)

vaziyatEjra_choices = (
    ("پیاده‌سازی شده و در حال اجرا", "پیاده‌سازی شده و در حال اجرا"),
    ("در حال طرح‌ریزی", "در حال طرح‌ریزی"),
    ("معلق", "معلق"),
    ("جایگزین شده است", "جایگزین شده است"),
    ("اقدامی صورت نگرفته", "اقدامی صورت نگرفته"),
)

typeStandard_choices = (
    ("مدیریتی", "مدیریتی"),
    ("فنی و تخصصی (عملیاتی)", "فنی و تخصصی (عملیاتی)"),
    ("محصول", "محصول"),
    ("سایر", "سایر")
)
geoDomainStandard_choices = (
    ("بین‌المللی", "بین‌المللی"),
    ("منطقه‌ای", "منطقه‌ای"),
    ("ملی", "ملی"),
    ("سازمانی", "سازمانی")
    
)

class StandardReferenceRelease(models.Model):
    persianReferenceName = models.CharField(max_length=250 , blank=True, null=True)
    englishReferenceName = models.CharField(max_length=250 , blank=True, null=True)
    namad                = models.CharField(max_length=10 , blank=True, null=True)
    website              = models.CharField(max_length=60 , blank=True, null=True)
    phoneNumber          = models.CharField(max_length=60 , blank=True, null=True)
    
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.persianReferenceName 


class Standard(models.Model):
    standardNumber                       = models.CharField(max_length=250, blank=True, null=True)
    standardTitlePersian                 = models.CharField(max_length=250, blank=True, null=True)
    standardTitleEnglish                 = models.CharField(max_length=250 , blank=True, null=True)
    namad                                = models.CharField(max_length=250 , blank=True, null=True)
    vaziyatEjra                          = models.CharField(max_length=250 , choices=vaziyatEjra_choices , blank=True, null=True)
    shamsiReleaseDate                    = models.CharField(max_length=250, blank=True, null=True)
    miladiReleaseDate                    = models.CharField(max_length=250, blank=True, null=True)
    tajdidNazarNumber                    = models.CharField(max_length=250, blank=True, null=True)
    refrerence                           = models.ForeignKey(StandardReferenceRelease , blank=True, null=True, related_name="refrerence" , on_delete = models.CASCADE )
    language                             = models.CharField(max_length=250 , choices=language_choices, blank=True, null=True)
    typeStandard                         = models.CharField(max_length=250 , choices=typeStandard_choices, blank=True, null=True)
    geoDomainStandard                    = models.CharField(max_length=250 , choices=geoDomainStandard_choices, blank=True, null=True)
    internationalStandardReference       = models.CharField(max_length=250, blank=True, null=True)
    internationalStandardReferenceNumber = models.CharField(max_length=250, blank=True, null=True)
    #کد واحد متولی
    
    vahedMotevaliCode    = models.ForeignKey(Vahed , blank=True, null=True, related_name="unitMotevaliCode2" , on_delete = models.CASCADE )
    vahedMortabetCode    = models.ManyToManyField(Vahed , blank=True,  related_name="unitMortabetCode3"  )
    
    #کد واحد ناظر
   
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
 

    def __str__(self):
        return  str(self.standardNumber)
    



class RequirementStandards(models.Model):
    
    clauseNumber        = models.CharField(verbose_name = 'شماره بند' , max_length=250  , blank=True, null=True)
    title               = models.CharField(verbose_name = 'عنوان' , max_length=250 , blank=True, null=True) 
    text                = models.TextField(verbose_name = 'متن' , blank=True, null=True)
    description         = models.TextField(verbose_name = 'توضیحات' , blank=True, null=True)
    
    parentClause        = models.ForeignKey('self' ,verbose_name = 'بند پدر' , on_delete=models.CASCADE, null=True, blank=True , related_name="parent")
    childClause         = models.ManyToManyField('self' ,verbose_name = 'زیربند ها' ) 
    standard            = models.ForeignKey(Standard ,verbose_name = 'Standard' , on_delete=models.CASCADE)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "الزامات استاندارد"
        verbose_name_plural = "الزامات استاندارد"
    
    def __str__(self):
        #return  str(self.standard.standardNumber) + ' - ' + str(self.clauseNumber )
        return  str(self.id)