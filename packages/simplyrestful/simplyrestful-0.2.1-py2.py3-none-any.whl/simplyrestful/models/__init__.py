from sqlalchemy.sql import ClauseElement
from geometry import Geometry
from model import Model
from simplyrestful.database import Base


def get_class_by_table_name(table_name):
  for c in Base._decl_class_registry.values():
    if hasattr(c, '__tablename__') and c.__tablename__ == table_name:
      return c


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True
