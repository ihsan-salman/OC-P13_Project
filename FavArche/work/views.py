'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import CategoryForm, EditCategoryForm
from .forms import WorksDescriptionForm
from .models import Works, Category, Favorite

from work.helper import wiki_page
from main.helper import get_user_work_image, get_user_work_comments


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
                                 <a href='/Oeuvre/ajout_categorie'>ici</a>.
                              </p>
        """
        hidden = "hidden"
        context = {'div': category_message, 'hidden': hidden}
    else:
        if request.method == 'POST':
            form_description = WorksDescriptionForm(request.POST)
            category = request.POST.get("category")
            category = Category.objects.get(name=category)
            work_image = request.FILES.get("work_img")
            if work_image is None:
                work_image = 'default_work.png'
            work = Works.objects.filter(name=request.POST.get(
                "work_name").title(),
                                        category_id=category.id)
            user_work = User.objects.get(username=request.user.username)
            description = request.POST.get('description')
            if request.POST.get('description') == '':
                if len(wiki_page(request.POST.get('work_name'))) == 1:
                    description = wiki_page(request.POST.get('work_name'))[0]
                else:
                    description = wiki_page(request.POST.get('work_name'))[0]
            if not work.exists():
                work = Works.objects.create(
                    name=request.POST.get("work_name"),
                    user=user_work,
                    image=work_image,
                    description=description,
                    category_id=category.id
                    )
                return redirect('/Oeuvre/personnel/')
            else:
                form_description = WorksDescriptionForm(request.POST)
                context = {'form_description': form_description}
                messages.error(request, """
                Vous semblez avoir rentrée des données
                déjà comprise dans la base données.""")
                return render(request,
                              'works/add_works.html',
                              context)
        else:
            form_description = WorksDescriptionForm()
        categories = Category.objects.all()
        hidden = "hidden"
        context = {'form_description': form_description,
                   'class_hidden': hidden,
                   'categories': categories}
    return render(request, 'works/add_works.html', context)


@login_required(login_url='/login/')
def add_category(request):
    ''' return add_category page '''
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/Oeuvre/ajout_oeuvre/')
            messages.warning(request, 'Cette catégorie existe déja...')
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'works/add_category.html', context)


@login_required(login_url='/login/')
def favorite_works(request):
    ''' return personal works page '''
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        work_id = request.POST.get('work_id')
        to_do = request.POST.get('to_do')
        work = Works.objects.get(id=work_id)
        fav_work = Favorite.objects.filter(
                favorite_works_id=work_id, user=user)
        if to_do == 'create' and not fav_work.exists():
            fav_work = Favorite.objects.create(favorite_works_id=work_id,
                                               user=user)
            work.fav.add(user)
        elif to_do == 'delete':
            fav_work.delete()
            work.fav.remove(user)
    user_fav_works = Favorite.objects.filter(user=user)
    context = {'favorites': user_fav_works}
    return render(request, 'works/favorite_works.html', context)


def work_details(request, work_name):
    ''' return detail page of each work '''
    try:
        work = Works.objects.get(name=work_name)
    except Works.DoesNotExist:
        return render(request, 'error_page/404.html', status=404)
    wiki_result = wiki_page(work_name)
    if len(wiki_result) == 2:
        if work.description == wiki_result[0]:
            context = {'work': work,
                       'description': 'ok',
                       'summary': wiki_result[0],
                       'wiki_url': wiki_result[1]}
        else:
            context = {'work': work,
                       'wiki_url': wiki_result[1]}
    else:
        messages.error(request, wiki_result[0])
        context = {'work': work}
    if request.method == 'POST':
        work_image = request.FILES.get('work_img')
        if work_image is not None:
            work.image = work_image
            work.save()
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
    context = {'form': form}
    return render(request, 'works/edit_category.html', context)


def search_by_category(request, category_name):
    ''' return works page by selected category '''
    category = Category.objects.get(name=category_name)
    works = Works.objects.filter(category=category)
    users = User.objects.all()
    user_image_list = get_user_work_image(works, users)
    user_comment_list = get_user_work_comments(works, users)
    context = {'category_name': category_name,
               'works': works,
               'users_img': user_image_list,
               'users_comment': user_comment_list}
    return render(request, 'works/search_category.html', context)


def search_by_work(request):
    ''' return work page by researched name '''
    if request.method == 'POST':
        work_name = request.POST.get('search_work')
        works = Works.objects.filter(name__contains=work_name)
        users = User.objects.all()
        user_image_list = get_user_work_image(works, users)
        user_comment_list = get_user_work_comments(works, users)
        context = {'work_name': work_name,
                   'works': works,
                   'users_img': user_image_list,
                   'users_comment': user_comment_list}
        return render(request, 'works/search_work.html', context)


def get_wiki(request):
    ''' return wikipedia data '''
    if request.method == 'POST':
        work_name = request.POST.get('work_name')
    wiki_result = wiki_page(work_name)
    if request.is_ajax():
        return HttpResponse(wiki_result[0] +
            'Nous vous invitons à compléter vous-mêmes le résumé')
