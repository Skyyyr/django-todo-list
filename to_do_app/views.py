import json

from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse_lazy
from datetime import datetime

from django.views.generic import UpdateView, DeleteView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from .models import ToDo, ToDoList


class ToDoListHandler(APIView):
    # creates a new list as long as the field of "name" is in request.data
    @staticmethod
    def post(self, request):
        try:
            new_list = ToDoList(**request.data)
            new_list.full_clean()
            new_list.save()
            return Response(f"{request.data.get('name')} was created", status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response("failure to create new list", status=HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get(self, request, id=None):
        if id is not None:
            # gets a specific list with all of its respective to_dos
            current_list = get_object_or_404(ToDoList, pk=id)
            serialized_list = serialize('json', [current_list])
            json_list = json.loads(serialized_list)
            items_in_list = json.loads(
                serialize('json', ToDo.objects.filter(to_do_list=current_list).order_by('pk')))
            json_list[0]['fields']['items'] = items_in_list
            return Response(json_list)

        else:
            # returns a list of to_do_lists
            all_lists = ToDoList.objects.order_by('pk')
            serialized_lists = serialize('json', all_lists)
            json_lists = json.loads(serialized_lists)
            return Response(json_lists)


class ToDoItem(APIView):
    @staticmethod
    def post(self, request, id):
        # creates a new to_do for a to_do_list
        current_list = get_object_or_404(ToDoList, pk=id)
        new_to_do_item = ToDo.objects.create(
            name=request.data['name'], to_do_list=current_list)
        new_to_do_item.full_clean()
        new_to_do_item.save()
        return Response(f"{new_to_do_item.name} was created", status=HTTP_201_CREATED)

    @staticmethod
    def get(self, request, id, item_id):
        # gets a specific to_do
        current_item = get_object_or_404(ToDo, pk=item_id, to_do_list=id)
        json_item = json.loads(serialize('json', [current_item]))
        return Response(json_item)

    @staticmethod
    def put(self, request, id, item_id):
        # marks a specific to_do as completed by setting the completed_at value to the time the request was sent
        current_item = get_object_or_404(ToDo, pk=item_id, to_do_list=id)
        current_item.completed_at = datetime.time(datetime.now())
        current_item.save()
        return Response(status=HTTP_204_NO_CONTENT)


class ToDoListCreateView(generic.CreateView):
    model = ToDoList
    fields = ['name']
    template_name = 'todo_list_form.html'
    success_url = reverse_lazy('home')


class ToDoListDetailView(generic.DetailView):
    model = ToDoList
    template_name = 'todo_list_detail.html'


class ToDoCreateView(generic.CreateView):
    model = ToDo
    fields = ['name', 'to_do_list']
    template_name = 'todo_form.html'
    success_url = reverse_lazy('home')


class ToDoDetailView(generic.DetailView):
    model = ToDo
    template_name = 'todo_detail.html'


class ToDoUpdateView(generic.UpdateView):
    model = ToDo
    fields = ['name', 'to_do_list', 'completed_at']
    template_name = 'todo_update_form.html'


class ToDoDeleteView(generic.DeleteView):
    model = ToDo
    success_url = reverse_lazy('home')


class ToDoListUpdateView(UpdateView):
    model = ToDoList
    fields = ['name']
    template_name = 'todo_update_list.html'
    success_url = reverse_lazy('home')  # Redirect to home page after update


class ToDoListDeleteView(DeleteView):
    model = ToDoList
    template_name = 'todo_delete_list.html'
    success_url = reverse_lazy('home')  # Redirect to home page after deletion


def home(request):
    todo_lists = ToDoList.objects.prefetch_related('todo_set').all()
    context = {
        'todo_lists': todo_lists
    }
    return render(request, 'todo_list_all.html', context)


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
