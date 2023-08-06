#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

from pysisyphus.helpers import fit_rigid, procrustes
from pysisyphus.optimizers.Optimizer import Optimizer

# [1] Nocedal, Wright - Numerical Optimization, 2006

class BFGSnb(Optimizer):

    def __init__(self, geometry, alpha=1.0, **kwargs):
        super(BFGSnb, self).__init__(geometry, **kwargs)

        self.alpha = alpha
        self.eye = np.eye(self.geometry.coords.size)
        self.inv_hessian = self.eye.copy()

    def reset_hessian(self):
        self.inv_hessian = self.eye.copy()
        self.log("Resetted hessian")

    def prepare_opt(self):
        procrustes(self.geometry)
        # Calculate initial forces before the first iteration
        self.coords.append(self.geometry.coords)
        self.forces.append(self.geometry.forces)
        self.energies.append(self.geometry.energy)

    def optimize(self):
        last_coords = self.coords[-1]
        last_forces = self.forces[-1]
        last_energy = self.energies[-1]

        unscaled_steps = self.inv_hessian.dot(last_forces)
        steps = self.scale_by_max_step(self.alpha*unscaled_steps)

        new_coords = last_coords + steps
        self.geometry.coords = new_coords
        #(last_coords, last_forces), self.inv_hessian = fit_rigid(
        #                                                self.geometry,
        #                                                (last_coords,
        #                                                 last_forces),
        #                                                 self.inv_hessian)

        new_forces = self.geometry.forces
        new_energy = self.geometry.energy

        # Because we add the step later on we restore the original
        # coordinates and set the appropriate energies and forces.
        self.geometry.coords = last_coords
        self.geometry.forces = new_forces
        self.geometry.energy = new_energy

        self.forces.append(new_forces)
        self.energies.append(new_energy)
        # [1] Eq. 6.5, gradient difference
        y = -(new_forces - last_forces)
        sigma = new_coords - last_coords
        # [1] Eq. 6.7, curvature condition
        curv_cond = sigma.dot(y)
        if curv_cond < 0:
            self.log(f"curvature condition {curv_cond:.07} < 0!")
        rho = 1.0 / y.dot(sigma)
        if ((np.array_equal(self.inv_hessian, self.eye))
            # When align = True the above expression will evaluate to
            # False. So we also check if we are in the first iteration.
            or (self.cur_cycle == 0)):
            beta = y.dot(sigma)/y.dot(y)
            self.inv_hessian = self.eye*beta
            self.log(f"Using initial guess for inverse hessian, beta={beta}")
        # Inverse hessian update
        A = self.eye - np.outer(sigma, y) * rho
        B = self.eye - np.outer(y, sigma) * rho
        self.inv_hessian = (A.dot(self.inv_hessian).dot(B)
                            + np.outer(sigma, sigma) * rho)

        return steps
