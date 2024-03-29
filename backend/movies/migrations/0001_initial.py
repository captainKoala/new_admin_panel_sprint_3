# Generated by Django 3.2 on 2022-06-06 10:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilmWork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, help_text='TimeStampedMixin.created.help_text', verbose_name='TimeStampedMixin.created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='TimeStampedMixin.modified.help_text', verbose_name='TimeStampedMixin.modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUIDMixin.ID.help_text', primary_key=True, serialize=False, verbose_name='UUIDMixin.ID')),
                ('title', models.CharField(help_text='Filmwork.title.help_text', max_length=255, verbose_name='Filmwork.title')),
                ('description', models.TextField(blank=True, help_text='Filmwork.description.help_text', null=True, verbose_name='Filmwork.description')),
                ('creation_date', models.DateField(blank=True, help_text='Filmwork.creation_date.help_text', null=True, verbose_name='Filmwork.creation_date')),
                ('rating', models.FloatField(blank=True, help_text='Filmwork.rating.help_text', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Filmwork.rating')),
                ('type', models.CharField(choices=[('movie', 'FilmWorkTypes.MOVIE'), ('tv', 'FilmWorkTypes.Tv_SHOW')], default='movie', help_text='Filmwork.type.help_text', max_length=16, verbose_name='Filmwork.type')),
            ],
            options={
                'verbose_name': 'FilmWork.verbose_name',
                'verbose_name_plural': 'FilmWork.verbose_name_plural',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, help_text='TimeStampedMixin.created.help_text', verbose_name='TimeStampedMixin.created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='TimeStampedMixin.modified.help_text', verbose_name='TimeStampedMixin.modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUIDMixin.ID.help_text', primary_key=True, serialize=False, verbose_name='UUIDMixin.ID')),
                ('name', models.CharField(help_text='Genre.title.help_text', max_length=255, verbose_name='Genre.title')),
                ('description', models.TextField(blank=True, help_text='Genre.description.help_text', null=True, verbose_name='Genre.description')),
            ],
            options={
                'verbose_name': 'Genre.verbose_name',
                'verbose_name_plural': 'Genre.verbose_name_plural',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='GenreFilmWork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUIDMixin.ID.help_text', primary_key=True, serialize=False, verbose_name='UUIDMixin.ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='GenreFilmWork.created.help_text', verbose_name='GenreFilmWork.created')),
            ],
            options={
                'verbose_name': 'GenreFilmWork.verbose_name',
                'verbose_name_plural': 'GenreFilmWork.verbose_name_plural',
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, help_text='TimeStampedMixin.created.help_text', verbose_name='TimeStampedMixin.created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='TimeStampedMixin.modified.help_text', verbose_name='TimeStampedMixin.modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUIDMixin.ID.help_text', primary_key=True, serialize=False, verbose_name='UUIDMixin.ID')),
                ('full_name', models.CharField(help_text='Person.full_name.help_text', max_length=128, verbose_name='Person.full_name')),
            ],
            options={
                'verbose_name': 'Person.verbose_name',
                'verbose_name_plural': 'Person.verbose_name_plural',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmWork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUIDMixin.ID.help_text', primary_key=True, serialize=False, verbose_name='UUIDMixin.ID')),
                ('role', models.CharField(help_text='PersonFilmWork.role.help_text', max_length=256, verbose_name='PersonFilmWork.role')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='PersonFilmWork.created.help_text', verbose_name='PersonFilmWork.created')),
                ('film_work', models.ForeignKey(help_text='PersonFilmWork.film_work.help_text', on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork', verbose_name='PersonFilmWork.film_work')),
                ('person', models.ForeignKey(help_text='PersonFilmWork.person.help_text', on_delete=django.db.models.deletion.CASCADE, to='movies.person', verbose_name='PersonFilmWork.person')),
            ],
            options={
                'verbose_name': 'PersonFilmWork.verbose_name',
                'verbose_name_plural': 'PersonFilmWork.verbose_name_plural',
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['full_name'], name='person_full_name_idx'),
        ),
        migrations.AddField(
            model_name='genrefilmwork',
            name='film_work',
            field=models.ForeignKey(help_text='GenreFilmWork.film_work.help_text', on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork', verbose_name='GenreFilmWork.film_work'),
        ),
        migrations.AddField(
            model_name='genrefilmwork',
            name='genre',
            field=models.ForeignKey(help_text='GenreFilmWork.genre.help_text', on_delete=django.db.models.deletion.CASCADE, to='movies.genre', verbose_name='GenreFilmWork.genre'),
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['name'], name='genre_name_idx'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(help_text='Filmwork.genres.help_text', through='movies.GenreFilmWork', to='movies.Genre', verbose_name='Filmwork.genres'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(help_text='Filmwork.persons.help_text', through='movies.PersonFilmWork', to='movies.Person', verbose_name='Filmwork.persons'),
        ),
        migrations.AddConstraint(
            model_name='personfilmwork',
            constraint=models.UniqueConstraint(fields=('film_work', 'person', 'role'), name='person_film_work_person_idx'),
        ),
        migrations.AddConstraint(
            model_name='genrefilmwork',
            constraint=models.UniqueConstraint(fields=('film_work', 'genre'), name='genre_film_work_film_work_idx'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['title'], name='film_work_title_idx'),
        ),
    ]
