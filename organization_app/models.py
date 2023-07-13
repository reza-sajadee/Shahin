from django.db import models
from django.db.models.fields.related import ForeignKey , ManyToManyField
from profile_app.models import Profile
from autocomplete import HTMXAutoComplete, widgets 
# Create your models here.


class Rade(models.Model):
    title                = models.CharField(max_length=150)
    radeCode             = models.CharField(max_length=15)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
    

class Hoze(models.Model):
    title                = models.CharField(max_length=150)
    hozeCode             = models.CharField(max_length=15)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
    
class Bakhsh(models.Model):
    title                = models.CharField(max_length=150)
    bakhshCode           = models.CharField(max_length=15)
    hoze                 = models.ForeignKey(Hoze , blank=True, null=True, related_name="hoze" , on_delete = models.CASCADE )
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
 
class Daste(models.Model):
    title                = models.CharField(max_length=150)
    dasteCode            = models.CharField(max_length=15)
    bakhsh               = models.ForeignKey(Bakhsh , blank=True, null=True, related_name="bakhsh" , on_delete = models.CASCADE )
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    

class SatheVahed(models.Model):
    title                = models.CharField(max_length=150)
    satheVahedCode       = models.CharField(max_length=15)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    

class TypePostSazmani(models.Model):
    title                = models.CharField(max_length=150)
    typePostSazmaniCode  = models.CharField(max_length=15)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
 

class Vahed(models.Model):
    title                = models.CharField(max_length=150 , blank=True,null=True)
  
    vahedMafogh          = models.ForeignKey('self', null=True,  blank=True , related_name='vahedMafoghChart' , on_delete = models.CASCADE)
    
    satheVahed           = models.ForeignKey(SatheVahed , blank=True, null=True, related_name="satheVahedChart" , on_delete = models.CASCADE )
    
    typePostSazmani      = models.ForeignKey(TypePostSazmani , blank=True, null=True, related_name="postSazmaniChart" , on_delete = models.CASCADE )
    daste                = models.ForeignKey(Daste , blank=True, null=True, related_name="DasteChart" , on_delete = models.CASCADE )
    bakhsh               = models.ForeignKey(Bakhsh , blank=True, null=True, related_name="bakhshChart" , on_delete = models.CASCADE )
    hoze                 = models.ForeignKey(Hoze , blank=True, null=True, related_name="hozeChartVahed" , on_delete = models.CASCADE )
    
    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)

    def __str__(self):
        return self.vahedCode()+' - ' + self.title
        #return str(self.id)
    def vahedCode(self):
        if(self.bakhsh == None and self.daste ==None ):
            return self.hoze.hozeCode + '000' + '000' 
        else:

            return self.hoze.hozeCode + self.bakhsh.bakhshCode + self.daste.dasteCode 
     

class SathPost(models.Model):
    title                = models.CharField(max_length=150)
    sathPostCode             = models.CharField(max_length=15)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    

class IndexMahaleKhedmat(models.Model):
    title = models.CharField(max_length=150)
    indexCode = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title 
    
    

class Post(models.Model):
    title                  = models.CharField(max_length=150 , blank=True,null=True)
    vahed                  = models.ForeignKey(Vahed , blank=True, related_name="chartPostSazmaniVahedCode" , on_delete = models.CASCADE ) 
    SathPost               = models.ForeignKey(SathPost , blank=True, related_name="chartPostSazmaniSathePostCode" , on_delete = models.CASCADE ) 
    zarfiyateMojaz         = models.IntegerField( blank=True , null=True)
    janamayiFeli           = models.IntegerField( blank=True , null=True)
    indexMahaleKhedmat     = models.ForeignKey(IndexMahaleKhedmat , blank=True, related_name="chartPostSazmaniIndexMahaleKhedmat" , on_delete = models.CASCADE ) 
    RadePostSazmani        = models.ForeignKey(Rade , blank=True, related_name="RadePostSazmaniCode" , on_delete = models.CASCADE ) 
    PostTypePostSazmani        = models.ForeignKey(TypePostSazmani , blank=True , null=True ,related_name="PostTypePostSazmani" , on_delete = models.CASCADE)
    postMafogh             = models.ForeignKey('self', null=True,  blank=True , related_name='PostMafoghCode' , on_delete = models.CASCADE)
    
    
    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    def codePostSazmani(self):
        return str(self.vahed.vahedCode()) + str(self.PostTypePostSazmani.typePostSazmaniCode)
    def __str__(self):
        return str(self.codePostSazmani() )
        #return str(self.id )
    
   
    
class JobBank(models.Model):
    
    jaNamayi              =models.CharField(max_length=150 , blank=True,null=True)
    indexKhedmat          =models.CharField(max_length=150 , blank=True,null=True)
    jobBankPost           = models.ForeignKey(Post , blank=True , null=True ,related_name="jobBankPost" , on_delete=models.CASCADE)
    profile               = models.ForeignKey(Profile , blank=True, null=True, related_name="profileCode" ,  on_delete = models.SET_NULL )
    counter               = models.IntegerField(default=0)
    
    created_at            = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at            = models.DateTimeField(auto_now=True , blank=True,null=True)

    
    
    def get_Job(self , id):
        return JobBank.objects.all().filter(id = id)[0]
    def get_codeShoghlSazmani(self):
        try:
            return str(self.jobBankPost.codePostSazmani()) + str(self.counter).zfill(3)
        except:
            return str('کد ندارد')
    def __str__(self):
        modelName = ''
        if (self.jobBankPost != None):
            modelName = str(self.jobBankPost.title)
        else:
            modelName = 'عنوان پست موجود نیست'
        if(self.profile):
            modelName = modelName + str(self.profile.firstName)
        else:
            modelName = 'فرد موجود نیست'
        if(self.profile):
            modelName = modelName + str(self.profile.lastName)
        else:
            modelName = 'فرد موجود نیست'
        
        return  modelName + '- ' + str(self.id)
        
  

class  GetItemsMultiAutoComplete(HTMXAutoComplete):
    name = "members"
    multiselect = True

    class Meta:
        model = JobBank


class PostDescription(models.Model):
    exclusive             = models.TextField(blank=True , null=True)    
    general               = models.TextField(blank=True , null=True    )
    typePostRelated           = models.ForeignKey(TypePostSazmani , blank=True , null=True , related_name="typePostRelated" , on_delete = models.CASCADE ) 
    created_at            = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at            = models.DateTimeField(auto_now=True , blank=True,null=True)

    
    
    def get_exclusive(self):
        return (self.exclusive.split('-'))
    def get_general(self):
        return (self.general.split('-'))
    
    def __str__(self):

            return str(self.typePostRelated.title)
        