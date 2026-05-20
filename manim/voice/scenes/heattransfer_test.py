from manim import *
import numpy as np
from heattransfer_helpers import (
    make_bowl, make_spoon, steam_wisps, make_particle_chain,
    make_pot_on_flame, convection_loop, make_sun_void, make_earth,
    glow_path, radiation_rays, make_campfire, make_face, make_stove,
    small_label, heat_tint,
)


class HeattransferTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        bowl = make_bowl([-4.7, -2.6, 0], scale=0.55)
        sp, handle = make_spoon([-3.9, 0.4, 0], [-4.55, -2.45, 0], scale=0.55)
        for i, seg in enumerate(handle):
            seg.set_color(heat_tint(1 - i / len(handle)))
        st = steam_wisps([-4.7, -2.35, 0], n=2, height=1.0)
        for w in st:
            w.set_stroke(opacity=0.5)

        chain, _, _ = make_particle_chain([-2.6, 1.6, 0], [-0.4, 1.6, 0],
                                          n=6, r=0.13)
        pot, water, flame = make_pot_on_flame([2.2, 1.4, 0], scale=0.5)
        loop = convection_loop([2.2, 1.4, 0], w=1.4, h=0.9)

        sun = make_sun_void([-4.6, 2.2, 0], scale=0.7)
        earth = make_earth([-1.6, 2.4, 0], scale=0.7)
        gp = glow_path([-4.2, 2.25, 0], [-2.0, 2.4, 0])
        rays = radiation_rays([-4.2, 2.25, 0], [-2.0, 2.4, 0], n=3,
                              spread=0.3, amp=0.08)

        fire = make_campfire([4.7, -2.4, 0], scale=0.55)
        face = make_face([6.0, -2.1, 0], scale=0.6, facing=LEFT)
        stove = make_stove([4.6, -0.4, 0], scale=0.6)

        lbl = small_label("heat transfer", [0, -3.4, 0], size=22)

        self.add(bowl, sp, st, chain, pot, water, flame, loop,
                 sun, earth, gp, rays, fire, face, stove, lbl)
        self.wait(0.4)
