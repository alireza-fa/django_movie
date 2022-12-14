# Generated by Django 3.2 on 2022-09-24 01:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='genre')),
                ('english_name', models.CharField(max_length=32, verbose_name='english name')),
                ('slug', models.SlugField(max_length=40, verbose_name='slug')),
                ('image_cover', models.ImageField(upload_to='', verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=120, verbose_name='name')),
                ('english_name', models.CharField(max_length=120, verbose_name='english name')),
                ('slug', models.SlugField(max_length=120, verbose_name='slug')),
                ('description', models.TextField(verbose_name='description')),
                ('poster', models.ImageField(blank=True, null=True, upload_to='', verbose_name='poster')),
                ('image_cover', models.ImageField(upload_to='', verbose_name='image cover')),
                ('image_background', models.ImageField(upload_to='', verbose_name='image background')),
                ('publish_at', models.DateField(verbose_name='publish_at')),
                ('created_at', models.DateField(verbose_name='created at')),
                ('trailer', models.CharField(blank=True, max_length=240, null=True, verbose_name='trailer')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'film'), (2, 'series')], default=1, verbose_name='type')),
                ('quality', models.PositiveSmallIntegerField(choices=[(1, '?????????? ????????'), (2, '?????????? ????????')], default=1, verbose_name='quality')),
                ('time_in_minutes', models.PositiveIntegerField(verbose_name='time in minutes')),
                ('ages', models.PositiveSmallIntegerField(verbose_name='ages')),
                ('is_free', models.BooleanField(default=True, verbose_name='is free')),
                ('country', models.CharField(choices=[('afghanistan', '??????????????????'), ('argentina', '????????????????'), ('austria', '????????????????'), ('azerbaijan', '??????????????????'), ('belgium', '??????????'), ('cameroon', '????????????'), ('canada', '????????????'), ('chile', '????????'), ('china', '??????'), ('colombia', '????????????'), ('denmark', '??????????????'), ('egypt', '??????'), ('finland', '????????????'), ('france', '????????????'), ('germany', '??????????'), ('hungary', '????????????????'), ('indonesia', '??????????????????'), ('iran', '??????????'), ('iraq', '????????'), ('italy', '??????????????'), ('japan', '????????'), ('mexico', '??????????'), ('morocco', '??????????'), ('nepal', '????????'), ('netherlands', '????????????'), ('poland', '??????????'), ('russia', '??????????'), ('sweden', '????????'), ('thailand', '????????????'), ('turkey', '??????????'), ('uk', '????????????????'), ('usa', '????????????'), ('vietnam', '????????????')], max_length=34, verbose_name='country')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Movie',
                'verbose_name_plural': 'Movies',
                'ordering': ('-publish_at',),
            },
        ),
        migrations.CreateModel(
            name='MovieComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('body', models.TextField(verbose_name='body')),
                ('is_reply', models.BooleanField(default=False, verbose_name='is reply')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='movie.movie', verbose_name='movie')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='movie.moviecomment', verbose_name='parent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Movie Comment',
                'verbose_name_plural': 'Movie Comments',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='SeasonPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('poster', models.ImageField(upload_to='', verbose_name='poster')),
                ('part', models.PositiveSmallIntegerField(verbose_name='part')),
            ],
            options={
                'verbose_name': 'Season Part',
                'verbose_name_plural': 'Season Parts',
                'ordering': ('part',),
            },
        ),
        migrations.CreateModel(
            name='SeriesSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('season', models.PositiveSmallIntegerField(verbose_name='season')),
                ('name', models.CharField(max_length=120)),
                ('image_background', models.ImageField(upload_to='', verbose_name='image background')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='movie.movie', verbose_name='series')),
            ],
            options={
                'verbose_name': 'Series Season',
                'verbose_name_plural': 'Series Seasons',
                'ordering': ('season',),
            },
        ),
        migrations.CreateModel(
            name='SeasonPartSubtitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('afghanistan', '??????????????????'), ('argentina', '????????????????'), ('austria', '????????????????'), ('azerbaijan', '??????????????????'), ('belgium', '??????????'), ('cameroon', '????????????'), ('canada', '????????????'), ('chile', '????????'), ('china', '??????'), ('colombia', '????????????'), ('denmark', '??????????????'), ('egypt', '??????'), ('finland', '????????????'), ('france', '????????????'), ('germany', '??????????'), ('hungary', '????????????????'), ('indonesia', '??????????????????'), ('iran', '??????????'), ('iraq', '????????'), ('italy', '??????????????'), ('japan', '????????'), ('mexico', '??????????'), ('morocco', '??????????'), ('nepal', '????????'), ('netherlands', '????????????'), ('poland', '??????????'), ('russia', '??????????'), ('sweden', '????????'), ('thailand', '????????????'), ('turkey', '??????????'), ('uk', '????????????????'), ('usa', '????????????'), ('vietnam', '????????????')], default='iran', max_length=32, verbose_name='language')),
                ('subtitle', models.FileField(max_length=240, upload_to='', verbose_name='subtitle')),
                ('season_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtitles', to='movie.seasonpart', verbose_name='season part')),
            ],
        ),
        migrations.AddField(
            model_name='seasonpart',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='movie.seriesseason', verbose_name='Season Part'),
        ),
        migrations.CreateModel(
            name='PartLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('quality', models.IntegerField(verbose_name='quality')),
                ('volume', models.CharField(max_length=34)),
                ('link', models.CharField(max_length=240)),
                ('season_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='movie.seasonpart', verbose_name='part link')),
            ],
            options={
                'verbose_name': 'Part Link',
                'verbose_name_plural': 'Part Links',
                'ordering': ('-quality',),
            },
        ),
        migrations.CreateModel(
            name='MovieReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('rate', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], verbose_name='rate')),
                ('subject', models.CharField(max_length=120, verbose_name='subject')),
                ('description', models.TextField(verbose_name='body')),
                ('is_active', models.BooleanField(default=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movie.movie', verbose_name='movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Movie Review',
                'verbose_name_plural': 'Movie Reviews',
            },
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movies', to='movie.genre', verbose_name='genre')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genres', to='movie.movie', verbose_name='movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieCommentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='movie.moviecomment', verbose_name='comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Movie Comment Like',
                'verbose_name_plural': 'Movie Comment Dislikes',
            },
        ),
        migrations.CreateModel(
            name='MovieCommentDislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='movie.movie', verbose_name='dislike')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Movie Comment Dislike',
                'verbose_name_plural': 'Movie Comment Dislikes',
            },
        ),
        migrations.CreateModel(
            name='FilmSubtitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('afghanistan', '??????????????????'), ('argentina', '????????????????'), ('austria', '????????????????'), ('azerbaijan', '??????????????????'), ('belgium', '??????????'), ('cameroon', '????????????'), ('canada', '????????????'), ('chile', '????????'), ('china', '??????'), ('colombia', '????????????'), ('denmark', '??????????????'), ('egypt', '??????'), ('finland', '????????????'), ('france', '????????????'), ('germany', '??????????'), ('hungary', '????????????????'), ('indonesia', '??????????????????'), ('iran', '??????????'), ('iraq', '????????'), ('italy', '??????????????'), ('japan', '????????'), ('mexico', '??????????'), ('morocco', '??????????'), ('nepal', '????????'), ('netherlands', '????????????'), ('poland', '??????????'), ('russia', '??????????'), ('sweden', '????????'), ('thailand', '????????????'), ('turkey', '??????????'), ('uk', '????????????????'), ('usa', '????????????'), ('vietnam', '????????????')], default='iran', max_length=32, verbose_name='language')),
                ('subtitle', models.FileField(max_length=240, upload_to='', verbose_name='subtitle')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtitles', to='movie.movie', verbose_name='film')),
            ],
        ),
        migrations.CreateModel(
            name='FilmLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=120)),
                ('quality', models.IntegerField(verbose_name='quality')),
                ('volume', models.CharField(max_length=32)),
                ('link', models.CharField(max_length=240)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='movie.movie')),
            ],
            options={
                'verbose_name': 'Film Link',
                'verbose_name_plural': 'Film Links',
                'ordering': ('-quality',),
            },
        ),
        migrations.CreateModel(
            name='FavoriteMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='movie.movie', verbose_name='movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Favorite Movie',
                'verbose_name_plural': 'Favorite Movies',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='FilmMovie',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('movie.movie',),
        ),
        migrations.CreateModel(
            name='SeriesMovie',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('movie.movie',),
        ),
    ]
