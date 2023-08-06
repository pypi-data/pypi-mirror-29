import json


class Hit(object):
    """Storage container for a hit on an indicator"""
    def __init__(self, name, event):
        self.name = name
        self.event = event

    @property
    def name(self):
        """The name of the library indicator that hit."""
        return self._name

    @name.setter
    def name(self, n):
        if isinstance(n, str):
            self._name = n
        else:
            raise ValueError('Name must be a string')

    @property
    def event(self):
        """The event that matched a library indicator."""
        return self._event

    @event.setter
    def event(self, e):
        if isinstance(e, dict):
            self._event = e
        else:
            raise ValueError('Event must be a dictionary')


class Alert(object):
    """Container for an alert"""

    def __init__(self, name, hits, total_score=None):
        self.name = name
        self.hits = hits
        self.total_score = total_score

    @property
    def name(self):
        """The name of the alert. This should be the same as the job name that hit."""
        return self._name

    @name.setter
    def name(self, n):
        if isinstance(n, str):
            self._name = n
        else:
            raise ValueError('Name must be a string')

    @property
    def hits(self):
        """A list of Hit objects."""
        return self._hits

    @hits.setter
    def hits(self, hit_list):
        for h in hit_list:
            if not isinstance(h, Hit):
                raise ValueError('Hits must be a list of Hit objects')
        self._hits = hit_list

    @property
    def total_score(self):
        """The total score from a filter job (if defined)."""
        return self._total_score

    @total_score.setter
    def total_score(self, ts):
        if isinstance(ts, int) or isinstance(ts, float) or ts is None:
            self._total_score = ts
        else:
            raise ValueError('Total score must be a number or None')

    def to_dict(self):
        """Convert the Alert object to a dictionary for parsing."""
        d = {self.name: {'total_score': self.total_score, 'hits': [{'indicator_name': h.name, 'event': h.event} for h in self.hits]}}
        return d

    def __len__(self):
        return len(self.hits)

    def __repr__(self):
        return '<Alert {}>'.format(self.to_dict())











