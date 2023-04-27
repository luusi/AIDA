from abc import ABC, abstractmethod
import copy
from typing import Optional, Dict

from aida.services import Service
from aida.custom_types import State


class AbstractServiceWrapper(ABC):

    def __init__(self, service: Service):
        self._service = service
        self.reset()

    @abstractmethod
    def update(self, starting_state: State, action_name: str):
        """Update service."""

    def reset(self):
        self._current_transition_function = copy.deepcopy(self._service.transition_function)
        self._current_state = self._service.initial_state

    @property
    def service(self):
        return self._service

    @property
    def current_transition_function(self):
        return copy.deepcopy(self._current_transition_function)

    @property
    def current_state(self):
        return self._current_state

    @property
    def states(self):
        return self._service.states

    @property
    def actions(self):
        return self._service.actions

    @property
    def final_states(self):
        return self._service.final_states

    @property
    def initial_state(self):
        return self._service.initial_state

    @property
    def transition_function(self):
        """Make wrapper look like the underlying service, except for the property "transition function"."""
        return self.current_transition_function


def initialize_wrapper(service: Service, current_state: Optional[State] = None, current_transition_function: Optional[Dict] = None) -> AbstractServiceWrapper:
    """
    Instantiate abstract service wrapper according to service type.

    Try to wrap the service as "breakable" and, if failed, use normal service wrapper.
    """
#    try:
#        wrapper = BreakableServiceWrapper(service)
#    except AssertionError:
    wrapper = NormalServiceWrapper(service)
    if current_state is not None:
        wrapper._current_state = current_state
    if current_transition_function is not None:
        wrapper._current_transition_function = current_transition_function
    return wrapper


class NormalServiceWrapper(AbstractServiceWrapper):

    def update(self, starting_state: State, action_name: str):
        """Do nothing."""