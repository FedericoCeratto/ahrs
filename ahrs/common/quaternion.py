# -*- coding: utf-8 -*-
"""
Quaternion Class


"""

import numpy as np
from . mathfuncs import *

class Quaternion:
    def __init__(self, v=None, *args, **kwargs):
        if v is None:
            q = np.array([1., 0., 0., 0.])
        if type(v) is list:
            q = np.array(v)
        if type(v) is np.ndarray:
            # if q.ndim not in [1, 2] or q.shape[-1] != 4:
            #     raise ValueError("Expected `q` to have shape (4,) or (N x 4), "
            #                      "got {}.".format(q.shape))
            q = np.concatenate(([0.0], v)) if v.shape[-1] == 3 else np.array(v)
        q /= np.linalg.norm(q)
        self._q = q
        self.w = self._q[0]
        self.v = self._q[1:]
        self.x, self.y, self.z = self.v

    def __str__(self):
        return "({:-.4f} {:+.4f}i {:+.4f}j {:+.4f}k)".format(self.w, self.x, self.y, self.z)

    def conj(self):
        if self._q.ndim < 2:
            return self._q[1:]*np.array([-1.0, -1.0, -1.0])
        return self._q[:, 1:]*np.array([-1.0, -1.0, -1.0])

    def prod(self, q):
        pq = np.array([
            self._q[0]*q[0] - self._q[1]*q[1] - self._q[2]*q[2] - self._q[3]*q[3],
            self._q[0]*q[1] + self._q[1]*q[0] - self._q[2]*q[3] + self._q[3]*q[2],
            self._q[0]*q[2] + self._q[1]*q[3] + self._q[2]*q[0] - self._q[3]*q[1],
            self._q[0]*q[3] - self._q[1]*q[2] + self._q[2]*q[1] + self._q[3]*q[0]])
        return pq

    def to_axang(self):
        axis = np.asarray(self._q[1:])
        denom = np.linalg.norm(axis)
        angle = 2.0*np.arctan2(denom, self._q[0])
        axis = np.array([0.0, 0.0, 0.0]) if angle == 0.0 else axis/denom
        return axis, angle

    def to_DCM(self):
        q = self._q
        return np.array([
            [1.0-2.0*(q[2]**2+q[3]**2), 2.0*(q[1]*q[2]-q[0]*q[3]), 2.0*(q[1]*q[3]+q[0]*q[2])],
            [2.0*(q[1]*q[2]+q[0]*q[3]), 1.0-2.0*(q[1]**2+q[3]**2), 2.0*(q[2]*q[3]-q[0]*q[1])],
            [2.0*(q[1]*q[3]-q[0]*q[2]), 2.0*(q[0]*q[1]+q[2]*q[3]), 1.0-2.0*(q[1]**2+q[2]**2)]])

