from cement import Controller, ex

class Tasks(Controller):
    class Meta:
        label = "task"
        stacked_type = "nested"
        stacked_on = "base"
