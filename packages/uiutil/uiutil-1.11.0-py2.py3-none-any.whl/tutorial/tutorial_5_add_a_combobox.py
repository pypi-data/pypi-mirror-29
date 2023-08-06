from uiutil import BaseFrame, standalone, Combobox
from uiutil.tk_names import NORMAL


class MyFrame(BaseFrame):

    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.combo = Combobox(value=1,
                              values=(1, 2, 3, 4, 5, "Text"),
                              enabled_state=NORMAL)
        self.combo.value = 3

standalone(frame=MyFrame,
           title="Welcome to UI Util app")
