

import os
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.mail import send_mail, BadHeaderError

from .forms import ContactForm, ImageForm
from .models import Works, Category


@login_required(login_url='/login/')
def personal_works(request):
    ''' return personal works page '''
    if Works.objects.count() != 0:
        works = Works.objects.filter(username=request.user.username)
        hidden = "hidden"
        context = {'works': works, 'class_hidden': hidden}
    else:
        message = """
        <p>Vous n'avez pas encore enregistré d'oeuvres !</p>
        <p>il n'est jamais tard pour le faire.</p>
        """
        context = {'message': message}
    return render(request, 'works/personal_works.html', context)


@login_required(login_url='/login/')
def add_works(request):
    ''' return personal works page '''
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST.get("work_name").title()
            category = request.POST.get("category")
            description = request.POST.get("description")
            category = Category.objects.filter(name=category)
            category_id = category[0].id
            work = Works.objects.filter(name=name,
                                        category_id=category_id)
            if not work.exists():
                work = Works.objects.create(
                    name=name,
                    username=request.user.username,
                    image=form.instance.image,
                    description=description,
                    category_id=category_id
                    )
                return redirect('/mes_oeuvres/')
            else :
                context = {}
                return render(request,
                              'works/add_works.html',
                              context)
    else:
        form = ImageForm()
    if Category.objects.count() == 0:
        category_message = """<p>Il n'y a aucune catégorie disponible. 
                                 Il est donc impossible d'enregistrer 
                                 une oeuvre pour le moment</p>
                              <p>
                                 Soyez le premier à en créer une 
                                 <a href='/Oeuvre/categorie'>ici</a>.
                              </p>
        """
        hidden = "hidden"
        context = {'div': category_message, 'hidden': hidden}
    else:
        categories = Category.objects.all()
        hidden = "hidden"
        context = {'form': form,
                   'class_hidden': hidden, 'categories': categories}
    return render(request, 'works/add_works.html', context)


@login_required(login_url='/login/')
def add_category(request):
    ''' return add_category page '''
    if request.method == 'POST':
        name = request.POST.get("name").title()
        description = request.POST.get("description")
        category = Category.objects.filter(name=name)
        if name != '' or description != '':
            if not category.exists():
                category = Category.objects.create(
                        name=name,
                        description=description
                    )
                category.save()
                return redirect('/Oeuvre/ajout/')
            else:
                category = category.first()
                messages.warning(request, 'Cette catégorie existe déja...')
        else:
            messages.warning(request, 'Veuillez entrer les informations demandées.')
    return render(request, 'works/add_category.html')


@login_required(login_url='/login/')
def favorite_works(request):
    ''' return personal works page '''
    return render(request, 'works/favorite_works.html')

def work_details(request, work_name):
    ''' return detail page of each work '''
    if request.method == 'GET':
        work_detail = Works.objects.filter(name=work_name)
        context = {'works': work_detail}
    return render(request, 'works/work_details.html', context)