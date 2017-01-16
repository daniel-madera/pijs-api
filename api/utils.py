from api.serializers import UserSerializer
from api.models import Group, Word
from gtts import gTTS
from django.conf import settings
import os.path
import datetime
import unicodedata
import re
import urllib
import time
from PIL import Image


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


def create_group_name_identifier(title, owner_last_name):
    title = unicodedata.normalize('NFKD', title.lower()).encode('ASCII', 'ignore').decode("utf-8")
    owner = unicodedata.normalize('NFKD', owner_last_name.lower()).encode('ASCII', 'ignore').decode("utf-8")
    title = re.sub(r'[^a-zA-Z0-9_]', '_', title)
    title = re.sub('_+', '_', title)
    now = datetime.datetime.now()
    year = now.year
    name = '%d_%s_%s' % (year, owner, title)
    c = Group.objects.filter(name__contains=name).count()
    if c > 0:
        name = name + '_' + c
    return name


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value.strip().lower()).encode('ascii', 'ignore').decode("utf-8")
    value = re.sub('[^\w\s-]', '', value)
    value = re.sub('[-\s]+', '-', value)
    return value


def remove_file(filename):
    try:
        os.remove(filename)
    except:
        pass


def save_sound(id, text, lang):
    remove_sound(id)
    newfilename = '../static/sounds/%d.mp3' % time.time()
    settings.STATIC_ROOT
    tts = gTTS(text=text, lang=lang)
    tts.save(newfilename)
    word = Word.objects.get(id=id)
    word.sound = newfilename
    word.save()
    return newfilename


def remove_sound(id):
    word = Word.objects.get(id=id)
    filename = word.sound
    remove_file(filename)
    word.sound = ''
    word.save()
    return word.sound


def save_picture(id, url):
    remove_picture(id)
    newfilename = '../static/images/%d.jpg' % time.time()
    if not retrieve_and_resize_picture(url, newfilename):
        return False
    word = Word.objects.get(id=id)
    word.picture = newfilename
    word.save()
    return newfilename


def retrieve_and_resize_picture(url, filename):
    try:
        urllib.request.urlretrieve(url, filename + '.bak')
        img = Image.open(filename + '.bak')
        img.thumbnail((400, 400))
        img.save(filename)
        os.remove(filename + '.bak')
    except Exception as e:
        remove_file(filename + '.bak')
        return False

    return True


def remove_picture(id):
    word = Word.objects.get(id=id)
    filename = word.picture
    remove_file(filename)
    word.picture = ''
    word.save()
    return word.picture


def absolute_difficulty(word, difficulty):
    if difficulty == 4:
        return 0

    tmp = 0
    if len(word) > 10:
        tmp = 2
    elif len(word) > 5:
        tmp = 1

    af = 3
    if difficulty == 2:
        af = 6
    elif difficulty == 1:
        af = 9

    return af - tmp


def new_interval(prev, af, l, n):
    of = [[1.20, 1.27, 1.33, 1.40, 1.47, 1.53, 1.60, 1.67, 1.73, 1.80],
          [1.20, 1.26, 1.32, 1.38, 1.44, 1.50, 1.56, 1.62, 1.68, 1.74],
          [1.20, 1.25, 1.31, 1.36, 1.42, 1.47, 1.53, 1.58, 1.64, 1.69],
          [1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.50, 1.55, 1.60, 1.65],
          [1.20, 1.25, 1.29, 1.34, 1.39, 1.43, 1.48, 1.52, 1.57, 1.61],
          [1.20, 1.24, 1.29, 1.33, 1.37, 1.41, 1.46, 1.50, 1.54, 1.59],
          [1.20, 1.24, 1.28, 1.32, 1.36, 1.40, 1.44, 1.48, 1.52, 1.56],
          [1.20, 1.24, 1.27, 1.31, 1.35, 1.39, 1.43, 1.46, 1.50, 1.54],
          [1.20, 1.24, 1.27, 1.31, 1.34, 1.38, 1.41, 1.45, 1.48, 1.52],
          [1.20, 1.23, 1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50]]
    n = n % 10

    if n == 0:
        return of[0][l]
    else:
        return prev * of[n - 1][af]
