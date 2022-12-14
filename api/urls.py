from django.urls import path, include

from . import accounts_views, movie_views, core_views, finance_views


app_name = 'api'

accounts_urls = [
    path('register/', accounts_views.UserRegisterView.as_view(), name='register'),
    path('register/verify_email/', accounts_views.UserVerifyEmailTORegisterView.as_view(),
         name='register_verify_email'),
    path('logout/', accounts_views.UserLogoutView.as_view(), name='user_logout'),
    path('change_password/', accounts_views.UserChangePasswordView.as_view(), name='password_change'),
    path('forget_password/', accounts_views.UserForgetPasswordView.as_view(), name='password_forget'),
    path('reset_password/<uuid:uuid>/', accounts_views.UserResetPasswordView.as_view(), name='password_reset'),
    path('profile/<int:pk>/', accounts_views.UserProfileView.as_view(), name='user_profile'),
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
    path('genres/', movie_views.GenreListView.as_view(), name='genre_list'),
    path('action/', movie_views.MovieActionView.as_view(), name='movie_action'),
    path('filter/', movie_views.MovieFilteringView.as_view(), name='movie_filter'),
]


core_urls = [
    path('magazine/', core_views.MagazineCreateView.as_view(), name='magazine_create'),
    path('contact/', core_views.ContactUsCreateSerializer.as_view(), name='contact_create'),
]


finance_urls = [
    path('plans/', finance_views.PlanListView.as_view(), name='plan_list'),
]


urlpatterns = [
    path('', include(core_urls)),
    path('token/', accounts_views.TokenJWTView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', accounts_views.TokenRefreshView.as_view(), name='token_refresh'),
    #
    path('accounts/', include(accounts_urls)),
    path('movies/', include(movie_urls)),
    path('finance/', include(finance_urls)),
]
