import os
import json
from electus import LibraryDefinition
from .combinations import WeightedFilter, Sequence, Join


class Library(object):
    """Initializes a library of features.

    :param lib_file: Path to a library configuration file.
    :type lib_file: str

    :ivar library: A list of initialized :class:`~electus.library.LibraryDefinition` objects.
    :type library: list
    """

    def __init__(self, lib_file=os.path.join(os.getcwd(), 'library.json')):

        self.library_config = lib_file
        self.library = [LibraryDefinition(name, self.library_config[name]) for name in self.library_config]

    @property
    def library_config(self):
        """The loaded library configuration dictionary as a dictionary."""
        return self._library_config

    @library_config.setter
    def library_config(self, lib):
        if isinstance(lib, dict):
            self._library_config = lib

        elif os.path.exists(lib):
            with open(lib, 'r') as f:
                self._library_config = json.load(f)
        else:
            raise IOError('Library file {} could not be found'.format(lib))


class Job(object):
    """ A collection of features look for.

    :param name: A unique name to describe the collection of features.
    :type name: str    
    :param job_config: A list of job configuration dictionaries.
    :type job_config: list        
    :param library: A list of initialized :class:`~electus.library.LibraryDefinition` objects.
    :type library: list

    :var valid_jobs: A list of supported job types.
    """

    valid_jobs = ['filter', 'sequence', 'join']

    def __init__(self, name, job_config, library):

        self.name = name
        self.job_type = job_config
        self.library = library

        self.features = job_config

        self.combination_engine = job_config


    @property
    def name(self):
        """A unique name to describe the collection of features."""
        return self._name

    @name.setter
    def name(self, n):
        if n and isinstance(n, str):
            self._name = n
        else:
            raise ValueError('Name must be a non-empty string')

    @property
    def job_type(self):
        """How the features should be combined. Valid options are sequence, join, and filter."""
        return self._job_type

    @job_type.setter
    def job_type(self, job_conf):
        if 'type' in job_conf:
            jt = job_conf['type'].lower()
            if jt not in self.valid_jobs:
                raise ValueError('Job type {} not in {}'.format(jt, self.valid_jobs))
            else:
                self._job_type = jt
        else:
            raise ValueError('Job config must have a "type" key')

    @property
    def library(self):
        """The library as specified by the library configuration file."""
        return self._library

    @library.setter
    def library(self, lib):
        for definition in lib:
            if not isinstance(definition, LibraryDefinition):
                raise ValueError('Library must be a list of LibraryDefinitions objects')
        self._library = lib

    @property
    def features(self):
        """A list of features specified in the library."""
        return self._features

    @features.setter
    def features(self, job_conf):
        if 'features' in job_conf:

            feature_list = job_conf['features']
            if not isinstance(feature_list, list):
                raise ValueError("Value of features must be a list of names of features defined in the library")

            lib_names = [x.name for x in self.library]
            lib_objs = []
            for feat in feature_list:
                try:
                    feat_idx = lib_names.index(feat)
                    lib_objs.append(self.library[feat_idx])
                except ValueError:
                    raise ValueError('Feature {} not found in library'.format(feat))
            self._features = lib_objs
        else:
            raise ValueError('Job config must have a "features" key')

    @property
    def combination_engine(self):
        """The function used to combine the list of features."""
        return self._combination_engine

    @combination_engine.setter
    def combination_engine(self, job_conf):
        if self.job_type == 'filter':
            if 'threshold' in job_conf:
                self._combination_engine = WeightedFilter(self.name, self.features, job_conf['threshold'])
            else:
                self._combination_engine = WeightedFilter(self.name, self.features)
        elif self.job_type == 'sequence':
            if 'sequence' not in job_conf:
                raise ValueError('Sequence jobs must have a "sequence" key. This is an ordered list of desired features')
            if 'time_window' not in job_conf:
                raise ValueError('Sequence jobs must have a "time_window" key. This is the maximum amount of time (in seconds) in which the sequence can occur')

            seq = job_conf['sequence']
            time_window = job_conf['time_window']

            self._combination_engine = Sequence(self.name, self.features, event_names=seq, time_window=time_window)

        elif self.job_type == 'join':
            if 'join_expression' not in job_conf:
                raise ValueError('Join jobs must have a "join_expression" key. This is a logical expression stating how to join the indicators')

            join_expr = job_conf['join_expression']
            self._combination_engine = Join(self.name, self.features, join_expr)


