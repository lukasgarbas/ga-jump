from universe import Universe
from figure import Figure
from typing import List


class Simulation:
    def __init__(
        self, actions: List[int], figure: Figure, 
        runtime: float = 8.6, fps: float = 1.0/30
        ):

        self.actions = actions
        self.universe = Universe()
        self.universe.add_figure(figure)
        self.runtime = runtime
        self.fps = fps
    
    def run(self) -> None:
        '''Runs the simulation for n seconds

        Simulates the universe (makes a 30 fps step)
        Figure makes 4 moves per second (0.25 * current_action)
        The overlap is calculated after making a move (4 fps)
        The ball is placed back when it reaches the left wall
        '''
        current_time = 0.0
        current_action = 1
        runtime_reached = False

        while not runtime_reached:
            self.universe.space.step(self.fps) 
            current_time = current_time + self.fps

            if 0.25 * current_action < current_time:
                movement = self.actions[current_action - 1]
                if movement == 1:
                    self.universe.move_left('up')
                if movement == 2:
                    self.universe.move_left('down')
                if movement == 3:
                    self.universe.move_right('up')
                if movement == 4:
                    self.universe.move_right('down')
                current_action = current_action + 1
                self.universe.calculate_overlap()

            ball_position = self.universe.obsticle.position.int_tuple[0]
            if ball_position < 70:
                self.universe.reset_obsticle_position()

            if current_time > self.runtime:
                runtime_reached = True

    def evaluate(self) -> float:
        return self.universe.score
