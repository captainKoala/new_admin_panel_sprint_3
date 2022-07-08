from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork, PersonFilmWork


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ('get', )

    def get_queryset(self):
        raise NotImplementedError('Please implement get_queryset method first!')

    def get_values(self):
        queryset = (
            self.get_queryset().values().annotate(
                genres=ArrayAgg('genres__name', distinct=True),
                actors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(persons__personfilmwork__role=PersonFilmWork.RoleChoices.ACTOR),
                    distinct=True
                ),
                directors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(persons__personfilmwork__role=PersonFilmWork.RoleChoices.DIRECTOR),
                    distinct=True
                ),
                writers=ArrayAgg(
                    'persons__full_name',
                    filter=Q(persons__personfilmwork__role=PersonFilmWork.RoleChoices.WRITER),
                    distinct=True
                ),
            ))
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    """Single Film work"""

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return self.model.objects.filter(pk=pk)

    def get_context_data(self, **kwargs):
        return dict(self.get_values()[0])


class MoviesListApi(MoviesApiMixin, BaseListView):
    """List of Film works"""

    paginate_by = 50

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        values = self.get_values()

        paginator, page, *_ = self.paginate_queryset(values, self.paginate_by)

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(page),
        }
        return context
