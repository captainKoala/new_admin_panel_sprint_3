from uuid import UUID
from pydantic import BaseModel, Field, root_validator, validator


class PersonData(BaseModel):
    person_id: UUID
    person_name: str
    person_role: str


class FilmworkData(BaseModel):
    id: UUID
    imdb_rating: float | None = Field(alias='rating', default=0.0)
    genre: list[str] = Field(alias='genres', default=[])
    title: str
    description: str | None
    persons: list[PersonData]

    @validator('imdb_rating')
    def set_imdb_rating(cls, imdb_rating):
        return imdb_rating or 0.0

    @root_validator
    @classmethod
    def compute_persons(cls, values: dict) -> dict:
        persons = values.get('persons', [])

        director_names = [p.person_name for p in persons if p.person_role == 'director']
        values['director'] = director_names

        writers = [p for p in persons if p.person_role == 'writer']
        values['writers_names'] = [a.person_name for a in writers]
        values['writers'] = [{'id': w.person_id, 'name': w.person_name} for w in writers]

        actors = [p for p in persons if p.person_role == 'actor']
        values['actors_names'] = ', '.join([a.person_name for a in actors])
        values['actors'] = [{'id': a.person_id, 'name': a.person_name} for a in actors]

        return values
