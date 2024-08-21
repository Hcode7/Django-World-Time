from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from .models import Email
from .forms import EmailForm


# Create your views here.


def home(request):
    local_name = request.GET.get('local_name', '')
    url = f'https://www.timeanddate.com/worldclock/{local_name}'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    time = soup.find('span', class_='h1')
    if time :
        text_span = time.get_text() 
        messages.success(request, f'The Time of {local_name} is {text_span}') 
    else: 
        text_span = 'The Local time not Found'
        messages.error(request, text_span)
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EmailForm()
    context = {
        'local_name' : local_name,
        'text_span' : text_span,
        'form' : form,
    }
    return render(request, 'pages/time.html', context)

