from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from api import utils
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from api import models
from api import serializers
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class RootViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def blank_response(self, request):
        return Response({}, status=status.HTTP_200_OK)


# ----------- GLOBAL DATA -----------------

class DifficultiesViewSet(viewsets.ModelViewSet):
    queryset = models.Difficulty.objects.all()
    serializer_class = serializers.DifficultySerializer


class LanguagesViewSet(viewsets.ModelViewSet):
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer


class WordClassViewSet(viewsets.ModelViewSet):
    queryset = models.WordClass.objects.all()
    serializer_class = serializers.WordClassSerializer


# ----------- GROUPS -----------------

class OwnedGroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SimpleGroupSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        return models.Group.objects.get(id=pk)


class OwnedGroupsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OwnedGroupSerializer

    def get_queryset(self):
        user = self.request.user.id
        return models.Group.objects.filter(owner=user)

    def create(self, request):
        request.data['owner'] = request.user.id
        request.data['name'] = utils.create_group_name_identifier(
            request.data['title'], request.user.last_name)
        serializer = serializers.SimpleGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoggedGroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LoggedGroupSerializer

    def get_object(self):
        id = self.kwargs['pk']
        return models.Group.objects.get(id=id)

    def sign_out(self, request, pk):
        user = request.user.id
        group = models.Group.objects.get(id=pk)
        group.users.remove(user)
        return Response({}, status=status.HTTP_200_OK)


class LoggedGroupsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LoggedGroupSerializer

    def get_queryset(self):
        user = self.request.user.id
        print(user)
        return models.Group.objects.filter(users=user)

    def sign_in(self, request):
        name = request.data['name']
        password = request.data['password']
        try:
            group = models.Group.objects.get(name=name, password=password)
            group.users.add(request.user.id)
            serializer = serializers.LoggedGroupSerializer(group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {'detail': "Group not found. Check password and name."},
                status=status.HTTP_400_BAD_REQUEST)


# ----------- MODULES -----------------

class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ModuleSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        return models.Module.objects.get(id=pk)


class ModulesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ModuleSerializer

    def get_queryset(self):
        textbook = self.kwargs['textbook_id']
        return models.Module.objects.filter(textbook=textbook)

    def custom_create(self, request, textbook_id):
        # custom create function to define textbook according to url's textbook_id param
        request.data['textbook'] = textbook_id
        serializer = serializers.ModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------- TESTS -----------------

class TestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SimpleTestSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        return models.Test.objects.get(id=pk)


class TestsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TestSerializer

    def get_queryset(self):
        user = self.request.user.id
        return models.Test.objects.filter(owner=user)

    def custom_create(self, request):
        # sets owner to logged user
        request.data['owner'] = request.user.id
        serializer = serializers.SimpleTestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestsOwnedViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TestPublicSerializer

    def get_queryset(self):
        user = self.request.user.id
        return models.Test.objects.filter(owner=user)


class TestsLoggedViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TestPublicSerializer

    def get_queryset(self):
        user = self.request.user.id
        return models.Test.objects.filter(groups__users=user)


# ----------- TEXTBOOKS -----------------

class TextbookViewSet(viewsets.ModelViewSet):
    # sets proper selializer for Textbook object
    serializer_class = serializers.TextbookSerializer

    # on get returns proper textbook object
    def get_object(self):
        pk = self.kwargs['pk']
        return models.Textbook.objects.get(id=pk)


class TextbooksViewSet(viewsets.ModelViewSet):
    # sets proper selializer for Textbook object
    serializer_class = serializers.TextbookSerializer

    def get_queryset(self):
        # filters retrieved textbooks to logged user's only
        user = self.request.user.id
        return models.Textbook.objects.filter(owner=user)

    def custom_create(self, request):
        # sets owner to logged user
        request.data['owner'] = request.user.id
        serializer = serializers.SimpleTextbookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TextbooksPublicViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TextbookPublicSerializer

    def get_queryset(self):
        return models.Textbook.objects.all()


# ----------- WORDS -----------------

class WordsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WordSerializer

    def get_queryset(self):
        # returns only if module_id and textbook_id is valid
        textbook_id = self.kwargs['textbook_id']
        module_id = self.kwargs['module_id']
        module = models.Module.objects.get(id=module_id)

        if module.in_textbook(textbook_id):
            return models.Word.objects.filter(module=module)
        else:
            return []

    def custom_create(self, request, textbook_id, module_id):
        request.data['module'] = module_id
        serializer = serializers.WordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WordsTestExamViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WordSerializer

    def get_queryset(self):
        test_id = self.kwargs['test_id']
        user = self.request.user.id
        words = models.Word.objects.filter(test=test_id).filter(Q(users__isnull=True) | Q(users=user)) \
            .exclude(userword__test_id=test_id, userword__done=True).distinct()
        return words


class WordsTestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SlugWordSerializer

    def get_queryset(self):
        test_id = self.kwargs['test_id']
        return models.Test.objects.get(id=test_id).words

    def add_words(self, request, test_id):
        words = request.data['words']
        test = models.Test.objects.get(id=test_id)
        test.words.set(words)
        test.save()
        serializer = serializers.TestSerializer(test)
        return Response(serializer.data, status.HTTP_200_OK)


class WordsImportViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SlugWordSerializer

    def custom_create(self, request, textbook_id):
        for module in request.data:
            module['textbook_id'] = int(textbook_id)
            m, created = models.Module.objects.get_or_create(textbook_id=module['textbook_id'], title=module['title'])

            for word in module['words']:
                word['module'] = m
                try:
                    w = models.Word(**word)
                    w.save()
                except ValidationError as e:
                    print(e.messages[0])

        return Response({}, status=status.HTTP_201_CREATED)


class WordViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WordSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        return models.Word.objects.get(id=pk)

    def save_picture(self, request, textbook_id, module_id, pk):
        word = models.Word.objects.get(id=pk)
        if request.data['action'] == 'save':
            path = utils.save_picture(word.id, request.data['url'])
            if path is False:
                return Response({'path': ''}, status=status.HTTP_400_BAD_REQUEST)
        else:
            path = utils.remove_picture(word.id)
        return Response({'path': path}, status=status.HTTP_200_OK)

    def save_sound(self, request, textbook_id, module_id, pk):
        word = models.Word.objects.get(id=pk)
        if request.data['action'] == 'save':
            textbook = models.Textbook.objects.get(id=word.module.textbook_id)
            lang = textbook.language.abbreviation
            path = utils.save_sound(word.id, word.value, lang)
        else:
            path = utils.remove_sound(word.id)
        return Response({'path': path}, status=status.HTTP_200_OK)


class WordUserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WordSerializer

    def get_queryset(self):
        user = self.request.user.id
        return models.UserWord.objects.filter(user_id=user)

    def save_user_word(self, request):
        user = request.user.id
        words = request.data['words']
        for word in words:
            try:
                user_word = models.UserWord.objects.get(user_id=user, word_id=word['id'], test_id=word['test'])
            except:
                user_word = models.UserWord(user_id=user, word_id=word['id'], test_id=word['test'])

            user_word.adaptive_difficulty_id = word['difficulty']
            prev = user_word.last_interval
            af = utils.absolute_difficulty(user_word.word.value, user_word.adaptive_difficulty_id)
            user_word.last_interval = utils.new_interval(prev, af, 0, 0)
            user_word.following_reminder = timezone.now() + timedelta(days=user_word.last_interval)
            user_word.done = bool(word['done'])
            user_word.save()

        return Response({}, status.HTTP_200_OK)

    def remind_word(self, request, pk):
        user = request.user.id
        user_word = models.UserWord.objects.get(user_id=user, word_id=pk)

        if request.data['action'] == 'success':
            user_word.success_repetitions += 1
        else:
            user_word.success_repetitions = 0
            user_word.memory_lapses += 1

        prev = user_word.last_interval
        af = utils.absolute_difficulty(user_word.word.value, user_word.adaptive_difficulty_id)
        n = user_word.success_repetitions
        l = user_word.memory_lapses
        user_word.last_interval = utils.new_interval(prev, af, l, n)
        user_word.following_reminder = timezone.now() + timedelta(days=user_word.last_interval)
        user_word.save()
        serializer = serializers.UserWordSerializer(user_word)
        return Response(serializer.data, status.HTTP_200_OK)

    def get_words_to_remind(self, request):
        user = request.user.id
        user_words_ids = models.UserWord.objects.filter(user_id=user, following_reminder__lt=timezone.now(), done=True)\
            .order_by('word__value').distinct('word__value').values_list('id', flat=True)
        user_words = models.UserWord.objects.filter(id__in=user_words_ids).order_by('following_reminder')
        serializer = serializers.UserWordRemindSerializer(user_words, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class StatisticsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WordSerializer
    queryset = models.Word.objects.all()

    def get_data(self, request):
        user = request.user.id
        mastered_words = models.UserWord.objects.filter(done=True, user_id=user)
        unique_words = mastered_words.values_list('word__value', flat=True).distinct()
        groups = models.Group.objects.filter(Q(owner=user) | Q(users=user)).distinct()
        groups_data = []
        user_data = {
            'mastered_words': mastered_words.count(),
            'mastered_unique_words': unique_words.count()
        }

        for group in groups:
            mastered_words = models.UserWord.objects.order_by('word__value', 'user_id') \
                .filter(done=True, user_id__in=group.users.values_list('id', flat=True))
            mastered_words = mastered_words.order_by('word__value', 'user_id').distinct('word__value', 'user_id')

            groups_data.append({
                'id': group.id,
                'title': group.title,
                'name': group.name,
                'owner': group.owner.first_name + ' ' + group.owner.last_name,
                'mastered_words': mastered_words.count()
            })

        data = {
            'user': user_data,
            'groups': groups_data
        }
        return Response(data, status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user.id
        return User.objects.filter(id=user)

    def custom_create(self, request):
        # add date_joined field
        request.data['date_joined'] = timezone.now().isoformat()
        # hash password
        request.data['password'] = make_password(request.data['password'])
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def validate_username(self, request):
        username = request.data['username']
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({}, status.HTTP_200_OK)

        return Response({}, status.HTTP_400_BAD_REQUEST)
