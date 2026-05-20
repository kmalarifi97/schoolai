from manim import *
import numpy as np
from centerofmass_helpers import (make_wrench, com_dot, parabola_path,
                                  point_on_parabola)

# "Every part of it goes a different way. But one single point traces a
#  clean, smooth arc."
DUR = 7.3

START = [-5.0, -1.6, 0]
END = [5.0, -1.6, 0]
PEAK = 2.6


class CenterofmassS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wr = make_wrench(scale=0.58)
        wr.move_to(point_on_parabola(START, END, PEAK, 0.0))

        arc = parabola_path(START, END, PEAK)
        cd = com_dot(point_on_parabola(START, END, PEAK, 0.0), scale=0.95)

        self.add(wr, cd)
        self.wait(0.4)

        t = ValueTracker(0.0)

        def upd_wr(m):
            p = point_on_parabola(START, END, PEAK, t.get_value())
            m.move_to(p)
            # continuous tumble end-over-end as it flies
            m.rotate(-0.22, about_point=p)

        def upd_dot(m):
            p = point_on_parabola(START, END, PEAK, t.get_value())
            m.move_to(p)

        wr.add_updater(upd_wr)
        cd.add_updater(upd_dot)
        # draw the clean arc the point will trace
        self.play(Create(arc), run_time=1.2)
        self.play(t.animate.set_value(1.0),
                  run_time=DUR - 2.6, rate_func=rate_functions.linear)
        wr.clear_updaters()
        cd.clear_updaters()
        self.wait(1.0)
