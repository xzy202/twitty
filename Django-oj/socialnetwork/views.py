from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

# Imports the Item class and forms
from socialnetwork.models import Posts , Entry , Comments
from socialnetwork.forms import RegistrationForm,  EditForm , AddForm, CommentForm

from datetime import datetime

# Action for the default route
from django.http import HttpResponse, Http404

from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

@login_required
@transaction.atomic
def edit(request):

    context={}
    if request.method == 'GET':

        entry = Entry.objects.select_for_update().get(created_by = request.user)
        create_form = EditForm(instance = entry)
        context = { 'entry': entry, 'form': create_form }

        if not create_form.is_valid():
            context = {'form': create_form, 'entry': entry} 
            all_items = Posts.objects.order_by("timestamp").reverse() 
            context['items'] = all_items
            context['user'] = request.user
            context['entry'] = entry
            context['form'] = create_form
            context['addform'] = AddForm()
            return render(request, 'socialnetwork/edit.html', context) 
                             
        all_items = Posts.objects.order_by("timestamp").reverse() 

        context['items'] = all_items
        context['user'] = request.user
        context['entry'] = entry
        context['form'] = create_form
        context['addform'] = AddForm()

        return render(request, 'socialnetwork/edit.html', context)

    entry = Entry.objects.select_for_update().get(created_by = request.user)
    create_form = EditForm(request.POST, request.FILES, instance = entry)
    if not create_form.is_valid():
            context = {'form': create_form, 'entry': entry} 
            all_items = Posts.objects.order_by("timestamp").reverse() 
            context['items'] = all_items
            context['user'] = request.user
            context['entry'] = entry
            context['form'] = create_form
            context['addform'] = AddForm()
            return render(request, 'socialnetwork/edit.html', context)      

    entry.update_time=datetime.now()
    entry.save()
    create_form.save()
    user = User.objects.select_for_update().get(username = request.user.username)
    user.first_name = entry.first_name
    user.last_name = entry.last_name
    user.save()

    context['entry']=entry
    context['form']=create_form

    all_items = Posts.objects.order_by("timestamp").reverse()
    context['items'] = all_items
    context['user'] = user
    context['entry'] = entry
    context['form'] = create_form
    context['addform'] = AddForm()

    return redirect(reverse('home'))

@ensure_csrf_cookie
@login_required
def ViewAllPost(request):
    
    if not request.user.is_authenticated:
	redirect(reverse('logout'))

    context={}
    entry = get_object_or_404(Entry, created_by = request.user)
     
    form = EditForm( instance=entry)

    all_items = Posts.objects.order_by("timestamp").reverse() 
    
    context['addform'] = AddForm()
    context['items'] = all_items
    context['user'] = request.user
    context['entry'] = entry
    context['form'] = form

    return render(request, 'socialnetwork/viewallpost.html', context)

@login_required
def AddPost(request):

    context = {}
    errors=[]
    entry = get_object_or_404(Entry, created_by = request.user)
    form = EditForm( instance = entry) 

    if request.method != 'POST' :
        errors.append('ADD must be done using the POST method')
        context={}
        all_items = Posts.objects.order_by("timestamp").reverse() 
        context['addform'] = AddForm()
        context['items'] = all_items
        context['user'] = request.user
        context['errors'] = errors
        context['form'] = form
        context['entry'] = entry
        return render(request,'socialnetwork/viewallpost.html',context)
    
    add_post = AddForm(request.POST)

    if not add_post.is_valid():
        context={}
        all_items = Posts.objects.order_by("timestamp").reverse() 
        context['addform'] = AddForm()
        context['items'] = all_items
        context['user'] = request.user
        context['form'] = form
        context['entry'] = entry
        context['formerrors'] = add_post
        return render(request, 'socialnetwork/viewallpost.html', context)

    new_item = Posts(user = request.user,timestamp=datetime.now(),text=add_post.cleaned_data['post'],entry = entry)
    new_item.save()


    items = Posts.objects.order_by("timestamp").reverse()

    context['form'] = form
    context['entry'] = entry
    context['items']= items
    context['errors']=errors
    context['addform']=AddForm()
    return render(request, 'socialnetwork/viewallpost.html', context)

# Action for the /todolist2/delete-item route.
@login_required
def DeletePost(request, item_id):

    errors = []
    if request.method != 'POST':
        errors.append('Deletes must be done using the POST method')
    else:
        # Deletes the item if present in the todo-list database.
        try:
            item_to_delete = get_object_or_404(Item, id=item_id)
            item_to_delete.delete()
        except ObjectDoesNotExist:
            errors.append('The item did not exist in the To Do List.')

    items = Item.objects.order_by("timestamp").reverse()
    context = {'items': items, 'errors': errors}
    return redirect(reverse('home'))
    # return render(request, 'socialnetwork/viewallpost.html', context)


@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email = form.cleaned_data['email'])
    new_user.is_active = False
    new_user.save()

#    entry = Entry(age=0 ,created_by=new_user,update_time=datetime.now(),creation_time= datetime.now())
#    entry.save()

    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to Voice @ CMU  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), 
       reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="zxiang@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'socialnetwork/needs-confirmation.html', context)
    
@transaction.atomic
def confirm_registration(request, username, token):
    new_user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(new_user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    new_user.is_active = True
    new_user.save()    

    entry = Entry(age=0 ,created_by=new_user,update_time=datetime.now(),creation_time= datetime.now())
    entry.save()

    return render(request, 'socialnetwork/confirmed.html', {})

@login_required
def follow(request,id):
    errors=[]
    context={}

    entry = get_object_or_404(Entry,created_by=request.user)
    new_user = get_object_or_404(User,id = id)

    entry.followers.add(new_user)
    entry.save()

    context['errors'] = errors

    items = Posts.objects.filter(user = new_user)
    items = Posts.objects.order_by("timestamp").reverse()
    context['items']= items
    context['user'] = new_user  

    return redirect(reverse('home'))
    # return render(request,'socialnetwork/viewprofile.html',context)

@login_required
def unfollow(request,id):
    errors=[]
    context={}

    entry = get_object_or_404(Entry, created_by=request.user)
    # new_user = get_object_or_404(User,id = id)
    new_user = get_object_or_404(User,id = id)


    entry.followers.remove(new_user)

    entry.save()

    context['errors'] = errors

    items = Posts.objects.filter(user = new_user)
    items = Posts.objects.order_by("timestamp").reverse()
    context['items']= items
    context['user'] = new_user
    # return render(request,'socialnetwork/viewprofile.html',context)
    return redirect(reverse('home'))

@login_required
def ViewProfile(request,id):
    errors=[]
    context={}

    context['errors'] = errors

    target = get_object_or_404( User, id = id )

    items = Posts.objects.filter(user = target)
    entry = Entry.objects.get(created_by= target)
    items = items.order_by("timestamp").reverse()

    context['entry'] = entry
    context['items']= items
    context['user'] = target
    context['master'] = request.user
    return render(request,'socialnetwork/viewprofile.html',context)

@login_required
def ViewFollower(request):

    context={}
    entry = get_object_or_404(Entry,created_by = request.user)
    form = EditForm(instance=entry)

  
    followers = entry.followers.values_list("id",flat=True).distinct()
    items = Posts.objects.filter(user__in=followers)

    items = items.order_by("timestamp").reverse()


    context['addform'] = AddForm()
    context['items'] = items
    context['user'] = request.user
    context['entry'] = entry
    context['form'] = form

    return render(request, 'socialnetwork/viewfollow.html', context)    


def get_photo(request, id):
    item = get_object_or_404(Entry, id=id)

    # Probably don't need this check as form validation requires a picture be uploaded.
    if not item.picture:
        raise Http404

    return HttpResponse(item.picture)

@login_required
def add_comment(request,id):
    errors = []
    if not 'item' in request.POST or not request.POST['item']:
        # print("nothing")
        message = 'You must enter an item to add.'
        json_error = '{ "error": "'+ message +'" }'
        return HttpResponse(json_error, content_type='application/json')

    

    new_form = CommentForm(request.POST)
    if not new_form.is_valid():
        # print("comment form is not valid")
        return redirect(reverse('home'))

    # pic = Entry.objects.select_for_update().get(created_by = request.user)
    new_comment = Comments(comment= request.POST['item'],user= request.user, timestamp=datetime.now(),postid = id)

    new_comment.save()
    post = get_object_or_404(Posts,id = id)    
    post.comments.add(new_comment)
    comments = post.comments.all()
    all_list=[]
    for item in comments:
        comment = item 
        user =User.objects.get(username = comment.user.username)
        entry = Entry.objects.get(created_by = comment.user)
        all_list.append(comment)
        all_list.append(user)
        all_list.append(entry)

    response_text = serializers.serialize('json', all_list)
    return HttpResponse(response_text, content_type='application/json')

@login_required
@transaction.atomic
def get_comment_json(request,id):
    post = get_object_or_404(Posts,id=id)    
    comments = post.comments.all()
    all_list=[]
    for item in comments:
        comment = item 
        user =User.objects.get(username = comment.user.username)
        entry = Entry.objects.get(created_by = comment.user)
        all_list.append(comment)
        all_list.append(user)
        all_list.append(entry)

    response_text = serializers.serialize('json', all_list)
    return HttpResponse(response_text, content_type='application/json')

@login_required
@transaction.atomic
def get_comments_json(request):
    post = get_object_or_404(Posts,id=id)    
    comments = post.comments.all()
    all_list=[]
    for item in comments:
        comment = item 
        user =User.objects.get(username = comment.user.username)
        entry = Entry.objects.get(created_by = comment.user)
        all_list.append(comment)
        all_list.append(user)
        all_list.append(entry)

    response_text = serializers.serialize('json', all_list)
    return HttpResponse(response_text, content_type='application/json')

@login_required
@transaction.atomic
def get_list_json(request):
    all_list=[]
    posts = Posts.objects.order_by("timestamp").reverse() 
    for post in posts:
        entry = post.entry
        user = post.user
        # username = post.user.username
        # picture = entry.picture
        # list1=[post,username,picture]
        all_list.append(post)
        all_list.append(entry)
        all_list.append(user)

    response_text = serializers.serialize('json', all_list)
    return HttpResponse(response_text, content_type='application/json')
