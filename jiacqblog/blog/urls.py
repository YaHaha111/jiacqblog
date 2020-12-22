from django.urls import path

from . import views




app_name = 'blog'


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('tags/<int:pk>/', views.tag, name='tag'),
    path('categories/<int:pk>/', views.category, name='category'),
    path('demo', views.demo, name='demo'),
    path('categories_menu/', views.categories_menu, name='categories_menu'),
    path('tags_menu/', views.tags_menu, name='tags_menu'),
    path('archives_menu/', views.archives_menu, name='archives_menu'),

]
