from django.urls import path, include

from . import accounts_views, movie_views, core_views


app_name = 'api'
# 917981

accounts_urls = [
    path('register/', accounts_views.UserRegisterView.as_view(), name='register'),
    path('register/verify_email/', accounts_views.UserVerifyEmailTORegisterView.as_view(),
         name='register_verify_email'),
    path('logout/', accounts_views.UserLogoutView.as_view(), name='user_logout'),
]

movie_urls = [
    path('', movie_views.MovieListView.as_view(), name='movie_list'),
    path('comments/<int:movie_id>/', movie_views.MovieCommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:movie_id>/<int:comment_id>/', movie_views.MovieCommentCreateView.as_view(),
         name='comment_create'),
    path('comment/like/<int:comment_id>/', movie_views.MovieCommentLikeView.as_view(), name='comment_like'),
    path('comment/dislike/<int:comment_id>/', movie_views.MovieCommentDislikeView.as_view(), name='comment_dislike'),
    path('reviews/<int:movie_id>/', movie_views.MovieReviewCreateView.as_view(), name='review_create'),
    path('links/<slug:slug>/', movie_views.MovieLinkView.as_view(), name='movie_links'),
    path('detail/<slug:slug>/', movie_views.MovieDetailView.as_view(), name='movie_detail'),
    path('favorite/add/<int:movie_id>/', movie_views.AddFavoriteMovieView.as_view(), name='favorite_add'),
]


core_urls = [
    path('magazine/', core_views.MagazineCreateView.as_view(), name='magazine_create'),
]


urlpatterns = [
    path('', include(core_urls)),
    path('token/', accounts_views.TokenJWTView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', accounts_views.TokenRefreshView.as_view(), name='token_refresh'),
    #
    path('accounts/', include(accounts_urls)),
    path('movies/', include(movie_urls)),
]
