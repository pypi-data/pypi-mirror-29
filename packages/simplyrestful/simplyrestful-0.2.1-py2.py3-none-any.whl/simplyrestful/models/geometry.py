import json
from geoalchemy2 import Geometry as GeoAlchemyGeometry
import geoalchemy2.shape
from shapely.geometry import shape, mapping
import geojson


class Geometry(GeoAlchemyGeometry):
    def result_processor(self, dialect, coltype):
        super_proc = super(Geometry, self).result_processor(dialect, coltype)

        def process(v):
            return v and mapping(
                geoalchemy2.shape.to_shape(super_proc(v))
            )

        return process

    def bind_processor(self, dialect):
        super_proc = super(Geometry, self).bind_processor(dialect)

        def process(v):
            return super_proc(
                'SRID=%d;%s' % (self.srid, shape(geojson.loads(json.dumps(v))).wkt)
                if isinstance(v, dict) else v
            )

        return process
