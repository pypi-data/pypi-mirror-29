"""
The MIT License (MIT)

Copyright (c) 2017 Microno95, Ekin Ozturk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy
import numpy.linalg

import desolver.utilities as deutil

error_coeff_arrayrk45ck = [[-0.0042937748015873],
                         [ 0.                ],
                         [ 0.0186685860938579],
                         [-0.0341550268308081],
                         [-0.0193219866071429],
                         [ 0.0391022021456804]]

# Based on arXiv:1501.04345v2 - BAB's9o7H
BABPrimes9o7H_coefficients = [[0.04649290043965892,
                               0.154901012702888,
                               0.31970548287359174,
                               -0.19292000881571322,
                               0.17182061279957458,
                               0.17182061279957458,
                               -0.19292000881571322,
                               0.31970548287359174,
                               0.154901012702888,
                               0.04649290043965892],
                              [0.1289555065927298,
                               0.10907642985488271,
                               -0.013886035680471514,
                               0.18375497456418036,
                               0.18419824933735726,
                               0.18375497456418036,
                               -0.013886035680471514,
                               0.10907642985488271,
                               0.1289555065927298,
                               0.0000000000000000]]

# Based on arXiv:1501.04345v2 - ABAs5o6H
ABAs5o6HA_coefficients = [[0.15585935917621682,
                          -0.007025499091957318,
                          0.35116613991574047,
                          0.35116613991574047,
                          -0.007025499091957318,
                          0.15585935917621682],
                         [-0.6859195549562167,
                          0.9966295909529364,
                          0.3785799280065607,
                          0.9966295909529364,
                          -0.6859195549562167,
                          0.0]]

# Based on RK45 Cash-Karp
RK45CK_coefficients = [numpy.array([1631.0 / 55296, 175.0 / 512, 575.0/ 13824, 44275.0 / 110592, 253.0 / 4096, 0.0]),
                       numpy.array([37.0 / 378, 0.0, 250.0 / 621, 125.0 / 594, 0.0, 512.0 / 1771]),
                       numpy.array([2825.0 / 27648, 0.0, 18575.0 / 48384, 13525.0 / 55296, 277.0 / 14336, 1.0 / 4.0])]



@deutil.named_function("Explicit Runge-Kutta 4",
                       alt_names=("Runge-Kutta 4", "RK4",),
                       order=4.0)
def explicitrk4(ode, vardict, soln, h, relerr, eqnum):
    """
    Implementation of the Explicit Runge-Kutta 4 method.
    Ode is a list of strings with the expressions defining the odes.
    Vardict is a dictionary containing the current variables.
    Soln is the list containing the computed values for the odes.
    h is the step-size in computing the next value of the variable(s)
    """

    dim = [eqnum, 4]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)
    dim = soln[0][0].shape
    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = soln[vari][-1]
        
    aux[:, 0] = numpy.array(deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim), dtype=soln[0][-1].dtype)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = soln[vari][-1] + aux[vari][0] * 0.5
    vardict.update({'t': vardict['t'] + 0.5 * h[0]})

    aux[:, 1] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = soln[vari][-1] + aux[vari][1] * 0.5

    aux[:, 2] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = soln[vari][-1] + aux[vari][2]
    vardict.update({'t': vardict['t'] + 0.5 * h[0]})


    aux[:, 3] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = soln[vari][-1] + (aux[vari][0] + aux[vari][1] * 2 + aux[vari][2] * 2 + aux[vari][3]) / 6
        pt = soln[vari]
        kt = numpy.array([vardict['y_{}'.format(vari)]])
        soln[vari] = numpy.concatenate((pt, kt))

@deutil.named_function("Explicit Gill's",
                       alt_names=("Gill's",),
                       order=5.0)
def explicitgills(ode, vardict, soln, h, relerr, eqnum):
    """
    Implementation of the Explicit Runge-Kutta 4 method.
    Ode is a list of strings with the expressions defining the odes.
    Vardict is a dictionary containing the current variables.
    Soln is the list containing the computed values for the odes.
    h is the step-size in computing the next value of the variable(s)
    """
    dim = [eqnum, 4]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)
    dim = soln[0][0].shape
    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = soln[vari][-1]

    aux[:, 0] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = soln[vari][-1] + aux[vari][0] * 0.5
    vardict.update({'t': vardict['t'] + 0.5 * h[0]})
    aux[:, 1] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)
    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = (soln[vari][-1] + aux[vari][0] * 0.4142135623730950 +
                                        aux[vari][1] * 0.2928932188134524)

    aux[:, 2] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)
    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = soln[vari][-1] + aux[vari][2]
    vardict.update({'t': vardict['t'] + 0.5 * h[0]})

    aux[:, 3] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = (soln[vari][-1] - aux[vari][1] * 0.7071067811865475 +
                                        aux[vari][2] * 1.7071067811865475)
    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = (soln[vari][-1] +
                                        (aux[vari][0] + aux[vari][1] * 0.585786437626905 +
                                         aux[vari][2] * 3.4142135623730950 + aux[vari][3]) / 6)
        pt = soln[vari]
        kt = numpy.array([vardict['y_{}'.format(vari)]])
        soln[vari] = numpy.concatenate((pt, kt))

@deutil.named_function("Explicit RK45CK",
                       alt_names=("RK45CK", "Runge-Kutta-Cash-Karp"),
                       order=4.0)
def explicitrk45ck(ode, vardict, soln, h, relerr, eqnum, tol=0.5):
    """
    Implementation of the Explicit Runge-Kutta-Fehlberg method.
    Ode is a list of strings with the expressions defining the odes.
    Vardict is a dictionary containing the current variables.
    Soln is the list containing the computed values for the odes.
    h is the step-size in computing the next value of the variable(s)
    """
    dim = [eqnum, 6]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    t_initial = vardict['t']
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)
    dim = soln[0][0].shape
    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = soln[vari][-1]


    aux[:, 0] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = soln[vari][-1] + aux[vari][0] / 5
    vardict.update({'t': t_initial + h[0] / 5})

    aux[:, 1] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = soln[vari][-1] + 3.0 * aux[vari][0] / 40 + 9.0 * aux[vari][1] / 40
    vardict.update({'t': t_initial + 3 * h[0] / 10})

    aux[:, 2] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = (soln[vari][-1] + (3.0 * aux[vari][0] - 9.0 * aux[vari][1] +
                                                          12.0 * aux[vari][2]) / 10)
    vardict.update({'t': t_initial + 3 * h[0] / 5})

    aux[:, 3] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = (soln[vari][-1] - 11.0 * aux[vari][0] / 54 - 5.0 * aux[vari][1] / 2 -
                                        70.0 * aux[vari][2] / 27 + 35.0 * aux[vari][3] / 27)
    vardict.update({'t': t_initial + h[0]})

    aux[:, 4] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = (soln[vari][-1] + numpy.sum(RK45CK_coefficients[0][[slice(None)] + [None]*(aux[vari].ndim - 1)] * aux[vari], axis=0))
    vardict.update({'t': t_initial + 7.0 * h[0] / 8})

    aux[:, 5] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    coeff = []
    for vari in range(eqnum):
        coeff.append([])
        coeff[vari].append(soln[vari][-1] + numpy.sum(RK45CK_coefficients[1][[slice(None)] + [None]*(aux[vari].ndim - 1)] * aux[vari], axis=0))
        coeff[vari].append(soln[vari][-1] + numpy.sum(RK45CK_coefficients[2][[slice(None)] + [None]*(aux[vari].ndim - 1)] * aux[vari], axis=0))
    error_coeff_array = [numpy.resize(i, dim) for i in error_coeff_arrayrk45ck]
    err_estimate = numpy.abs(
        numpy.ravel([numpy.sum(aux[vari] * error_coeff_array, axis=0) for vari in range(eqnum)])).max()
    vardict.update({'t': t_initial + h[0]})
    if err_estimate != 0:
        h[1] = h[0]
        corr = h[0] * tol * (relerr * h[0] / err_estimate) ** (1.0 / 4.0)
        if abs(corr + t_initial) < abs(h[2]):
            if corr != 0:
                h[0] = corr
        else:
            h[0] = abs(h[2] - t_initial)
    if err_estimate > relerr * h[0] / (tol ** 3):
        for vari in range(eqnum):
            vardict.update({'y_{}'.format(vari): soln[vari][-1]})
        vardict.update({'t': t_initial})
        explicitrk45ck(ode, vardict, soln, h, relerr, eqnum)
    else:
        for vari in range(eqnum):
            vardict.update({'y_{}'.format(vari): coeff[vari][0]})
            pt = soln[vari]
            kt = numpy.array([coeff[vari][1]])
            soln[vari] = numpy.concatenate((pt, kt))

@deutil.named_function("Explicit Midpoint",
                       alt_names=("Midpoint",),
                       order=2.0)
def explicitmidpoint(ode, vardict, soln, h, relerr, eqnum):
    """
    Implementation of the Explicit Midpoint method.
    """

    dim = [eqnum, 2]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)
    dim = soln[0][0].shape

    for vari in range(eqnum):
        vardict["y_{}".format(vari)] = soln[vari][-1]

    aux[:, 0] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] + soln[vari][-1] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict["y_{}".format(vari)] = aux[vari, 0]

    vardict.update({'t': vardict['t'] + 0.5 * h[0]})

    aux[:, 0] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] + soln[vari][-1] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict["y_{}".format(vari)] = numpy.array(soln[vari][-1] + h[0] * aux[vari][0])
        pt = soln[vari]
        kt = numpy.array([vardict['y_{}'.format(vari)]])
        soln[vari] = numpy.concatenate((pt, kt))

    vardict.update({'t': vardict['t'] + 0.5 * h[0]})

@deutil.named_function("Explicit Heun's",
                       alt_names=("Heun's",),
                       order=2.0)
def heuns(ode, vardict, soln, h, relerr, eqnum):
    """
    Implementation of Heun's method.
    """

    dim = [eqnum, 2]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)
    dim = soln[0][0].shape

    for vari in range(eqnum): vardict['y_{}'.format(vari)] = soln[vari][-1]

    aux[:, 0] = deutil.resize_to_correct_dims([ode[vari](**vardict) for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum): vardict['y_{}'.format(vari)] = aux[vari][0] * h[0] + soln[vari][-1]

    vardict.update({'t': vardict['t'] + h[0]})

    aux[:, 1] = deutil.resize_to_correct_dims([ode[vari](**vardict) for vari in range(eqnum)], eqnum, dim)
    for vari in range(eqnum):
        vardict["y_{}".format(vari)] = soln[vari][-1] + h[0] * (aux[vari][0] + aux[vari][1]) * 0.5
        pt = soln[vari]
        kt = numpy.array([vardict['y_{}'.format(vari)]])
        soln[vari] = numpy.concatenate((pt, kt))

@deutil.named_function("Explicit Euler",
                       alt_names=("Forward Euler", "Euler"),
                       order=1.0)
def foreuler(ode, vardict, soln, h, relerr, eqnum):
    """
    Implementation of the Explicit/Forward Euler method.
    """

    dim = [eqnum, 1]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)
    dim = soln[0][0].shape

    for vari in range(eqnum): vardict['y_{}'.format(vari)] = soln[vari][-1]

    aux[:, 0] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] + soln[vari][-1] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = aux[vari, -1]
        pt = soln[vari]
        kt = numpy.array([aux[vari, -1]])
        soln[vari] = numpy.concatenate((pt, kt))

    vardict.update({'t': vardict['t'] + h[0]})

@deutil.named_function("Explicit Improved Forward Euler",
                       alt_names=("Improved Forward Euler", "IFE"),
                       order=2.0)
def impforeuler(ode, vardict, soln, h, relerr, eqnum):
    """
    Implementation of an Improved Forward Euler method.
    """

    dim = [eqnum, 2]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)
    dim = soln[0][0].shape
    for vari in range(eqnum):
        vardict.update({'y_{}'.format(vari): soln[vari][-1]})

    aux[:, 0] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict.update({"y_{}".format(vari): aux[vari][0] + soln[vari][-1]})

    aux[:, 1] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict.update({"y_{}".format(vari): soln[vari][-1] + 0.5 * (aux[vari][0] + aux[vari][1])})
        pt = soln[vari]
        kt = numpy.array([vardict['y_{}'.format(vari)]])
        soln[vari] = numpy.concatenate((pt, kt))
    vardict.update({'t': vardict['t'] + h[0]})

@deutil.named_function("Explicit Euler-Trapezoidal",
                       alt_names=("Euler-Trapezoidal", "Euler-Trap", "Predictor-Corrector Euler"),
                       order=3.0)
def eulertrap(ode, vardict, soln, h, relerr, eqnum):
    """
    Implementation of the Euler-Trapezoidal method.
    """

    dim = [eqnum, 3]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)
    dim = soln[0][0].shape
    for vari in range(eqnum):
        vardict.update({'y_{}'.format(vari): soln[vari][-1]})

    aux[:, 0] = deutil.resize_to_correct_dims([ode[vari](**vardict) for vari in range(eqnum)], eqnum, dim)

    aux[:, 1] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] + soln[vari][-1] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict.update({'y_{}'.format(vari): aux[vari][1]})
    vardict.update({'t': vardict['t'] + h[0]})

    aux[:, 2] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict.update({"y_{}".format(vari): soln[vari][-1] + h[0] * (aux[vari][0] + aux[vari][2])})
        pt = soln[vari]
        kt = numpy.array([vardict['y_{}'.format(vari)]])
        soln[vari] = numpy.concatenate((pt, kt))

@deutil.named_function("Explicit Adaptive Heun-Euler",
                       alt_names=("Adaptive Heun-Euler", "AHE"),
                       order=1.0)
def adaptiveheuneuler(ode, vardict, soln, h, relerr, eqnum, tol=0.9):
    """
    Implementation of the Adaptive Heun-Euler method.
    """

    dim = [eqnum, 2]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)

    dim = soln[0][0].shape

    for vari in range(eqnum):
        vardict.update({'y_{}'.format(vari): soln[vari][-1]})

    aux[:, 0] = deutil.resize_to_correct_dims([ode[vari](**vardict) for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict.update({"y_{}".format(vari): aux[vari][0] * h[0] + soln[vari][-1]})
    vardict.update({'t': vardict['t'] + h[0]})

    aux[:, 1] = deutil.resize_to_correct_dims([ode[vari](**vardict) for vari in range(eqnum)], eqnum, dim)

    err = [(aux[vari][0] - aux[vari][1]) * h[0] for vari in range(eqnum)]
    err = numpy.abs(err).max()
    err *= ((h[2] - vardict['t'] + h[0]) / h[0])
    if err >= relerr:
        vardict.update({'t': vardict['t'] - h[0]})
        if err != 0:
            h[0] *= tol * (relerr / err)
        adaptiveheuneuler(ode, vardict, soln, h, relerr, eqnum)
    else:
        if err < relerr and err != 0:
            h[0] *= (relerr / err) ** (1.0 / 2.0)
        for vari in range(eqnum):
            vardict.update({"y_{}".format(vari): soln[vari][-1] + (aux[vari][0] + aux[vari][1]) * 0.5 * h[0]})
            pt = soln[vari]
            kt = numpy.array([vardict['y_{}'.format(vari)]])
            soln[vari] = numpy.concatenate((pt, kt))

@deutil.named_function("Explicit Symplectic Forward Euler",
                       alt_names=("Symplectic Euler",),
                       order=2.0)
def sympforeuler(ode, vardict, soln, h, relerr, eqnum):
    """
    Implementation of the Symplectic Euler method.
    """

    dim = [eqnum, 1]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)
    dim = soln[0][0].shape
    for vari in range(eqnum):
        vardict.update({'y_{}'.format(vari): soln[vari][-1]})
    for vari in range(eqnum):
        if vari % 2 == 1:
            aux[vari][0] = numpy.resize((ode[vari](**vardict) * h[0] * 0.5 + soln[vari][-1]), dim)
    for vari in range(eqnum):
        if vari % 2 == 1:
            vardict.update({"y_{}".format(vari): aux[vari][0]})
    for vari in range(eqnum):
        if vari % 2 == 0:
            aux[vari][0] = numpy.resize((ode[vari](**vardict) * h[0] + soln[vari][-1]), dim)
    for vari in range(eqnum):
        if vari % 2 == 0:
            vardict.update({"y_{}".format(vari): aux[vari][0]})
    for vari in range(eqnum):
        if vari % 2 == 1:
            aux[vari][0] = numpy.resize((ode[vari](**vardict) * h[0] * 0.5 + soln[vari][-1]), dim)
    for vari in range(eqnum):
        if vari % 2 == 1:
            vardict.update({"y_{}".format(vari): aux[vari][0]})
    for vari in range(eqnum):
        pt = soln[vari]
        kt = numpy.array([vardict['y_{}'.format(vari)]])
        soln[vari] = numpy.concatenate((pt, kt))
    vardict.update({'t': vardict['t'] + h[0]})

@deutil.named_function("Explicit BABS9O7H",
                       alt_names=("BABS9O7H", "BABs9o7H"),
                       order=7.0)
def sympBABs9o7H(ode, vardict, soln, h, relerr, eqnum):
    """
    Implementation of the Symplectic BAB's9o7H method based on arXiv:1501.04345v2
    """

    dim = [eqnum, 1]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)
    dim = soln[0][0].shape
    for vari in range(eqnum):
        vardict.update({'y_{}'.format(vari): soln[vari][-1]})
    for stage in range(0, len(BABPrimes9o7H_coefficients[0])):
        for vari in range(1, eqnum, 2):
            aux[vari][0] = numpy.resize((vardict["y_{}".format(vari)] +
                                         BABPrimes9o7H_coefficients[0][stage] * ode[vari](**vardict) * h[0] / 2),
                                        dim)
        for vari in range(1, eqnum, 2):
            vardict.update({"y_{}".format(vari): aux[vari][0]})
        for vari in range(0, eqnum, 2):
            aux[vari][0] = numpy.resize((vardict["y_{}".format(vari)] +
                                         BABPrimes9o7H_coefficients[1][stage] * ode[vari](**vardict) * h[0]),
                                        dim)
        for vari in range(0, eqnum, 2):
            vardict.update({"y_{}".format(vari): aux[vari][0]})
        for vari in range(1, eqnum, 2):
            aux[vari][0] = numpy.resize((vardict["y_{}".format(vari)] +
                                         BABPrimes9o7H_coefficients[0][stage] * ode[vari](**vardict) * h[0] / 2),
                                        dim)
        for vari in range(1, eqnum, 2):
            vardict.update({"y_{}".format(vari): aux[vari][0]})
    for vari in range(eqnum):
        pt = soln[vari]
        kt = numpy.array([aux[vari][0]])
        soln[vari] = numpy.concatenate((pt, kt))
    vardict.update({'t': vardict['t'] + h[0]})

@deutil.named_function("Explicit ABAS5O6HA",
                       alt_names=("ABAS5O6HA", "ABAs5o6HA"),
                       order=6.0)
def sympABAs5o6HA(ode, vardict, soln, h, relerr, eqnum):
    """
    Implementation of the Symplectic ABAs5o6HA method based on arXiv:1501.04345v2
    """

    dim = [eqnum, 1]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)
    dim = soln[0][0].shape
    for vari in range(eqnum):
        vardict.update({'y_{}'.format(vari): soln[vari][-1]})
    for stage in range(0, len(ABAs5o6HA_coefficients[0])):
        for vari in range(0, eqnum, 2):
            aux[vari][0] = numpy.resize((vardict["y_{}".format(vari)] +
                                         ABAs5o6HA_coefficients[1][stage] * ode[vari](**vardict) * h[0] / 2),
                                        dim)
        for vari in range(0, eqnum, 2):
            vardict.update({"y_{}".format(vari): aux[vari][0]})
        for vari in range(1, eqnum, 2):
            aux[vari][0] = numpy.resize((vardict["y_{}".format(vari)] +
                                         ABAs5o6HA_coefficients[0][stage] * ode[vari](**vardict) * h[0]), dim)
        for vari in range(1, eqnum, 2):
            vardict.update({"y_{}".format(vari): aux[vari][0]})
        for vari in range(0, eqnum, 2):
            aux[vari][0] = numpy.resize((vardict["y_{}".format(vari)] +
                                         ABAs5o6HA_coefficients[1][stage] * ode[vari](**vardict) * h[0] / 2),
                                        dim)
        for vari in range(0, eqnum, 2):
            vardict.update({"y_{}".format(vari): aux[vari][0]})
    for vari in range(eqnum):
        pt = soln[vari]
        kt = numpy.array([aux[vari][0]])
        soln[vari] = numpy.concatenate((pt, kt))
    vardict.update({'t': vardict['t'] + h[0]})



@deutil.named_function("Alt Euler",
                       alt_names=("AltE",),
                       order=1.0)
def alt_foreuler(ode, vardict, soln, h, relerr, eqnum):
    """
    Implementation of the Explicit/Forward Euler method.
    """

    dim = [eqnum, 1]
    dim.extend(soln[0][0].shape)
    dim = tuple(dim)
    if numpy.iscomplexobj(soln[0]):
        aux = numpy.resize([0. + 0j], dim)
    else:
        aux = numpy.resize([0.], dim)
    dim = soln[0][0].shape

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = soln[vari][-1]

    aux[:, 0] = deutil.resize_to_correct_dims([ode[vari](**vardict) * h[0] + soln[vari][-1] for vari in range(eqnum)], eqnum, dim)

    for vari in range(eqnum):
        vardict['y_{}'.format(vari)] = aux[vari, -1]
        pt = soln[vari]
        kt = numpy.array([aux[vari, -1]])
        soln[vari] = numpy.concatenate((pt, kt))
    vardict.update({'t': vardict['t'] + h[0]})
