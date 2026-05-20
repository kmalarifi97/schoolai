from manim import *
import numpy as np
from thermalbudget_helpers import (efc_layout, heat_rate_control,
                                   small_label)

# "Energy Forms and Changes. She sets the heat rate and the amount.
#  Turns the energy chunks and the thermometer on."
DUR = 9.6


class ThermalbudgetS1B13(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        title = small_label("Energy Forms and Changes",
                            [0, 3.0, 0], color="#EAE4D5", size=26)
        self.play(FadeIn(title), run_time=1.0)

        efc = efc_layout([-1.4, -0.3, 0], scale=0.95, heat=0.0,
                         melt=0.0, chunks=False)
        self.add(efc.heater, efc.beaker, efc.water, efc.ice,
                 efc.thermo)

        hr = heat_rate_control([3.4, 1.0, 0], frac=0.3, w=2.4,
                               label="heat rate")
        self.play(FadeIn(hr), run_time=0.9)
        self.play(hr.knob.animate.move_to(
            [hr.rail.get_left()[0] + 2.4 * 0.6,
             hr.knob.get_center()[1], 0]), run_time=1.2,
            rate_func=rate_functions.ease_in_out_sine)

        # turn the energy chunks + thermometer on
        efc_hot = efc_layout([-1.4, -0.3, 0], scale=0.95, heat=0.7,
                             melt=0.0, chunks=True)
        self.play(Transform(efc, efc_hot), run_time=1.6)
        self.wait(DUR - 5.7)
