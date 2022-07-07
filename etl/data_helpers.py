from uuid import UUID
from pydantic import BaseModel, Field, root_validator


class PersonData(BaseModel):
    person_id: UUID
    person_name: str
    person_role: str


class FilmworkData(BaseModel):
    id: UUID
    rating: float = Field(alias='imdb_rating', default=0.0)
    genres: list[str]
    title: str
    description: str | None
    persons: list[PersonData]

    @root_validator
    @classmethod
    def compute_persons(cls, values: dict) -> dict:
        if 'persons' in values:
            persons = values.get('persons', [])

            director_names = [p.person_name for p in persons if p.person_role == 'director']
            values['director'] = ', '.join(director_names)

            writers = [p for p in persons if p.person_role == 'writer']
            values['writers_names'] = ', '.join([a.person_name for a in writers])
            values['writers'] = [{'id': w.person_id, 'name': w.person_name} for w in writers]

            actors = [p for p in persons if p.person_role == 'actor']
            values['actors_names'] = ', '.join([a.person_name for a in actors])
            values['actors'] = [{'id': a.person_id, 'name': a.person_name} for a in actors]
        if 'genres' in values:
            values['genre'] = ', '.join(values.get('genres', []))
        return values
