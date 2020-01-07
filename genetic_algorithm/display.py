import pyglet
from pymunk.pyglet_util import DrawOptions
from universe import Universe
from figure import Figure
from typing import List, Text


class Display(pyglet.window.Window):
    def __init__(
        self, actions: List[int], figure: Figure, label: Text = '', runtime: float = 8.2
        ):
        super().__init__(width=1000, height=400, caption='Jumping over the ball', resizable=False)
        self.actions = actions 
        self.universe = Universe()
        self.universe.add_figure(figure)
        self.current_action = 1
        self.current_time = 0.0
        self.fps = 1.0/30
        self.add_label(label)
        self.runtime = runtime

    def add_label(self, label) -> None:
        self.label = pyglet.text.Label(
            label, font_name = 'Arial', font_size = 22, 
            x = 170, y = 320, anchor_x='center', anchor_y='center'
        )

    def on_draw(self) -> None:
        super().clear()
        self.universe.space.debug_draw(DrawOptions())
        self.label.draw()

    def update(self, dt) -> None:
        self.universe.space.step(self.fps)
        self.current_time = self.current_time + self.fps
        if 0.25 * self.current_action < self.current_time:
            movement = self.actions[self.current_action - 1]
            if movement == 1:
                self.universe.move_left('up')
            if movement == 2:
                self.universe.move_left('down')
            if movement == 3:
                self.universe.move_right('up')
            if movement == 4:
                self.universe.move_right('down')
            self.current_action = self.current_action + 1
            self.universe.calculate_overlap()     
        
        ball_position = self.universe.obsticle.position.int_tuple[0]  
        if ball_position < 70:
            self.universe.reset_obsticle_position()
        
        if self.current_time > self.runtime:
            self.close()
    
    def close(self) -> None:
        super().close()
        pyglet.app.exit()

    def display_simulation(self) -> None:
        pyglet.clock.schedule_interval(self.update, self.fps)
        pyglet.app.run()
    
    def get_score(self) -> float:
        return self.universe.score
