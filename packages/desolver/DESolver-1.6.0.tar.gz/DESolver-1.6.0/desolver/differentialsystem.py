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

import re
import numpy
import numpy.linalg
import sys
import time
import shutil
import types
import sympy as smp
from sympy.parsing.sympy_parser import parse_expr

import desolver.integrationschemes as ischemes
import desolver.exceptiontypes as etypes

namespaceInitialised = False
available_methods = {}
methods_inv_order = {}
raise_KeyboardInterrupt = False

# This regex string will match any unacceptable arguments attempting to be passed to eval
precautions_regex = r"(\.*\_*(builtins|class|(?<!(c|C))os|shutil|sys|time|dict|tuple|list|module|super|name|subclasses|base|lambda)\_*)"

def init_module(raiseKBINT=True):
    global namespaceInitialised
    if not namespaceInitialised:
        global raise_KeyboardInterrupt
        raise_KeyboardInterrupt = raiseKBINT
        global precautions_regex
        precautions_regex = re.compile(precautions_regex)
        methods_ischemes = [(ischemes.__dict__.get(a)) for a in dir(ischemes)
                             if isinstance(ischemes.__dict__.get(a), types.FunctionType)]
        available_methods.update(dict([(func.__name__, func) for func in methods_ischemes if hasattr(func, "__alt_names__")] +
                                        [(alt_name, func) for func in methods_ischemes if hasattr(func, "__alt_names__") for alt_name in func.__alt_names__]))

        methods_inv_order.update({func: 1.0/func.__order__ for name, func in available_methods.items()})

        namespaceInitialised = True
    elif raiseKBINT:
        raise_KeyboardInterrupt = True
    else:
        pass

class OdeSystem:
    """Ordinary Differential Equation class. Designed to be used with a system of ordinary differential equations."""
    def __init__(self, n=(1,), equ=tuple(tuple()), t=(0, 0), savetraj=0, stpsz=1.0, eta=0, relerr=4e-16, constants=None):
        """Initialises the system to the parameters passed or to default values.

        Keyword arguments:
            n: Specifies the dimensions of the system in the form of a tuple.
               Can be arbitrary as long as the values are integral. Uses numpy convention so
               a scalar is (1,), a vector is (1,3), a 2x2 matrix is (1,2,2),
               an (M,T) tensor is (1,n_1,...,n_M,k_1,...,k_T) as expected.
            equ: Specifies the list of differential equations and their initial conditions.
                 Use in the form of strings where t and y_{} are the variables.
                 The curly braces are to be replaced by values that range from 0 to k where
                 k = total_number_of_equations - 1.
                 ie. y_0 will be the first equation, y_1 the second, and so on.
            t: A tuple of the form (initial time, final time) aka the integration limits.
            savetraj: Set to True or False to specify whether or not the trajectory of the
                      integration should be recorded.
            stpsz: Sets the step-size for the integration, choose a value that is slightly less than the highest frequency
                   changes in value of the solutions to the equations.
            eta: Set to True or False to specify whether or not the integration process should return an eta,
                 current progress and simple information regarding step-size and current time.
                 NOTE: This may slow the integration process down as the process of outputting
                       these values create overhead.
            relerr: Denotes the target relative global error. Useful for adaptive methods.

        Variable-length arguments:
            consts: Arbitrary set of keyword arguments that define the constants to be used in the system."""

        if len(t) != 2:
            raise etypes.LengthError("Two time bounds were required, only {} were given!".format(len(t)))
        for k, i in enumerate(equ):
            if 't' not in i[0] and 'y_' not in i[0]:
                ischemes.deutil.warning("Equation {} has no variables".format(k))
        self.relative_error_bound = relerr
        self.equRepr = []
        for i in equ:
            try:
                try:
                    temp = parse_expr(precautions_regex.sub("LUBADUBDUB", str(i[0])))
                except:
                    if isinstance(i[0], smp.Expr):
                        temp = i[0]
                    else:
                        temp = parse_expr("t")
            except:
                print(i[0])
                raise
            self.equRepr.append(temp)
        self.eta = eta
        self.eqnum = len(equ)
        self.consts = constants if constants is not None else dict()
        self.symbols = set(smp.symbols(" ".join(["y_{}".format(i) for i in range(self.eqnum)]) + " t " + " ".join([k for k in self.consts])))
        self.equ = [smp.lambdify(self.symbols, i, numpy, dummify=False) for i in self.equRepr]
        self.dim = tuple([1] + list(n))
        self.y = [numpy.resize(equ[i][1] if (len(equ[i]) == 2) else 0.0, self.dim) for i in range(self.eqnum)]
        self.t = float(t[0])
        self.sample_times = [self.t]
        self.t0 = float(t[0])
        self.t1 = float(t[1])
        self.soln = [[numpy.resize(value, self.dim)] for value in self.y]
        for k in self.consts:
            self.consts.update({k: numpy.resize(self.consts[k], self.dim)})
        self.traj = savetraj
        self.method = ischemes.explicitrk4
        if (stpsz < 0 < t[0] - t[1]) or (stpsz > 0 > t[0] - t[1]):
            self.dt = stpsz
        else:
            self.dt = -1 * stpsz

    def set_end_time(self, t):
        """Changes the final time for the integration of the ODE system

        Required arguments:
        t: Denotes the final time."""
        self.t1 = float(t)
        self.check_time_bounds()

    def get_end_time(self):
        """Returns the final time of the ODE system."""
        return self.t1

    def set_start_time(self, t):
        """Changes the initial time for the integration of the ODE system.

        Required arguments:
        t: Denotes the initial time."""
        self.t0 = float(t)
        self.check_time_bounds()

    def get_start_time(self):
        """Returns the initial time of the ODE system."""
        return self.t0

    def check_time_bounds(self):
        if not (abs(self.t0) < abs(self.t) < abs(self.t1)):
            self.t = self.t0

    def set_current_time(self, t):
        """Changes the current time for the integration of the ODE system.

        Required arguments:
        t: Denotes the current time"""
        self.t = float(t)

    def get_current_time(self):
        """Returns the current time of the ODE system"""
        return self.t

    def set_time(self, t=()):
        """Alternate interface for changing current, beginning and end times.

        Keyword arguments:
        t:  -- A length of 1 denotes changes to current time.
            -- A length of 2 denotes changes to beginning and end times in that order.
            -- A length of 3 denotes changes to all three times in order of current, beginning and end.
            -- A length larger than 3 will behave the same as above and ignore values beyond the 3rd index."""
        if len(t) == 1:
            ischemes.deutil.warning("You have passed a tuple that only contains one element, "
                    "this will be taken as the current time.")
            self.t = t[0]
        elif len(t) == 2:
            self.t0 = t[0]
            self.t1 = t[1]
        elif len(t) == 3:
            self.t = t[0]
            self.t0 = t[1]
            self.t1 = t[2]
        elif len(t) > 3:
            ischemes.deutil.warning("You have passed an array longer than 3 elements, "
                    "the first three will be taken as the principle values.")
            self.t = t[0]
            self.t0 = t[1]
            self.t1 = t[2]
        else:
            ischemes.deutil.warning("You have passed an array that is empty, this doesn't make sense.")

    def set_step_size(self, h):
        """Sets the step size that will be used for the integration.

        Required arguments:
        dt: Step size value. For systems that grow exponentially choose a smaller value, for oscillatory systems choose
            a value slightly less than the highest frequency of oscillation. If unsure, use an adaptive method in the
            list of available methods (view by calling availmethods()) followed by setmethod(), and finally call
            setrelerr() with the keyword argument auto_calc_dt set to True for an approximately good step size."""
        self.dt = h

    def get_step_size(self):
        """Returns the step size that will be attempted for the next integration step"""
        return self.dt

    def get_relative_error(self):
        """Returns the target relative error used by the timestep autocalculator and the adaptive integration methods.
        Has no effect when the integration method is non-adaptive. These are all the symplectic integrators and the fixed order schemes.
        """
        return self.relative_error_bound

    @staticmethod
    def available_methods(suppress_print=False):
        """Prints and then returns a dict of methods of integration that are available."""
        if not suppress_print:
            print(available_methods.keys())
        return available_methods

    def set_method(self, method):
        """Sets the method of integration.

        Required arguments:
        method: String that denotes the key to one of the available methods in the dict() returned by availmethods()."""
        if method in available_methods.keys():
            self.method = available_methods[method]
        else:
            print("The method you selected does not exist in the list of available methods, "
                  "call availmethods() to see what these are")

    def get_method(self):
        """
        Returns the method used to integrate the system.
        """
        for method, func in available_methods.items():
            if self.method is func:
                return method

    def show_equations(self):
        """Prints the equations that have been entered for the system.

        Returns the equations themselves as a list of strings."""
        for i in range(self.eqnum):
            print("dy_{} =".format(i), self.equRepr[i])
        return self.equRepr

    def number_of_equations(self):
        """Prints then returns the number of equations in the system"""
        print(self.eqnum)
        return self.eqnum

    def initial_conditions(self):
        """Prints the initial conditions of the system"""
        for i in range(self.eqnum):
            print("y_{}({}) = {}".format(i, self.t0, self.y[i]))
        return self.y

    def final_conditions(self, p=1):
        """Prints the final state of the system.

        Identical to initial conditions if the system has not been integrated"""
        if p:
            for i in range(self.eqnum):
                print("y_{}({}) = {}".format(i, self.t1, self.soln[i][-1]))
        return self.soln

    def show_system(self):
        """Prints the equations, initial conditions, final states, time limits and defined constants in the system."""
        for i in range(self.eqnum):
            print("Equation {}\ny_{}({}) = {}\ndy_{} = {}\ny_{}({}) = {}\n".format(i, i, self.t0, self.y[i], i,
                                                                                   str(self.equRepr[i]), i, self.t,
                                                                                   self.soln[i][-1]))
        if self.consts:
            print("The constants that have been defined for this system are: ")
            print(self.consts)
        print("The time limits for this system are:\n "
              "t0 = {}, t1 = {}, t_current = {}, step_size = {}".format(self.t0, self.t1, self.t, self.dt))

    def add_constants(self, **additional_constants):
        """Takes an arbitrary list of keyword arguments to add to the list of available constants.

        Variable-length arguments:
        additional_constants: A dict containing constants and their corresponding values."""
        self.consts.update({k: numpy.resize(additional_constants[k], self.dim) for k in additional_constants})
        self.symbols = set(smp.symbols(" ".join(["y_{}".format(i) for i in range(self.eqnum)]) + " t " + " ".join([k for k in self.consts])))
        self.equ = [smp.lambdify(self.symbols, i, "numpy", dummify=False) for i in self.equRepr]

    def remove_constants(self, **constants_removal):
        """Takes an arbitrary list of keyword arguments to remove from the list of available constants.

        Variable-length arguments:
        additional_constants: A tuple or list containing the names of the constants to remove.
                              The names must be denoted by strings."""
        for i in constants_removal:
            if i in self.consts.keys():
                del self.consts[i]

        self.symbols = set(smp.symbols(" ".join(["y_{}".format(i) for i in range(self.eqnum)]) + " t " + " ".join([k for k in self.consts])))
        self.equ = [smp.lambdify(self.symbols, i, "numpy", dummify=False) for i in self.equRepr]

    def set_dimensions(self, m=None):
        """Changes the dimensions of the system.

        Keyword arguments:
        m: Takes a tuple that describes the dimensions of the system. For example, to integrate 3d vectors one would
        pass (3,1)."""
        if m is not None:
            if isinstance(m, float):
                raise ValueError('The dimension of a system cannot be a float')
            elif isinstance(m, int):
                self.dim = (1, m,)
            else:
                if any([not isinstance(m_elem, int) for m_elem in m]):
                    raise ValueError("The dimensions of a system cannot contain a float")
                self.dim = tuple([1] + list(m))
            self.y = [numpy.resize(i, m) for i in self.y]
            solntime = self.soln[-1]
            self.soln = [[numpy.resize(i, m)] for i in self.soln[:-1]]
            self.soln.append(solntime)

    def get_dimensions(self):
        """Returns the dimensions of the current system in the form of a tuple of ints.

        Follows numpy convention so numpy dimensions and OdeSystem dimensions are interchangeable.
        """
        return self.dim

    def record_trajectory(self, b=None):
        """Sets whether or not the trajectory of the system will be recorded.

        Keyword arguments:
        b: A boolean value that denotes if the trajectory should be recorded.
           1 - implies record; 0 - implies don't record.
           If b is None, then this will return the current state of
           whether or not the trajectory is to be recorded"""
        if b is None:
            return self.traj
        else:
            self.traj = b

    def get_trajectory(self, var_names=tuple()):
        if isinstance(var_names, tuple):
            if len(var_names) == 0:
                return self.soln
            elif len(var_names) > 0:
                return [self.soln[int(i.split("_")[-1]) if isinstance(i, str) else i] for i in var_names]
        elif isinstance(var_names, str):
            return [self.soln[int(var_names.split("_")[-1])]]
        elif isinstance(var_names, int):
            return [self.soln[var_names]]
        else:
            raise TypeError("var_names should either be a tuple of variable names or a single variable name as a string!")

    def get_sample_times(self):
        return self.sample_times

    def reset(self, t=None):
        """Resets the system to a previous time.

        Keyword arguments:
        t: If specified after the system has recorded the trajectory of the system during integration, then this will
           revert to that time. Otherwise the reversion of the system will be to its state prior to integration."""
        if t is not None:
            if self.traj:
                k = numpy.array(self.soln[-1])
                ind = numpy.argmin(numpy.square(numpy.subtract(k, t)))
                for i, k in enumerate(self.soln):
                    self.soln[i] = list(numpy.delete(k, numpy.s_[ind + 1:], axis=0))
                self.t = t
            else:
                ischemes.deutil.warning('Trajectory has not been recorded for prior integration, cannot revert to t = {}\nPlease '
                        'call reset() and record trajectory by calling recordtraj() before integrating'.format(t))
        else:
            for i in range(self.eqnum):
                self.soln[i] = [self.y[i]]
            self.t = self.t0
            self.sample_times = [self.t]

    def integrate(self, t=None, callback=None):
        """Integrates the system to a specified time.

        Keyword arguments:
        t: If t is specified, then the system will be integrated to time t.
           Otherwise the system will integrate to the specified final time.
           NOTE: t can be negative in order to integrate backwards in time, but use this with caution as this
                 functionality is slightly unstable."""
        eta = self.eta
        if t:
            tf = t
        else:
            tf = self.t1
        steps = 0
        heff = [self.dt, self.dt]
        if numpy.sign(tf - self.t) != numpy.sign(self.dt):
            if numpy.sign(self.dt) != 0:
                heff = [-1.0 * i for i in heff]
            else:
                heff = [tf - self.dt for i in heff]
            self.dt = heff[0]
        while abs(heff[0]) > abs(tf - self.t):
            heff = [i * 0.5 for i in heff]
        heff.append(tf)
        time_remaining = [0, 0]
        vardict = {'t': self.t}
        vardict.update(self.consts)
        etaString = ''
        while heff[0] != 0 and heff[1] != 0 and abs(self.t) < abs(tf * (1 - 4e-16)):
            try:
                heff[1] = heff[0]
                if eta:
                    time_remaining[0] = time.perf_counter()
                if abs(heff[0] + self.t) > abs(tf):
                    heff[0] = (tf - self.t)
                try:
                    self.method(self.equ, vardict, self.soln, heff, self.relative_error_bound, self.eqnum)
                except etypes.RecursionError:
                    print("Hit Recursion Limit. Will attempt to compute again with a smaller step-size. "
                          "If this fails, either use a different relative error requirement or "
                          "increase maximum recursion depth. Can also occur if the initial value of all "
                          "variables is set to 0.")
                    heff[1] = heff[0]
                    heff[0] = 0.5 * heff[0]
                    self.method(self.equ, vardict, self.soln, heff, self.relative_error_bound, self.eqnum)
                except:
                    raise
                if heff[0] == 0:
                    heff[0] = (tf - self.t) * 0.5
                self.t = vardict['t']
                if self.traj:
                    self.sample_times.append(vardict['t'])
                else:
                    self.soln = [numpy.array([i[-1]]) for i in self.soln]
                    self.sample_times = [vardict['t']]
                if eta:
                    temp_time = 0.4 * time_remaining[1] + (((tf - self.t) / heff[0]) *
                                                           0.6 * (time.perf_counter() - time_remaining[0]))
                    if temp_time != 0 and numpy.abs(time_remaining[1]/temp_time - 1) > 0.2:
                        time_remaining[1] = temp_time
                    pLeft = round(1 - abs(tf - self.t) / abs(tf - self.t0), ndigits=3)
                    prevLen = len(etaString)
                    etaString = "{}% ----- ETA: {} -- Current Time and Step Size: {:.2e} and {:.2e}".format(
                                "{:.2%}".format(pLeft).zfill(7),
                                ischemes.deutil.convert_suffix(time_remaining[1]),
                                self.t, heff[0])
                    if prevLen > len(etaString):
                        print("\r" + " " * prevLen, end='\r')
                    print(etaString, end='\r')
                    sys.stdout.flush()
                steps += 1
                if callback is not None: callback(self)
            except KeyboardInterrupt:
                if raise_KeyboardInterrupt: raise
            except:
                raise
        if eta:
            sys.stdout.flush()
            print('\r' + ' ' * (shutil.get_terminal_size()[0] - 2), end='')
            print("\r100%")
        else:
            print("100%")
        self.t = self.sample_times[-1]
        self.dt = heff[0]
