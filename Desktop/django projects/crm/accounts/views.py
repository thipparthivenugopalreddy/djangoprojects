from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from accounts.models import *
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import createform,loginown,CustomerForm
from accounts.filters import filterorder
from accounts.forms import registerform
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import unauthenticated,allow,adminonly
from django.contrib.auth.models import Group

@login_required(login_url="login")
@adminonly
def home(r):
    c=Customer.objects.all()
    o=Order.objects.all()
    total_c=c.count()
    total_o=o.count()
    Delivered=Order.objects.filter(status='Delivered').count()
    Pending=Order.objects.filter(status='Pending').count()
    context={'c':c,'o':o,'Delivered':Delivered,'Pending':Pending,'total_c':total_c,'total_o':total_o}

    return render(r,"accounts/dashboard.html",context)

@login_required(login_url="login")
@allow(allowed_roles=['admin'])
def customers(r,pk):
    c=Customer.objects.get(id=pk)

    o=c.order_set.all()

    total_o=c.order_set.all().count()

    myfilter=filterorder(r.GET,queryset=o)

    o=myfilter.qs

    context={'c':c,'total_o':total_o,'o':o,'myfilter':myfilter}

    return render(r,"accounts/customer.html",context)

@login_required(login_url='login')
@allow(allowed_roles=['admin'])
def products(r):
    p=Product.objects.all()
    return render(r,"accounts/products.html",{'p':p})

@login_required(login_url="login")
@allow(allowed_roles=['admin'])
def create_order(r,id):
    customer=Customer.objects.get(id=id)
    orderform=inlineformset_factory(Customer,Order,fields=('product','order_no','status'),extra=10)

    formset=orderform(queryset=Order.objects.none(),instance=customer)
    # form=createform(initial={'customer':customer})
    if r.method=='POST':
        form=orderform(r.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(r,"accounts/order_form.html",{'formset':formset})

@login_required(login_url="login")
@allow(allowed_roles=['admin'])
def update_order(r,pk):
    o=Order.objects.get(id=pk)
    form=createform(instance=o)
    if r.method=='POST':
        form=createform(r.POST,instance=o)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(r,"accounts/update.html",{'form':form})

@login_required(login_url="login")
@allow(allowed_roles=['admin'])
def delete(r,pk):
    o=Order.objects.get(id=pk)
    if r.method=='POST':
        o.delete()
        return redirect('home')
    return render(r,"accounts/delete.html",{'o':o})

@unauthenticated
def loginpage(r):
    if r.method=='POST':
        username=r.POST.get('username')
        password=r.POST.get('password')
        user=authenticate(r,username=username,password=password)
        if user is not None:
            login(r,user)
            return redirect("home")
        elif user is None:
            messages.error(r,"something went wrong")
    return render(r,"accounts/login.html")

@unauthenticated
def registerpage(r):
    form=registerform()
    if r.method=='POST':
        form=registerform(r.POST)
        if form.is_valid():
            user=form.save()
            # group=Group.objects.get(name='customer')
            # user.groups.add(group)
            # Customer.objects.create(customer=user,name=user.username)
            login(r,user)
            return redirect("home")
    return render(r,"accounts/register.html",{'form':form})


def logoutpage(r):
    logout(r)
    return redirect("home")

@login_required(login_url="login")
@allow(allowed_roles=['customer'])
def user(r):
    orders=r.user.customer.order_set.all()
    total_o=orders.count()
    Delivered=orders.filter(status='Delivered').count()
    Pending=orders.filter(status="Pending").count()
    context={'orders':orders,'total_o':total_o,'Delivered':Delivered,'Pending':Pending}
    return render(r,"accounts/user.html",context)
@login_required(login_url="login")
@allow(allowed_roles=['customer'])
def accountSettings(r):
    customer=r.user.customer
    form=CustomerForm(instance=customer)
    if r.method=="POST":
        form=CustomerForm(r.POST,r.FILES,instance=customer)
        if form.is_valid():
            form.save()
    return render(r,"accounts/account_settings.html",{'form':form})

def all(r):
    mail=User.objects.values_list('email',flat=True)
    print(mail)
    return HttpResponse("done")
