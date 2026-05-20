from manim import *
import numpy as np
from rotke_helpers import mass_disk, energy_bar, small_label

# "And where the mass sits matters. The same mass, far from the axis,
#  moves faster — and stores far more."
DUR = 8.8


class RotkeS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        LC = np.array([-3.4, 1.5, 0])
        RC = np.array([3.4, 1.5, 0])
        near = mass_disk(LC, radius=1.25, at_rim=False)
        far = mass_disk(RC, radius=1.25, at_rim=True)
        self.play(FadeIn(near), FadeIn(far), run_time=1.0)
        self.add(small_label("mass near the hub",
                             LC + np.array([0, -1.7, 0]), size=22,
                             color="#8C98A6"))
        self.add(small_label("same mass, at the rim",
                             RC + np.array([0, -1.7, 0]), size=22,
                             color="#8C98A6"))

        # both spin at the same rate; rim mass clearly moves faster
        near.add_updater(lambda m, dt: m.rotate(-1.3 * dt,
                                                about_point=LC))
        far.add_updater(lambda m, dt: m.rotate(-1.3 * dt,
                                               about_point=RC))

        bbase_l = np.array([-3.4, -3.5, 0])
        bbase_r = np.array([3.4, -3.5, 0])
        bL = energy_bar(0.02, bbase_l, width=0.5)
        bR = energy_bar(0.02, bbase_r, width=0.5)
        self.add(bL, bR)
        tL = energy_bar(0.55, bbase_l, width=0.5)
        tR = energy_bar(2.0, bbase_r, width=0.5)
        self.play(Transform(bL, tL), Transform(bR, tR), run_time=1.6)
        self.wait(DUR - 2.6)
        near.clear_updaters()
        far.clear_updaters()
