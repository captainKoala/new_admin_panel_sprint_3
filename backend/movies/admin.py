from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    autocomplete_fields = ('genre', )


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ('person', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', 'description', )
    ordering = ('name', 'description', )


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    list_display = ('title', 'creation_date', 'rating', 'get_genres', )
    list_filter = ('type', 'genres', )
    search_fields = ('title', 'description', )
    list_prefetch_related = ('genres', )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(*self.list_prefetch_related)

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = _('FilmWorkAdmin.get_genres')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name', )
    ordering = ('full_name', )
