'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


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

from .forms import ContactForm, ImageForm, CategoryForm, EditCategoryForm
from .models import Works, Category

from work.helper import wiki_page


@login_required(login_url='/login/')
def personal_works(request):
    ''' return personal works page '''
    user = User.objects.get(username=request.user.username)
    if Works.objects.filter(user=user).count() != 0:
        user = User.objects.get(username=request.user.username)
        works = Works.objects.filter(user=user)
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
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            name = request.POST.get("work_name").title()
            category = request.POST.get("category")
            description = request.POST.get("description")
            if description == "":
                description = "à remplir"
            category = Category.objects.get(name=category)
            work = Works.objects.filter(name=name,
                                        category_id=category.id)
            user_work = User.objects.get(username=request.user.username)
            if form.is_valid():
                image = form.instance.image
                if not work.exists():
                    work = Works.objects.create(
                        name=name,
                        user=user_work,
                        image=image,
                        description=description,
                        category_id=category.id
                        )
                    return redirect('/Oeuvre/personnel/')
                else :
                    form = ImageForm(request.POST, request.FILES)
                    context = {'form': form}
                    messages.error(request, """
                    Vous semblez avoir rentrée des données déjà comprise dans la base données.""")
                    return render(request,
                                  'works/add_works.html',
                                  context)
        else:
            form = ImageForm()
        categories = Category.objects.all()
        hidden = "hidden"
        context = {'form': form,
                   'class_hidden': hidden, 'categories': categories}
    return render(request, 'works/add_works.html', context)


@login_required(login_url='/login/')
def add_category(request):
    ''' return add_category page '''
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/Oeuvre/ajout/')
            messages.warning(request, 'Cette catégorie existe déja...')
    else:
        form = CategoryForm()
    context = {'form': form,}
    return render(request, 'works/add_category.html', context)


@login_required(login_url='/login/')
def favorite_works(request):
    ''' return personal works page '''
    return render(request, 'works/favorite_works.html')

def work_details(request, work_name):
    ''' return detail page of each work '''
    if request.method == 'GET':
        work_detail = Works.objects.filter(name=work_name)
        wiki_result = wiki_page(work_name)
        if len(wiki_result) == 2:
            context = {'works': work_detail,
                       'wikipedia_url': wiki_result[0],
                       'wikipedia_summary': wiki_result[1]}
        else:
            messages.error(request, wiki_result[0])
            context = {'works': work_detail}
    return render(request, 'works/work_details.html', context)


@login_required(login_url='/login/')
def edit_works(request, work_name):
    ''' return edit page of each page '''
    categories = Category.objects.all()
    if request.method == 'GET':
        editable_work = Works.objects.filter(name=work_name)
        context = {'work': editable_work[0], 'categories': categories}
    elif request.method == 'POST':
        editable_work = Works.objects.filter(name=work_name)
        editable_work = editable_work[0]
        name = request.POST.get("work_name").title()
        if editable_work.name != name and editable_work.name != '':
            editable_work.name = name
            editable_work.save()
        category = request.POST.get("category")
        if editable_work.category != category:
            category = Category.objects.get(name=category)
            editable_work.category = category
            editable_work.save()
        description = request.POST.get("description")
        if editable_work.description != description:
            editable_work.description = description
            editable_work.save()
        else:
            pass
        return redirect('/Oeuvre/personnel')
        context = {'work': editable_work, 'categories': categories}
    return render(request, 'works/edit_work.html', context)


@login_required(login_url='/login/')
def edit_category(request, category_name):
    ''' return edit category page '''
    category_instance = Category.objects.get(name=category_name)
    if request.method == 'POST':
        form = EditCategoryForm(request.POST, instance=category_instance)
        if form.is_valid():
            form.save()
            return redirect('/categories/')
    else:
        form = EditCategoryForm(instance=category_instance)
    context = {'form': form,}
    return render(request, 'works/edit_category.html', context)