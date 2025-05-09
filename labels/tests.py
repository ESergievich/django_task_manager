import os
import json

from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse_lazy
from labels.models import Label
from task_manager.settings import FIXTURE_DIRS


class SetupTestLabels(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.labels_url = reverse_lazy('labels')
        self.create_label_url = reverse_lazy('label_create')
        self.update_label_url = reverse_lazy("label_update", kwargs={"pk": 1})
        self.delete_label1_url = reverse_lazy("label_delete", kwargs={"pk": 1})
        self.delete_label3_url = reverse_lazy("label_delete", kwargs={"pk": 3})
        self.user1 = get_user_model().objects.get(pk=1)
        self.label1 = Label.objects.get(pk=1)
        with open(os.path.join(FIXTURE_DIRS[0], "one_label.json")) as file:
            self.test_label = json.load(file)


class TestLabelsList(SetupTestLabels):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_open_labels_page_with_login(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(self.labels_url)
        self.assertEqual(response.status_code, 200)

    def test_open_labels_page_with_no_login(self):
        response = self.client.get(self.labels_url)
        self.assertEqual(response.status_code, 302)


class TestCreateLabel(SetupTestLabels):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_open_create_label_page_with_login(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(self.create_label_url)
        self.assertEqual(response.status_code, 200)

    def test_open_create_label_page_with_no_login(self):
        response = self.client.get(self.create_label_url)
        self.assertEqual(response.status_code, 302)

    def test_create_label(self):
        self.client.force_login(user=self.user1)
        response = self.client.post(path=self.create_label_url,
                                    data=self.test_label)
        self.assertRedirects(response=response, expected_url=self.labels_url)
        self.assertEqual(response.status_code, 302)

        self.label4 = Label.objects.get(pk=4)
        self.assertEqual(first=self.label4.name,
                         second=self.test_label.get('name'))
        self.assertEqual(Label.objects.all().count(), 4)


class TestUpdateLabel(SetupTestLabels):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_open_update_label_page_with_login(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(self.update_label_url)
        self.assertEqual(response.status_code, 200)

    def test_open_update_label_page_with_no_login(self):
        response = self.client.get(self.update_label_url)
        self.assertEqual(response.status_code, 302)

    def test_update_label(self):
        self.client.force_login(self.user1)
        self.label1 = Label.objects.get(pk=1)
        self.assertNotEqual(self.label1.name, self.test_label.get("name"))

        response = self.client.post(path=self.update_label_url,
                                    data=self.test_label)
        self.assertEqual(response.status_code, 302)

        self.label1 = Label.objects.get(pk=1)
        self.assertEqual(first=self.label1.name,
                         second=self.test_label.get('name')
                         )


class TestDeleteLabel(SetupTestLabels):
    fixtures = ['users.json', 'tasks.json', 'statuses.json', 'labels.json']

    def test_open_delete_page_with_login(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(path=self.delete_label1_url)
        self.assertEqual(first=response.status_code, second=200)

    def test_open_delete_page_with_no_login(self):
        response = self.client.get(path=self.delete_label1_url)
        self.assertEqual(first=response.status_code, second=302)

    def test_delete_label(self):
        self.client.force_login(user=self.user1)
        response = self.client.delete(path=self.delete_label3_url)
        self.assertEqual(first=response.status_code, second=302)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=3)

    def test_cant_delete_label_with_task(self):
        self.client.force_login(user=self.user1)
        with self.assertRaises(expected_exception=ProtectedError):
            self.client.delete(path=self.delete_label1_url)
        self.assertEqual(first=Label.objects.all().count(), second=3)
