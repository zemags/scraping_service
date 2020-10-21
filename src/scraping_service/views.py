from django.shortcuts import render
import datetime

def home(request):
    date = datetime.datetime.now().date()
    name = 'John'
    context = {'date': date, 'name': name}
    return render(request, 'base.html', context)