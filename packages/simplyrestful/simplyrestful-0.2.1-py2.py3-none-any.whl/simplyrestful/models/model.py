from simplyrestful.database import Base


class Model(Base):
    __abstract__ = True

    @property
    def relationships(self):
        return {
            relationship.local_remote_pairs[0][0].name: relationship.key
            for relationship in self.__mapper__.relationships
        }

    @property
    def relationship_classes(self):
        return [
            getattr(self.__class__, t).property.mapper.class_
            for f, t in self.relationships.iteritems()
        ]

    @property
    def primary_keys(self):
        return [c.name for c in self.__mapper__.primary_key]

    @property
    def columns(self):
        return [c.name for c in self.model.__table__.columns]
