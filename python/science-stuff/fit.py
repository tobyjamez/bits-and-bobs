import scipy.odr as odr
import numpy as np


def polyfit(x, y, xerr, yerr, deg):
    """
    Perform a polynomial fit on data with 2 dimensional errors using the
    scipy.odr orthogonal distance regression pacage.
    @param x: x data
    @param y: y data
    @param xerr: errors on x data
    @param yerr: errors on y data
    @param deg: degree
    """
    model = odr.Model(lambda B, x: _func(B, x, deg=deg))
    data = odr.Data(x, y, wd=1./pow(xerr, 1), we=1./pow(yerr, 1))
    beta0 = np.polyfit(x, y, deg)  # np.polyfit w/o errors as estimate.
    odr_fit = odr.ODR(data, model, beta0=beta0)

    fit = odr_fit.run()

    return fit.beta


def _func(B, x, deg):
    """
    Polynomial function definition.
    @param B: vector of parameters
    @param x: xdata
    @param deg: degree of fit
    """
    f = sum([B[deg - i] * pow(x, i) for i in range(deg)])
    return f
