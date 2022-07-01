from datetime import datetime
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, root_validator


class PersonData(BaseModel):
    person_id: UUID
    person_name: str
    person_role: str


class FilmworkData(BaseModel):
    id: UUID
    rating: float = Field(alias='imdb_rating', default=0.0)
    genre: str
    title: str
    description: str
    persons: list[PersonData]

    @root_validator
    @classmethod
    def compute_persons(cls, values: dict) -> dict:
        if 'persons' in values:
            persons = values['persons']

            director_names = [p.person_name for p in persons if p.person_role == 'director']
            values['director'] = ', '.join(director_names)

            writers = [p for p in persons if p.person_role == 'writer']
            values['writers_names'] = ', '.join([a.person_name for a in writers])
            values['writers'] = writers

            actors = [p for p in persons if p.person_role == 'actor']
            values['actors_names'] = ', '.join([a.person_name for a in actors])
            values['actors'] = actors
        return values

# print(f1.json(exclude={'persons': True, 'actors': {'__all__': {'person_role'}}}))

    # creation_date: datetime | None
    # type: str
    # created: datetime
    # modified: datetime

#
# @dataclass
# class GenreData:
#     name: str
#     description: str
#     created: str  # ToDo: maybe datetime ???
#     modified: str  # ToDo: maybe datetime ???
#     id: uuid.UUID = field(default_factory=uuid.uuid4)
#
#
# @dataclass
# class GenreFilmworkData:
#     film_work_id: uuid
#     genre_id: uuid
#     created: str  # ToDo: maybe datetime ???
#     id: uuid.UUID = field(default_factory=uuid.uuid4)
#
#
# @dataclass
# class PersonFilmworkData:
#     film_work_id: uuid
#     person_id: uuid
#     role: str
#     created: str  # ToDo: maybe datetime ???
#     id: uuid.UUID = field(default_factory=uuid.uuid4)
#
#
# @dataclass
# class PersonData:
#     full_name: str
#     created: str  # ToDo: maybe datetime ???
#     modified: str  # ToDo: maybe datetime ???
#     id: uuid.UUID = field(default_factory=uuid.uuid4)