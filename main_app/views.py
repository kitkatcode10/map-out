
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic import ListView, DetailView

from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Itinerary, Vacation, Packing, Photo
from .forms import ItineraryForm

import os




S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'vacaycollector'

# Create your views here.
def home(request):
    return redirect ('about')

def about(request):
    return render(request, 'about.html')

@login_required
def vacations_index(request):
  vacations = Vacation.objects.filter(user=request.user)
  return render(request, 'vacations/index.html', {'vacations': vacations})

@login_required
def vacations_detail(request, vacation_id):
  vacation = Vacation.objects.get(id=vacation_id)
  packing_vacation_doesnt_have = Packing.objects.exclude(id__in = vacation.packing.all().values_list('id'))
  itinerary_form = ItineraryForm()
  return render(request, 'vacations/detail.html', {'vacation': vacation, 'itinerary_form': itinerary_form, 'packing': packing_vacation_doesnt_have})

@login_required
def add_itinerary(request, vacation_id):
  form = ItineraryForm(request.POST)
  if form.is_valid():
    new_itinerary = form.save(commit=False)
    new_itinerary.vacation_id = vacation_id
    new_itinerary.save()
  return redirect('detail', vacation_id=vacation_id)

@login_required
def delete_itinerary(request, vacation_id, itinerary_id):
  i = Itinerary.objects.get(id=itinerary_id)
  i.delete()
  return redirect('detail', vacation_id=vacation_id)

@login_required
def assoc_packing(request, vacation_id, packing_id):
  Vacation.objects.get(id=vacation_id).packing.add(packing_id)
  return redirect('detail', vacation_id=vacation_id)

@login_required
def unassoc_packing(request, vacation_id, packing_id):
  Vacation.objects.get(id=vacation_id).packing.remove(packing_id)
  return redirect('detail', vacation_id=vacation_id)

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


class VacationCreate(LoginRequiredMixin, CreateView): 
  model = Vacation 
  fields = [ "name", "destination", "date", "duration", "style", "travellers", "transportation" ]
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form) 

class VacationUpdate(LoginRequiredMixin, UpdateView):
  model = Vacation 
  fields = [ "name", "destination", "date", "duration", "style", "travellers", "transportation" ]

class VacationDelete(LoginRequiredMixin, DeleteView):
  model = Vacation
  success_url = '/vacations/'

class PackingCreate(LoginRequiredMixin, CreateView):
  model = Packing
  fields = '__all__'


class PackingDetail(LoginRequiredMixin, DetailView):
  model = Packing


class PackingList(LoginRequiredMixin, ListView):
  model = Packing


class PackingUpdate(LoginRequiredMixin, UpdateView):
  model= Packing
  fields = '__all__'

def add_photo(request, vacation_id):
  my_key = os.environ['aws_secret_access_key']
	# photo-file was the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to cat_id or cat (if you have a cat object)
      photo = Photo(url=url, vacation_id=vacation_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', vacation_id=vacation_id)