from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url="/login/")

def receipes(request):   # sourcery skip: extract-method, last-if-guard

    if request.method == "POST":
        data = request.POST
        receipe_name=data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        Receipe.objects.create(
                receipe_name=receipe_name,
                receipe_description = receipe_description,
                receipe_image = receipe_image
                )
        
        return redirect('/receipe/')
    
    queryset = Receipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))

    context = {'receipes': queryset}
    return render(request , 'receipe.html',context)

def delete_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect('/receipe/')

def update_receipe(request, id):  # sourcery skip: extract-method
    queryset = Receipe.objects.get(id = id)
    if request.method == "POST":
        data=request.POST
        receipe_name=data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        queryset.receipe_image = receipe_image
            	
        queryset.save()
        return redirect('/receipe/')
        

    context = {'receipe': queryset}
    return render(request, 'update_receipe.html',context)

def new_func(queryset):
    queryset.save()

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid Username")
            return redirect('/login/')

        user =authenticate(username = username, password = password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        
        else:
            login(request, user)
            return redirect('/receipe/')
        

    return render(request,'login.html')

# def login_page(request):
#     if request.method == 'POST':
  
#         # AuthenticationForm_can_also_be_used__
  
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username = username, password = password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, f' welcome {username} !!')
#             return redirect('/receipe/')
#         else:
#             messages.info(request, f'account done not exit plz sign in')

#     return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register_page(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if  User.objects.filter(username=username):
            messages.info(request, "Username is not unique")
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Account Created Successfully")

        return redirect('/')

    return render(request,'register.html')
