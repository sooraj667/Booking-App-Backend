from rest_framework.response import Response 
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import Usermodelserializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from beautician.models import *
from customers.models import *
from beautician.serializers import BeauticianSerializer,ServicesSerializer,StudioSerializer
from customers.serializers import Customerserializer,Appointmentserializer
from rest_framework.serializers import Serializer


class Login(APIView):
    def post(self,request):
        email=request.data.get("email")
        password=request.data.get("password")
        print(f"EMEILLLLLLLL {email} PASWORDDDDD {password}")
        try:
            found=User.objects.get(email=email)
        except:
            return Response({"message":'NotMatched'})
    

        hashedpassword=found.password
        matched = check_password(password, hashedpassword)
    
        
       
           
        if matched==True:

            obj=User.objects.get(email=email)
            serialized_object=Usermodelserializer(obj)
      
            
            allcustdatas=Customer.objects.all()
            allcustdatas=Customerserializer(allcustdatas,many=True)
            allbeautdatas=Beautician.objects.all()
            allbeautdatas=BeauticianSerializer(allbeautdatas,many=True)
            allservices=Services.objects.all()
            allservices=ServicesSerializer(allservices,many=True)
            allappointments=Appointment.objects.all()
            allappointment_serialized=Appointmentserializer(allappointments,many=True)
       
            for item in allappointments:
                req_id=item.id
                beautobj=item.beautician
                custobj=item.customer
                studioobj=item.studio
                for item in allappointment_serialized.data:
                    if item["id"]==req_id:
                        item["beautician"]=BeauticianSerializer(beautobj).data
                        item["customer"]=Customerserializer(custobj).data
                        item["studio"]=StudioSerializer(studioobj).data





            

            refresh=RefreshToken.for_user(obj)  
            return Response({"message":'Matched',"admindata":serialized_object.data,"allbeautdatas":allbeautdatas.data,"allcustdatas":allcustdatas.data,"allservices":allservices.data,"allappointments":allappointment_serialized.data,"accesstoken":str(refresh.access_token),"refreshtoken":str(refresh)})
        else:
            return Response({"message":'NotMatched'})
        

class Blockbeaut(APIView):
    def post(self,request):
        beautid=request.data.get("beautid")
        beautobj=Beautician.objects.get(id=beautid)
        if beautobj.isblocked=="False":
            beautobj.isblocked="True"
        else:
            beautobj.isblocked="False"


        
        beautobj.save()
        allbeautdatas=Beautician.objects.all()
        allbeautdatas=BeauticianSerializer(allbeautdatas,many=True)
      
        return Response({"message":'Blocked',"allbeautdatas":allbeautdatas.data,})
    
    
class Blockcust(APIView):
    def post(self,request):
        custid=request.data.get("custid")
        custobj=Customer.objects.get(id=custid)
        if custobj.isblocked=="False":
            custobj.isblocked="True"
        else:
            custobj.isblocked="False"

        custobj.save()
        allcustdatas=Customer.objects.all()
        allcustdatas=Customerserializer(allcustdatas,many=True)
      
        return Response({"message":'Blocked',"allcustdatas":allcustdatas.data})
    

class Addnewservice(APIView):
    def post(self,request):
        servicename=request.data.get("servicename")
        servicedesc=request.data.get("servicedesc")
        image=request.data.get("imageurl")
        Services.objects.create(name=servicename,description=servicedesc,image=image)
        allservices=Services.objects.all()
        allservices=ServicesSerializer(allservices,many=True)
        return Response({"allservices":allservices.data})

        
      
          






        