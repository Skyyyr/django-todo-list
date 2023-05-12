from django.core.serializers import serialize
from django.test import TestCase, Client
from django.urls import reverse, resolve
from .models import To_do_list, To_do

import json

# Create your tests here.


class Test_Endpoints(TestCase):
    fixtures = [
        "to_do_list.json",
        "to_do.json",
    ]

    def setUp(self):
        client = Client()

    def test_creating_a_list(self):
        response = self.client.post(reverse('create_a_list_or_get_lists'), data={
            "name": "My new todo list"
        }, content_type="application/json")
        self.assert_(response.status_code == 201)

    def test_getting_a_list_of_to_do_lists(self):
        response = self.client.get(reverse('create_a_list_or_get_lists'))
        with self.subTest():
            self.assert_(response.status_code == 200)
        content = json.loads(response.content)
        self.assertEquals(json.loads(
            serialize('json', To_do_list.objects.all())), content)

    def test_get_a_list(self):
        response = self.client.get(
            reverse("get_a_list", args=[To_do_list.objects.all().first().id]))
        with self.subTest():
            self.assert_(response.status_code == 200)
        content = json.loads(response.content)
        self.assertEquals([{'model': 'to_do_list_app.to_do_list', 'pk': 1,
                            'fields': {'name': 'My new todo list', 'items': [{
                                'model': 'to_do_app.to_do', 'pk': 1,
                                'fields': {'name': 'My new todo item', 'created_at': '13:35:53',
                                           'completed_at': '17:52:04.081', 'to_do_list': 1}},
                                {'model': 'to_do_app.to_do', 'pk': 2,
                                 'fields': {'name': 'a new item', 'created_at': '14:14:53.542',
                                            'completed_at': '15:01:48.032', 'to_do_list': 1}
                                 }]}}], content)

    def test_get_a_list_does_not_exist(self):
        response = self.client.get(reverse("get_a_list", args=[25]))
        self.assert_(response.status_code == 404)

    def test_creating_a_todo_item(self):
        response = self.client.post(reverse("create_new_item", 
            args=[To_do_list.objects.all().first().id]), 
            data={"name": "My new todo item"}, 
            content_type="application/json")
        self.assert_(response.status_code == 201)

    def test_get_an_item_from_a_list(self):
        response = self.client.get(reverse("get_an_item", args=[1,1]))
        with self.subTest():
            self.assert_(response.status_code == 200)
        content = json.loads(response.content)
        self.assertEquals(content, json.loads(serialize('json',[To_do.objects.get(id = 1)])))
    
    def test_get_a_none_existing_item_from_a_list(self):
        response = self.client.get(reverse("get_an_item", args=[1,15]))
        self.assert_(response.status_code == 404)

    def test_get_an_item_from_a_none_existing_list(self):
        response = self.client.get(reverse("get_an_item", args=[15,1]))
        self.assert_(response.status_code == 404)

    def test_complete_an_item_from_a_list(self):
        response = self.client.put(reverse("complete_an_item", args=[1,1]))
        self.assert_(response.status_code == 204)

    def test_complete_a_none_existing_item_from_a_list(self):
        response = self.client.put(reverse("complete_an_item", args=[1,15]))
        self.assert_(response.status_code == 404)
    
    def test_complete_an_item_from_a_none_existing_list(self):
        response = self.client.put(reverse("complete_an_item", args=[15,1]))
        self.assert_(response.status_code == 404)