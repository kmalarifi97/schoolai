from manim import *
import numpy as np
from impulse_helpers import (make_car, crumple_car, make_driver, make_wall,
                             momentum_bar, force_time_graph, icon_airbag,
                             icon_knees, icon_boxer, small_label, big_label)


class ImpulseTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        wall = make_wall(height=3.0, x=3.2)
        car_c = make_car(crumple=True, scale=0.6).move_to([-3.5, 1.9, 0])
        car_r = make_car(crumple=False, scale=0.6).move_to([-3.5, 0.4, 0])
        car_cr = crumple_car(make_car(crumple=True, scale=0.6)).move_to(
            [0.0, 1.9, 0])
        drv = make_driver(scale=0.7).move_to([0.0, 0.4, 0])

        pbar = momentum_bar(0.7, length=2.4, height=0.34).move_to(
            [-4.2, -1.4, 0])

        gw = force_time_graph("wide", width=3.0, height=1.9,
                              title="long").scale(0.9).move_to([-1.3, -1.7, 0])
        gn = force_time_graph("narrow", width=3.0, height=1.9,
                              title="short").scale(0.9).move_to([1.9, -1.7, 0])

        ab = icon_airbag(0.8).move_to([4.6, 2.0, 0])
        kn = icon_knees(0.8).move_to([4.6, 0.6, 0])
        bx = icon_boxer(0.8).move_to([4.6, -0.9, 0])

        self.add(wall, car_c, car_r, car_cr, drv, pbar, gw, gn, ab, kn, bx)
        self.add(small_label("test", [0, -3.4, 0], size=22))
        self.wait(0.3)
