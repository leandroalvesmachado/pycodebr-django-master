from django.http import HttpResponse
from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import CarForm, CarModelForm

# Class based views
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Autorização para as views
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

# function based view
def cars_view(request):
    # return render(
    #     request,
    #     'cars.html',
    #     {'cars': {'model': 'Carro 1'}}
    # )

    # retorna todos os carros
    # cars = Car.objects.all()

    # brand__name = Acessando a entidade Brand a coluna name, pois o brand na tabela cars é uma fk
    # cars = Car.objects.filter(brand__name='Fiat')

    # filtrando pela coluna model
    # cars = Car.objects.filter(model='Opala')

    # filtrando qualquer carro que contem a string Opala
    # cars = Car.objects.filter(model__contains='opala')

    # captura todos os parametros vindo do request get
    # request.GET

    # captura na request, no método GET, o parametro search
    # order_by('model') = A a Z
    # order_by('-model') = Z a A
    cars = Car.objects.all().order_by('model')
    search = request.GET.get('search')

    if search:
        # procura exatamente a string
        # cars = cars.filter(model__contains=search)

        # i = ignore case, tanto faz A,a
        cars = cars.filter(model__icontains=search).order_by('model')
    
    return render(request,'cars.html', {
        'cars': cars
    })


# class based views (usando a view base)
# reescrevendo a função cars_view
class CarsView(View):
    
    def get(self, request):
        cars = Car.objects.all().order_by('model')
        search = request.GET.get('search')

        if search:
            cars = cars.filter(model__icontains=search).order_by('model')
        
        return render(request,'cars.html', {
            'cars': cars
        })


# class based views (usando a view generic para listagem ListView)
# reescrevendo a classe CarsView
class CarsListView(ListView):
    model = Car # Car.objects.all() default
    template_name = "cars.html"
    context_object_name = "cars"

    # quando você precisa escrever as suas consultas, filtros, etc..
    # sobrescrever o método, personalizando
    def get_queryset(self):
        cars = super().get_queryset().order_by('model') # Car.objects.all().order_by('model')
        search = self.request.GET.get('search')
        if search:
            cars = cars.filter(model__icontains=search).order_by('model')
        return cars
    


def new_car_view(request):
    if request.method == "POST":
        new_car_form = CarModelForm(request.POST, request.FILES)

        # dados do form recebidos
        # print(new_car_form.data)

        if new_car_form.is_valid():
            new_car_form.save()
            return redirect('cars_list')
    else:
        new_car_form = CarModelForm()

    return render(request, 'new_car.html', {
        'new_car_form': new_car_form
    })




# class based views (usando a view base)
# reescrevendo a função new_car_view
class NewCarView(View):

    def get(self, request):
        new_car_form = CarModelForm()
        
        return render(request, 'new_car.html', {
            'new_car_form': new_car_form
        })

    def post(self, request):
        new_car_form = CarModelForm(request.POST, request.FILES)

        if new_car_form.is_valid():
            new_car_form.save()
            return redirect('cars_list')

        return render(request, 'new_car.html', {
            'new_car_form': new_car_form
        })


# class based views (usando a view generic para criar CreateView)
# reescrevendo a classe NewCarView
@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = "new_car.html"
    success_url = "/cars/"


class CarDetailView(DetailView):
    model = Car
    template_name = "car_detail.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = "car_update.html"
    # success_url = "/cars/"

    # sobrescrevendo o success_url
    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = "car_delete.html"
    success_url = "/cars/"

