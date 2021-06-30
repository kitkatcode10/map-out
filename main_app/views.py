
from django.shortcuts import render, redirect
from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Vacation 


from .models import Vacation

# Create your views here.
def home(request):
    return redirect ('about')

def about(request):
    return render(request, 'about.html')

def vacations_index(request):
  vacations = Vacation.objects.all()
  return render(request, 'vacations/index.html', {'vacations': vacations})


def vacations_detail(request, vacation_id):
  vacation = Vacation.objects.get(id=vacation_id)
  return render(request, 'vacations/detail.html', {'vacation': vacation})

class VacationDelete(DeleteView):
  model = Vacation
  success_url= '/vacations/'



# def about(request):
#     return render(request, 'about.html')
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('about') 
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

#Implement Authorization
# Now we can simply "decorate" any view function that requires a user to be logged in like this:

# @login_required
# def cats_index(request):

# Implement Authorization on Class-based Views
# Finally, we can protect class-based views like this:

# class CatCreate(LoginRequiredMixin, CreateView):
#   ...

class VacationCreate(LoginRequiredMixin, CreateView): 
  model = Vacation 
  fields = '__all__'
  success_url = '/vacations/'
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form) 

class VacationUpdate(LoginRequiredMixin, UpdateView):
  model = Vacation 
  fields = '__all__'

  # fields = ['destination', 'description', 'date', 'duration', 'typeoftrip', 'travellers', 'transportation'] wanted to try the all, here if we need it -KW
