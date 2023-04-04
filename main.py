from tkinter import *
import math


class CCircle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.selected = False

    def draw(self, canvas):
        if self.selected:
            canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius,
                               fill="blue")
        else:
            canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)

    def contains_point(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2) <= self.radius


class App:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master, width=600, height=600)
        self.canvas.pack()
        self.objects = []
        self.current_selection = None
        self.ctrl_pressed = False
        self.multi_select = False

        # Создание чекбоксов
        self.ctrl_var = BooleanVar()
        self.ctrl_var.set(False)
        ctrl_check = Checkbutton(master, text="Ctrl", variable=self.ctrl_var)
        ctrl_check.pack(side=LEFT)

        self.multi_var = BooleanVar()
        self.multi_var.set(False)
        multi_check = Checkbutton(master, text="Multi-select", variable=self.multi_var)
        multi_check.pack(side=LEFT)

        # Mouse - events
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.canvas.bind("<Control-KeyPress>", self.on_ctrl_press)
        self.canvas.bind("<Control-KeyRelease>", self.on_ctrl_release)
        self.canvas.bind("<Key>", self.on_key_press)  # добавляем связь с функцией on_key_press

        # Create delete button
        self.delete_button = Button(master, text="Delete", command=self.delete_selection)
        self.delete_button.pack()

        # Таймер перерисовки
        self.canvas.after(50, self.refresh)

    def refresh(self):
        self.canvas.delete(ALL)
        for obj in self.objects:
            obj.draw(self.canvas)
        self.canvas.after(50, self.refresh)

    def on_mouse_click(self, event):
        # Проверка нажатия мышки на объект
        for obj in self.objects:
            if obj.contains_point(event.x, event.y):
                if self.ctrl_var.get():
                    obj.selected = not obj.selected
                    if self.multi_var.get():
                        for obj in self.objects:
                            if obj.contains_point(event.x, event.y):
                                obj.selected = True
                else:
                    for other in self.objects:
                        other.selected = False
                    obj.selected = True
                self.current_selection = obj
                return

        obj = CCircle(event.x, event.y, 20)
        self.objects.append(obj)
        if not self.multi_var.get():
            # If multi-select is not enabled, unselect all other objects
            for other in self.objects:
                other.selected = False
        obj.selected = True
        self.current_selection = obj

    def on_mouse_move(self, event):
        if self.current_selection:
            self.current_selection.x = event.x
            self.current_selection.y = event.y

    def on_mouse_release(self, event):
        self.current_selection = None

    def on_ctrl_press(self, event):
        self.ctrl_pressed = True

    def on_ctrl_release(self, event):
        self.ctrl_pressed = False

    def delete_selection(self):
        for obj in self.objects:
            if obj.selected:
                self.canvas.delete(obj)
                self.objects.remove(obj)
        for obj in self.objects:
            obj.selected = False
        # Unselect all objects after deleting
        self.current_selection = None

    def on_key_press(self, event):
        if event.keysym == "<Delete>":
            self.delete_selection()
            print('pressed delete')
        elif event.keysym == "m":
            self.multi_var.set(not self.multi_var.get())
        elif event.keysym == "<Escape>":
            for obj in self.objects:
                obj.selected = False
            self.current_selection = None


root = Tk()
app = App(root)
root.mainloop()
