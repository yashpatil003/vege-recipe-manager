from django.shortcuts import redirect, render
from django.urls import reverse
from .model import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login ,logout    
from django.contrib.auth.decorators import login_required



@login_required(login_url="/logins/")
def recipes(request):
    if request.method == "POST":


        data=request.POST
        recipe_image= request.FILES.get('recipe_image')
        recipe_description = data.get('recipe_name')
        recipe_name = data.get('recipe_name')

        Recepies.objects.create(
        
        recipe_name = recipe_name,
        recipe_description  =recipe_description ,
        recipe_image =recipe_image
        )

        return redirect('/recipes/')
    
    queryset = Recepies.objects.all()
    context = {'recipes': queryset}


        
        
    return render(request, 'recipes.html',context)

def update_recipe(request,id):
        queryset =Recepies.objects.get(id =id)
        context = {'recipes': queryset}
        queryset.update()
        return render(request, 'update_recipes.html',context)
        

def logins(request):
    if request.method == "POST":
        print(f"Received POST data: {request.POST}")  # Debugging

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        print(f"Username: {username}, Password: {'Yes' if password else 'No'}")  # Debugging output

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            print(f"Authentication failed for: {username}")
            return redirect(reverse("logins"))

        login(request, user)
        print(f"User {user.username} logged in successfully!")
        return redirect(reverse("recipes"))

    return render(request, "logins.html")

def logout_page(request):
    logout(request)
    return redirect('logins')
    



from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("First_name")  
        last_name = request.POST.get("lastname")
        username = request.POST.get("Username")
        password = request.POST.get("Password")

        if User.objects.filter(username=username).exists():  # ✅ Corrected this line
            messages.info(request, "Username already exists")
            return redirect('/register/')

        # ✅ Create a new user and save to the database
        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, "Account created successfully!")
        # return redirect("/success/")  # Redirect after successful registration

    return render(request, "register.html")


def delete_receipe(request,id):
    queryset =Recepies.objects.get(id =id)
    queryset.delete()
    return redirect('/recipes/')
