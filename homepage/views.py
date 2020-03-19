from django.shortcuts import render, redirect, HttpResponse
from .forms import HandleForm
# Create your views here.
def home(request):
    if request.method == 'POST':
        form = HandleForm(request.POST)
        if form.is_valid():
            handle = form.cleaned_data.get('handle') 
            return redirect('/stalk/' + handle)
    else:
        form = HandleForm()

    return render(request, 'homepage/home.html', {'form': form})

def stalk(request, handle):
    context = {
        'handle': handle,
    }
    return render(request, 'homepage/stalk.html', context)