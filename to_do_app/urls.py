from django.urls import path, re_path
from .views import ToDoListHandler, ToDoItem, home
from .views import (
    ToDoListCreateView,
    ToDoListDetailView,
    ToDoListUpdateView,
    ToDoListDeleteView,
    ToDoCreateView,
    ToDoDetailView,
    ToDoUpdateView,
    ToDoDeleteView,
)


urlpatterns = [
    # Viewable CRUD pages that don't mess with the API views for postman
    path('home', home, name='home'),
    path('lists/create/', ToDoListCreateView.as_view(), name='create_a_list'),
    path('lists/<int:pk>/', ToDoListDetailView.as_view(), name='get_a_list'),
    path('lists/<int:pk>/update/', ToDoListUpdateView.as_view(), name='update_a_list'),
    path('lists/<int:pk>/delete/', ToDoListDeleteView.as_view(), name='delete_a_list'),
    path('lists/<int:pk>/todos/create/', ToDoCreateView.as_view(), name='create_new_item'),
    path('lists/<int:list_pk>/todos/<int:pk>/', ToDoDetailView.as_view(), name='get_an_item'),
    path('lists/<int:list_pk>/todos/<int:pk>/update/', ToDoUpdateView.as_view(), name='update_an_item'),
    path('lists/<int:list_pk>/todos/<int:pk>/delete/', ToDoDeleteView.as_view(), name='delete_an_item'),

    # CRUD Routes for postman API calls
    path('', ToDoListHandler.as_view(), name='create_a_list_or_get_lists'),
    path('<int:id>/', ToDoListHandler.as_view(), name='get_a_list'),
    path('<int:id>/todos/', ToDoItem.as_view(), name='create_new_item'),
    path('<int:id>/todos/<int:item_id>/', ToDoItem.as_view(), name='get_an_item'),
    path('<int:id>/todos/<int:item_id>/complete/', ToDoItem.as_view(), name='complete_an_item'),
]

urlpatterns += [re_path(r'^.*$', home)]
