from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),  # This is for the logged-in user's profile
    path('profile/<str:username>/', views.profile, name='user_profile'),  # This is for other users' profiles
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/edit/', views.user_profile_edit, name='profile_edit'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('post/<int:post_id>/share/', views.share_post, name='share_post'),
]
