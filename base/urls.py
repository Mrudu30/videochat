from django.urls import path
from . import views
from accounts import views as av

urlpatterns = [
    path('',views.lobby,name='home'),
    path('room/',views.room),
    path('get_token/',views.getToken),
    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
    path('login/',av.loginaccount,name='login'),
    path('signupaccount/', av.signupaccount, name='signup'),
    path('logout/', av.logoutaccount, name='logout'),
    path("profile/", av.profile , name="profile"),
    path('edit_details/=?<str:pk>/',av.edit_user,name='edit_details'),
]
