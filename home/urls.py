from django.urls import path
from . import views
from ticketapp import views as adminviews
urlpatterns = [
    path('', views.index, name="Index Page"),
    path('doc/<pid>', views.software, name="Software"),   
    path('ticket', views.TicketCreateView.as_view(), name="Ticket "),
    path('chatpage/<pid>', views.ChatRoom, name="CHat Room"), 
    path('chatpage', views.ChatRoomapp, name="CHat Room"),  
    path('login', views.loginview, name="loginpage"),
    
]
