from manim import *
import numpy as np
from power_helpers import stairwell, stick_figure, carried_box, wall_clock

# "Carry a heavy box up four flights of stairs. Take ten minutes,
#  resting often."
DUR = 7.0


class PowerS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        st = stairwell(4, step_w=0.78, step_h=0.62, origin=[-4.6, -2.9, 0])
        clk = wall_clock([3.3, 1.9, 0], radius=0.85)
        clk.hand.rotate(0, about_point=clk.center_pt)
        self.play(Create(st, run_time=1.2), FadeIn(clk, run_time=1.0))

        start = st.corners[0] + np.array([-0.7, 0.0, 0])
        fig = stick_figure("climb", scale=0.9).move_to(start)
        box = carried_box().next_to(fig, UP, buff=0.04)
        grp = VGroup(fig, box)
        self.play(FadeIn(grp), run_time=0.7)

        # slow climb with rests; clock hand sweeps to "10:00" (full turn)
        targets = [st.corners[1], st.corners[2], st.corners[3], st.top]
        for i, c in enumerate(targets):
            dest = c + np.array([0.0, 0.55, 0])
            self.play(
                grp.animate.move_to(dest),
                Rotate(clk.hand, -TAU / 4, about_point=clk.center_pt),
                run_time=1.0, rate_func=rate_functions.ease_in_out_sine)
            self.wait(0.35)  # resting often
        self.wait(max(0.3, DUR - 7.0))
