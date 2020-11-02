from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


# Create your views here.
def home_view(request):
    form = FindForm()
    context = {'form': form}
    return render(request, 'scraping/home.html', context)


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')

    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        filter_dict = dict()
        # two underscore to get acccess to models table
        if city:
            filter_dict['city__slug'] = city.lower()
        if language:
            filter_dict['language__slug'] = language.lower()
        qs = Vacancy.objects.filter(**filter_dict)
    else:
        qs = Vacancy.objects.all()

    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)