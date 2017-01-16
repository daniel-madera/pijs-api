from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from api.models import Difficulty, Language, Group, Module, Textbook, Word, WordClass


class AdditionalDataTests(APITestCase):
    fixtures = ['app-startup', 'test-data']
    client = APIClient()

    # url /difficulties/
    # tests if status code is OK
    # length of returned objects equals db
    # check if returend data are in proper order
    def test_difficulties(self):
        self.client.force_login(user=User.objects.get(username='novak'))
        count = Difficulty.objects.count()
        response = self.client.get('/difficulties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count)
        self.assertEqual(response.data[0]['title'], 'snadné')

    # url /languages/
    # tests if status code is OK
    # length of returned objects equals db
    # check if returend data are in proper order
    def test_languages(self):
        self.client.force_login(user=User.objects.get(username='novak'))
        count = Language.objects.count()
        response = self.client.get('/languages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count)
        self.assertEqual(response.data[0]['title'], 'angličtina')

    # url /word_classes/
    # tests if status code is OK
    # length of returned objects equals db
    # check if returend data are in proper order
    def test_word_classes(self):
        self.client.force_login(user=User.objects.get(username='novak'))
        count = WordClass.objects.count()
        response = self.client.get('/word_classes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count)
        self.assertEqual(response.data[0]['title'], 'podstatné jméno')


class AuthTests(APITestCase):
    fixtures = ['app-startup', 'test-data']
    client = APIClient()

    # check if token is succesfully recieved
    def test_token_recieve(self):
        data = {'username': 'novak', 'password': 'password123'}
        response = self.client.post('/api-token-auth/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['token']), 189)

    # checks if data are able to fetch only if user has proper JWT token
    def test_authorized_access(self):
        data = {'username': 'novak', 'password': 'password123'}
        response = self.client.post('/api-token-auth/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['token']), 189)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])
        response = self.client.get('/textbooks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # checks status on unauthorized attempt
    def test_unauthorized_access(self):
        response = self.client.get('/textbooks/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GroupsTest(APITestCase):
    fixtures = ['app-startup', 'test-data']
    client = APIClient()

    # url /groups/
    # checks if user recieves his groups and attempts to create new group
    def test_groups(self):
        self.client.force_login(user=User.objects.get(username='novak'))
        data = {'title': 'Nová skupina', 'textbook': 1, 'password': 'pass',
                'name': 'name1223'}
        count = Group.objects.filter(owner=2).count()
        response = self.client.get('/groups/owned/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, len(response.data))
        response = self.client.post('/groups/owned/', data)
        count_after = Group.objects.filter(owner=2).count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count_after, count + 1)


class ModuleTests(APITestCase):
    fixtures = ['app-startup', 'test-data']
    client = APIClient()

    # url /textbooks/1/modules
    # checks if module is created and saved in db
    def test_create(self):
        self.client.force_login(user=User.objects.get(username='novak'))
        data = {'title': 'Nová lekce 1', 'textbook': 1}
        count = Module.objects.filter(textbook=1).count()
        response = self.client.post('/textbooks/1/modules/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.filter(textbook=1).count(), count + 1)

    # url /textbooks/1/modules/2
    # checks if module is partialy updated
    def test_patch(self):
        self.client.force_login(user=User.objects.get(username='novak'))
        data = {'title': 'Nový název lekce patch'}
        response = self.client.patch('/textbooks/1/modules/2/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # url /textbooks/1/modules/
    # checks if modules are properly retrieved
    def test_list(self):
        self.client.force_login(user=User.objects.get(username='novak'))
        count = Module.objects.filter(textbook=1).count()
        response = self.client.get('/textbooks/1/modules/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count)


class TextbookTests(APITestCase):
    fixtures = ['app-startup', 'test-data']
    client = APIClient()

    # url /textbooks/
    # checks if textbook is created and stored in db
    def test_create(self):
        self.client.force_login(user=User.objects.get(username='novak'))
        data = {'title': 'Test1', 'language': 3}
        count = Textbook.objects.count()
        response = self.client.post('/textbooks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Textbook.objects.count(), count + 1)

    # url /textbooks/1
    # checks if textbook is partialy updated
    def test_patch(self):
        self.client.force_login(user=User.objects.get(username='novak'))
        data = {'title': 'Nový název učebnice patch'}
        response = self.client.patch('/textbooks/1/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # url /textbooks/1
    # checks if textbook is properly retrieved
    def test_retrieve(self):
        self.client.force_login(user=User.objects.get(username='novak'))
        response = self.client.get('/textbooks/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # url /textbooks/
    # checks if textbooks are properly retrieved
    # checks if textbook list is filtered only to textbooks of currently logged user
    def test_list(self):
        self.client.force_login(user=User.objects.get(username='novak'))
        textbooks = Textbook.objects.filter(owner=2)
        count = textbooks.count()
        response = self.client.get('/textbooks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count)
