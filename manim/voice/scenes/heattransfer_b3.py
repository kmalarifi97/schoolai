from manim import *
import numpy as np
from heattransfer_helpers import make_particle_chain, heat_tint

# "The hot end's particles jiggle hard. They knock their neighbors, who
#  knock theirs. The jiggle passes along."
DUR = 9.2


class HeattransferS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        chain, particles, bonds = make_particle_chain(
            [-5.0, 0.2, 0], [5.0, 0.2, 0], n=9, r=0.22)
        self.play(FadeIn(bonds), FadeIn(particles), run_time=1.2)
        self.wait(0.5)

        n = len(particles)
        homes = [p.get_center().copy() for p in particles]

        # the relay: each particle jiggles, then hands it to the next
        for i, p in enumerate(particles):
            t = 1.0 - i / (n - 1)
            jig = 0.20 + 0.16 * t
            p.set_color(heat_tint(t))
            self.play(
                p.animate.shift(RIGHT * jig).set_color(heat_tint(t)),
                run_time=0.20, rate_func=rate_functions.there_and_back)
            self.play(p.animate.move_to(homes[i]).set_color(
                heat_tint(max(0.15, t * 0.7))),
                run_time=0.12)
        self.wait(DUR - 1.7 - 0.32 * n)
