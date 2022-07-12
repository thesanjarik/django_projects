from django.shortcuts import render, redirect
from main.models import Product, Category, Tag, Review, ConfirmCode
from main.forms import ProductForm, RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, FormView
from django.views import View


class ConfirmView(View):
    def get(self, request, *args, **kwargs):
        try:
            confirm_code = ConfirmCode.objects.get(code=kwargs['code'])
            user = confirm_code.user
            user.is_active = True
            user.save()
            return redirect('/login/')
        except:
            return redirect('/register/')


class IndexView(View):
    def get(self, request):
        dict_ = {
           'key': 'Hello World!',
           'color': '#FC5ED7',
           'list_': ['Ablai', "Salima", "Sangar", "Janat"]
        }
        return render(request, 'index.html', context=dict_)

    def post(self, request):
        pass


# def product_list_view(request):
#     products = Product.objects.all()
#     context = {
#         'product_list': products,
#         'category_list': Category.objects.all()
#     }
#
#     return render(request, 'products.html', context=context)

class ContextData:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['category_list'] = Category.objects.all()
        return context


class ProductListView(ContextData, ListView):
    queryset = Product.objects.all()
    template_name = 'products.html'
    context_object_name = 'product_list'





# def product_detail_view(request, id):
#     product = Product.objects.get(id=id)
#     return render(request, 'detail.html', context={'product_detail': product,
#                                                    'category_list': Category.objects.all(),
#                                                    'reviews': Review.objects.filter(product=product)})


class ProductDetailView(ContextData, DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['reviews'] = Review.objects.filter(product=self.object)
        return context


# def category_product_filter_view(request, category_id):
#     context = {
#         'product_list': Product.objects.filter(category_id=category_id),
#         'category_list': Category.objects.all()
#     }
#     return render(request, 'products.html', context=context)


class CategoryProductFilterView(ContextData, ListView):
    queryset = Product.objects.all()
    template_name = 'products.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.filter(category_id=self.request.resolver_match.kwargs['category_id'])


class AddProductFormView(ContextData, FormView):
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = '/products/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# def add_product_view(request):
#     form = ProductForm()
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/products/')
#     return render(request, 'add_product.html', context={
#             'form': form,
#             'category_list': Category.objects.all()
#         })

def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save
            return redirect('/register/')
    return render(request, 'register.html', context={
        'form': form
    })

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user=user)
            return redirect('/login/')

    return render(request, 'login.html', context={
        'form': form
    })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')

