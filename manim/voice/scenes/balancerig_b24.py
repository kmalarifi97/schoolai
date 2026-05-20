from manim import *
import numpy as np
from balancerig_helpers import balancing_act, com_marker

# "Now you know which videos to go back to."
# visual ends with: [Hold 3s in silence] -- honored as a held final
# still frame, ~3s added to this scene's run time. No literal text.
BASE_DUR = 4.4
HOLD = 3.0
DUR = BASE_DUR + HOLD


class BalancerigS1B24(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # the combined level-rig image, alone and still
        b = balancing_act([0, -0.3, 0], half_w=3.0,
                          bricks=[(-3, 2), (2, 3)], scale=0.95)
        com = com_marker([0, -1.5, 0], scale=1.0, label=False)
        self.play(FadeIn(b["group"]), FadeIn(com), run_time=1.6)

        # it holds alone. Stillness. [Hold 3s in silence]
        self.wait(BASE_DUR - 1.6)
        self.wait(HOLD)            # the deliberate 3s silent hold
