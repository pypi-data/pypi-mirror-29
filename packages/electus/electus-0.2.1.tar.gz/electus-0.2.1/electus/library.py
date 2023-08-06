import re


class LibraryDefinition(object):
    """Defines a set of indicators.

    :param name: A unique name for the feature.
    :type name: str
    :param definition: A dictionary that is used to configure the feature.
    :type definition: dict

    :ivar indicators: A list of :class:`Indicator` objects that describe what to look for in an event.
    :type indicators: list
    """
    
    def __init__(self, name, definition):
        self.name = name

        self.dt_field = definition
        self.weight = definition

        self.indicators = []
        for ind in definition['indicators']:
            if 'field' not in ind:
                raise ValueError(
                    'The indicators dictionary requires a "field" key. The keys given were: {}'.format(list(ind.keys())))
            if 'value' not in ind:
                raise ValueError(
                    'The indicators dictionary requires a "value" key. The keys given were: {}'.format(list(ind.keys())))

            self.indicators.append(Indicator(ind))

    @property
    def name(self):
        """The name of the feature."""
        return self._name

    @name.setter
    def name(self, n):
        if n and isinstance(n, str):
            if re.search(r'[^a-zA-Z0-9_.]+', n):
                raise ValueError("Name can only contain alphanumeric characters, underscores and periods. Name is: {}".format(n))
            if re.match(r'^\d', n):
                raise ValueError("Name cannot start with a number. The name is: {}".format(n))
            self._name = n
        else:
            raise ValueError('Name must be a non-empty string')

    @property
    def dt_field(self):
        """The name of the field in the event that specifies the time at which it occurred."""
        return self._dt_field

    @dt_field.setter
    def dt_field(self, d):
        if 'datetime_field' in d:
            dt = d['datetime_field']
            if dt and isinstance(dt, str):
                self._dt_field = dt
            else:
                raise ValueError('The value of datetime_field must be a string')
        else:
            raise ValueError(
                'The library definition dictionary requires a "datetime_field" key. The keys given were: {}'.format(list(d.keys())))

    @property
    def weight(self):
        """The score to assign if this feature matches an event."""
        return self._weight

    @weight.setter
    def weight(self, d):
        if 'weight' in d:
            w = d['weight']

            if isinstance(w, int) or isinstance(w, float):
                self._weight = w
            else:
                raise ValueError('Weight must be a number')
        else:
            self._weight = 5.0

    def eval_indicators(self, event):
        """Check if the event matches all of the indicators."""
        did_match = []

        for ind in self.indicators:
            if ind.field not in event:
                return False

            if ind.regex:
                # If the specified regex matches then count it as a hit
                if ind.value.match(event[ind.field]):
                    did_match.append(True)
                else:
                    did_match.append(False)
            elif not ind.case_sensitive and not ind.regex and event[ind.field].lower() == ind.value:
                if ind.match:
                    did_match.append(True)
                else:
                    did_match.append(False)
            elif event[ind.field] == ind.value:
                # Check whether or not matching is desired
                if ind.match:
                    did_match.append(True)
                else:
                    did_match.append(False)
            else:
                did_match.append(False)

        return all(did_match)


class Indicator(object):
    """Define an individual indicator
    
    :param ind: An individual indicator from the config.
    :type ind: dict
    """

    def __init__(self, ind):

        self.field = ind['field']
        self.value = ind['value']
        self.match = ind.get('match', True)
        self.regex = ind.get('is_regex', False)
        self.case_sensitive = ind.get('case_sensitive', True)

        # Precompile the regex for performance reasons
        if self.regex:
            if self.case_sensitive:
                self.value = re.compile(self.value.replace('\\', r'\\'))
            else:
                self.value = re.compile(self.value.replace('\\', r'\\'), flags=re.IGNORECASE)

        if self.case_sensitive is False and self.regex is False:
            self.value = self.value.lower()

    @property
    def field(self):
        """The key to look for in the event object."""
        return self._field

    @field.setter
    def field(self, f):
        if isinstance(f, str):
            self._field = f
        else:
            raise ValueError('Field must be a string')

    @property
    def value(self):
        """The value to match on in the event object."""
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    @property
    def match(self):
        """Whether or not to match that object."""
        return self._match

    @match.setter
    def match(self, m):
        if isinstance(m, bool):
            self._match = m
        else:
            raise ValueError('Match must be a boolean')

    @property
    def regex(self):
        """If the value is to be used is a regex (otherwise a straight comparison will be used)."""
        return self._regex

    @regex.setter
    def regex(self, r):
        if isinstance(r, bool):
            self._regex = r
        else:
            raise ValueError('Regex must be a boolean')

    @property
    def case_sensitive(self):
        """Whether or not to do case sensitive comparisons."""
        return self._case_sensitive

    @case_sensitive.setter
    def case_sensitive(self, c):
        if isinstance(c, bool):
            self._case_sensitive = c
        else:
            raise ValueError('Case sensitive must be a boolean')

    def __repr__(self):
        return "<Indicator field: {}, value: {}, match: {}, case_sensitive: {}, regex: {}>".format(self.field, self.value,
                                                                                             self.match, self.case_sensitive,
                                                                                             self.regex)
