from pythomata import SimpleDFA


class TargetSimulatorDFA:
    """Simulate a target DFA."""

    def __init__(self, target: SimpleDFA):
        """Initialize the simulator."""
        self.target = target

        self._current_state = self.target.initial_state

    @property
    def current_state(self):
        return self._current_state

    def reset(self):
        """Reset the target to its initial state."""
        self._current_state = self.target.initial_state

    def update_state(self, action) -> None:
        """Update the state given an action."""
        transitions_from_state = self.target.transition_function[self._current_state]
        next_state = transitions_from_state[action]
        self._current_state = next_state