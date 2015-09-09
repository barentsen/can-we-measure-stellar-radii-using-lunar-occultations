"""
This script determines whether a 450 Hz camera can observe multiple frames
during the partial occulation of a star by the moon.

If the begin and end time of a partial occultation could be measured accurately,
it could be used to determine the radius of the star and hence the radius of
its transiting planets.
"""
import numpy as np

import matplotlib.pyplot as pl

import astropy.units as u
from astropy import log


LUNAR_PERIOD = 27.3 * u.day
LUNAR_RADIUS = 1737.4 * u.km
LUNAR_DISTANCE = 384472 * u.km

RADII_MIN, RADII_MAX = 0.1, 30
DISTANCE_MIN, DISTANCE_MAX = 1, 100


def angular_diameter(radius, distance):
    """Returns the apparent (angular) diameter of an object on the sky [arcsec],
    given its intrinsic radius and distance.

    Parameters
    ----------
    radius : astropy `Quantity` object
    distance : astropy `Quantity` object

    Returns
    -------
    angular_diameter : astropy `Quantity` object
        apparent diameter in arcseconds
    """
    result = 2 * np.arctan2(2 * radius, 2. * distance)
    return result.to(u.arcsec)


def angular_speed_of_the_moon():
    """Returns the angular speed of the moon in the sky, relative to the stars."""
    return (360.*u.deg / LUNAR_PERIOD).to(u.arcsec / u.second)


if __name__ == '__main__':
    log.info("The moon moves at {:.2f}".format(angular_speed_of_the_moon()))
    log.info("The apparent diameter of the moon is {:.2f}".format(angular_diameter(LUNAR_RADIUS, LUNAR_DISTANCE)))

    radii = np.linspace(RADII_MIN, RADII_MAX, 100) * u.solRad
    distances = np.linspace(DISTANCE_MIN, DISTANCE_MAX, 100) * u.pc
    grid = np.meshgrid(radii, distances)

    durations = angular_diameter(grid[0], grid[1]) / angular_speed_of_the_moon()
    hz_for_10_samples = 450 * durations.value

    pl.figure()
    pl.imshow(hz_for_10_samples,
              extent=(RADII_MIN, RADII_MAX, DISTANCE_MIN, DISTANCE_MAX),
              origin="lower",
              aspect="auto",
              vmin=0, vmax=10,    
              interpolation="nearest",
              label="duration [s]",
              cmap="ocean_r")
    cbar = pl.colorbar()
    cbar.ax.set_ylabel("# Frames", fontsize=20)
    pl.xlabel("Stellar radius [sol rad]", fontsize=20)
    pl.ylabel("Distance to the star [pc]", fontsize=20)
    pl.legend()
    pl.title("# Frames obtained by a 450 Hz camera during\n"
             "the partial occulation of a star by the moon",
             fontsize=20)
    pl.tight_layout()
    pl.savefig("the-answer.pdf")
    pl.close()
