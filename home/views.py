from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from ticketapp.models import Documentation, Ticket
from ticketapp.forms import Ticket, TicketForm, TicketUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q
from django.contrib.auth import get_user_model
from ticketapp.models import ChatApp
from django.contrib.auth import login , authenticate, logout
# Create your views here.

def index(request):
    return render (request, 'index.html')

def software(request, pid):
    data = Documentation.objects.filter(field_section=pid).values()
    print(data)
    return render (request, 'docs-page.html',{'data':data})

def ticket(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = TicketForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                customer_full_name = form.cleaned_data['customer_full_name']
                customer_phone_number = form.cleaned_data['customer_phone_number']
                customer_email = form.cleaned_data['customer_email']
                issue_description = form.cleaned_data['issue_description']
                ticket_section = form.cleaned_data['ticket_section']
                urgent_status = form.cleaned_data['urgent_status']
                assigned_to = form.cleaned_data['assigned_to']
                username = request.user
                if username.pk is None:
                    username.save()

            # Save the data to the database
                new_entry = Ticket(title=title, customer_full_name=customer_full_name,user_id = username,
                               customer_phone_number=customer_phone_number, customer_email=customer_email,
                               issue_description=issue_description, ticket_section=ticket_section,
                               urgent_status=urgent_status, assigned_to=assigned_to)
                new_entry.save()
                return HttpResponseRedirect('/')           
        else:
            form = TicketForm()  # Create an instance of the form
            return render(request, 'ticket_form.html', {'form': form})
        


class TicketCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket_form.html'
    success_url = ('/')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def ChatRoom(request, pid):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/')
    else:
        User = get_user_model()
        pid = pid
        users = User.objects.all()
        if request.method =="POST":
            sender = request.user.email
            recever = pid
            chat = request.POST.get('chat')
            chatdata = ChatApp(sender=sender, recever=recever, chat=chat)
            chatdata.save()
            return HttpResponseRedirect(recever)
        
        recever = pid
        sender = request.user.email
        chatval = ChatApp.objects.filter(Q(sender=sender, recever=recever) | Q(sender=recever, recever=sender))
        # print(chatval)
        data = {'users':users, 'recever':recever, 'chatval':chatval}
        return render(request, 'chatroom.html', data)

def ChatRoomapp(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/')
    else:
        User = get_user_model()
        users = User.objects.all()
        data = {'users':users}
        return render(request, 'chatroom.html', data)
    
def loginview(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email , password=password)
        # user.login()
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/ticket')
        else:
            return render(request, 'login.html')
        
    else:
        return render (request, 'login.html')
