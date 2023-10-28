from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path("signup/",Signup.as_view(),name="Signup"),
    path("login/",Login.as_view(),name="Login"),
    path("changeimage/",Changeimage.as_view(),name="Changeimage"),
    path("booknow/",Booknow.as_view(),name="Booknow"),
    path("getbeautdatas/",Getbeautdatas.as_view(),name="Getbeautdatas"),
    path("getbookings/",Getbookings.as_view(),name="Getbookings"),
    path("getlandingpage/",Getlandingpage.as_view(),name="Getlandingpage"),
    path("editdetails/",Editdetails.as_view(),name="Editdetails"),
    path("getallservices/",Getallservices.as_view(),name="Getallservices"),
    path("getsingleservice/",Getsingleservice.as_view(),name="Getsingleservice"),
    path("getservicebeauts/",Getservicebeauts.as_view(),name="Getservicebeauts"),
    path("getviewmoreservicebeauts/",Getviewmoreservicebeauts.as_view(),name="Getviewmoreservicebeauts"),
    path("confirmotp/",Confirmotp.as_view(),name="Confirmotp"),
    path("forgotpassword/",Forgotpassword.as_view(),name="Forgotpassword"),
    path("changepassword/",ChangePassword.as_view(),name="ChangePassword"),
    path("check-availability/",Checkavailability.as_view(),name="Checkavailability"),
    path("booking-completed-beautdetails/",Bookingbeautdetails.as_view(),name="Bookingbeautdetails"),
    path("cancel-booking/",CancelBooking.as_view(),name="CancelBooking"),
    path("get-wallet-amount/",GetWalletAmount.as_view(),name="GetWalletAmount"),
    path("get-previous-bookings/",GetPreviousBookings.as_view(),name="GetPreviousBookings"),
    path("add-review/",AddReview.as_view(),name="AddReview"),
    path("getreviews/",GetReviews.as_view(),name="GetReviews"),
    path("getallservicefee/",GetAllServiceFee.as_view(),name="GetAllServiceFee"),
    path("gettopbeauticians/",GetTopBeauticians.as_view(),name="GetTopBeauticians"),
    path("add-to-favourites/",AddToFavourites.as_view(),name="AddToFavourites"),
    path("all-favourites/",GetAllFavourites.as_view(),name="GetAllFavourites"),
    path("getallbeauticians/",GetAllBeauticians.as_view(),name="GetAllBeauticians"),
    path("remove-from-favourties/",RemoveFromFavourites.as_view(),name="RemoveFromFavourites"),
    path("get-beaut-workshops/",GetBeautWorkshops.as_view(),name="GetBeautWorkshops"),
    path("workshop-booknow/",WorkShopBooknow.as_view(),name="WorkShopBooknow"),
    path("check-if-workshop-booked/",CheckWorkshopBooked.as_view(),name="CheckWorkshopBooked"),
    path("workshop-booknow-using-wallet/",WorkShopBookNowWallet.as_view(),name="WorkShopBookNowWallet"),
    path("getallworkshops/",GetAllWorkshops.as_view(),name="GetAllWorkshops"),
    path("get-currentuser-workshops/",GetCurrentUserWorkShops.as_view(),name="GetCurrentUserWorkShops"),
    path("cancel-workshop-booking/",CancelWorkshopBooking.as_view(),name="CancelWorkshopBooking"),
    path("get-currentuser-attended-workshops/",GetAttendedWorkshops.as_view(),name="GetAttendedWorkshops"),
    path("get-currentuser-cancelled-workshops/",GetCancelledWorkshops.as_view(),name="GetCancelledWorkshops"),
    path("gettopworkshop/",GetTopWorkshop.as_view(),name="GetTopWorkshop"),
   


    
    
]