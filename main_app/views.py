
from django.shortcuts import render, redirect
from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic import ListView, DetailView

from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Vacation, Packing 
from .forms import ItineraryForm
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
  packing_vacation_doesnt_have = Packing.objects.exclude(id__in = vacation.packing.all().values_list('id'))
  itinerary_form = ItineraryForm()
  return render(request, 'vacations/detail.html', {'vacation': vacation, 'itinerary_form': itinerary_form, 'packing': packing_vacation_doesnt_have})

class VacationDelete(DeleteView):
  model = Vacation
  success_url= '/vacations/'

def add_itinerary(request, vacation_id):
  form = ItineraryForm(request.POST)
  if form.is_valid():
    new_itinerary = form.save(commit=False)
    new_itinerary.vacation_id = vacation_id
    new_itinerary.save()
  return redirect('detail', vacation_id=vacation_id)

def assoc_packing(request, vacation_id, packing_id):
  Vacation.objects.get(id=vacation_id).packing.add(packing_id)
  return redirect('detail, vacation_id=vacation_id')

def unassoc_packing(request, vacation_id, packing_id):
  Vacation.objects.get(id=vacation_id).packing.remove(packing_id)
  return redirect('detail', vacation_id=vacation_id)

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

class PackingCreate(CreateView):
  model = Packing
  fields = '__all__'


class PackingDetail(DetailView):
  model = Packing


class PackingList(ListView):
  model = Packing


class PackingUpdate(UpdateView):
  model= Packing
  fields = '__all__'
