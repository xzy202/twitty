"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from socialnetwork import views

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$',views.ViewAllPost, name='home'),
    url(r'^addpost$', views.AddPost,name = 'addpost'),
    url(r'^login$', auth_views.login, {'template_name':'socialnetwork/login.html'}, name='login'),
    
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login,name='logout'),
    url(r'^register$', views.register,name='register'),

    url(r'^delete-item/(?P<item_id>\d+)$', views.DeletePost, name='deletepost'),
    url(r'^edit$', views.edit, name='edit'),    

    url(r'^follow/(\d+)$',views.follow,name='follow'),
    url(r'^unfollow/(\d+)$',views.unfollow,name='unfollow'),
    url(r'^viewprofile/(?P<id>\d+)$',views.ViewProfile, name='viewprofile'),
    url(r'^viewfollower$',views.ViewFollower, name='viewfollower'),  
    url(r'^photo/(?P<id>\d+)$', views.get_photo, name='photo'), 
    url(r'^add-comment/(?P<id>\d+)$', views.add_comment),
    url(r'^get-list-json$', views.get_list_json),
    url(r'^get-comment-json/(?P<id>\d+)$',views.get_comment_json),
    url(r'^get-comments-json$',views.get_comments_json),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        views.confirm_registration, name='confirm'),
]
