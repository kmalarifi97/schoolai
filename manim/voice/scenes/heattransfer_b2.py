from manim import *
import numpy as np
from heattransfer_helpers import make_spoon, small_label, heat_tint

# "Nothing moved up that handle. So how did the heat travel through
#  solid metal?"
DUR = 7.0


class HeattransferS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # just the handle, hot at the bottom, cool at top
        sp, handle = make_spoon([1.2, 2.6, 0], [-1.4, -2.4, 0], scale=1.1)
        n = len(handle)
        for i, seg in enumerate(handle):
            seg.set_color(heat_tint(1.0 - i / (n - 1)))
        self.add(sp)
        self.wait(0.7)

        q = Text("?", font="sans", font_size=92, color="#C9A24A")
        q.move_to([1.6, 0.6, 0])
        self.play(Write(q), run_time=1.0)
        lbl = small_label("solid metal — nothing flows",
                          [0, -3.2, 0], color="#8C98A6", size=24)
        self.play(FadeIn(lbl), run_time=1.0)
        self.play(q.animate.scale(1.12),
                  rate_func=rate_functions.there_and_back, run_time=1.0)
        self.wait(DUR - 3.7)
