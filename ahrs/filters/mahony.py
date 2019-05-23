# -*- coding: utf-8 -*-
"""
Mahony Algorithm as proposed by R. Mahony et al [1]_ in 2010.

This implementation is based in the one made by S. Madgwick.

References
----------
.. [1] Nonlinear Complementary Filters on the Special Orthogonal Group; R.
   Mahony et al. 2010. (https://hal.archives-ouvertes.fr/hal-00488376/document)

"""

import numpy as np
from ahrs.common.orientation import *

class Mahony:
    """
    Class of Mahony algorithm
    """
    __dict__ = {
        "Kp": 1.0,
        "Ki": 0.0,
        "samplePeriod": 1.0/256.0
    }
    def __init__(self, *args, **kwargs):
        # Integral Error
        self.eInt = np.array([0.0, 0.0, 0.0])
        self.__dict__.update(kwargs)

    def updateIMU(self, g, a, q, **kwargs):
        """
        Mahony's AHRS algorithm with an IMU architecture.

        Adapted to Python from original implementation by Sebastian Madgwick.

        Parameters
        ----------
        g : array
            Sample of tri-axial Gyroscope in radians.
        a : array
            Sample of tri-axial Accelerometer.
        q : array
            A-priori quaternion.
        Kp : float
            Proportional filter gain.
        Ki : float
            Integral filter gain.
        samplePeriod : float
            Sampling rate in seconds. Inverse of sampling frequency.

        Returns
        -------
        q : array
            Estimated quaternion.

        """
        # Read input parameters
        Kp = kwargs['Kp'] if 'Kp' in kwargs.keys() else self.__dict__['Kp']
        Ki = kwargs['Ki'] if 'Ki' in kwargs.keys() else self.__dict__['Ki']
        samplePeriod = kwargs['samplePeriod'] if 'samplePeriod' in kwargs.keys() else self.__dict__['samplePeriod']
        # Normalise accelerometer measurement
        a_norm = np.linalg.norm(a)
        if a_norm == 0:     # handle NaN
            return q
        a /= a_norm
        # Assert values
        q /= np.linalg.norm(q)
        qw, qx, qy, qz = q[0], q[1], q[2], q[3]
        # Estimated direction of gravity and magnetic flux
        v = np.array([2.0*(qx*qz - qw*qy),
                    2.0*(qw*qx + qy*qz),
                    qw**2 - qx**2 - qy**2 + qz**2])
        e = np.cross(a, v)
        self.eInt = self.eInt + e*samplePeriod if Ki > 0 else np.array([0.0, 0.0, 0.0])
        # Apply feedback term
        g += Kp*e + Ki*self.eInt
        # Compute rate of change of quaternion
        qDot = 0.5*q_prod(q, [0.0, g[0], g[1], g[2]])
        # Integrate to yield Quaternion
        q += qDot*samplePeriod
        q /= np.linalg.norm(q)
        return q

    def updateMARG(self, g, a, m, q, **kwargs):
        """
        Mahony's AHRS algorithm with a MARG architecture.

        Adapted to Python from original implementation by Sebastian Madgwick.

        Parameters
        ----------
        g : array
            Sample of tri-axial Gyroscope in radians.
        a : array
            Sample of tri-axial Accelerometer.
        m : array
            Sample of tri-axial Magnetometer.
        q : array
            A-priori quaternion.
        Kp : float
            Proportional filter gain.
        Ki : float
            Integral filter gain.
        samplePeriod : float
            Sampling rate in seconds. Inverse of sampling frequency.

        Returns
        -------
        q : array
            Estimated quaternion.

        """
        # Read input parameters
        Kp = kwargs['Kp'] if 'Kp' in kwargs.keys() else self.__dict__['Kp']
        Ki = kwargs['Ki'] if 'Ki' in kwargs.keys() else self.__dict__['Ki']
        samplePeriod = kwargs['samplePeriod'] if 'samplePeriod' in kwargs.keys() else self.__dict__['samplePeriod']
        # Normalise accelerometer measurement
        a_norm = np.linalg.norm(a)
        if a_norm == 0:     # handle NaN
            return q
        a /= a_norm
        # Normalise magnetometer measurement
        m_norm = np.linalg.norm(m)
        if m_norm == 0:     # handle NaN
            return q
        m /= m_norm
        # Assert values
        qw, qx, qy, qz = q[0], q[1], q[2], q[3]
        # Reference direction of Earth's magnetic feild
        h = q_prod(q, q_prod([0, m[0], m[1], m[2]], q_conj(q)))
        b = [0.0, np.linalg.norm([h[1], h[2]]), 0.0, h[3]]
        # Estimated direction of gravity and magnetic flux
        v = np.array([2.0*(qx*qz - qw*qy),
                    2.0*(qw*qx + qy*qz),
                    qw**2 - qx**2 - qy**2 + qz**2])
        w = np.array([2.0*b[1]*(0.5 - qy**2 - qz**2) + 2.0*b[3]*(qx*qz - qw*qy),
                    2.0*b[1]*(qx*qy - qw*qz) + 2.0*b[3]*(qw*qx + qy*qz),
                    2.0*b[1]*(qw*qy + qx*qz) + 2.0*b[3]*(0.5 - qx**2 - qy**2)])
        # Error is sum of cross product between estimated direction and measured direction of fields
        e = np.cross(a, v) + np.cross(m, w)
        self.eInt = self.eInt + e*samplePeriod if Ki > 0 else np.array([0.0, 0.0, 0.0])
        # Apply feedback term
        g += Kp*e + Ki*self.eInt
        # Compute rate of change of quaternion
        qDot = 0.5*q_prod(q, [0.0, g[0], g[1], g[2]])
        # Integrate to yield Quaternion
        q += qDot*samplePeriod
        q /= np.linalg.norm(q)
        return q
