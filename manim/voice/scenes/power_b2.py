from manim import *
import numpy as np
from power_helpers import stairwell, stick_figure, carried_box, wall_clock

# "Now carry the same box, up the same stairs, in twenty seconds."
DUR = 6.0


class PowerS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        st = stairwell(4, step_w=0.78, step_h=0.62, origin=[-4.6, -2.9, 0])
        clk = wall_clock([3.3, 1.9, 0], radius=0.85)
        self.add(st, clk)
        self.wait(0.4)

        start = st.corners[0] + np.array([-0.7, 0.0, 0])
        fig = stick_figure("climb", scale=0.9).move_to(start)
        box = carried_box().next_to(fig, UP, buff=0.04)
        grp = VGroup(fig, box)
        self.play(FadeIn(grp), run_time=0.4)

        # sprint: one fast continuous move; hand snaps a short arc (0:20)
        path = [st.corners[1], st.corners[2], st.corners[3], st.top]
        anims = []
        for c in path:
            anims.append(grp.animate.move_to(c + np.array([0.0, 0.55, 0])))
        self.play(Succession(*anims, run_time=1.4,
                              rate_func=rate_functions.rush_into),
                  Rotate(clk.hand, -TAU * 0.06, about_point=clk.center_pt,
                         run_time=1.4))
        self.wait(max(0.3, DUR - 3.6))
