from .element import Element


from collections.abc import Callable

class Event(Element):
    def __init__(self, action: Callable, condition: Callable, activations_limit: int = -1, termination_condition: Callable = None):
        """
        action: Callable. The action to be done when the condition is satisfied.
        condition: Callable. The condition for the action to be executed.
        activations_limit: int. Amount of times this event will be called. A negative value means the event will be active indefinitely.
        An example:
        
        button = Button(...)
        Event(action=lambda: print('Hello!'), condition=lambda: button.pressed))

        This will print the worlds 'Hello!' when the button is pressed
        """
        super().__init__()

        self.condition = condition
        self.action = action
        self.activations_limit = activations_limit
        self.termination_condition = termination_condition


    @property
    def inactive(self):
        return self.activations_limit == 0  # if negative, the event is permanent

    def update(self):
        if self.termination_condition and self.termination_condition():
            self.activations_limit = 0
        if self.activations_limit != 0 and self.condition():
            self.action()
            self.activations_limit -= 1 if self.activations_limit > 0 else 0 # gotta make it work for -1

