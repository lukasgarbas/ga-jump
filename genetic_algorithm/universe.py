import pymunk
from pymunk import Vec2d
from figure import Figure
from typing import Text


class Universe:
    def __init__(self):
        self._space = pymunk.Space()
        self._space.gravity = 0, -120
        self._add_walls()
        self._add_obsticle()
        self._score = 0.0

    def _add_walls(self) -> None:
        static_lines = [ 
            pymunk.Segment(self._space.static_body, Vec2d(50,50), Vec2d(950,50), 2),
            pymunk.Segment(self._space.static_body, Vec2d(50,50), Vec2d(50,350), 2),
            pymunk.Segment(self._space.static_body, Vec2d(50,350), Vec2d(950,350), 2),
            pymunk.Segment(self._space.static_body, Vec2d(950,350), Vec2d(950,50), 2) 
        ]
        static_lines[0].friction = 1.0
        self.space.add(static_lines)
  
    def _add_obsticle(self, radius: int = 20) -> None:
        circle_moment = pymunk.moment_for_circle(1.0, 0, radius)
        circle_body = pymunk.Body(1.0, circle_moment)
        circle_body.body_type = pymunk.Body.KINEMATIC
        circle_shape = pymunk.Circle(circle_body, radius)
        circle_shape.filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 1)
        circle_body.position = 930, 70
        circle_body.angular_velocity = 2.0
        circle_body.velocity = (-100, 0)

        self._space.add(circle_body, circle_shape)
        self._obsticle = circle_body
        self._obsticle_shape = circle_shape

    def add_figure(self, figure: Figure) -> None:
        center_poly = figure.center_poly
        right_poly = figure.right_poly
        left_poly = figure.left_poly
        left_joint = figure.left_joint
        right_joint = figure.right_joint

        self._figure = figure
        self._space.add (
            center_poly.body, center_poly.shape,
            left_poly.body, left_poly.shape,
            right_poly.body, right_poly.shape,
            left_joint.joint, left_joint.motor,
            right_joint.joint, right_joint.motor
        )

    def reset_obsticle_position(self) -> None:
        self._obsticle.position = 930, 70

    def move_left(self, direction) -> None:
        ''' Moves left polygon up/down '''
        self._score += 10.0
        self._figure.move_left(direction)

    def move_right(self, direction: Text) -> None:
        ''' Moves righ polygon up/down '''
        self._score += 10.0
        self._figure.move_right(direction)

    def calculate_distance(self) -> None:
        ''' Calculates the distance between the ball and 
        the figure (center polygon) at the current time step '''
        obsticle_x = self._obsticle.position.int_tuple[0]
        figure_x = self._figure.center_poly.body.position.int_tuple[0]
        distance = obsticle_x - figure_x
        return distance

    def calculate_overlap(self) -> None:
        ''' Calculates overlap at the current time step '''
        overlap = 0.0
        obsticle_bb = self._obsticle_shape.bb
        center_poly_bb = self._figure.center_poly.shape.bb
        right_poly_bb = self._figure.left_poly.shape.bb
        left_poly_bb = self._figure.right_poly.shape.bb
        if obsticle_bb.intersects(center_poly_bb):
            dx = max(center_poly_bb.left, obsticle_bb.left) - min(center_poly_bb.top, obsticle_bb.top)
            overlap += dx
        if obsticle_bb.intersects(left_poly_bb):
            dx = max(left_poly_bb.left, obsticle_bb.left) - min(left_poly_bb.top, obsticle_bb.top)
            overlap += dx
        if obsticle_bb.intersects(right_poly_bb):
            dx = max(right_poly_bb.left, obsticle_bb.left) - min(right_poly_bb.top, obsticle_bb.top)
            overlap += dx
        self._score += overlap
        return overlap
    
    @property
    def score(self) -> float:
        return self._score

    @property
    def space(self) -> float:
        return self._space
    
    @property
    def figure(self) -> Figure:
        return self._figure

    @property
    def obsticle(self) -> pymunk.Body:
        return self._obsticle
