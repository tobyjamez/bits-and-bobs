"""
----------------------------------------------------------------
Numerical methods for solving differential equations
----------------------------------------------------------------
Toby James - March 2018

A selection of numerical methods for the solution of linear differential
equations.

"""
# ma = - bv - kx + F(t)

import numpy as np
from cmath import sqrt


# Exact solution:
def exact(b, m, k, x, v, t, *args, **kwargs):
    """
    Return the exact solution, where it exists.

    Params:

        b: the damping coefficient of the system,
           where damping force = b * v.

        m: the mass of the osciallator.

        k: the spring constant of the oscillator.

        x: the initial displacement of the oscillator.

        v: the initial velocity of the oscillator.

        t: the time series across which to simulate the system.

    Mathematical backing:

        x = A exp((i * omega - gamma) *t)
                                 2
        gamma = b
                m

        omega ^ 2 = k - b ^ 2
                    m   4 m ^ 2

    Returns:

        a tuple of the displacement array and the velocity array.
    """
    gamma = b/m
    omega = sqrt(k/m - (b ** 2/(4 * m ** 2)))
    A = 1/(2 * omega) * (v + x * gamma/2) + x / 2
    B = x - A
    x_out = (A * np.exp((omega * 1j - gamma / 2) * t) +
             B * np.exp((-omega * 1j - gamma / 2) * t))
    v_out = ((omega * 1j - gamma / 2) * A * np.exp((omega * 1j -
                                                    gamma / 2) * t) +
             (-omega * 1j - gamma / 2) * B * np.exp((-omega * 1j -
                                                     gamma / 2) * t))

    return [x_out, v_out]


# Euler's method:
def euler(b, m, k, x, v, t, h, force=None, time=None, *args, **kwargs):
    """
    Euler's method for solving linear differential equations.

    Params:

        b: the damping coefficient of the system,
           where damping force = b * v.

        m: the mass of the osciallator.

        k: the spring constant of the oscillator.

        x: the initial displacement of the oscillator.

        v: the initial velocity of the oscillator.

        t: the time series across which to simulate the system.

        h: the step size with which the values are calculated.

    Kwargs:

        force: a force to be applied to the oscillator.

        time: the time at which the force should be applied.

    Mathematical backing:
        Euler's method is iterative and follows the following recurrence
        relation:

        a_n = - b v_n - k x_n
                m     m

        v_n+1 = v_n + h a_n

        x_n+1 = x_n + h v_n

    Returns:

        a tuple of the displacement array and the velocity array.
    """
    x_array = [x]
    v_array = [v]
    while len(x_array) != len(t):
            a = -b/m * v - k/m * x
            if force is not None and time is not None and \
               len(x_array) * h - h < time < len(x_array) * h + h:

                a += force / m
            v += h * a
            x += h * v
            x_array.append(x)
            v_array.append(v)
    return [x_array, v_array]


# Improved Euler:
def imp_euler(b, m, k, x, v, t, h, force=None, time=None, *args, **kwargs):
    """
    The improved Euler method for solving linear differential equations.

    Params:

        b: the damping coefficient of the system,
           where damping force = b * v.

        m: the mass of the osciallator.

        k: the spring constant of the oscillator.

        x: the initial displacement of the oscillator.

        v: the initial velocity of the oscillator.

        t: the time series across which to simulate the system.

        h: the step size with which the values are calculated.

    Kwargs:

        force: a force to be applied to the oscillator.

        time: the time at which the force should be applied.

    Mathematical backing:
        The improved Euler method is iterative and follows the following
        recurrence relation:

        a_n = - b v_n - k x_n
                m       m

        v_n+1 = v_n + h a_n

        x_n+1 = x_n + h v_n + 1 h ^ 2 a_n
                              2
    Returns:

        a tuple of the displacement array and the velocity array.
    """
    x_array = [x]
    v_array = [v]
    while len(x_array) != len(t):
            a = -b/m * v - k/m * x
            if force is not None and time is not None and \
               len(x_array) * h - h < time < len(x_array) * h + h:

                a += force/m

            v += h * a
            x += h * v + (h ** 2) * a/2
            v_array.append(v)
            x_array.append(x)

    return [x_array, v_array]


# Verlet:
def verlet(b, m, k, x, v, t, h, force=None, time=None, *args, **kwargs):
    """
    Verlet's method for solving linear differential equations.

    Params:

        b: the damping coefficient of the system,
           where damping force = b * v.

        m: the mass of the osciallator.

        k: the spring constant of the oscillator.

        x: the initial displacement of the oscillator.

        v: the initial velocity of the oscillator.

        t: the time series across which to simulate the system.

        h: the step size with which the values are calculated.

    Kwargs:

        force: a force to be applied to the oscillator.

        time: the time at which the force should be applied.

    Mathematical backing:
        Verlet's method is iterative and follows the following
        recurrence relation:

        x_n+1 = A x_n + B x_n-1

        A = 2 (2 m - k h ^ 2)
                     D

        B = (b h - 2 m)
                 D

        D = 2 m + b h

    Returns:

        a tuple of the displacement array and the velocity array.
    """
    x_array = [x]
    v_array = [v]
    a = 0

    D = 2 * m + b * h
    A = 2 * (2 * m - k * h ** 2) / D
    B = (b * h - 2 * m) / D
    _x = x
    x += v * h
    x_array.append(x)
    v_array.append(v)
    while len(x_array) != len(t):

            if force is not None and time is not None and \
               len(x_array) * h - h < time < len(x_array) * h + h:

                a += force/m

            x_ = A * x + B * _x + a * h ** 2
            a = 0
            _x = x
            x = x_
            x_array.append(x)
            v = (x_ - _x)/(2 * h)
            v_array.append(v)

    return [x_array, v_array]


# Euler-Cromer method:
def euler_cromer(b, m, k, x, v, t, h, force=None, time=None, *args, **kwargs):
    """
    The Euler-Cromer method for solving linear differential equations.

    Params:

        b: the damping coefficient of the system,
           where damping force = b * v.

        m: the mass of the osciallator.

        k: the spring constant of the oscillator.

        x: the initial displacement of the oscillator.

        v: the initial velocity of the oscillator.

        t: the time series across which to simulate the system.

        h: the step size with which the values are calculated.

    Kwargs:

        force: a force to be applied to the oscillator.

        time: the time at which the force should be applied.

    Mathematical backing:
        The Euler-Cromer method is iterative and follows the following
        recurrence relation:

        v_n+1 = v_n + (-k * x_n - b v_n)* h
                        m         m

        x_n+1 = x_n + v_n+1 * h

    Returns:

        a tuple of the displacement array and the velocity array.
    """
    x_array = [x]
    v_array = [v]
    a = 0
    while len(x_array) != len(t):
            if force is not None and time is not None and \
               len(x_array) * h - h < time < len(x_array) * h + h:

                a += force/m

            v += (-b / m * v - k / m * x) * h + a * h
            a = 0
            x += v * h
            v_array.append(v)
            x_array.append(x)

    return [x_array, v_array]


# Chi Squared:
def chi_sq(y_array, model_array):
    """
    Return the sum of the squares of the differences between the
    measured and modelled values for for a systen.

    Params:

        y_array: the measured values.

        y_model: the modelled values.

    Returns:

        the sum of the squares of the differences between y_array and
        y_model.
    """
    return sum([((np.absolute((y - model)) ** 2) / model) for y, model in
                zip(y_array, model_array)])


# Energy stored in the system:
def energy(k, x_array, m, v_array):
    """
    Calculate the energy stored in an oscillating system.

    Params:

        k: the spring constant of the system.

        x_array: the displacement array for the system.

        m: the mass of the osciallator.

        v_array: the velocity array for the system.

    Mathematical backing:

        at a specific time, the system has a displacement x and a
        velocity v. The energy is split between the potential and
        kinetic energy stored in the system. The potential energy, by
        Hooke's law is given by

            E_P = 1 * k * x ^ 2,
                  2

        and the kinetic energy is given by

            E_K = 1 * m * v ^ 2.
                  2

        The total energy is the sum of these two values.

    Returns:

        the energy array of the system, as it evolves with time.

    """
    return np.array([0.5 * k * np.real(x) ** 2 + 0.5 * m *
                    np.real(v) ** 2 for x, v, in zip(x_array, v_array)])
