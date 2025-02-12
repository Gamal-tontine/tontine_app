from django.shortcuts import render

def index(request):
    return render(request,'blog/index.html')

def about(request):
    return render(request,'blog/about.html')

def team(request):
    return render(request,'blog/team.html')

def services(request):
    return render(request,'blog/services.html')

def contact(request):
    return render(request,'blog/contact.html')

