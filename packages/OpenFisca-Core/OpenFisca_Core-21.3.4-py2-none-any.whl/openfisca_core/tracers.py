# -*- coding: utf-8 -*-

import logging
import copy
from collections import defaultdict

log = logging.getLogger(__name__)


class Tracer(object):
    """
        A tracer that records simulation steps to enable exploring calculation steps in details.

        .. py:attribute:: requested_calculations

            ``set`` containing calculations that have been directly requested by the client.

            Value example:

            >>> {'income_tax<2017-01>', 'basic_income<2017-01>'}

        .. py:attribute:: stack

            ``list`` of the calculations that have started, but have not finished. The first item is one of the :attr:`requested_calculations`, and each other item is a dependency of the one preceding him. Note that after a calculation is finished, :attr:`stack` is always ``[]``.

            Value example:

            >>> ['income_tax<2017-01>', 'global_income<2017-01>', 'salary<2017-01>']

        .. py:attribute:: trace

            ``dict`` containing, for each calculation, its result and its immediate dependencies.

            Value example:

            .. code-block:: python

              {
                'income_tax<2017-01': {
                  'dependencies':['global_income<2017-01>', 'nb_children<2017-01>']
                  'value': 600
                  },
                'global_income<2017-01>': {...}
              }

        .. py:attribute:: usage_stats

            ``dict`` containing, for each variable computed, the number of times the variable was requested.

            Value example:

            .. code-block:: python

              {
                'salary': {
                  'nb_requests': 17
                  },
                'global_income': {
                  'nb_requests': 1
                  }
              }

    """
    def __init__(self):
        log.warn("The tracer is a feature that is still currently under experimentation. You are very welcome to use it and send us precious feedback, but keep in mind that the way it is used and the results it gives might change without any major version bump.")
        self.requested_calculations = set()
        self.stack = []
        self.trace = {}
        self.usage_stats = defaultdict(lambda: {"nb_requests": 0})
        self._computation_log = []

    def clone(self):
        new = Tracer()
        new.requested_calculations = copy.copy(self.requested_calculations)
        new.stack = copy.copy(self.stack)
        new.trace = copy.deepcopy(self.trace)
        new._computation_log = copy.copy(self._computation_log)
        new.usage_stats = copy.deepcopy(self.usage_stats)
        return new

    @staticmethod
    def _get_key(variable_name, period, **parameters):
        if parameters.get('extra_params'):
            return u"{}<{}><{}>".format(variable_name, period, '><'.join(map(str, parameters['extra_params']))).encode('utf-8')
        return u"{}<{}>".format(variable_name, period).encode('utf-8')

    def record_calculation_start(self, variable_name, period, **parameters):
        """
            Record that OpenFisca started computing a variable.

            :param str variable_name: Name of the variable starting to be computed
            :param Period period: Period for which the variable is being computed
            :param list parameters: Parameter with which the variable is being computed
        """
        key = self._get_key(variable_name, period, **parameters)

        if self.stack:  # The variable is a dependency of another variable
            parent = self.stack[-1]
            self.trace[parent]['dependencies'].append(key)
        else:  # The variable has been requested by the client
            self.requested_calculations.add(key)

        if not self.trace.get(key):
            self.trace[key] = {'dependencies': []}
        self.stack.append(key)
        self._computation_log.append((key, len(self.stack)))
        self.usage_stats[variable_name]['nb_requests'] += 1

    def record_calculation_end(self, variable_name, period, result, **parameters):
        """
            Record that OpenFisca finished computing a variable.

            :param str variable_name: Name of the variable starting to be computed
            :param Period period: Period for which the variable is being computed
            :param numpy.ndarray result: Result of the computation
            :param list parameters: Parameter with which the variable is being computed
        """
        key = self._get_key(variable_name, period, **parameters)
        expected_key = self.stack.pop()

        if not key == expected_key:
            raise ValueError(
                u"Something went wrong with the simulation tracer: result of '{0}' was expected, got results for '{1}' instead. This does not make sense as the last variable we started computing was '{0}'."
                .format(expected_key, key).encode('utf-8')
                )
        self.trace[key]['value'] = result

    def record_calculation_abortion(self, variable_name, period, **parameters):
        """
            Record that OpenFisca aborted computing a variable. This removes all trace of this computation.

            :param str variable_name: Name of the variable starting to be computed
            :param Period period: Period for which the variable is being computed
            :param list parameters: Parameter with which the variable is being computed
        """
        key = self._get_key(variable_name, period, **parameters)
        expected_key = self.stack.pop()

        if not key == expected_key:
            raise ValueError(
                u"Something went wrong with the simulation tracer: calculation of '{1}' was aborted, whereas the last variable we started computing was '{0}'."
                .format(expected_key, key).encode('utf-8')
                )

        if self.stack:
            parent = self.stack[-1]
            self.trace[parent]['dependencies'].remove(key)
        del self.trace[key]

    def print_computation_log(self, aggregate = False):
        """
            Print the computation log of a simulation.

            If ``aggregate`` is ``False`` (default), print the value of each computed vector.

            If ``aggregate`` is ``True``, only print the minimum, maximum, and average value of each computed vector.
            This mode is more suited for simulations on a large population.
        """
        for node, depth in self._computation_log:
            if not self.trace.get(node):
                value = "Calculation aborted due to a circular dependency"
            else:
                value = self.trace[node]['value']
                if aggregate:
                    try:
                        avg = sum(value) / len(value)
                    except TypeError:
                        avg = None
                    value = {
                        'min': min(value),
                        'max': max(value),
                        'avg': avg,
                        }
            print("{}{} >> {}".format('  ' * depth, node, value))
