import tkinter as tk
from threading import Thread


class InfoWindow(Thread):
    def __init__(self):
        super().__init__()
        self.start()
        self.gesture_counter = 0

    def run(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.configure(background='white')
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-disabled", True)
        self.root.wm_attributes("-transparentcolor", "white")

        self.gesture = tk.StringVar()
        self.hand_pos = tk.StringVar()
        self.hand_found = tk.StringVar()

        self.label = tk.Label(self.root, textvariable=self.gesture, font=('Times', '30'), fg='black', bg='#fffffe')
        self.label.pack(side="bottom", anchor="e")
        self.label2 = tk.Label(self.root, text='Predicted gesture', font=('Times', '30'), fg='black', bg='#fffffe')
        self.label2.pack(side="bottom", anchor="e")
        self.label3 = tk.Label(self.root, textvariable=self.hand_pos, font=('Times', '30'), fg='black', bg='#fffffe')
        self.label3.pack(side="bottom", anchor="e")
        self.label4 = tk.Label(self.root, text='Hand position (x,y,w,h)', font=('Times', '30'), fg='black',
                               bg='#fffffe')
        self.label4.pack(side="bottom", anchor="e")
        self.label5 = tk.Label(self.root, textvariable=self.hand_found, font=('Times', '30'), fg='black', bg='#fffffe')
        self.label5.pack(side="bottom", anchor="e")

        self.root.mainloop()

    def set_gesture(self, value):
        if value != 'move':
            self.gesture.set(str(value))
            self.gesture_counter = 0
        elif self.gesture_counter < 5:
            self.gesture_counter += 1
        else:
            self.gesture.set(str(value))

    def set_hand_pos(self, value):
        if value is None:
            self.hand_found.set('Hand not found')
        else:
            self.hand_found.set('Hand found')
            self.hand_pos.set(str(value))
