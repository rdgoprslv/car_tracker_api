from ..models import mapper_registry
from ..meta import engine


def create_db():
    mapper_registry.metadata.create_all(engine)
