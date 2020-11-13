from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from accounts.forms import OrderForm, CreateUserForm, CustomerForm
from accounts.models import Product, Order, Customer
from .decorators import unauthenticated_user, allowed_users, admin_only
from .filters import OrderFilter


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, "Account was created for" + username)
            return redirect("login")

    context = {"form": form}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(request, username)
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username OR password is incorrect")

    context = {}
    return render(request, "accounts/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def user_page(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {"orders": orders, "total_orders": total_orders,
               "delivered": delivered, "pending": pending}
    return render(request, "accounts/user.html", context)


@login_required(login_url="login")
@admin_only
def home(request) -> HttpResponse:
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {"orders": orders, "customers": customers,
               "total_customers": total_customers,
               "total_orders": total_orders, "delivered": delivered,
               "pending": pending}
    return render(request, "accounts/dashboard.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer", "admin"])
def products(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {"products": products})


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer", "admin"])
def customer(request, pk_test):
    customers = Customer.objects.get(id=pk_test)
    orders = customers.order_set.all()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    order_count = orders.count()
    context = {"customers": customers, "orders": orders,
               "order_count": order_count, "myFilter": myFilter}
    return render(request, "accounts/customer.html", context)


@login_required(login_url="login")
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order,
                                         fields=('products', 'status'),
                                         extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url="login")
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        print(request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "accounts/order_form.html", context)


@login_required(login_url="login")
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect("home")
    context = {"item": order}
    return render(request, "accounts/delete.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer","admin"])
def account_settings(request):
    # customer = Customer.objects.get(id=pk)
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {"form": form}
    return render(request, "accounts/account_settings.html", context=context)
