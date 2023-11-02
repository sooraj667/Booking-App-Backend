from rest_framework.response import Response 
from rest_framework.views import APIView
from .models import Appointment
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from beautician.models import *
from beautician.serializers import *
from datetime import datetime
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import random
from rest_framework.serializers import Serializer
from dateutil import parser


def generate_otp():
    return str(random.randint(1000, 9999))



class Confirmotp(APIView):
    def post(self,request):
        user_entered_otp=request.data.get("otp")
        email=request.data.get("email")
        try:
            otpobj=OTP.objects.get(otp=user_entered_otp,email=email)
            otpobj.delete()
            return Response({"message":'Success'}) 
        except:
            return Response({"message":'Failed'})

class Signup(APIView):
    def post(self,request):
        pname=request.data.get("pname")
        email=request.data.get("email")
        phone=request.data.get("phone")
        password=request.data.get("password")

        try:
            check_obj=Customer.objects.get(email=email)
            return Response({"message":'Email-Failed'}) 
        except:
            pass

        try:
            check_obj=Customer.objects.get(phone=phone)
            return Response({"message":'Phone-Failed'}) 
        except:
            pass

        otpvalue=generate_otp()
        OTP.objects.create(otp=otpvalue,email=email)
      
        subject = "OTP for registration in Groom UP"
        message = f"Your OTP for registration is {otpvalue}.Please enter this otp to register."
        recipient = email
        send_mail(subject, 
              message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)

        hashed_password=make_password(password)

        newobj=Customer.objects.create(name=pname,email=email,phone=phone,password=hashed_password,wallet_amount=0)
        serialized_object=Customerserializer(newobj)
        return Response({"message":'Created',"beautdata":serialized_object.data})
    
    
class Login(APIView):
    
    def post(self,request):
        email=request.data.get("email")
        password=request.data.get("password")
        try:
            custobj=Customer.objects.get(email=email)
        except:
            return Response({"message":'NotMatched'})

        valid=check_password(password,custobj.password)

        if not valid:
            return Response({"message":'NotMatched'})


        found=Customer.objects.filter(email=email).count()    
        if valid:
            
            serialized_object=Customerserializer(custobj)
            allbeauticians=Beautician.objects.all()
           
            allbeauticians_serialized=BeauticianSerializer(allbeauticians,many=True)
           
            # for item in allbeauticians:
            #     required_id=item.id
            #     expertinobj=item.expertin 
            #     for item in allbeauticians_serialized.data:
            #         if item["id"]==required_id:
            #             item["expertin"]=ServicesSerializer(expertinobj).data
                
            refresh=RefreshToken.for_user(custobj)  
            return Response({"message":'Matched',"custdata":serialized_object.data,"allbeautdata":allbeauticians_serialized.data,"accesstoken":str(refresh.access_token),"refreshtoken":str(refresh)})
        else:
            return Response({"message":'NotMatched'})
        

class Changeimage(APIView):
   
    def post(self,request):
     
        id=request.data.get("id")
        image=request.data.get("imageurl")

        

        obj=Customer.objects.get(id=id)  
        if obj:
            obj.image=image
            obj.save()
            serialized_object=Customerserializer(obj)
            
            return Response({"message":'Added',"custdata":serialized_object.data})
        else:
            return Response({"message":'NotAdded'})
        

class Booknow(APIView):
    
    def post(self,request):
     
        beautid=request.data.get("beautid")
        custid=request.data.get("custid")
        date=request.data.get("date")
        time=request.data.get("time")
        studio=request.data.get("studio")
        servicename=request.data.get("servicename")
        typeofpayment=request.data.get("type")

        servicename=servicename.split(" - ")[0]
      


        


        beautobj=Beautician.objects.get(id=beautid)
        custobj=Customer.objects.get(id=custid)

        # very first date format worked locally
        # date_format = '%a %b %d %Y %H:%M:%S GMT%z (%Z)' 


        date_string_cleaned = date.split('(')[0].strip()
        parseddateandtime = datetime.strptime(date_string_cleaned,"%a %b %d %Y %H:%M:%S GMT%z")
        

        


        
        date_format = '%a %b %d %Y %H:%M:%S (%Z)'
        # parseddateandtime = datetime.strptime(date, date_format)

        
        parseddate=parseddateandtime.date()
     
        studioobj=Studio.objects.get(beautician=beautobj,place=studio)

        service_obj=Services.objects.get(name=servicename)
        service_obj_req=Servicefees.objects.get(beautician=beautobj,service=service_obj) 

        if typeofpayment=="wallet":
                if custobj.wallet_amount<service_obj_req.servicefee:
                    return Response({"message":'not_enough_wallet_amount' ,"available_amount":custobj.wallet_amount})




        beautobj.wallet_amount+=service_obj_req.servicefee
        beautobj.save()
        
        try:
            Blockeddate.objects.get(beautician=beautobj,date=parseddate)
            return Response({"message":'Date is Blocked'})
        except:
            parsed_time = datetime.strptime(time, "%I:%M %p").time()
         

            Appointment.objects.create(customer=custobj,beautician=beautobj,date=parseddate,time=parsed_time,studio=studioobj,service=service_obj_req)
            beautobj.appointment_count+=1
            beautobj.save()
            if typeofpayment=="wallet":
                custobj.wallet_amount-=service_obj_req.servicefee
                custobj.save()
            return Response({"message":'Appointmentdone'})

        
   
        

class Getbeautdatas(APIView):
    
    def post(self,request):
  
        beautid=request.data.get("beautid")
      
        try:
            beautobj=Beautician.objects.get(id=beautid)
            studioobjs=Studio.objects.filter(beautician=beautobj)
            studioobjs_serialized=StudioSerializer(studioobjs,many=True)

            serviceobjs=Servicefees.objects.filter(beautician=beautobj)
            serviceobjs_serialized=ServicefeesSerializer(serviceobjs,many=True)

            for item in serviceobjs:
                req_service=item.service
                serviceid=req_service.id
                for item in serviceobjs_serialized.data:
                    if item["service"]==serviceid:
                        item["service"]=ServicesSerializer(req_service).data
                        

                
            

          
            return Response({"message":"success","studiodata":studioobjs_serialized.data,"servicedata":serviceobjs_serialized.data})
        except:
            return Response({"message":"not success"})

        
        

        
class Getbookings(APIView):
    
    def post(self,request):
 
        custid=request.data.get("custid")

        try:
            custobj=Customer.objects.get(id=custid)
  
            appointmentsobjs=Appointment.objects.filter(customer=custobj,date__gte=date.today())
            appointmentsobjs_serialized=Appointmentserializer(appointmentsobjs,many=True)

            # studioobjs=Studio.objects.filter(beautician=beautobj)
            # studioobjs_serialized=StudioSerializer(studioobjs,many=True)

            # serviceobjs=Servicefees.objects.filter(beautician=beautobj)
            # serviceobjs_serialized=ServicefeesSerializer(serviceobjs,many=True)
   
     
            for item in appointmentsobjs:
                serviceobj=item.service
                beauticianobj=item.beautician
                studioobj=item.studio

                baseservice=serviceobj.service
                baseservice_serialized=ServicesSerializer(baseservice)
               
                

                serviceobj_serialized=ServicefeesSerializer(serviceobj)
                beauticianobj_serialized=BeauticianSerializer(beauticianobj)
                studioobj_serialized=StudioSerializer(studioobj)
                

                
                
                serviceid=serviceobj.id
                beauticianid=beauticianobj.id
                studioid=studioobj.id
               
                for item in appointmentsobjs_serialized.data:
                    if item["service"]==serviceid:
                        item["service"]=serviceobj_serialized.data
                        item["service"]["service"]=baseservice_serialized.data
                    if  item["beautician"]==beauticianid:
                        item["beautician"]=beauticianobj_serialized.data
                    if  item["studio"]==studioid:
                        item["studio"]=studioobj_serialized.data


                

                        

                
           

           
            return Response({"message":"success","appointmentdata":appointmentsobjs_serialized.data})
        except:
            return Response({"message":"not success"})
        
class Getlandingpage(APIView):
   
    def post(self,request):
 
        custid=request.data.get("custid")
       
        try:
            custobj=Customer.objects.get(id=custid)
            
 
            appointmentsobjs=Appointment.objects.filter(customer=custobj,date=date.today())
            
            appointmentsobjs_serialized=Appointmentserializer(appointmentsobjs,many=True)

            # studioobjs=Studio.objects.filter(beautician=beautobj)
            # studioobjs_serialized=StudioSerializer(studioobjs,many=True)

            # serviceobjs=Servicefees.objects.filter(beautician=beautobj)
            # serviceobjs_serialized=ServicefeesSerializer(serviceobjs,many=True)
       
   
            for item in appointmentsobjs:
                serviceobj=item.service
                beauticianobj=item.beautician
                studioobj=item.studio

                baseservice=serviceobj.service
                baseservice_serialized=ServicesSerializer(baseservice)

                

                serviceobj_serialized=ServicefeesSerializer(serviceobj)
                beauticianobj_serialized=BeauticianSerializer(beauticianobj)
                studioobj_serialized=StudioSerializer(studioobj)
                

                
                
                serviceid=serviceobj.id
                beauticianid=beauticianobj.id
                studioid=studioobj.id
               
                for item in appointmentsobjs_serialized.data:
                    if item["service"]==serviceid:
                        item["service"]=serviceobj_serialized.data
                        item["service"]["service"]=baseservice_serialized.data
                    if  item["beautician"]==beauticianid:
                        item["beautician"]=beauticianobj_serialized.data
                    if  item["studio"]==studioid:
                        item["studio"]=studioobj_serialized.data


                

                        

                
 

        
            return Response({"message":"success","todays_appointmentdata":appointmentsobjs_serialized.data})
        except:
            return Response({"message":"not success"})
        


class Editdetails(APIView):
   
    def post(self,request): 
        id=request.data.get("id")
        name=request.data.get("name")
        email=request.data.get("email")
        phone=request.data.get("phone")
        custobj=Customer.objects.get(id=id)
        custobj.name=name
        custobj.email=email
        custobj.phone=phone 
        custobj.save()
        customer_serialized=Customerserializer(custobj)
        return Response({"message":'Added',"allcustdatas":customer_serialized.data})
    
class Getallservices(APIView):

    def get(self,request): 
        allservices=Services.objects.all()
        allservices_serialized=ServicesSerializer(allservices,many=True)
        return Response({"message":'Added',"allservices":allservices_serialized.data})
    
class Getsingleservice(APIView):
 
    def post(self,request): 
        serviceid=request.data.get("serviceid")
      
        serviceobj=Services.objects.get(id=serviceid)
        service_serialized=ServicesSerializer(serviceobj)
        return Response({"message":'Added',"service":service_serialized.data})
    


class Getservicebeauts(APIView):
  
    def post(self,request): 
        serviceid=request.data.get("serviceid")
        serviceobj=Services.objects.get(id=serviceid)
        servicefeesobjs=Servicefees.objects.filter(service=serviceobj,topservice=True)
        servicefeesobjs_serialized=ServicefeesSerializer(servicefeesobjs,many=True)
     

        return Response({"message":'Added',"services":servicefeesobjs_serialized.data})


class Getviewmoreservicebeauts(APIView):
  
    def post(self,request): 
        serviceid=request.data.get("serviceid")
        serviceobj=Services.objects.get(id=serviceid)
        servicefeesobjs=Servicefees.objects.filter(service=serviceobj).exclude(topservice=True)
        servicefeesobjs_serialized=ServicefeesSerializer(servicefeesobjs,many=True)
     

        return Response({"message":'Added',"services":servicefeesobjs_serialized.data})
    
class Forgotpassword(APIView):
    def post(self,request): 
        email=request.data.get("email")
        try:
            custobj=Customer.objects.get(email=email)
            id=custobj.id
            subject = "Forgot Password"
            message = "http://localhost:3000/forgotpassword/"
            recipient = email
            send_mail(subject, 
                message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            return Response({"message":'success',"id":id})
        except:
            return Response({"message":'failed'})
        

class ChangePassword(APIView):
    def post(self,request): 
        id=request.data.get("id")
        password=request.data.get("password")
       
        
        custobj=Customer.objects.get(id=id)
        custobj.password=make_password(password)
        custobj.save()
      
        return Response({"message":'success'})
       

class Checkavailability(APIView):
    def post(self,request): 
        date=request.data.get("date")
        time=request.data.get("time")

        date_format = '%a %b %d %Y %H:%M:%S GMT%z (%Z)'
        parseddateandtime = datetime.strptime(date, date_format)

        
        parseddate=parseddateandtime.date()
        parsed_time = datetime.strptime(time, "%I:%M %p").time()    

     

        try:
            Appointment.objects.get(date=parseddate,time=parsed_time)
            message="Not Available"
            return Response({"message":message})
        except:
            message="Available"
            return Response({"message":message})
       
   

class Bookingbeautdetails(APIView):
  
    def post(self,request): 
     
        beautid=request.data.get("beautid")
        custid=request.data.get("custid")
        beautobj=Beautician.objects.get(id=beautid)
        custobj=Customer.objects.get(id=custid)
        recent_appointment=Appointment.objects.filter(beautician=beautobj,customer=custobj).last()
        recent_appointment_serialized=Appointmentserializer(recent_appointment)
        beautname=beautobj.name
        return Response({"beauticianname":beautname,"recentappointment":recent_appointment_serialized.data})
    
class CancelBooking(APIView):
  
    def post(self,request): 
        id=request.data.get("bookingid")
        appointment=Appointment.objects.get(id=id)
        servicefee=appointment.service.servicefee
        appointment.beautician.wallet_amount-=servicefee
        appointment.customer.wallet_amount+=servicefee
        appointment.beautician.appointment_count-=1
        appointment.status="Cancelled"

        appointment.beautician.save()
        appointment.customer.save()
        appointment.save()
        
    
        
        
        return Response({"message":"Success"})
    
class GetWalletAmount(APIView):
    def post(self,request): 
        custid=request.data.get("id")
        amount=Customer.objects.get(id=custid).wallet_amount
        
        return Response({"message":'success',"amount":amount})
        

  
    
        
class GetPreviousBookings(APIView):
    
    def post(self,request):
 
        custid=request.data.get("custid")

        try:
            custobj=Customer.objects.get(id=custid)
  
            appointmentsobjs=Appointment.objects.filter(customer=custobj,date__lt=date.today(),status="Confirmed")
            appointmentsobjs_serialized=Appointmentserializer(appointmentsobjs,many=True)

            # studioobjs=Studio.objects.filter(beautician=beautobj)
            # studioobjs_serialized=StudioSerializer(studioobjs,many=True)

            # serviceobjs=Servicefees.objects.filter(beautician=beautobj)
            # serviceobjs_serialized=ServicefeesSerializer(serviceobjs,many=True)
   
     
            for item in appointmentsobjs:
                serviceobj=item.service
                beauticianobj=item.beautician
                studioobj=item.studio

                baseservice=serviceobj.service
                baseservice_serialized=ServicesSerializer(baseservice)
               
                

                serviceobj_serialized=ServicefeesSerializer(serviceobj)
                beauticianobj_serialized=BeauticianSerializer(beauticianobj)
                studioobj_serialized=StudioSerializer(studioobj)
                

                
                
                serviceid=serviceobj.id
                beauticianid=beauticianobj.id
                studioid=studioobj.id
               
                for item in appointmentsobjs_serialized.data:
                    if item["service"]==serviceid:
                        item["service"]=serviceobj_serialized.data
                        item["service"]["service"]=baseservice_serialized.data
                    if  item["beautician"]==beauticianid:
                        item["beautician"]=beauticianobj_serialized.data
                    if  item["studio"]==studioid:
                        item["studio"]=studioobj_serialized.data


                

                        

                


           
            return Response({"message":"success","appointmentdata":appointmentsobjs_serialized.data})
        except:
            return Response({"message":"not success"})
        
class AddReview(APIView):
  
    def post(self,request): 
        id=request.data.get("bookingid")
        content=request.data.get("reviewcontent")
        print(content,"ITH CONTENT ADAAAAAAAAAAAAAAAAAAAAAAAaaa")
        appointment=Appointment.objects.get(id=id)
        Review.objects.create(beautician=appointment.beautician,customer=appointment.customer,content=content)
        return Response({"message":"Success"})





class GetReviews(APIView):
   
    def post(self,request):
     
        beautid=request.data.get("beautid")
        allreviews=Review.objects.filter(beautician=Beautician.objects.get(id=beautid))
        print(allreviews,"NOKKKKK")
        allreviews_serialized=Reviewserializer(allreviews,many=True)
        if allreviews==[]:
            return Response({"message":"empty"})
        else:
            return Response({"message":"notempty","reviews":allreviews_serialized.data})
        

class GetAllServiceFee(APIView):
   
    def get(self,request):
        allservices=Servicefees.objects.all()
        allservices_serialized=ServicefeesSerializer(allservices,many=True)
        return Response({"message":"success","allservices":allservices_serialized.data})


class GetTopBeauticians(APIView):
   
    def get(self,request):
        allbeauts=Beautician.objects.all()
        
        maximum=0

        ranking_dict={}
        req_beautobj1=None
        req_beautobj2=None
        req_beautobj3=None


        for item in allbeauts:
            if item.appointment_count>=maximum:
                req_beautobj1=item
                maximum=req_beautobj1.appointment_count
        req_beautobj1_ser=BeauticianSerializer(req_beautobj1)
        ranking_dict["first"]=req_beautobj1_ser.data
        maximum=0
        for item in allbeauts:
            if item==req_beautobj1:
                continue
            if item.appointment_count>=maximum:
                req_beautobj2=item
                maximum=req_beautobj2.appointment_count
        req_beautobj2_ser=BeauticianSerializer(req_beautobj2)
        ranking_dict["second"]=req_beautobj2_ser.data

        maximum=0
        for item in allbeauts:
            if item==req_beautobj1 or item==req_beautobj2:
                continue
            if item.appointment_count>=maximum:
                req_beautobj3=item
                maximum=req_beautobj3.appointment_count
        req_beautobj3_ser=BeauticianSerializer(req_beautobj3)
        ranking_dict["third"]=req_beautobj3_ser.data










        ranking_dict_serialized=RankingDictSerializer(ranking_dict)
        


        
        return Response({"message":"success","topbeauticians":ranking_dict_serialized.data})
    



class AddToFavourites(APIView):
  
    def post(self,request): 

      

        if request.data.get("bookingid"):
            bookingid=request.data.get("bookingid")
            appointment=Appointment.objects.get(id=bookingid)
            beaut=appointment.beautician
            cust=appointment.customer
       
           

        if request.data.get("myid"):
            myid=request.data.get("myid")
            custid=request.data.get("custid")
            beaut=Beautician.objects.get(id=myid)
            cust=Customer.objects.get(id=custid)

        
        
        try:
            FavouriteStylists.objects.get(beautician=beaut,customer=cust)
            return Response({"message":"already_present"})

        except:
            FavouriteStylists.objects.create(beautician=beaut,customer=cust)
            return Response({"message":"done"})


class GetAllFavourites(APIView):
  
    def post(self,request): 
        id=request.data.get("custid")
        all_favourites=FavouriteStylists.objects.filter(customer=Customer.objects.get(id=id))
        all_favourites_serialized=FavouriteStylistsSerializer(all_favourites,many=True)
        return Response({"message":"done","allfavourites":all_favourites_serialized.data})

class GetAllBeauticians(APIView):
  
    def get(self,request): 
        all=Beautician.objects.all()
        all_serialized=BeauticianSerializer(all,many=True)

        allfav=FavouriteStylists.objects.all()
        allfavs_serialized=FavouriteStylistsSerializer(allfav,many=True)

        allrevs=Review.objects.all()
        allrevs_serialized=Reviewserializer(allrevs,many=True)
        
        return Response({"message":"done","allbeauticians":all_serialized.data,"allfavs":allfavs_serialized.data,"allrevs":allrevs_serialized.data})
    
class RemoveFromFavourites(APIView):
  
    def post(self,request): 
        id=request.data.get("id")
        obj=FavouriteStylists.objects.get(id=id)
        obj.delete()
        
        return Response({"message":"done"})
    
class GetBeautWorkshops(APIView):
  
    def post(self,request): 
        id=request.data.get("beautid")
        obj=Beautician.objects.get(id=id)
        all=Workshop.objects.filter(beautician=obj)
        if all.count()==0:
            return Response({"message":"no-workshops"})
        else:
            all_serialized=WorkshopSerializer(all,many=True)
            return Response({"message":"done","allworkshops":all_serialized.data})
        
class WorkShopBooknow(APIView):
  
    def post(self,request): 
        workshopid=request.data.get("workshopid")
        custid=request.data.get("custid")
        type=request.data.get("type")
      
        workshop_obj=Workshop.objects.get(id=workshopid)
        cust_obj=Customer.objects.get(id=custid)
        workshop_obj.customers.add(cust_obj)
        workshop_obj.save()
        try:
            booking_obj=WorkshopBooking.objects.get(workshop=workshop_obj,customer=cust_obj)
            booking_obj.status="Confirmed"
            booking_obj.save()
            return Response({"message":"done"})
        except:
            WorkshopBooking.objects.create(customer=cust_obj,workshop=workshop_obj,status="Confirmed") 
       
        return Response({"message":"done"})
    

class CheckWorkshopBooked(APIView):
  
    def post(self,request): 
        workshopid=request.data.get("workshopid")
        custid=request.data.get("custid")
    
       
      
        workshop_obj=Workshop.objects.get(id=workshopid)
        cust_obj=Customer.objects.get(id=custid)
        try:
            WorkshopBooking.objects.get(workshop=workshop_obj,customer_id=custid,status="Confirmed") 
            return Response({"message":"already-present"})
        except:
            return Response({"message":"not-present"})



class WorkShopBookNowWallet(APIView):
  
    def post(self,request): 
        workshopid=request.data.get("workshopid")
        custid=request.data.get("custid")
        type="Wallet Payment"
      
        workshop_obj=Workshop.objects.get(id=workshopid)
        cust_obj=Customer.objects.get(id=custid)
        if cust_obj.wallet_amount < workshop_obj.price:
            return Response({"message":"not-enough-wallet-money"})
        
        workshop_obj.customers.add(cust_obj)
        workshop_obj.save()
        cust_obj.wallet_amount-=workshop_obj.price
        cust_obj.save()
        try:
            booking_obj=WorkshopBooking.objects.get(workshop=workshop_obj,customer=cust_obj)
            booking_obj.status="Confirmed"
            booking_obj.save()
            return Response({"message":"done"})
        except:
            WorkshopBooking.objects.create(customer=cust_obj,workshop=workshop_obj)
            return Response({"message":"done"}) 
    
class GetAllWorkshops(APIView):
  
    def get(self,request): 
        current_date=datetime.now().date()
        all=Workshop.objects.filter(conducting_date__gt=current_date)
        if all.count()==0:
            return Response({"message":"no-workshops"})
        
        all_serialized=WorkshopSerializer(all,many=True)
        
       
        return Response({"message":"done","allworkshops":all_serialized.data})
    
class GetCurrentUserWorkShops(APIView):
  
    def post(self,request): 
        cust_obj=Customer.objects.get(id=request.data.get("custid"))
        current_date = datetime.now().date()  
        current_time = datetime.now().time()
        all=cust_obj.workshop.filter(conducting_date__gte=current_date)
        
        if all.count()==0:
            return Response({"message":"no-workshops"})
        else:
            all_serialized=WorkshopSerializer(all,many=True)

            return Response({"message":"done","allworkshops":all_serialized.data})
        
class CancelWorkshopBooking(APIView):
  
    def post(self,request): 
        id=request.data.get("id")
        cust_id=request.data.get("cust_id")
        workshop_obj=Workshop.objects.get(id=id)
        cust_obj=Customer.objects.get(id=cust_id)
        workshop_obj.customers.remove(cust_obj)
        workshop_obj.save()
       

        ws_booking_obj=WorkshopBooking.objects.get(workshop=workshop_obj,customer=cust_obj)
        ws_booking_obj.status="Cancelled"
        ws_booking_obj.save()
        cust_obj.wallet_amount+=workshop_obj.price
        cust_obj.save() 
       
       
        
       

        return Response({"message":"done"})


class GetAttendedWorkshops(APIView):
  
    def post(self,request): 
        cust_obj=Customer.objects.get(id=request.data.get("custid"))
        current_date = datetime.now().date()  
        current_time = datetime.now().time()
        all=cust_obj.workshop.filter(conducting_date__lt=current_date)
        
        if all.count()==0:
            return Response({"message":"no-workshops"})
        else:
            all_serialized=WorkshopSerializer(all,many=True)

            return Response({"message":"done","allworkshops":all_serialized.data})
        
class GetCancelledWorkshops(APIView):
  
    def post(self,request): 
        all_bookings=WorkshopBooking.objects.filter(customer_id=request.data.get("custid"),status="Cancelled")

        
        if all_bookings.count()==0:
            return Response({"message":"no-workshops"})
        else:
            all_bookings_serialized=WorkshopBookingSerializer(all_bookings,many=True)

            return Response({"message":"done","all_bookings":all_bookings_serialized.data})




class GetTopWorkshop(APIView):
   
    def get(self,request):
        

        work_dict={}
        all=WorkshopBooking.objects.all()
        if all.count()==0:
            return Response({"message":"failed"})
        for item in all:
            if item.workshop.id not in work_dict:
                work_dict[item.workshop.id]=1
            else:
                work_dict[item.workshop.id]+=1
       
            

        print(work_dict,"DDSS")
        max_val=0
        for k,v in work_dict.items():
            if v>max_val:
                max_val=v
                
                try:
                    workshop=Workshop.objects.get(id=k)
                except:
                    return Response({"message":"no-workshops"}) 
        workshop_serialized=WorkshopSerializer(workshop)

        return Response({"message":"success","topworkshop":workshop_serialized.data})

      
        
       
class CheckIfBlocked(APIView):
  
    def post(self,request): 
        cust=Customer.objects.get(id=request.data.get("id"))
        if cust.isblocked:
            return Response({"message":"blocked"})
        
        else:
            return Response({"message":"notblocked"})
        

class ResendOTP(APIView):
  
    def post(self,request): 
        cust=Customer.objects.get(email=request.data.get("email"))
        otpobj=OTP.objects.filter(email=cust.email)
        otpobj.delete()
        otpvalue=generate_otp()
        email=cust.email
        OTP.objects.create(otp=otpvalue,email=email)
      
        subject = "OTP for registration in Groom UP"
        message = f"Your OTP for registration is {otpvalue}.Please enter this otp to register."
        recipient = email
        send_mail(subject, 
              message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)

        return Response({"message":"success"})



        
       
    

        
