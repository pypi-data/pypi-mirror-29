import itertools
from datetime import timedelta
from dateutil.parser import parse
from operator import itemgetter
import boolean

from electus import LibraryDefinition
from .alert import Hit, Alert

class Join(object):
    """ Alert if a combination of events occurs."""

    def __init__(self, name, definitions, join_expression):
        self.name = name
        self.definitions = definitions
        self.join_expression = join_expression
        try:
            self._subsets = self.parse_join_logic(self.join_expression)
        except boolean.ParseError:
            raise ValueError("Could not parse join logic for {}".format(self.name))

    @property
    def name(self):
        """Name of the join job passed in from the configuration."""
        return self._name

    @name.setter
    def name(self, n):
        if isinstance(n, str):
            self._name = n
        else:
            raise ValueError('Name must be a string')

    @property
    def definitions(self):
        """A list of :class:`~electus.library.LibraryDefinition` objects."""
        return self._definitions

    @definitions.setter
    def definitions(self, d):
        if isinstance(d, list):
            for definition in d:
                if not isinstance(definition, LibraryDefinition):
                    raise ValueError('Definitions must be a list of LibraryDefinitions objects')

            self._definitions = d
        else:
            raise ValueError('Definitions must be a list of LibraryDefinitions objects')

    @property
    def join_expression(self):
        """A logical expression to determine combinations of indicators."""
        return self._join_expression

    @join_expression.setter
    def join_expression(self, expr):
        if isinstance(expr, str):
            self._join_expression = expr
        else:
            raise ValueError('Join expression must be a string')

    @staticmethod
    def parse_join_logic(expression):
        """Parse an expression with boolean logic and return all possible subsets.

        :param: expression: A boolean logic expression
        :type expression: str
    
        :returns: The list of possible subsets from the boolean expression.
        :rtype: list

        >>> parse_join_logic('(( A and ( B or C ) ))')
        [("A", "B"), ("A", "C")]

        .. warning::
            Tokens in the expression can only consist of alphanumeric characters and underscores. Tokens cannot start with
            a number.

        """

        algebra = boolean.BooleanAlgebra()
        TRUE, FALSE, NOT, AND, OR, symbol = algebra.definition()

        parsed = algebra.parse(expression)

        symbols = parsed.get_symbols()
        # Get all possible combinations of symbols
        mappings = (dict(zip(symbols, values)) for values in itertools.product([FALSE, TRUE], repeat=len(symbols)))

        # Only take the valid solutions
        solutions = []
        for m in mappings:
            if parsed.subs(m, simplify=True):
                solutions.append([k.obj for k,v in m.items() if v == TRUE])

        # Only take the minimum amount of subsets
        # E.g. [[A, B, C], [A, B], [A, C]] should reduce to [[A, B], [A, C]]
        all_subsets = sorted(s1 for s1 in solutions if not any(set(s1) > set(s2) for s2 in solutions))
        # Remove duplicates
        all_subsets = [list(x) for x in set(tuple(x) for x in all_subsets)]

        return all_subsets

    def check_subset(self, hit_names):
        """Check if a subset specified by join_expression is a subset of all hits.

        :param hit_names: List of names of all of the features that have hit.
        :type hit_names: list

        :return: True if a set specified by join_expression is a subset of hit_names. False otherwise.
        """
        for s in self._subsets:
            if set(s) <= set(hit_names):
                return True

        return False

    def alert(self, events):
        """Alert if a combination of events (as specified by join_expression) occurs.

        :param events: A list of events in chronological order.
        :type events: list

        :return: An Alert object if a valid combination occurs in the sequence of events.
        :rtype: :class:`~electus.alert.Alert`
        """

        if events is None:
            return None

        hits = []
        for idx, event in enumerate(reversed(events)):

            for definition in self.definitions:
                # Check if the indicators match
                if definition.eval_indicators(event):
                    hit = Hit(name=definition.name, event=event)
                    hits.append(hit)

            if idx == 0:
                # If the latest event does not create a hit then exit
                if not hits:
                    break

        hit_names = [h.name for h in hits]
        if self.check_subset(hit_names):
            return Alert(name=self.name, hits=hits)


class WeightedFilter(object):
    """Alert if the sum of the weights is above the given threshold."""
    def __init__(self, name, definitions, threshold=10.0):
        
        self.name = name
        self.definitions = definitions
        self.threshold = threshold

    @property
    def name(self):
        """Name of the filter job passed in from the configuration."""
        return self._name

    @name.setter
    def name(self, n):
        if isinstance(n, str):
            self._name = n
        else:
            raise ValueError('Name must be a string')

    @property
    def definitions(self):
        """A list of :class:`~electus.library.LibraryDefinition` objects."""
        return self._definitions

    @definitions.setter
    def definitions(self, d):
        if isinstance(d, LibraryDefinition):
            d = [d]

        if isinstance(d, list):
            for definition in d:
                if not isinstance(definition, LibraryDefinition):
                    raise ValueError('Definitions must be a list of LibraryDefinitions objects')

            self._definitions = d
        else:
            raise ValueError('Definitions must be a list of LibraryDefinitions objects')

    @property
    def threshold(self):
        """Threshold for the sum of feature scores."""
        return self._threshold

    @threshold.setter
    def threshold(self, t):

        if isinstance(t, int) or isinstance(t, float):
            self._threshold = t
        else:
            raise ValueError('Weight must be a number')

    def get_score(self, event):
        """Calculate the total score for an event.

        :param event: An event.
        :type event: dict

        :returns: The total score for that event and a list of :class:`~electus.alert.Hit` objects.
        :rtype: float, list
        """
        score = 0
        hits = []
        for definition in self.definitions:
            if definition.eval_indicators(event):
                hit = Hit(name=definition.name, event=event)
                hits.append(hit)
                score += definition.weight

        return score, hits

    def alert(self, events, fetch_all_events=False):
        """Alert if the total score is above the threshold and the latest event contributed to that score

        :param events: A list of events in chronological order.
        :type events: list

        :param fetch_all_events: If true then calculate the score for all events. If false stop when the threshold is passed.
        :type fetch_all_events: bool

        :returns: If the threshold is passed then return an Alert with events that contributed to the score.
        :rtype: :class:`~electus.alert.Alert`
        """
        total_score = 0
        hits = []

        for idx, event in enumerate(reversed(events)):
            score, event_hits = self.get_score(event)
            total_score += score
            if score > 0:
                hits.extend(event_hits)

            # If the latest event does not contribute to the score then exit
            if (idx == 0) and (score == 0):
                break

            if (fetch_all_events is False) and (total_score >= self.threshold):
                return Alert(self.name, hits=hits, total_score=total_score)

        if total_score >= self.threshold:
            return Alert(self.name, hits=hits, total_score=total_score)
        else:
            return None


class Sequence(object):
    """Alert if the sequence of events occurs in the specified time period"""
    def __init__(self, name, definitions, event_names, time_window):
        self.name = name
        self.definitions = definitions
        self.event_names = event_names
        self.time_window = time_window

    @property
    def name(self):
        """Name of the sequence job passed in from the configuration."""
        return self._name

    @name.setter
    def name(self, n):
        if isinstance(n, str):
            self._name = n
        else:
            raise ValueError('Name must be a string')

    @property
    def definitions(self):
        """A list of :class:`~electus.library.LibraryDefinition` objects."""
        return self._definitions

    @definitions.setter
    def definitions(self, d):
        if isinstance(d, list):
            for definition in d:
                if not isinstance(definition, LibraryDefinition):
                    raise ValueError('Definitions must be a list of LibraryDefinitions objects')

            self._definitions = d
        else:
            raise ValueError('Definitions must be a list of LibraryDefinitions objects')

    @property
    def event_names(self):
        """The ordered list of event names to look for."""
        return self._event_names

    @event_names.setter
    def event_names(self, names):
        if isinstance(names, str):
            names = [names]

        if isinstance(names, list):
            for name in names:
                if not isinstance(name, str):
                    raise ValueError('Event names must be a list of strings')

            self._event_names = names
        else:
            raise ValueError('Event names must be a list of strings')

    @property
    def time_window(self):
        """The number of seconds to look back from the latest event."""
        return self._time_window

    @time_window.setter
    def time_window(self, t):

        if isinstance(t, int) or isinstance(t, float):
            self._time_window = t
        else:
            raise ValueError('Time_window must be the size of the time window in seconds (as int or float)')

    def check_subsequence_match(self, hits):
        """Check if the all event_names are in the list of hit names."""
        # Sort by time
        sorted_hits = sorted(hits, key=itemgetter(1))
        hit_names = [x.name for x, y in sorted_hits]

        name_iter = iter(hit_names)
        return all(n in name_iter for n in self.event_names)

    def alert(self, events):
        """Alert if the sequence of events occurs in the specified time period.

        :param events: A list of events in chronological order
        :type events: list

        :returns: An Alert object with the list of hits if the sequence is found.
        :rtype: :class:`~electus.alert.Alert`
        """

        if events is None:
            return None

        hits = []
        event_info_list = []
        for idx, event in enumerate(reversed(events)):
            timestamps = []
            event_info = None

            for definition in self.definitions:
                # Want to find a timestamp to check if it is in the specified time range
                if definition.dt_field in event:
                    timestamps.append(parse(event[definition.dt_field]))

                # Check if the indicators match
                if definition.eval_indicators(event):
                    event_info = (definition, parse(event[definition.dt_field]))
                    hits.append(Hit(name=definition.name, event=event))
            try:
                ts = max(timestamps)
            except ValueError:
                ts = None

            if idx == 0:
                end_time = ts
                start_time = ts - timedelta(seconds=self.time_window)
                # If the latest event does not create a hit then exit
                if not event_info:
                    break
            # Check if the event is within the given time window
            if ts is not None:

                if start_time <= ts <= end_time:
                    if event_info:
                        event_info_list.append(event_info)
                else:
                    break

        if self.check_subsequence_match(event_info_list):
            return Alert(name=self.name, hits=hits)