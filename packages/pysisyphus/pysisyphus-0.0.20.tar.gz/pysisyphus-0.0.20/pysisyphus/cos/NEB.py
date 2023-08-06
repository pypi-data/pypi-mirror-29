#!/usr/bin/env python3

from multiprocessing import Pool

import numpy as np

from pysisyphus.cos.ChainOfStates import ChainOfStates

# [1] http://aip.scitation.org/doi/pdf/10.1063/1.1323224
#     10.1063/1.1323224
# [2] http://onlinelibrary.wiley.com/doi/10.1002/jcc.20780/pdf
#     10.1002/jcc.20780
# https://github.com/cstein/neb/blob/master/neb/neb.py


class NEB(ChainOfStates):

    def __init__(self, images, variable_springs=False,
                 k_max=0.3, k_min=0.01, **kwargs):
        super(NEB, self).__init__(images, **kwargs)

        assert(k_max > k_min), "k_max has to be bigger than k_min!"
        self.variable_springs = variable_springs
        self.k_max = k_max
        self.k_min = k_min

        self.climb = False
        self.delta_k = self.k_max - self.k_min
        self.k = list()

        self.perp_forces = list()
        self.par_forces = list()

    def update_springs(self):
        self.k = np.full(len(self.images)-1, self.k_min)

    def set_variable_springs(self):
        shifted_energies = self.energy - self.energy.min()
        energy_max = max(shifted_energies)
        energy_ref = .85 * energy_max
        for i in range(len(self.k)):
            # The ith spring connects images i-1 and i.
            e_i = i + 1
            ith_energy = max(shifted_energies[e_i], shifted_energies[e_i-1])
            if ith_energy < energy_ref:
                self.k[i] = self.k_min
            else:
                self.k[i] = (self.k_max - self.delta_k
                             * (energy_max - ith_energy)
                             / (energy_max - energy_ref)
                )
        self.log("updated springs: " + self.fmt_k())

    def fmt_k(self):
        return ", ".join([str(f"{k:.03f}") for k in self.k])

    @property
    def parallel_forces(self):
        indices = range(len(self.images))
        par_forces = [self.get_parallel_forces(i) for i in indices]
        return np.array(par_forces).flatten()

    def get_parallel_forces(self, i):
        # Check if there are enough springs
        if (len(self.k) is not len(self.images)-1):
            self.update_springs()

        if i not in self.moving_indices:
            return self.zero_vec

        if (i is 0) or (i is len(self.images) - 1):
            # We can't use the last image index because there is one
            # spring less than there are images.
            spring_index = min(i, len(self.images)-2)
            return self.k[spring_index] * self.get_tangent(i)

        prev_coords = self.images[i-1].coords
        ith_coords = self.images[i].coords
        next_coords = self.images[i+1].coords
        return (self.k[i] * (np.linalg.norm(next_coords-ith_coords)
                             - np.linalg.norm(ith_coords-prev_coords)
               ) * self.get_tangent(i)
        )

    def get_climbing_forces(self, ind):
        climbing_image = self.images[ind]
        ci_forces = climbing_image.forces
        tangent = self.get_tangent(ind)
        climbing_forces = ci_forces - 2*ci_forces.dot(tangent)*tangent

        return climbing_forces, climbing_image.energy

    def par_calc(self, i):
        image = self.images[i]
        image.calc_energy_and_forces()
        return image

    # See https://stackoverflow.com/a/15786149
    # This way we can reuse the parents setter.
    @ChainOfStates.forces.getter
    def forces(self):
        indices = range(len(self.images))

        if self._forces is None:
            # Parallel calculation
            if self.parallel > 0:
                with Pool(processes=self.parallel) as pool:
                    image_number = len(self.images)
                    par_images = pool.map(self.par_calc, range(image_number))
                    self.images = par_images
            # Serial calculation
            else:
                [image.calc_energy_and_forces() for image in self.images]
            self.counter += 1

        # Index of the highest energy image (HEI)
        hei_index = np.argmax([image.energy for image in self.images])

        move_inds = self.moving_indices
        # Don't climb it not yet enabled or requested.
        if not self.climb:
            climb_indices = tuple()
        # We can do two climbing (C2) neb if the highest energy image (HEI)
        # is in moving_indices but not the first or last item in this list.
        elif hei_index in move_inds[1:-1]:
            climb_indices = (hei_index-1, hei_index+1)
        # Do one image climbing (C1) neb if the HEI is the first or last
        # item in moving_indices.
        elif (hei_index == 1) or (hei_index == move_inds[-1]):
            climb_indices = (hei_index, )
        # Don't climb when the HEI is the first or last image of the whole
        # NEB.
        else:
            climb_indices = tuple()
            self.log("Want to climb but can't. HEI is first or last image!")

        total_forces = list()
        for i in indices:
            if i in climb_indices:
                climb_forces, climb_en = self.get_climbing_forces(i)
                self.log(f"climbing with image {i}, E = {climb_en:.6f} au")
                total_forces.append(climb_forces)
            else:
                par_forces = self.get_parallel_forces(i)
                perp_forces = self.get_perpendicular_forces(i)
                total_forces.append(par_forces + perp_forces)

        self._forces = np.array(total_forces).flatten()

        return self._forces
