from django.urls import path
from .views import To_do_list_handler, To_do_item


urlpatterns = [
    path('', To_do_list_handler.as_view(), name='create_a_list_or_get_lists'),
    path('<int:id>/', To_do_list_handler.as_view(), name='get_a_list'),
    path('<int:id>/todos/', To_do_item.as_view(), name='create_new_item'),
    path('<int:id>/todos/<int:item_id>/', To_do_item.as_view(), name='get_an_item'),
    path('<int:id>/todos/<int:item_id>/complete/', To_do_item.as_view(), name='complete_an_item'),
]
