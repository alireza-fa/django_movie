from django.urls import path, include

from . import accounts_views, movie_views


app_name = 'api'


accounts_urls = [
    path('register/', accounts_views.UserRegisterView.as_view(), name='register'),
    path('register/verify_email/', accounts_views.UserVerifyEmailTORegisterView.as_view(),
         name='register_verify_email'),
    path('logout/', accounts_views.UserLogoutView.as_view(), name='user_logout'),
]

movie_urls = [
    path('', movie_views.MovieListView.as_view(), name='movie_list'),
    path('<slug:slug>/', movie_views.MovieDetailView.as_view(), name='movie_detail'),
    path('links/<slug:slug>/', movie_views.MovieLinkView.as_view(), name='movie_links'),
]


urlpatterns = [
    path('token/', accounts_views.TokenJWTView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', accounts_views.TokenRefreshView.as_view(), name='token_refresh'),
    #
    path('accounts/', include(accounts_urls)),
    path('movies/', include(movie_urls)),
]
