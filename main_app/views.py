from django.shortcuts import render,redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView


from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Vacation

# Create your views here.
def about(request):
    return render(request, 'about.html')

def vacations_index(request):
  vacations = Vacation.objects.all()
  return render(request, 'vacations/index.html', {'vacations': vacations})


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