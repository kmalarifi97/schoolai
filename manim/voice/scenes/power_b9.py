from manim import *
import numpy as np
from power_helpers import piano, pulley, small_label, STAIR_COL, POWER_COL

# "A weak motor can lift a piano. Eventually. A strong one lifts it
#  now. Same work, different power."
DUR = 8.5


class PowerS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # two stations
        topL = np.array([-3.2, 2.7, 0])
        topR = np.array([3.2, 2.7, 0])
        plL = pulley(topL, radius=0.30)
        plR = pulley(topR, radius=0.30)
        floor_y = -2.9
        target_y = 1.4

        pnL = piano([topL[0], floor_y + 0.3, 0], scale=1.0)
        pnR = piano([topR[0], floor_y + 0.3, 0], scale=1.0)
        lbL = small_label("weak motor", [topL[0], 3.4, 0], size=24)
        lbR = small_label("strong motor", [topR[0], 3.4, 0], size=24)

        def rope(top, pno):
            return Line([top[0], top[1] - 0.30, 0],
                        [top[0], pno.get_top()[1], 0],
                        color=STAIR_COL, stroke_width=3)

        rL = always_redraw(lambda: rope(topL, pnL))
        rR = always_redraw(lambda: rope(topR, pnR))
        self.play(FadeIn(plL), FadeIn(plR), FadeIn(pnL), FadeIn(pnR),
                  FadeIn(lbL), FadeIn(lbR), run_time=1.0)
        self.add(rL, rR)
        self.wait(0.4)

        # strong one lifts now; weak one lifts slowly, finishes later
        self.play(pnR.animate.move_to([topR[0], target_y, 0]),
                  run_time=1.1, rate_func=rate_functions.ease_out_sine)
        self.play(pnL.animate.move_to([topL[0], target_y, 0]),
                  run_time=3.0, rate_func=rate_functions.linear)
        rL.clear_updaters()
        rR.clear_updaters()

        eq = small_label("same work — different power", [0, -2.9, 0],
                         size=28, color=POWER_COL)
        self.play(FadeIn(eq), run_time=0.8)
        self.wait(max(0.3, DUR - 7.3))
