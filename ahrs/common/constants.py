# -*- coding: utf-8 -*-
"""
Common constants used in AHRS and Geodesy
=========================================

- Constants are defined in SI Units (second, metre, kilogram) unless otherwise
  noted, or when constants are unitless.

References
----------
.. [1] World Geodetic System 1984. Its Definition and Relationships with Local
       Geodetic Systems. National Geospatial-Intelligence Agency (NGA)
       Standarization Document. 2014.
       (ftp://ftp.nga.mil/pub2/gandg/website/wgs84/NGA.STND.0036_1.0.0_WGS84.pdf)
.. [2] F. Chambat. Mean radius, mass, and inertia for reference Earth models.
       Physics of the Earth and Planetary Interiors Vol 124 (2001) p237–253.
.. [3] Archinal, B.A. et al. 2018. "Report of the IAU/IAG Working Group on
       cartographic coordinates and rotational elements: 2015" Celestial Mech.
       Dyn. Astr. 130:22.
       (https://link.springer.com/epdf/10.1007/s10569-017-9805-5)
.. [4] 2018 CODATA Recommended Values of the Fundamental Constants of Physics
       and Chemistry. NIST. June 2019.
       (https://physics.nist.gov/cuu/pdf/wallet_2018.pdf)
.. [5] 2014 CODATA Recommended Values of the Fundamental Constants of Physics
       and Chemistry. NIST. August 2015.
       (https://physics.nist.gov/cuu/pdf/wallet_2014.pdf)
.. [6] Ryan S. Park. Planets and Pluto: Physical Characteristics. NASA Jet
       Propulsion Laboratory. California Institute of Technology. 29th May 2020.
       (https://ssd.jpl.nasa.gov/?planet_phys_par)
.. [7] David R. Williams. Planetary Fact Sheet - Metric. NASA Goddard Space
       Flight Center. 21st October 2019.
       (https://nssdc.gsfc.nasa.gov/planetary/factsheet/)

"""
import numpy as np

# TRIGONOMETRY
M_PI = np.pi
DEG2RAD = np.pi/180.0
RAD2DEG = 180.0/np.pi

##### Geodetic constants as defined in WORLD GEODETIC SYSTEM 1984 (rev. 2014)
# Defining parameters
EARTH_EQUATOR_RADIUS = 6_378_137.0              # Semi-major axis of Earth (Equatorial Radius) [m]
EARTH_FLATTENING_INV = 298.257223563            # Flattening Factor of the Earth
EARTH_GM = 3.986004418e14                       # Earth's Gravitational Constant (Atmosphere included) [m^3/s^2]
EARTH_ROTATION = 7.292115e-5                    # Earth's Rotation rate [rad/s]
# Fundamental constants
LIGHT_SPEED = 2.99792458e8                      # Velocity of light in vacuum [m/s]
EARTH_ATMOSPHERE_MASS = 5.148e18                # Total mean mass of the Atmosphere (with water vapor) [kg]
DYNAMIC_ELLIPTICITY = 3.2737949e-3              # Dynamic Ellipticity (H)
# Universal Constant of Gravitation [m^3/(kg*s^2)]
UNIVERSAL_GRAVITATION_WGS84 = 6.67428e-11       # As defined in latest report of WGS 84
UNIVERSAL_GRAVITATION_CODATA2018 = 6.67430e-11  # As recommended by CODATA 2018 in latest report of NIST 2019
UNIVERSAL_GRAVITATION_CODATA2014 = 6.67408e-11  # As recommended by CODATA 2014 and referenced by NASA's Jet Propulsion Laboratory
EARTH_GM_GPSNAV = 3.9860050e14                  # Earth's Gravitational Constant for GPS Navigation Message [m^3/s^2]
# Derived geometric constants
EARTH_FLATTENING = 1/EARTH_FLATTENING_INV       # Earth's Flattening (reduced)
EARTH_POLAR_RADIUS = 6_356_752.3142             # Semi-minor axis of Earth (Polar Radius) [m]
EARTH_FIRST_ECCENTRICITY = 8.1819190842622e-2
EARTH_FIRST_ECCENTRICITY_2 = EARTH_FIRST_ECCENTRICITY**2
EARTH_SECOND_ECCENTRICITY = 8.2094437949696e-2
EARTH_SECOND_ECCENTRICITY_2 = EARTH_SECOND_ECCENTRICITY**2
EARTH_LINEAR_ECCENTRICITY = 5.2185400842339e5
EARTH_POLAR_CURVATURE_RADIUS = 6_399_593.6258   # Polar radius of Curvature [m]
EARTH_AXIS_RATIO = 9.96647189335e-1             # Axis ratio: EARTH_POLAR_RADIUS / EARTH_EQUATOR_RADIUS
EARTH_MEAN_RADIUS = 6_371_200.0                 # Earth's Arithmetic Mean radius [m] ((2*EQUATOR_RADIUS + POLAR_RADIUS) / 3)
EARTH_MEAN_AXIAL_RADIUS = 6_371_008.7714        # Mean Radius of the Three Semi-axes [m]
EARTH_AUTHALIC_RADIUS = 6_371_007.1810          # Radius of equal area sphere [m]
EARTH_EQUIVOLUMETRIC_RADIUS = 6_371_000.79      # Tadius of equal volume sphere [m] ((EQUATOR_RADIUS^2 * POLAR_RADIUS)^(1/3))
EARTH_C20_DYN = -4.84165143790815e-4            # Earth's Dynamic Second Degree Zonal Harmonic (C_2,0 dyn)
EARTH_C22_DYN = 2.43938357328313e-6             # Earth's Dynamic Second Degree Sectorial Harmonic (C_2,2 dyn)
EARTH_C20_GEO = -4.84166774985e-4               # Earth's Geographic Second Degree Zonal Harmonic
EARTH_J2 = 1.08263e-3                           # Earth's Dynamic Form Factor
# Derived physical constants
NORMAL_GRAVITY_POTENTIAL = 6.26368517146        # Normal Gravity Potential on the Ellipsoid [m^2/s^2]
EQUATORIAL_NORMAL_GRAVITY = 9.7803253359        # Normal Gravity at the Equator (on the ellipsoid) [m/s^2]
POLAR_NORMAL_GRAVITY = 9.8321849379             # Normal Gravity at the Pole (on the ellipsoid) [m/s^2]
MEAN_NORMAL_GRAVITY = 9.7976432223              # Mean Normal Gravity [m/s^2]
SOMIGLIANA_GRAVITY = 1.931852652458e-3          # Somigliana's Formula Normal Gravity constant
NORMAL_GRAVITY_FORMULA = 3.449786506841e-3      # Normal Gravity Formula constant (EARTH_ROTATION^2 * EQUATOR_RADIUS^2 * POLAR_RADIUS / EARTH_GM)
EARTH_MASS = 5.9721864e24                       # Earth's Mass (Atmosphere inclulded) [kg]
EARTH_GM_1 = 3.986000982e14                     # Geocentric Gravitational Constant (Atmosphere excluded) [m^3/s^2]
EARTH_GM_2 = 3.4359e8                           # Gravitational Constant of the Earth’s Atmosphere [m^3/s^2]

EARTH_SIDEREAL_DAY = 86164.09053083288          # Earth's duration of sidereal day [s]
##### Planetary Characteristics (without Earth)
MOON_EQUATOR_RADIUS = 1_738_100.0
MOON_POLAR_RADIUS = 1_736_000.0
MOON_MASS = 7.346e22
MOON_GM = MOON_MASS*UNIVERSAL_GRAVITATION_CODATA2018
MOON_ROTATION = 1.109027709148159e-7            # Inferred from [7]
MOON_J2 = 2.027e-4                              # As defined in [7]
MERCURY_EQUATOR_RADIUS = 2_440_530.0            # As defined in [6]
MERCURY_POLAR_RADIUS = 2_438_260.0
MERCURY_ROTATION = 1.2399326882596827e-6        # Inferred from [7]
MERCURY_MASS = 3.30114e23                       # As defined in [6]
MERCURY_GM = MERCURY_MASS*UNIVERSAL_GRAVITATION_CODATA2018
MERCURY_J2 = 5.03e-5                            # As defined in [7]
VENUS_EQUATOR_RADIUS = 6_051_800.0              # As defined in [6]
VENUS_POLAR_RADIUS = 6_051_800.0
VENUS_ROTATION = -2.9923691869737844e-7         # Inferred from [7]
VENUS_MASS = 4.86747e24
VENUS_GM = VENUS_MASS*UNIVERSAL_GRAVITATION_CODATA2018
VENUS_J2 = 4.458e-6                             # As defined in [7]
MARS_EQUATOR_RADIUS = 3_396_190.0               # As defined in [6]
MARS_POLAR_RADIUS = 3_376_200.0
MARS_ROTATION = 7.088235959185674e-5
MARS_MASS = 6.41712e23
MARS_GM = MARS_MASS*UNIVERSAL_GRAVITATION_CODATA2018
MARS_J2 = 1.96045e-3                            # As defined in [7]
JUPITER_EQUATOR_RADIUS = 71_492_000.0           # As defined in [6]
JUPITER_POLAR_RADIUS = 66_854_000.0
JUPITER_ROTATION = 1.758518138029551e-4         # Inferred from [7]
JUPITER_MASS = 1.898187e27
JUPITER_GM = JUPITER_MASS*UNIVERSAL_GRAVITATION_CODATA2018
JUPITER_J2 = 1.4736e-2                          # As defined in [7]
SATURN_EQUATOR_RADIUS = 60_268_000.0            # As defined in [6]
SATURN_POLAR_RADIUS = 54_364_000.0
SATURN_ROTATION = 1.637884057802486e-4          # Inferred from [7]
SATURN_MASS = 5.683174e26
SATURN_GM = SATURN_MASS*UNIVERSAL_GRAVITATION_CODATA2018
SATURN_J2 = 1.6298e-2                           # As defined in [7]
URANUS_EQUATOR_RADIUS = 25_559_000.0            # As defined in [6]
URANUS_POLAR_RADIUS = 24_973_000.0
URANUS_ROTATION = -1.012376653716682e-4         # Inferred from [7]
URANUS_MASS = 8.68127e25
URANUS_GM = URANUS_MASS*UNIVERSAL_GRAVITATION_CODATA2018
URANUS_J2 = 3.343430e-3                         # As defined in [7]
NEPTUNE_EQUATOR_RADIUS = 24_764_000.0           # As defined in [6]
NEPTUNE_POLAR_RADIUS = 24_341_000.0
NEPTUNE_ROTATION = 1.083382527619075e-4         # Inferred from [7]
NEPTUNE_MASS = 1.024126e26
NEPTUNE_GM = NEPTUNE_MASS*UNIVERSAL_GRAVITATION_CODATA2018
NEPTUNE_J2 = 3.411e-3                           # As defined in [7]
PLUTO_EQUATOR_RADIUS = 1_188_300.0              # As defined in [6]
PLUTO_POLAR_RADIUS = 1_188_300.0
PLUTO_ROTATION = -1.138559183467410e-05         # Inferred from [7]
PLUTO_MASS = 1.303e22
PLUTO_GM = PLUTO_MASS*UNIVERSAL_GRAVITATION_CODATA2018

##### Local information
MUNICH_LATITUDE = 48.137154
MUNICH_LONGITUDE = 11.576124
MUNICH_HEIGHT = 519.0
