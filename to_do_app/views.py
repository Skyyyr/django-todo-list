from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.serializers import serialize
from django.utils.timezone import datetime
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import To_do, To_do_list
import json

# Create your views here.


class To_do_list_handler(APIView):
    # creates a new list as long as the field of "name" is in request.data
    def post(self, request):
        try:
            new_list = To_do_list(**request.data)
            new_list.full_clean()
            new_list.save()
            return Response(f"{request.data.get('name')} was created", status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response("failure to create new list", status=HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, id=None):
        if id is not None:
            # gets a specific list with all of its respective to_dos
            current_list = get_object_or_404(To_do_list, pk=id)
            serialized_list = serialize('json', [current_list])
            json_list = json.loads(serialized_list)
            items_in_list = json.loads(
                serialize('json', To_do.objects.filter(to_do_list=current_list).order_by('pk')))
            json_list[0]['fields']['items'] = items_in_list
            return Response(json_list)

        else:
            # returns a list of to_do_lists
            all_lists = To_do_list.objects.order_by('pk')
            serialized_lists = serialize('json', all_lists)
            json_lists = json.loads(serialized_lists)
            return Response(json_lists)


class To_do_item(APIView):
    def post(self, request, id):
        # creates a new to_do for a to_do_list
        current_list = get_object_or_404(To_do_list, pk=id)
        new_to_do_item = To_do.objects.create(
            name=request.data['name'], to_do_list=current_list)
        new_to_do_item.full_clean()
        new_to_do_item.save()
        return Response(f"{new_to_do_item.name} was created", status=HTTP_201_CREATED)

    def get(self, request, id, item_id):
        # gets a specific to_do
        current_item = get_object_or_404(To_do, pk=item_id, to_do_list=id)
        json_item = json.loads(serialize('json', [current_item]))
        return Response(json_item)

    def put(self, request, id, item_id):
        # marks a specific to_do as completed by setting the completed_at value to the time the request was sent
        current_item = get_object_or_404(To_do, pk=item_id, to_do_list=id)
        current_item.completed_at = datetime.time(datetime.now())
        current_item.save()
        return Response(status=HTTP_204_NO_CONTENT)
