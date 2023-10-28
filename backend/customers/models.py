from django.db import models
from beautician.models import *


class Customer(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    image=models.CharField(max_length=300,blank=True,null=True)
    isblocked=models.CharField(max_length=200,default="False")
    wallet_amount=models.DecimalField(max_digits=10,decimal_places=2)


    def __str__(self):
        return f"{self.name} - {self.email} - {self.phone}"
    


class Appointment(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    beautician=models.ForeignKey(Beautician,on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    studio=models.ForeignKey(Studio,on_delete=models.CASCADE)
    service=models.ForeignKey(Servicefees,on_delete=models.CASCADE)
    booked_timing=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200,default="Confirmed")


    def __str__(self):
        return f"{self.customer.email} - {self.beautician.name}"

class Review(models.Model):
    beautician=models.ForeignKey(Beautician,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    content=models.CharField(max_length=200)
   

class FavouriteStylists(models.Model):
    beautician=models.ForeignKey(Beautician,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)


   
class Workshop(models.Model):
    beautician=models.ForeignKey(Beautician,on_delete=models.CASCADE)
    customers=models.ManyToManyField(Customer,related_name="workshop")
    subject=models.CharField(max_length=200)
    total_seats=models.PositiveIntegerField()
    conducting_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status=models.CharField(max_length=200,default="To be conducted")
    description=models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    registration_deadline = models.DateField()


   
    def __str__(self):  
        return f"{self.beautician.name} - {self.subject} -{self.conducting_date}"
    

class WorkshopBooking(models.Model):
    workshop=models.ForeignKey(Workshop,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    booked_date=models.DateField(auto_now_add=True)
    booked_time=models.TimeField(auto_now_add=True)
    status=models.CharField(max_length=200,default="Confirmed")
    

   
    def __str__(self):  
        return f"{self.customer.name},{self.booked_time} "
    
class WorkshopLink(models.Model):
    workshop=models.ForeignKey(Workshop,on_delete=models.CASCADE)
    link_id=models.CharField(max_length=200)
    
    

   
    def __str__(self):  
        return f"{self.link_id},{self.workshop.subject} "