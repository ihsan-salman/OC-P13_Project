'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError

from work.models import Works, Category, Favorite
from social.models import Comment
from .forms import EditProfileForm
from .models import Profile
from .helper import get_popular_category, get_user_social_image
from .helper import get_user_work_image, get_user_work_comments


def index(request):
    ''' Return index page result '''
    try:
        all_favorite = Favorite.objects.all()
        popular_category = get_popular_category()
        users = User.objects.all()
        user_image_list1 = get_user_social_image(request, users)
        works = Works.objects.filter(time__year=2022)
        user_image_list2 = get_user_work_image(works, users)
        comment_list = get_user_work_comments(works, users)
    except Exception as err:
        return HttpResponse(err)
    if request.method == 'POST':
        work_id = request.POST.get('work_id')
        comment = request.POST.get('comment')
        user_work = Works.objects.get(id=work_id)
        user = User.objects.get(username=request.user.username)
        if comment != '':
            user_comment = Comment.objects.create(
                content=comment,
                user=user,
                work=user_work)
        else:
            messages.error(request, "Rentrez un commentaire valide")
        if request.is_ajax():
            return HttpResponse("OK")
    context = {'works': works,
               'user_image': user_image_list2,
               'users': users,
               'social_user_img': user_image_list1,
               'comment_list': comment_list,
               'favorites': all_favorite,
               'popular_categories': popular_category}
    return render(request, 'favarche/index.html', context)


def contact(request):
    ''' Return contact page result '''
    if request.method == 'POST':
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        email_message = request.POST.get("message")
        if email != '' or subject != '' or email_message != '':
            try:
                send_mail(subject,
                          email_message,
                          email,
                          [os.environ.get('EMAIL_HOST_USER')])
                return redirect('/')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            return render(request, 'error_page/404.html', status=404)
    return render(request, 'favarche/informative/contact.html')


def about_us(request):
    ''' Return about page result '''
    return render(request, 'favarche/informative/about.html')


def functionality(request):
    ''' Return functionality page result '''
    return render(request, 'favarche/informative/functionality.html')


def category(request):
    ''' Return category page result '''
    number_list = []
    for i in range(Category.objects.count()):
        number_list.append(i + 1)
    context = {'categories': Category.objects.all(),
               'number_list': number_list}
    return render(request, 'favarche/informative/category.html', context)


@login_required(login_url='/login/')
def personal_account(request):
    ''' return the template of user's personal informations '''
    user = User.objects.get(username=request.user.username)
    user_profile_img = Profile.objects.get(user_id=user.id)
    if request.method == 'POST':
        user_profile_img.image = request.FILES['user_img']
        user_profile_img.save()
    context = {'img': user_profile_img}
    return render(request, 'favarche/account/my_account.html', context)


@login_required(login_url='/login/')
def edit_account(request):
    '''return the template to change user's personal informations '''
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/mon_compte/')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request,
                  'favarche/account/edit_account.html',
                  {'form': form})
