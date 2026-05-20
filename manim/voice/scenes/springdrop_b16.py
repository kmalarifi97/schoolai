from manim import *
import numpy as np
from springdrop_helpers import (make_bell, target_line, rise_path,
                                small_label, energy_bar)

# "After — he explains the gap. Overshot? Too much stored. Fell short?
#  Too little. The bars name the error."
DUR = 9.0


class SpringdropS1B16(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        bell = make_bell([-3.4, 1.8, 0], scale=0.8)
        bell_y = 1.6
        tl = target_line(bell_y, x0=-5.4, x1=-1.4)
        self.add(bell, tl)

        over = rise_path([-3.4, -2.4, 0], 3.0, color="#C98A6B",
                         width=3, fall=False).set_opacity(0.6)
        short = rise_path([-3.4, -2.4, 0], 0.2, color="#C98A6B",
                          width=3, fall=False).set_opacity(0.6)
        self.play(Create(over), run_time=1.2)
        ov = small_label("overshot: too much stored", [1.4, 1.8, 0],
                         size=22, color="#8C8576")
        self.play(FadeIn(ov), run_time=0.8)
        self.play(Create(short), run_time=1.2)
        sh = small_label("fell short: too little", [1.4, -1.8, 0],
                         size=22, color="#8C8576")
        self.play(FadeIn(sh), run_time=0.8)

        bar = energy_bar("stored", 0.85, [4.4, 0, 0], color="#7FB8E8",
                         max_h=2.6, w=0.7)
        self.play(FadeIn(bar), run_time=1.0)
        self.wait(DUR - 6.2)
