from sqlalchemy import and_

from settings import settings


class Filter(object):

    map = {
        'eq': '__eq__',
        'gt': '__gt__', 'ge': '__ge__',
        'lt': '__lt__', 'le': '__le__',
        'in': 'in_', 'notin': 'notin_',
        'like': 'like', 'notlike': 'notlike',
        'ilike': 'ilike', 'notilike': 'notilike',
        'is': 'is_', 'isnot': 'isnot',
        'intersects': 'ST_Intersects',
        'contains': 'ST_Intersects'
    }

    multiple = ['in', 'notin']  # TODO: Implement Between filter

    def __init__(self, model, filters):
        self.model = model
        self.filters = filters

        self._orm_filters = []
        self.joins = []
        self.order_by = []

        size = int(self.filters.pop('limit', settings['DEFAULT_PAGE_SIZE']))

        self.limit = settings['MAX_PAGE_SIZE'] if size > settings['MAX_PAGE_SIZE'] else size
        self.offset = int(self.filters.pop('offset', 0))

        self._translate_order()
        self._translate_filters()

    @property
    def orm_filters(self):
        return and_(*self._orm_filters)

    def _translate_filters(self):
        for f, value in self.filters.iteritems():
            split = f.split('__')

            last = split[-1]

            op = split.pop() if last in self.map else 'eq'

            column_name = split.pop()

            model = self.model
            for nested in split:
                model = getattr(model, nested).mapper.class_
                if model not in self.joins:
                    self.joins.append(model)

            if op in self.multiple:
                value = value.split(';')
                if not value[-1]:
                    value.pop()

            self._orm_filters.append(
                getattr(
                    getattr(model, column_name),
                    self.map[op]
                )(value)
            )

    def _translate_order(self):
        ops = ['asc', 'desc']
        order = self.filters.pop('order_by', None)
        orders = order.split(';') if order else []
        for order in orders:
            split = order.split('__')
            last = split[-1]

            op = split.pop() if last in ops else 'asc'

            column_name = split.pop()

            model = self.model
            for nested in split:
                model = getattr(model, nested).mapper.class_
                self.joins.append(model)
            self.order_by.append(
                getattr(getattr(model, column_name), op)()
            )
