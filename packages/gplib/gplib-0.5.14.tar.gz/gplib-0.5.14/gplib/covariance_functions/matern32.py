# -*- coding: utf-8 -*-
#
#    Copyright 2018 Ibai Roman
#
#    This file is part of GPlib.
#
#    GPlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GPlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GPlib. If not, see <http://www.gnu.org/licenses/>.

import numpy as np

from .stationary_function import StationaryFunction
from ..parameters import OptimizableParameter
from ..transformations import LogTransformation

SQRT_3 = np.sqrt(3.0)


class Matern32(StationaryFunction):
    """

    """
    def __init__(self, data, is_ard):
        hyperparams = [
            OptimizableParameter(
                'output_variance2', LogTransformation,
                default_value=np.std(data['Y']),
                min_value=np.exp(-10), max_value=np.exp(10)
            )
        ]

        super(Matern32, self).__init__(data, is_ard, hyperparams)

    def stationary_function(self, sq_dist):
        """
        It applies the Matern (v=3/2) kernel function
        element-wise to the distance matrix.

        .. math::
            k_{M32}(r)=(1+\dfrac{\sqrt{3}r}{l}) exp (-\dfrac{\sqrt{3}r}{l})

        :param sq_dist: Distance matrix
        :param hyperparams:
        :return: Result matrix with kernel function applied element-wise.
        """
        dist = np.sqrt(sq_dist)
        return np.multiply((1 + SQRT_3*dist), np.exp(-SQRT_3*dist)) * \
            self.get_param_value('output_variance2')

    def dkr_dx(self, sq_dist, dr_dx):
        """
        Measures gradient of the kernel function in X.

        :param sq_dist: Square distance
        :param dr_dx:
        :return: 3D array with the gradient of the kernel function in every
         dimension of X.
        """
        dist = np.sqrt(sq_dist)
        grad_r2 = -1.5 * np.exp(-SQRT_3 * dist)
        result = grad_r2[:, :, np.newaxis] * dr_dx
        return result * self.get_param_value('output_variance2')

    def dkr_dtheta(self, sq_dist, dr_dtheta):
        """
        Measures gradient of the kernel function in the
        hyper-parameter space.

        :param sq_dist: Square distance
        :param dr_dtheta:
        :return: 3D array with the gradient of the kernel function in every
         dimension the length-scale hyper-parameter space.
        """
        dist = np.sqrt(sq_dist)
        grad_r2 = -1.5 * np.exp(-SQRT_3 * dist)
        return np.multiply((1 + SQRT_3 * dist), np.exp(-SQRT_3 * dist)), \
            grad_r2[:, :, np.newaxis] * \
            dr_dtheta * self.get_param_value('output_variance2')
