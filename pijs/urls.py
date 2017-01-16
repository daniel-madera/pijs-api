from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from api import views


urlpatterns = [
    url(r'^$', views.RootViewSet.as_view({
        'get': 'blank_response'
    })),

    # ------------------ AUTH -------------------

    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'^api-token-auth/', obtain_jwt_token),

    url(r'^api-token-refresh/', refresh_jwt_token),

    # --------------- GLOBAL DATA -------------------

    url(r'^difficulties/$', views.DifficultiesViewSet.as_view({
        'get': 'list'
    })),

    url(r'^word_classes/$', views.WordClassViewSet.as_view({
        'get': 'list'
    })),

    url(r'^languages/$', views.LanguagesViewSet.as_view({
        'get': 'list'
    })),

    url(r'^statistics/$', views.StatisticsViewSet.as_view({
        'get': 'get_data'
    })),

    # ---------------- GROUPS ----------------------

    url(r'^groups/owned/$', views.OwnedGroupsViewSet.as_view({
        'post': 'create',
        'get': 'list'
    })),

    url(r'^groups/logged/$', views.LoggedGroupsViewSet.as_view({
        'post': 'sign_in',
        'get': 'list'
    })),

    url(r'^groups/owned/(?P<pk>[0-9]+)/$', views.OwnedGroupViewSet.as_view({
        'patch': 'partial_update',
        'delete': 'destroy'
    })),

    url(r'^groups/logged/(?P<pk>[0-9]+)/$', views.LoggedGroupViewSet.as_view({
        'delete': 'sign_out'
    })),

    # ----------------- TESTS -------------------

    url(r'^tests/$', views.TestsViewSet.as_view({
        'post': 'custom_create',
        'get': 'list'
    })),

    url(r'^tests/owned/$', views.TestsOwnedViewSet.as_view({
        'get': 'list'
    })),

    url(r'^tests/logged/$', views.TestsLoggedViewSet.as_view({
        'get': 'list'
    })),

    url(r'^tests/(?P<pk>[0-9]+)/$', views.TestViewSet.as_view({
        'patch': 'partial_update',
        'delete': 'destroy'
    })),

    url(r'^tests/(?P<test_id>[0-9]+)/words/$', views.WordsTestViewSet.as_view({
        'get': 'list',
        'post': 'add_words'
    })),

    url(r'^tests/(?P<test_id>[0-9]+)/words/exam/$', views.WordsTestExamViewSet.as_view({
        'get': 'list'
    })),

    # ----------------- TEXTBOOKS -------------------

    url(r'^textbooks/$', views.TextbooksViewSet.as_view({
        'post': 'custom_create',
        'get': 'list'
    })),

    url(r'^textbooks/public/$', views.TextbooksPublicViewSet.as_view({
        'get': 'list'
    })),

    url(r'^textbooks/(?P<pk>[0-9]+)/$', views.TextbookViewSet.as_view({
        'patch': 'partial_update',
        'get': 'retrieve',
        'delete': 'destroy'
    })),

    # ----------------- MODULES -------------------

    url(r'^textbooks/(?P<textbook_id>[0-9]+)/modules/$', views.ModulesViewSet.as_view({
        'post': 'custom_create',
        'get': 'list'
    })),

    url(r'^textbooks/(?P<textbook_id>[0-9]+)/import/$', views.WordsImportViewSet.as_view({
        'post': 'custom_create',
    })),

    url(r'^textbooks/(?P<textbook_id>[0-9]+)/modules/(?P<pk>[0-9]+)/$', views.ModuleViewSet.as_view({
        'patch': 'partial_update',
    })),

    # ----------------- WORDS -------------------

    url(r'^textbooks/(?P<textbook_id>[0-9]+)/modules/(?P<module_id>[0-9]+)/words/$', views.WordsViewSet.as_view({
        'post': 'custom_create',
        'get': 'list'
    })),

    url(r'^textbooks/(?P<textbook_id>[0-9]+)/modules/(?P<module_id>[0-9]+)/words/(?P<pk>[0-9]+)/$', views.WordViewSet.as_view({
        'patch': 'partial_update',
        'get': 'retrieve',
        'delete': 'destroy'
    })),

    url(r'^textbooks/(?P<textbook_id>[0-9]+)/modules/(?P<module_id>[0-9]+)/words/(?P<pk>[0-9]+)/sound/$', views.WordViewSet.as_view({
        'post': 'save_sound',
    })),

    url(r'^textbooks/(?P<textbook_id>[0-9]+)/modules/(?P<module_id>[0-9]+)/words/(?P<pk>[0-9]+)/picture/$', views.WordViewSet.as_view({
        'post': 'save_picture'
    })),

    url(r'^words/user/$', views.WordUserViewSet.as_view({
        'post': 'save_user_word'
    })),

    url(r'^remind/words/(?P<pk>[0-9]+)/$', views.WordUserViewSet.as_view({
        'post': 'remind_word'
    })),

    url(r'^remind/words/$', views.WordUserViewSet.as_view({
        'get': 'get_words_to_remind'
    })),

    url(r'^users/is_valid/$', views.UserViewSet.as_view({
        'post': 'validate_username'
    })),

    url(r'^users/$', views.UserViewSet.as_view({
        'post': 'custom_create'
    }))
]
