import kivy.app
from kivy.graphics.context_instructions import PushMatrix, Rotate, Scale, PopMatrix
from kivy.properties import BooleanProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import numpy as np


def matrixToNumpy(mat):
    a = []
    for i in range(4):
        b = []
        for j in range(4):
            b.append(mat[i*4+j])
        a.append(b)
    npmat = np.mat(a)
    return npmat


class MyButton(Button):

    def on_touch_down(self, touch):
        if not self.parent.touched:
            self.parent.touched = True
            if self.parent.mat is None:
                scale = matrixToNumpy(self.parent.sca.matrix)
                rotate = matrixToNumpy(self.parent.rot.matrix)
                self.parent.mat = np.matmul(rotate, scale)
                self.parent.inv_mat = self.parent.mat.I
            npTouch = np.mat([touch.x, touch.y, 0, 1.0])
            convTouch = np.matmul(npTouch, self.parent.inv_mat)
            touch.x = convTouch[0,0]
            touch.y = convTouch[0,1]
        background_normal = 'Textures/Grass.png'
        return super(MyButton, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        self.parent.touched = False
        background_normal = 'Textures/Grass.png'
        return super(MyButton, self).on_touch_up(touch)


class MyGridLayout(GridLayout):
    touched = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)
        self.mat = None
        self.inv_mat = None


class MyApp(kivy.app.App):
    def build(self):
        layout = MyGridLayout(cols=10)
        with layout.canvas.before:
            PushMatrix()
            layout.sca = Scale(1.0, 0.5, 1.0)
            layout.rot = Rotate(angle=30, axis=(0,0,1), origin=(400,300,0))
        with layout.canvas.after:
            PopMatrix()
        for i in range (1, 101):
            layout.add_widget(MyButton(background_normal = 'Textures/Grass.png' ,
                     pos_hint = {"x":500, "y":500}))
        return layout

MyApp().run()