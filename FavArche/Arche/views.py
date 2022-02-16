'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


import os
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.mail import send_mail, BadHeaderError

from .forms import RegisterForm, CustomAuthenticationForm, EditProfileForm
from .forms import ContactForm, ImageForm
from .models import Profile, Works, Category


def index(request):
    ''' Return index page result '''
    return render(request, 'favarche/index.html')


def contact(request):
    ''' Return contact page result '''
    context = {}
    if request.method == 'POST':
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        email_message = request.POST.get("message")
        print(email, subject, email_message)
        try:
            send_mail(subject, 
                      email_message, 
                      email, 
                      [os.environ['EMAIL_HOST_USER']])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('/contact/')
    return render(request, 'favarche/informative/contact.html')

def about_us(request):
    ''' Return about page result '''
    return render(request, 'favarche/informative/about.html')


def functionality(request):
    ''' Return functionality page result '''
    return render(request, 'favarche/informative/functionality.html')


def create_account(request):
    '''return the template to create an user account
       and add in the database all related information'''
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            name = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = make_password(request.POST.get('password1'))
            user = User.objects.filter(username=name)
            if not user.exists():
                # If a contact is not registered, create a new one.
                user = User.objects.create(
                    username=name,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
                user.save()
                profile_user = Profile.objects.create(
                    user=user)
                profile_user.save()
            else:
                user = user.first()

            return redirect('/connexion/')
        else:
            # Form data doesn't match the expected format.
            # Add errors to the template.
            context['errors'] = form.errors.items()
    else:
        form = RegisterForm()
    return render(request, 'registration/create_account.html', {'form': form})


class CustomLoginView(LoginView):
    ''' Standart login form and class as view '''
    authentication_form = CustomAuthenticationForm


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
    return render(request, 'favarche/works/personal_works.html', context)


@login_required(login_url='/login/')
def add_works(request):
    ''' return personal works page '''
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            work_name = request.POST.get("work_name")
            category = request.POST.get("category")
            description = request.POST.get("description")
            category = Category.objects.filter(name=category)
            category_id = category[0].id
            work = Works.objects.filter(name=work_name,
                                        category_id=category_id)
            if not work.exists():
                work = Works.objects.create(
                    name=work_name,
                    username=request.user.username,
                    image=form.instance.image,
                    description=description,
                    category_id=category_id
                    )
                return redirect('/mes_oeuvres/')
            else :
                context = {}
                return render(request,
                              '/favarche/works/add_works.html',
                              context)
    else:
        form = ImageForm()
    if Category.objects.count() == 0:
        category_message = """<p>Il n'y a aucune catégorie disponible. 
                                 Il est donc impossible d'enregistrer 
                                 une oeuvre pour le moment</p>
                              <p>
                                 Soyez le premier à en créer une 
                                 <a href='/ajout_categorie'>ici</a>.
                              </p>
        """
        context = {'div': category_message}
    else:
        categories = Category.objects.all()
        hidden = "hidden"
        context = {'form': form,
                   'class_hidden': hidden, 'categories': categories}
    return render(request, 'favarche/works/add_works.html', context)


@login_required(login_url='/login/')
def add_category(request):
    ''' return add_category page '''
    if request.method == 'POST':
        name = request.POST.get("name")
        description = request.POST.get("description")
        category = Category.objects.filter(name=name)
        if not category.exists():
            category = Category.objects.create(
                    name=name,
                    description=description
                )
            category.save()
        else:
            category = category.first()
        return redirect('/ajout_oeuvre/')
    return render(request, 'favarche/works/add_category.html')


@login_required(login_url='/login/')
def favorite_works(request):
    ''' return personal works page '''
    return render(request, 'favarche/works/favorite_works.html')


@login_required(login_url='/login/')
def personal_account(request):
    ''' return the template of user's personal informations '''
    return render(request, 'favarche/account/my_account.html')


@login_required(login_url='/login/')
def edit_account(request):
    '''return the template to change user's personal informations '''
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/my_account/')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request,
                  'favarche/account/edit_account.html',
                  {'form': form})


@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        context = {'form': form}
    return render(request, 'registration/change_password.html', context)


def page_not_found(request, exception):
    '''return the 404 error page'''
    return render(request, 'error_page/404.html', status=404)


def server_error(request):
    '''return the 500 error page'''
    return render(request, 'error_page/500.html', status=500)