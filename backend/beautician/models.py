from django.db import models





class Services(models.Model):
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    is_available=models.BooleanField(default=True)
    image=models.CharField(max_length=350,blank=True,null=True)

    def __str__(self):
        return f"{self.name} - {self.description} "
    

class Beautician(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    image=models.CharField(max_length=300,blank=True,null=True)
    # services=models.ManyToManyField(Services,related_name='beauticians_providing_services')
    isblocked=models.CharField(max_length=200,default="False")
    wallet_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    appointment_count=models.PositiveIntegerField(default=0)
    bio=models.CharField(max_length=200,default=" ",blank=True,null=True)
   

    def __str__(self):
        return f"{self.name} - {self.email} - {self.phone}"
    
class Servicefees(models.Model):
    beautician=models.ForeignKey(Beautician,on_delete=models.CASCADE)  
    service=models.ForeignKey(Services,on_delete=models.CASCADE)
    servicefee=models.PositiveIntegerField(null=True)
    blocked=models.BooleanField(default=False)
    topservice=models.BooleanField(default=False)

class Blockeddate(models.Model):
    beautician=models.ForeignKey(Beautician,on_delete=models.CASCADE)
    date=models.DateField()
    
    def __str__(self):
        return f"{self.beautician.name} - {self.date}"
    

class Studio(models.Model):
    beautician=models.ForeignKey(Beautician,on_delete=models.CASCADE)
    studio_name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    place=models.CharField(max_length=200)
    district=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    pincode=models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):  
        return f"{self.beautician.name} - {self.locality} -{self.place}"

class OTP(models.Model):
    otp=models.PositiveIntegerField(blank=True,null=True)
    email=models.CharField(max_length=200,blank=True,null=True)
    

    def __str__(self):
        return f"{self.otp}"


