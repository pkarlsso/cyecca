from __future__ import annotations

import casadi as ca

from beartype import beartype
from beartype.typing import List

from cyecca.lie.base import *
from cyecca.lie.group_so3 import *
from cyecca.symbolic import SERIES, taylor_series_near_zero

__all__ = ["se3", "SE3Quat", "SE3Mrp"]


@beartype
class SE3LieAlgebra(LieAlgebra):
    def __init__(self):
        super().__init__(n_param=6, matrix_shape=(4, 4))

    def elem(self, param: PARAM_TYPE) -> SE3LieAlgebraElement:
        return SE3LieAlgebraElement(algebra=self, param=param)

    def bracket(self, left: SE3LieAlgebraElement, right: SE3LieAlgebraElement):
        c = left.to_Matrix() @ right.to_Matrix() - right.to_Matrix() @ left.to_Matrix()
        return self.elem(
            param=ca.vertcat(c[0, 3], c[1, 3], c[2, 3], c[2, 1], c[0, 2], c[1, 0])
        )

    def addition(
        self, left: SE3LieAlgebraElement, right: SE3LieAlgebraElement
    ) -> SE3LieAlgebraElement:
        return self.elem(param=left.param + right.param)

    def scalar_multiplication(
        self, left: (float, int), right: SE3LieAlgebraElement
    ) -> SE3LieAlgebraElement:
        return self.elem(param=left * right.param)

    def adjoint(self, arg: SE3LieAlgebraElement):
        v = arg.param[:3]
        vx = so3.elem(arg.param[:3]).to_Matrix()
        w = so3.elem(arg.param[3:]).to_Matrix()
        horz1 = ca.horzcat(w, vx)
        horz2 = ca.horzcat(ca.SX(3, 3), w)
        return ca.vertcat(horz1, horz2)

    def to_Matrix(self, arg: SE3LieAlgebraElement) -> ca.SX:
        Omega = so3.elem(arg.param[3:]).to_Matrix()
        v = arg.param[:3]
        Z14 = ca.SX(1, 4)
        horz = ca.horzcat(Omega, v)
        return ca.vertcat(horz, Z14)

    def from_Matrix(self, arg: ca.SX) -> SE3LieAlgebraElement:
        assert arg.shape == self.matrix_shape
        return self.elem(
            ca.vertcat(arg[0, 3], arg[1, 3], arg[2, 3], arg[2, 1], arg[0, 2], arg[1, 0])
        )

    def wedge(self, arg: (ca.SX, ca.DM)) -> SE3LieAlgebraElement:
        return self.elem(param=arg)

    def vee(self, arg: SE3LieAlgebraElement) -> ca.SX:
        return arg.param


@beartype
class SE3LieAlgebraElement(LieAlgebraElement):
    """
    This is an SE3 Lie algebra elem
    """

    def __init__(self, algebra: SE3LieAlgebra, param: PARAM_TYPE):
        super().__init__(algebra, param)


se3 = SE3LieAlgebra()


@beartype
class SE3LieGroup(LieGroup):
    def __init__(self, SO3: SO3LieGroup):
        super().__init__(algebra=se3, n_param=SO3.n_param + 3, matrix_shape=(4, 4))
        self.SO3 = SO3

    def elem(self, param: PARAM_TYPE) -> SE3LieGroupElement:
        return SE3LieGroupElement(group=self, param=param)

    def product(self, left: SE3LieGroupElement, right: SE3LieGroupElement):
        R = self.SO3.elem(left.param[3:]).to_Matrix()
        v = R @ right.param[:3] + left.param[:3]
        theta = (self.SO3.elem(left.param[3:]) * self.SO3.elem(right.param[3:])).param
        x = ca.vertcat(v, theta)
        return self.elem(param=x)

    def inverse(self, arg: SE3LieGroupElement):
        v = arg.param[:3]
        theta = arg.param[3:]
        theta_inv = self.SO3.elem(param=theta).inverse()
        R = self.SO3.elem(param=theta).to_Matrix()
        p = -R.T @ v
        return self.elem(param=ca.vertcat(p, theta_inv.param))

    def identity(self) -> SE3LieGroupElement:
        return self.elem(ca.vertcat(ca.SX(3, 1), self.SO3.identity().param))

    def adjoint(self, arg: SE3LieGroupElement):
        v = arg.param[:3]
        vx = so3.elem(param=v).to_Matrix()
        R = self.SO3.elem(param=arg.param[3:]).to_Matrix()
        horz1 = ca.horzcat(R, ca.times(vx, R))
        horz2 = ca.horzcat(ca.SX(3, 3), R)
        return ca.vertcat(horz1, horz2)

    def exp(self, arg: SE3LieAlgebraElement) -> SE3LieGroupElement:
        u = arg.param[:3]  # translation
        omega = self.SO3.algebra.elem(arg.param[3:])
        Omega = omega.to_Matrix()
        rotation = omega.exp(self.SO3).param
        theta = ca.norm_2(omega.param)

        A = SERIES["(1 - cos(x))/x^2"](theta)
        B = SERIES["(x - sin(x))/x^3"](theta)
        V = ca.SX.eye(3) + A * Omega + B * Omega @ Omega
        p = V @ u  # position
        return self.elem(ca.vertcat(p, rotation))

    def log(self, arg: SE3LieGroupElement) -> SE3LieAlgebraElement:
        X = self.SO3.elem(arg.param[3:])
        t = arg.param[:3]

        omega = X.log()
        theta = ca.norm_2(omega.param)
        Omega = omega.to_Matrix()

        A = SERIES["(1 - x*sin(x)/(2*(1 - cos(x))))/x^2"](theta)
        V_inv = ca.SX.eye(3) - Omega / 2 + A * Omega @ Omega
        u = V_inv @ t
        return self.algebra.elem(ca.vertcat(u, omega.param))

    def to_Matrix(self, arg: SE3LieGroupElement) -> ca.SX:
        R = self.SO3.elem(arg.param[3:]).to_Matrix()
        t = arg.param[:3]
        Z13 = ca.SX(1, 3)
        I1 = ca.SX.eye(1)
        horz1 = ca.horzcat(R, t)
        horz2 = ca.horzcat(Z13, I1)
        return ca.vertcat(horz1, horz2)

    def from_Matrix(self, arg: ca.SX) -> SE3LieGroupElement:
        assert arg.shape == self.matrix_shape
        raise NotImplementedError("")


@beartype
class SE3LieGroupElement(LieGroupElement):
    """
    This is an SE3 Lie group elem
    """

    def __init__(self, group: SE3LieGroup, param: PARAM_TYPE):
        super().__init__(group, param)


SE3Mrp = SE3LieGroup(SO3=SO3Mrp)
SE3Quat = SE3LieGroup(SO3=SO3Quat)
