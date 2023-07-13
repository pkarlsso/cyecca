from __future__ import annotations

from enum import Enum

import numpy as np
import numpy.typing as npt
from numpy import floating

from beartype import beartype
from beartype.typing import List

from ._base import LieAlgebra, LieAlgebraElement, LieGroup, LieGroupElement


@beartype
class SO3LieAlgebra(LieAlgebra):
    def __init__(self):
        super().__init__(n_param=3, matrix_shape=(3, 3))

    def bracket(
        self, left: LieAlgebraElement, right: LieAlgebraElement
    ) -> LieAlgebraElement:
        assert self == left.algebra
        assert self == right.algebra
        c = left.to_matrix()@right.to_matrix() - right.to_matrix()@left.to_matrix()
        return self.element(param=np.array([c[2, 1], c[0, 2], c[1, 0]]))

    def addition(
        self, left: LieAlgebraElement, right: LieAlgebraElement
    ) -> LieAlgebraElement:
        assert self == left.algebra
        assert self == right.algebra
        return self.element(param=left.param + right.param)

    def scalar_multipication(self, left : Real, right: LieAlgebraElement) -> LieAlgebraElement:
        assert self == right.algebra
        return self.element(param=left * right.param)

    def adjoint(self, left: LieAlgebraElement) -> npt.NDArray[np.floating]:
        assert self == left.algebra
        raise NotImplementedError("adjoint not implemented")

    def to_matrix(self, left: LieAlgebraElement) -> npt.NDArray[np.floating]:
        assert self == left.algebra
        return np.array([
            [0, -left.param[2], left.param[1]],
            [left.param[2], 0, -left.param[0]],
            [-left.param[1], left.param[0], 0]])
    
    def wedge(self, left: npt.NDArray[np.floating]) -> LieAlgebraElement:
        self = SO3LieAlgebra()
        return self.element(param=left)
    
    def vee(self, left: LieAlgebraElement) -> npt.NDArray[np.floating]:
        assert self == left.algebra
        return left.param


class Axis(Enum):
    x = 1
    y = 2
    z = 3

class EulerType(Enum):
    body_fixed = 1
    space_fixed = 2

def rotation_matrix(axis : Axis, angle : Real):
    if axis== Axis.x:
        return np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]
        ])
    elif axis == Axis.y:
        return np.array([
                [np.cos(angle), 0, np.sin(angle)],
                [0, 1, 0],
                [-np.sin(angle), 0, np.cos(angle)]
            ])
    elif axis == Axis.z:
        return np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
    else:
        raise ValueError('unknown axis')


so3 = SO3LieAlgebra()


@beartype
class SO3EulerLieGroup(LieGroup):
    def __init__(self, euler_type : EulerType, sequence : List[Axis]):
        super().__init__(algebra=so3, n_param=3, matrix_shape=(3, 3))
        self.euler_type = euler_type
        assert len(sequence) == 3
        self.sequence = sequence

    def product(self, left: LieGroupElement, right: LieGroupElement):
        assert self == left.group
        assert self == right.group
        return self.element(param=left.param + right.param)

    def inverse(self, left: LieGroupElement) -> LieGroupElement:
        assert self == left.group
        return self.element(param=-left.param)

    def identity(self) -> LieGroupElement:
        return self.element(param=np.array.zeros(self.n_param, 1))

    def adjoint(self, left: LieGroupElement):
        assert self == left.group
        return left.to_matrix()

    def exp(self, left: LieAlgebraElement) -> LieGroupElement:
        assert self.algebra == left.algebra
        v = self.param
        w = left.to_matrix()
        theta = np.linalg.norm(v)
        A = np.where(np.abs(theta) < EPS, 1 - theta**2/6 + theta**4/120, np.sin(theta)/theta)
        B = np.where(np.abs(theta)<EPS, 0.5 - theta ** 2 / 24 + theta ** 4 / 720, (1 - np.cos(theta)) / theta ** 2)
        R = np.eye(3) + A * w + B * w @ w
        return 

    def log(self, left: LieGroupElement) -> LieAlgebraElement:
        assert self == left.group
        raise NotImplementedError("log not implemented")

    def to_matrix(self, left: LieGroupElement) -> npt.NDArray[np.floating]:
        assert self == left.group
        m = np.eye(3)
        for axis, angle in zip(self.sequence, left.param):
            if self.euler_type == EulerType.body_fixed:
                m = m @ rotation_matrix(axis=axis, angle=angle)
            elif self.euler_type == EulerType.space_fixed:
                m = rotation_matrix(axis=axis, angle=angle) @ m
            else:
                raise ValueError('euler_type must be body_fixed or space_fixed')
        return np.array(m)


SO3Euler = SO3EulerLieGroup


@beartype
class SO3QuatLieGroup(LieGroup):
    def __init__(self):
        super().__init__(algebra=so3, n_param=4, matrix_shape=(3, 3))

    def product(self, left: LieGroupElement, right: LieGroupElement):
        assert self == left.group
        assert self == right.group
        q = left.param
        p = right.param
        return self.element(param=np.array([
            q[0] * p[0] - q[1] * p[1] - q[2] * p[2] - q[3] * p[3],
            q[1] * p[0] + q[0] * p[1] - q[3] * p[2] + q[2] * p[3],
            q[2] * p[0] + q[3] * p[1] + q[0] * p[2] - q[1] * p[3],
            q[3] * p[0] - q[2] * p[1] + q[1] * p[2] + q[0] * p[3]
        ]))

    def inverse(self, left: LieGroupElement) -> LieGroupElement:
        assert self == left.group
        q = left.param
        return self.element(param=np.array([
            q[0], -q[1], -q[2], -q[3]
        ]))

    def identity(self) -> LieGroupElement:
        return self.element(param=np.array([1, 0, 0, 0]))

    def adjoint(self, left: LieGroupElement):
        assert self == left.group
        raise left.to_matrix()

    def exp(self, left: LieAlgebraElement) -> LieGroupElement:
        assert self.algebra == left.algebra
        v = left.param
        theta = np.linalg.norm(v)
        c = np.sin(theta/2)
        q = np.array([np.cos(theta/2), c*v[0]/theta, c*v[1]/theta, c*v[2]/theta])
        return SO3QuatLieGroup.element(param=np.where(np.abs(theta)>1e-7, q, np.array([1,0,0,0])))
    
    def log(self, left: LieGroupElement) -> LieAlgebraElement:
        assert self == left.group
        q = left.param
        theta = 2*np.arccos(q[0])
        c = np.sin(theta/2)
        v = np.array([theta*q[1]/c, theta*q[2]/c, theta*q[3]/c])
        return so3.element(param=np.where(np.abs(c)>1e-7, v, np.array([0,0,0])))
    
    def to_matrix(self, left: LieGroupElement) -> npt.NDArray[np.floating]:
        assert self == left.group
        a, b, c, d = left.param
        aa = a*a
        ab = a*b
        ac = a*c
        ad = a*d
        bb = b*b
        bc = b*c
        bd = b*d
        cc = c*c
        cd = c*d
        dd = d*d
        return np.array([
            [aa + bb - cc - dd, 2 * (bc - ad), 2 * (ac + bd)],
            [2 * (bc + ad), aa - bb + cc - dd, 2 * (cd - ab)],
            [2 * (bd - ac), 2 * (ab + cd), aa - bb - cc + dd]
        ])

SO3Quat = SO3QuatLieGroup()

@beartype
class SO3MRPLieGroup(LieGroup):
    def __init__(self):
        super().__init__(algebra=so3, n_param=4, matrix_shape=(3, 3))

    def product(self, left: LieGroupElement, right: LieGroupElement):
        assert self == left.group
        assert self == right.group
        a = left.param[:3]
        b = right.param[:3]
        na_sq = np.dot(a, a)
        nb_sq = np.dot(b, b)
        res = np.zeros((4,))
        den = 1 + na_sq * nb_sq - 2 * np.dot(b, a)
        res[:3] = ((1 - na_sq) * b + (1 - nb_sq) * a - 2 * np.cross(b, a)) / den
        res[3] = 0  # shadow state
        return self.element(param=res)

    def inverse(self, left: LieGroupElement) -> LieGroupElement:
        assert self == left.group
        r = left.param
        return self.element(param=np.array([
            -r[0], -r[1], -r[2], r[3]
        ]))
    
    def identity(self) -> LieGroupElement:
        return self.element(param=np.array([0, 0, 0, 0]))
    
    def shadow(self, left: LieGroupElement):
        assert self == left.group
        r = left.param
        n_sq = np.dot(r[:3], r[:3])
        res = np.zeros((4, 1))
        res[:3] = -r[:3] / n_sq
        res[3] = np.logical_not(r[3])
        return res
    
    def shadow_if_necessary(self, left: LieGroupElement):
        assert self == left.group
        r = left.param
        return np.where(np.linalg.norm(r[:3]) > 1, cls.shadow(r), r)

    def adjoint(self, left: LieGroupElement):
        assert self == left.group
        raise left.to_matrix()

    def exp(self, left: LieAlgebraElement) -> LieGroupElement:
        assert self.algebra == left.algebra
        v = left.param
        angle = np.linalg.norm(v)
        res = np.zeros((4,))
        res[:3] = np.tan(angle / 4) * v / angle
        res[3] = 0
        return SO3MRPLieGroup.element(param=np.where(angle>1e-7, res, np.array([0,0,0,0])))

    def log(self, left: LieGroupElement) -> LieAlgebraElement:
        assert self == left.group
        r = left.param
        n = np.linalg.norm(r[:3])
        v = 4*np.arctan(n)*r[:3]/n
        return so3.element(param=np.where(n > 1e-7, v, np.array([0,0,0])))

    def to_matrix(self, left: LieGroupElement) -> npt.NDArray[np.floating]:
        assert self == left.group
        r = left.param
        a = r[:3]
        X = so3.element(param=a).to_matrix()
        n_sq = np.dot(a, a)
        X_sq = X @ X
        R = np.eye(3) + (8 * X_sq - 4 * (1 - n_sq) * X) / (1 + n_sq) ** 2
        # return transpose, due to convention difference in book
        return R.T

SO3MRP = SO3MRPLieGroup()
