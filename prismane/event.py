from .element import Element


from collections.abc import Callable

class Event(Element):
    def __init__(self, action: Callable, condition: Callable, activations_limit: int = -1):
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

    def update(self):
        if self.condition() and self.activations_limit != 0:
            self.action()
            self.activations_limit -= 1

