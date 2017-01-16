from api import models
from django.contrib.auth.models import User
from rest_framework import serializers


# ----------- GLOBAL DATA -----------------

class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Difficulty
        fields = '__all__'


class WordClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WordClass
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = '__all__'


# ----------- USER -----------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name'
        )


# ----------- WORDS -----------------

class SlugUserWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserWord
        fields = ('done', 'adaptive_difficulty')


class UserWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserWord
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    word_users = SlugUserWordSerializer(source='userword_set', many=True, read_only=True)

    class Meta:
        model = models.Word
        fields = (
            'id', 'value', 'meaning', 'definition',
            'usage', 'picture', 'sound', 'difficulty',
            'module', 'word_class',
            'word_users'
        )


class SlugWordSerializer(serializers.ModelSerializer):
    lang = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Word
        fields = ('id', 'value', 'meaning', 'picture', 'sound', 'lang')

    def get_lang(self, obj):
        return obj.module.textbook.language.abbreviation


class UserWordRemindSerializer(serializers.ModelSerializer):
    word = SlugWordSerializer()

    class Meta:
        model = models.UserWord
        fields = (
            'word', 'following_reminder'
        )


# ----------- TEXTBOOKS -----------------

class TextbookSerializer(serializers.ModelSerializer):
    language = serializers.PrimaryKeyRelatedField(queryset=models.Language.objects.all())
    owner = OwnerSerializer()

    class Meta:
        model = models.Textbook
        fields = (
            'id', 'title', 'language', 'owner'
        )


class SimpleTextbookSerializer(serializers.ModelSerializer):
    language = serializers.PrimaryKeyRelatedField(queryset=models.Language.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = models.Textbook
        fields = (
            'id', 'title', 'language', 'owner'
        )


class TextbookPublicSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = models.Textbook
        fields = (
            'id', 'title', 'language', 'owner'
        )

    def get_language(self, obj):
        return obj.language.abbreviation

    def get_owner(self, obj):
        return "%s %s" % (obj.owner.first_name, obj.owner.last_name)


# ----------- TESTS -----------------

class TestSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    textbook = TextbookPublicSerializer()
    words_count = serializers.SerializerMethodField(read_only=True)
    words = SlugWordSerializer(read_only=True, many=True)
    groups = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all(), many=True)

    class Meta:
        model = models.Test
        fields = (
            'id', 'title', 'owner', 'textbook', 'groups', 'words_count', 'words'
        )

    def get_words_count(self, obj):
        return obj.words.count()


class SimpleTestSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    textbook = serializers.PrimaryKeyRelatedField(queryset=models.Textbook.objects.all())
    groups = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all(), many=True)

    class Meta:
        model = models.Test
        fields = (
            'id', 'title', 'owner', 'textbook', 'groups'
        )


class TestPublicSerializer(serializers.ModelSerializer):
    textbook = TextbookPublicSerializer()
    done_words_count = serializers.SerializerMethodField(read_only=True)
    words_count = serializers.SerializerMethodField(read_only=True)
    owner = OwnerSerializer()

    class Meta:
        model = models.Test
        fields = (
            'id', 'title', 'owner', 'words_count', 'done_words_count', 'textbook'
        )

    def get_done_words_count(self, obj):
        request = self.context.get('request', None)
        try:
            return models.UserWord.objects.filter(done=True, test_id=obj.id, user_id=request.user.id).count()
        except:
            return 0

    def get_words_count(self, obj):
        return obj.words.count()


# ----------- MODULES -----------------

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Module
        fields = '__all__'


# ----------- GROUPS -----------------

class OwnedGroupSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    users_count = serializers.SerializerMethodField()
    tests_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Group
        fields = (
            'id', 'title', 'name', 'password', 'owner', 'users_count', 'tests_count'
        )

    def get_users_count(self, obj):
        return obj.users.count()

    def get_tests_count(self, obj):
        return obj.test_set.count()


class LoggedGroupSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    users_count = serializers.SerializerMethodField()
    tests_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Group
        fields = (
            'id', 'title', 'name', 'owner', 'users_count', 'tests_count'
        )

    def get_users_count(self, obj):
        return obj.users.count()

    def get_tests_count(self, obj):
        return obj.test_set.count()


class SimpleGroupSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = models.Group
        fields = (
            'id', 'title', 'name', 'password', 'owner'
        )


# class TextbookModuleSerializer(serializers.ModelSerializer):
#     modules = ModuleSerializer(many=True)

#     class Meta:
#         model = models.Textbook
#         fields = (
#             'id', 'title', 'modules'
#         )
