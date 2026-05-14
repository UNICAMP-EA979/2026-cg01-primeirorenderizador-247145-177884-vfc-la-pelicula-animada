import copy
from collections.abc import Iterable
from typing import Callable

import numpy as np
from scipy.spatial.transform import Rotation


class Node:
    '''
    Scene node.

    Represents any element that exists in the application scene.
    '''

    def __init__(self, name: str = "") -> None:
        '''
        Node initializer

        Args:
            name (str, optional): node name. Defaults to "".
        '''
        self.name = name

        self.translation: np.ndarray = np.zeros(3)  # Translação
        self.rotation: np.ndarray = np.zeros(3)  # Ângulos da rotação em graus
        self.scale: np.ndarray = np.ones(3)  # Escala

        self.render_data = {}
        self.callbacks: list[Callable[["Node", float, float], None]] = []

        self._children: set[Node] = set()
        self._parent: Node | None = None

    @property
    def model_transform(self) -> np.ndarray:
        # Create identity matrix
        identity = np.eye(4)
        
        # Scale matrix
        scale_matrix = np.array([
            [self.scale[0], 0, 0, 0],
            [0, self.scale[1], 0, 0],
            [0, 0, self.scale[2], 0],
            [0, 0, 0, 1]
        ])
        
        # Rotation matrix (from Euler angles)
        # Convert rotation angles from degrees to radians
        rx = np.radians(self.rotation[0])
        ry = np.radians(self.rotation[1])
        rz = np.radians(self.rotation[2])
        
        # Rotation matrices around X, Y, Z axes
        rot_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(rx), -np.sin(rx), 0],
            [0, np.sin(rx), np.cos(rx), 0],
            [0, 0, 0, 1]
        ])
        
        rot_y = np.array([
            [np.cos(ry), 0, np.sin(ry), 0],
            [0, 1, 0, 0],
            [-np.sin(ry), 0, np.cos(ry), 0],
            [0, 0, 0, 1]
        ])
        
        rot_z = np.array([
            [np.cos(rz), -np.sin(rz), 0, 0],
            [np.sin(rz), np.cos(rz), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        rotation_matrix = rot_z @ rot_y @ rot_x
        
        # Translation matrix
        translation_matrix = np.array([
            [1, 0, 0, self.translation[0]],
            [0, 1, 0, self.translation[1]],
            [0, 0, 1, self.translation[2]],
            [0, 0, 0, 1]
        ])
        
        # Compose transformations: T × R × S
        return translation_matrix @ rotation_matrix @ scale_matrix

    @property
    def parent(self) -> "Node | None":
        '''
        Parent node
        '''
        return self._parent

    @property
    def children(self) -> Iterable["Node"]:
        '''
        Set of children
        '''
        return frozenset(self._children)

    def clone(self) -> "Node":
        '''
        Creates a new node with same properties (except for children)

        Returns:
            Node: node clone.
        '''
        clone = copy.deepcopy(self)
        clone._children = set()

        if self.parent is not None:
            self.parent.add_child(clone)

        return clone

    def add_child(self, child: "Node") -> None:
        '''
        Add a child node to this node

        Args:
            child (Node): child to add
        '''
        if child in self._children:
            return

        self._children.add(child)

        if child._parent is not None:
            child._parent._children.remove(child)
        child._parent = self

    def update(self, delta_time: float, time_since_start: float) -> None:
        '''
        Execute the application update code for this node

        Args:
            delta_time (float): time since last update
            time_since_start (float): time since application start
        '''
        for callback in self.callbacks:
            callback(self, delta_time, time_since_start)
