'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from operator import itemgetter
from django.contrib.auth.models import User

from work.models import Category, Works
from .models import Profile
from social.models import Comment


def get_user_social_image(request, users):
    ''' return all users image for social section in main page '''
    user_image_list = []
    if users.count() != 0:
        for user in users:
            if request.user.is_authenticated:
                if user.username != request.user.username:
                    image = Profile.objects.get(user=user)
                    user_image_list.append(image)
            else:
                image = Profile.objects.get(user=user)
                user_image_list.append(image)
    return user_image_list

def get_user_work_image(works, users):
    ''' return all users images for works section in main page '''
    user_image_list = []
    if works.count() != 0:
        for work in works:
            user = User.objects.get(username=work.user)
            image = Profile.objects.get(user=user)
            user_image_list.append(image)
    return user_image_list

def get_user_work_comments(works, users):
    ''' return all users comments for works section in main page '''
    comment_list = []
    if works.count() != 0:
        for work in works:
            user = User.objects.get(username=work.user)
            comment = Comment.objects.filter(work=work.id)
            comment_list.append(comment)
    return comment_list


def get_popular_category():
    ''' return 5 most numerous category between works '''
    categories = Category.objects.all()
    works_list_with_count = []
    popular_categories = []
    for category in categories:
        works_by_category = Works.objects.filter(category=category)
        works_count_by_category = works_by_category.count()
        works_list_with_count.append([category,
                                      works_count_by_category])
    works_list_with_count = sorted(works_list_with_count,
                                   key=itemgetter(1),
                                   reverse=True)
    works_list_with_count = works_list_with_count[:5]
    for category in works_list_with_count:
        popular_categories.append(category[0])
    return popular_categories
    




