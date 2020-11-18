from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .forms import FindForm, VacancyForm
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


def v_detail(request, pk):
    #obj = Vacancy.objects.get(pk=pk)  # by primary keyfrom request find in BD
    obj = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'scraping/detail.html',{'object': obj})


class VacancyDetail(DetailView):
    # class based view
    # redefine attrs
    queryset = Vacancy.objects.all()
    template_name = 'scraping/detail.html'
    context_object_name = 'object'  # to get access in html file by this name or other you want


class VacancyList(ListView):
    model = Vacancy
    template_name = 'scraping/list.html'
    form = FindForm()

    paginate_by = 5  # define pagination in classbased view
    #  to show pagination in html the name must be page_obj

    def get_context_data(self, **kwargs):  # add to html context['object_list']  and add smth to context
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')

        context['form'] = self.form  #  pass form to context

        return context

    def get_queryset(self):  # redefine  queryset like Model_name.objects.all()
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
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

        return qs


class VacancyCreate(CreateView):
    model = Vacancy
    #fields = '__all__'  # pass all fields from db table to html form

    form_class = VacancyForm  # from scraping.forms

    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')  #  like redirectafter submit


class VacancyUpdate(UpdateView):
    model = Vacancy
    #fields = '__all__'  # pass all fields from db table to html form

    form_class = VacancyForm

    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')  #  like redirectafter submit


class VacancyDelete(DeleteView):
    model = Vacancy
    template_name = 'scraping/delete.html'
    success_url = reverse_lazy('home')  #  like redirectafter submit

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Vacancy successfully deleted.')
        return self.post(request, *args, **kwargs)  # without connfirmation