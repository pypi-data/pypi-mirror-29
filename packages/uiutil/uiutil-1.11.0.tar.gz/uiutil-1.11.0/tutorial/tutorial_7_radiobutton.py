# encoding: utf-8

from uiutil import BaseFrame, standalone, RadioButton, Label, Position
from stateutil.persist import Persist

radio_persist = Persist(persistent_store={},
                        key="rad",
                        value="Second")


class MyFrame(BaseFrame):
    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.radio = RadioButton(text="First",
                                 link=radio_persist,
                                 command=self.set_label)

        RadioButton(text="Second",
                    associate=self.radio,
                    column=Position.NEXT)

        RadioButton(text="Third",
                    associate=self.radio,
                    column=Position.NEXT)

        self.label = Label(row=Position.NEXT,
                           column=Position.START,
                           columnspan=3,
                           value="")
        self.set_label()

    def set_label(self):
        self.label.value = self.radio.value + " is selected"


standalone(frame=MyFrame,
           title="Welcome to UI Util app")
