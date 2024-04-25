from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    peoples=[
        {'name':'avhisheik das','age':24},
        {'name':'sunanda Datta','age':20},
        {'name':'Najam Uddin','age':26},
        {'name':'Anik das','age':34}
    ]
    return render(request,"index.html",context = {'peoples':peoples})

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")