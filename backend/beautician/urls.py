from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path("signup/",Signup.as_view(),name="Signup"),
    path("login/",Login.as_view(),name="Login"),
    path("changeimage/",Changeimage.as_view(),name="Changeimage"),
    path("addnewservice/",Addnewservice.as_view(),name="Addnewservice"),
    path("editdetails/",Editdetails.as_view(),name="Editdetails"),
    path("getbookings/",Getbookings.as_view(),name="Getbookings"),
    path("getstudios/",Getstudios.as_view(),name="Getstudios"),
    path("addstudio/",Addstudio.as_view(),name="Addstudio"),
    path("editstudio/",Editstudio.as_view(),name="Editstudio"),
    path("deletestudio/",Deletestudio.as_view(),name="Deletestudio"),
    path("confirmotp/",Confirmotp.as_view(),name="Confirmotp"),
    path("todays-schedule/",Todaysschedule.as_view(),name="Todaysschedule"),
    path("forgotpassword/",Forgotpassword.as_view(),name="Forgotpassword"),
    path("changepassword/",ChangePassword.as_view(),name="ChangePassword"),
    path("get-wallet-amount/",Getwalletamount.as_view(),name="Getwalletamount"),
    path("get-previous-booking/",GetPreviousBookings.as_view(),name="GetPreviousBookings"),
    path("get-single-studio/",GetSingleStudio.as_view(),name="GetSingleStudio"),
    path("get-single-studio/",GetSingleStudio.as_view(),name="GetSingleStudio"),
    path("add-bio/",AddBio.as_view(),name="AddBio"),
    path("add-to-expertise/",AddToExpertise.as_view(),name="AddToExpertise"),
    path("check-workshop-time/",CheckWorkshopTIme.as_view(),name="CheckWorkshopTIme"),
    path("add-workshop/",AddWorkshop.as_view(),name="AddWorkshop"),
    path("get-beaut-workshops/",GetBeautWorkshops.as_view(),name="GetBeautWorkshops"),
    path("cancel-workshop/",CancelWorkshop.as_view(),name="CancelWorkshop"),
    path("send-email-link/",SendEmailLink.as_view(),name="SendEmailLink"),
    path("video-call-link/",VideoCallLink.as_view(),name="VideoCallLink"),
    path("generate-roomid/",GenerateRoomId.as_view(),name="GenerateRoomId"),
    path("get-currentbeaut-completed-workshops/",GetBeautCompletedWorkshops.as_view(),name="GetBeautCompletedWorkshops"),



    

    
]