from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Difficulty(models.Model):
    title = models.CharField(max_length=30, unique=True)
    # pro budoucí možné rozšíření na dynamické
    # přidělování obtížnosti slov
    # range = models.FloatRangeField()

    def __str__(self):
        return '%s' % self.title

    class Meta:
        ordering = ['id']


class Language(models.Model):
    title = models.CharField(max_length=70, unique=True)
    abbreviation = models.CharField(max_length=3, unique=True)
    # reprezentace překladu hlásek pro daný jazyk pro určení
    # podobnosti slov (např. němčiny v => f, ö => e)
    # sounds = models.CharField(max_length=200)

    def __str__(self):
        return '%s (%s)' % (self.title, self.abbreviation)

    class Meta:
        ordering = ['id']


class WordClass(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        ordering = ['id']


class Textbook(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=70)

    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s [%s], (owner: %s)' % (self.title, self.language.abbreviation, self.owner.username)

    class Meta:
        unique_together = ('owner', 'title')
        ordering = ['id']


class Word(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    value = models.CharField(max_length=100)
    meaning = models.CharField(max_length=100)
    definition = models.CharField(max_length=254, null=True, blank=True)
    usage = models.CharField(max_length=254, null=True, blank=True)
    picture = models.CharField(max_length=100, null=True, blank=True)
    sound = models.CharField(max_length=100, null=True, blank=True)

    difficulty = models.ForeignKey(Difficulty, on_delete=models.PROTECT)
    module = models.ForeignKey('Module', related_name='words', on_delete=models.CASCADE)
    word_class = models.ForeignKey(WordClass, related_name='words', on_delete=models.PROTECT)
    # able to access user.word_set()
    users = models.ManyToManyField(User, through='UserWord', blank=True)

    def __str__(self):
        return '<Word %s: %s (from %s) [%s, %s]>' % \
            (self.value, self.meaning, self.module.textbook.title,
                self.difficulty.title, self.word_class.title)

    def clean(self, *args, **kwargs):
        # validation if word already exists in same textbook
        if self.id is None:
            textbook_id = self.module.textbook_id
            module_ids = Module.objects.filter(textbook_id=textbook_id).values_list('id', flat=True)
            n_words_in_textbook = Word.objects.filter(value=self.value, module__in=module_ids).count()

            if n_words_in_textbook > 0:
                raise ValidationError(
                    'Word %s already exists in textbook %s (%d).' %
                    (self.value, self.module.textbook.title, self.module.textbook_id))

        super(Word, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Word, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('value', 'module')
        ordering = ['id']


class Module(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=70)

    textbook = models.ForeignKey(Textbook, related_name='modules', on_delete=models.CASCADE)

    def __str__(self):
        return '%s (textbook: %s)' % (self.title, self.textbook.title)

    def in_textbook(self, textbook_id):
        textbook_id = int(textbook_id)
        return self.textbook.id == textbook_id

    class Meta:
        ordering = ['textbook', 'title']
        unique_together = ('title', 'textbook')


class UserWord(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    following_reminder = models.DateTimeField(null=True)
    last_interval = models.FloatField()
    memory_lapses = models.PositiveIntegerField(default=0)
    success_repetitions = models.PositiveIntegerField(default=0)
    absolute_difficulty = models.PositiveIntegerField(default=0)
    done = models.BooleanField(default=False)

    adaptive_difficulty = models.ForeignKey(Difficulty)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)

    def __str__(self):
        return '%s user\'s word %s' % (self.user.username, self.word.value)

    class Meta:
        ordering = ['id']
        unique_together = ('user', 'word', 'test')


class Group(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=70)
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=40)

    owner = models.ForeignKey(User, related_name='owned_groups')
    users = models.ManyToManyField(User)

    def __str__(self):
        return '%s (%s:%s) users: %s' % \
            (self.title, self.name, self.password, self.users.count())

    class Meta:
        ordering = ['id']


class Test(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=70)
    hidden = models.BooleanField(default=False)

    owner = models.ForeignKey(User, related_name='owned_tests')
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, blank=True)
    words = models.ManyToManyField(Word, blank=True)

    def __str__(self):
        return '%s [hidden: %s, words: %d]' % (self.title, self.hidden, self.words.count())

    class Meta:
        ordering = ['id']
