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
        '''
        The model transformation from object space to world space

        Returns:
            np.ndarray: 4x4 model transformation
        '''

        ## SEU CÓDIGO AQUI #####################################################
        # Crie as matrizes de transformação e concatene elas

        # Scale matrix
        S = np.eye(4)

        # Translation matrix
        T = np.eye(4)

        for i in range(3):
            S[i, i] = self.scale[i]
            T[i, 3] = self.translation[i]

        # Rotation matrix
        # Dica: utilize o método Rotation.from_euler para criar a rotação
        # Observe que os ângulos de rotação estão em graus
        R = Rotation.from_euler("XYZ", self.rotation, degrees=True).as_matrix()
        
        R_full = np.eye(4)
        R_full[:3, :3] = R


        # Combine the transformations: first scale, then rotate, then translate
        final_transformation = T @ R_full @ S
        #########################################################################

        return final_transformation

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
