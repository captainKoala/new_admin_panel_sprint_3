from dataclasses import dataclass, field
import uuid


@dataclass
class FilmworkData:
    title: str
    description: str
    creation_date: str  # ToDo: maybe datetime ???
    type: str  # ToDo: maybe ENUM ???
    created: str  # ToDo: maybe datetime ???
    modified: str  # ToDo: maybe datetime ???
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    rating: float = field(default=0.0)


@dataclass
class GenreData:
    name: str
    description: str
    created: str  # ToDo: maybe datetime ???
    modified: str  # ToDo: maybe datetime ???
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmworkData:
    film_work_id: uuid
    genre_id: uuid
    created: str  # ToDo: maybe datetime ???
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmworkData:
    film_work_id: uuid
    person_id: uuid
    role: str
    created: str  # ToDo: maybe datetime ???
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonData:
    full_name: str
    created: str  # ToDo: maybe datetime ???
    modified: str  # ToDo: maybe datetime ???
    id: uuid.UUID = field(default_factory=uuid.uuid4)