import pymunk 
from typing import Tuple


class Polygon:
    def __init__(
        self, left: float, bottom: float, right: float, 
        top: float, mass: float = 1.0
        ):
        self._points = (left, bottom, right, top)
        self._mass = mass
        self._shape = self._create_shape()
        self._body = self._create_body()

    def _create_shape(self) -> pymunk.Poly:
        shape = pymunk.Poly(None, self._points)
        shape.filter = pymunk.ShapeFilter(categories=1)
        return shape

    def _create_body(self) -> pymunk.Body:
        vertices = self._shape.get_vertices()
        moment = pymunk.moment_for_poly(self._mass, vertices, offset=(10,10))
        body = pymunk.Body(self._mass, moment)
        self._shape.body = body
        body.friction = 1.0
        return body

    def set_center_of_gravity(self, center: Tuple[float, float]) -> None:
        self._shape.body.center_of_gravity = center

    def set_position(self, position) -> None:
        self._body.position = position

    @property
    def shape(self) -> pymunk.Poly:
        return self._shape

    @property
    def body(self) -> pymunk.Body:
        return self._body

    @property
    def points(self) -> Tuple[int, int, int, int]:
        return self._points
    
    @property
    def centroid(self) -> Tuple[int, int]:
        center = self._shape.bb.center().int_tuple
        return center


class Joint:
    def __init__(self, joint, motor):
        self._joint = joint
        self._motor = motor

    @property
    def motor(self) -> pymunk.SimpleMotor:
        return self._motor

    @property
    def joint(self) -> pymunk.PivotJoint:
        return self._joint


class Figure:
    def create_center_poly(self, polygon: Polygon) -> None:
        polygon.set_position((500, 70))
        polygon.set_center_of_gravity((15, 0))
        self._center_poly = polygon

    def create_right_poly(self, polygon: Polygon) -> None:
        '''Creates the right polygon

        Sets its positon to the center of the window
        attaches right poly to the center poly using a pivot joint 
        adds motor to the joint to control movements
        '''
        polygon.set_position((500, 70)) 

        pivot_point = polygon.points[0]
        joint = pymunk.PivotJoint(
            self._center_poly.body, polygon.body, pivot_point, pivot_point
        )
        motor = pymunk.SimpleMotor(
            polygon.body, self._center_poly.body, 0
        )
        motor.collide_bodies = True
        motor.max_force = 3000
        self._right_joint = Joint(joint, motor)
        self._right_poly = polygon
    
    def create_left_poly(self, polygon: Polygon) -> None:
        '''Creates the left polygon

        Sets its positon to the center of the window
        attaches left poly to the center poly using a pivot joint 
        adds motor to the joint to control movements
        '''
        polygon.set_position((500, 70))

        pivot_point = polygon.points[0]
        joint = pymunk.PivotJoint(
            self._center_poly.body, polygon.body, pivot_point, pivot_point
        )
        motor = pymunk.SimpleMotor(
            polygon.body, self._center_poly.body, 0
        )
        motor.collide_bodies = True
        motor.max_force = 3000
        self._left_joint = Joint(joint, motor)
        self._left_poly = polygon

    def move_left(self, direction: str) -> None:
        '''Moves the left polygon

        Movement is done by changing the spinning rate of the left motor
        '''
        if direction == 'up':
            self._left_joint.motor.rate = 100.0
        if direction == 'down':
            self._left_joint.motor.rate = -100.0
    
    def move_right(self, direction) -> None:
        '''Moves the right polygon

        Movement is done by changing the spinning rate of the right motor
        '''
        if direction == 'up':
            self._right_joint.motor.rate = -100.0
        if direction == 'down':
            self._right_joint.motor.rate = 100.0

    @property
    def center_poly(self) -> Polygon:
        return self._center_poly

    @property
    def left_poly(self) -> Polygon:
        return self._left_poly

    @property
    def right_poly(self) -> Polygon:
        return self._right_poly
    
    @property
    def left_joint(self) -> Joint:
        return self._left_joint
    
    @property
    def right_joint(self) -> Joint:
        return self._right_joint
