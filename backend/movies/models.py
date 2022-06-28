from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin


class Genre(TimeStampedMixin, UUIDMixin):
    """Film work genre."""
    name = models.CharField(
        verbose_name=_('Genre.title'),
        help_text=_('Genre.title.help_text'),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_('Genre.description'),
        help_text=_('Genre.description.help_text'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.name[:17]}...' if len(self.name) > 20 else self.name

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _('Genre.verbose_name')
        verbose_name_plural = _('Genre.verbose_name_plural')
        indexes = [models.Index(
            name='genre_name_idx',
            fields=['name'],
        )]


class Person(TimeStampedMixin, UUIDMixin):
    """Person."""
    full_name = models.CharField(
        verbose_name=_('Person.full_name'),
        help_text=_('Person.full_name.help_text'),
        max_length=128,
    )

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'content"."person'
        verbose_name = _('Person.verbose_name')
        verbose_name_plural = _('Person.verbose_name_plural')
        indexes = [models.Index(
            name='person_full_name_idx',
            fields=['full_name'],
        )]


class FilmWork(TimeStampedMixin, UUIDMixin):
    """Film work."""

    class FilmWorkTypes(models.TextChoices):
        MOVIE = ('movie', _('FilmWorkTypes.MOVIE'))
        TV_SHOW = ('tv', _('FilmWorkTypes.Tv_SHOW'))

    title = models.CharField(
        verbose_name=_('Filmwork.title'),
        help_text=_('Filmwork.title.help_text'),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_('Filmwork.description'),
        help_text=_('Filmwork.description.help_text'),
        blank=True,
        null=True,
    )
    creation_date = models.DateField(
        verbose_name=_('Filmwork.creation_date'),
        help_text=_('Filmwork.creation_date.help_text'),
        blank=True,
        null=True,
    )
    rating = models.FloatField(
        verbose_name=_('Filmwork.rating'),
        help_text=_('Filmwork.rating.help_text'),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        blank=True,
        null=True,
    )
    type = models.CharField(
        verbose_name=_('Filmwork.type'),
        help_text=_('Filmwork.type.help_text'),
        max_length=16,
        choices=FilmWorkTypes.choices,
        default=FilmWorkTypes.MOVIE,
    )
    genres = models.ManyToManyField(
        verbose_name=_('Filmwork.genres'),
        help_text=_('Filmwork.genres.help_text'),
        to=Genre,
        through='GenreFilmWork',
    )
    persons = models.ManyToManyField(
        verbose_name=_('Filmwork.persons'),
        help_text=_('Filmwork.persons.help_text'),
        to=Person,
        through='PersonFilmWork',
    )

    def __str__(self):
        return f'{self.title[:17]}...' if len(self.title) > 20 else self.title

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _('FilmWork.verbose_name')
        verbose_name_plural = _('FilmWork.verbose_name_plural')
        indexes = [
            models.Index(
                name='film_work_title_idx',
                fields=['title']
            ),
        ]


class GenreFilmWork(UUIDMixin):
    """Genre-Filmwork: many-to-many auxiliary model."""

    film_work = models.ForeignKey(
        verbose_name=_('GenreFilmWork.film_work'),
        help_text=_('GenreFilmWork.film_work.help_text'),
        to='FilmWork',
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        verbose_name=_('GenreFilmWork.genre'),
        help_text=_('GenreFilmWork.genre.help_text'),
        to='Genre',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        verbose_name=_('GenreFilmWork.created'),
        help_text=_('GenreFilmWork.created.help_text'),
        auto_now_add=True,
    )

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _('GenreFilmWork.verbose_name')
        verbose_name_plural = _('GenreFilmWork.verbose_name_plural')
        constraints = [models.UniqueConstraint(
            name='genre_film_work_film_work_idx',
            fields=['film_work', 'genre'],
        )]

    def __str__(self):
        return f'{self.film_work} - {self.genre}'

    def __repr__(self):
        return self.__str__()


class PersonFilmWork(UUIDMixin):
    """Person-Filmwork: many-to-many auxiliary model."""

    class RoleChoices(models.TextChoices):
        ACTOR = ('actor', _('RoleChoices.ACTOR'))
        DIRECTOR = ('director', _('RoleChoices.DIRECTOR'))
        WRITER = ('writer', _('RoleChoices.WRITER'))

    film_work = models.ForeignKey(
        verbose_name=_('PersonFilmWork.film_work'),
        help_text=_('PersonFilmWork.film_work.help_text'),
        to='FilmWork',
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        verbose_name=_('PersonFilmWork.person'),
        help_text=_('PersonFilmWork.person.help_text'),
        to='Person',
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        verbose_name=_('PersonFilmWork.role'),
        help_text=_('PersonFilmWork.role.help_text'),
        choices=RoleChoices.choices,
        default=RoleChoices.ACTOR,
        max_length=16,
    )
    created = models.DateTimeField(
        verbose_name=_('PersonFilmWork.created'),
        help_text=_('PersonFilmWork.created.help_text'),
        auto_now_add=True,
    )

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _('PersonFilmWork.verbose_name')
        verbose_name_plural = _('PersonFilmWork.verbose_name_plural')
        constraints = [
            models.UniqueConstraint(
                name='person_film_work_person_idx',
                fields=['film_work', 'person', 'role'],
            )
        ]

    def __str__(self):
        return f'{self.film_work} - {self.person}'

    def __repr__(self):
        return self.__str__()
