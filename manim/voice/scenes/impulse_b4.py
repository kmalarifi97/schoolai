from manim import *
import numpy as np
from impulse_helpers import small_label, big_label, P_COLOR

# "Call that quantity of motion momentum — mass moving, how much there
#  is to stop."
DUR = 7.2


class ImpulseS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        block = Square(side_length=1.0, fill_color=P_COLOR,
                       fill_opacity=0.85, stroke_color="#4A6E8C",
                       stroke_width=2).move_to([-1.0, 0.4, 0])
        m_tag = small_label("mass", block.get_center(), color="#11161B",
                            size=24)
        self.play(FadeIn(block), FadeIn(m_tag), run_time=1.0)

        v_arr = Arrow(block.get_right() + RIGHT * 0.05,
                      block.get_right() + RIGHT * 1.7, buff=0,
                      color="#EAE4D5", stroke_width=5)
        v_lbl = small_label("velocity", v_arr.get_center()
                            + np.array([0, 0.35, 0]), size=24)
        self.play(GrowArrow(v_arr), FadeIn(v_lbl), run_time=1.0)

        grp = VGroup(block, m_tag, v_arr, v_lbl)
        brace = Brace(grp, DOWN, color="#8C98A6")
        p = big_label("p", brace.get_bottom() + np.array([0, -0.45, 0]),
                      color=P_COLOR, size=56)
        p.font_size = 56
        self.play(GrowFromCenter(brace), run_time=0.8)
        self.play(Write(p), run_time=0.9)

        cap = small_label("how much there is to stop",
                          [0, -2.6, 0], color="#8C98A6", size=24)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(DUR - 5.5)
