class BaseAC(object):

    def format_filters(self, filters={}):
        return {'filters[{}]'.format(key): value for key, value in filters.items()}

    def format_ordering(self, ordering={}):
        return {'orders[{}]'.format(key): value for key, value in ordering.items()}
