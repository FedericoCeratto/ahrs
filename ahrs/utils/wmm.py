"""
World Magnetic Model
====================

The main utility of the World Magnetic Model (WMM) is to provide magnetic
declination for any desired location on the globe.

In addition to the magnetic declination, the WMM also provides the complete
geometry of the field from 1 km below the World Geodetic System (WGS 84)
ellipsoid surface to approximately 850 km above it. The magnetic field extends
deep into the Earth and far out into space, but the WMM is not valid at these
extremes.

The strongest contribution to Earth's magnetism is the magnetic field produced
by the Earth’s liquid-iron outer core, called the "core field". Magnetic
minerals in the crust and upper mantle make a further contribution that can be
locally significant. All these fields of "internal" origin and their large
scale components are included in the WMM.

"External" magnetic fields, arising from electric currents in the upper
atmosphere and near-Earth space, are time-varying and produce secondary
magnetic fields, which are not represented in the WMM.

The mathematical method of the WMM is an expansion of the magnetic potential
into spherical harmonic functions to degree and order 12.

The secular variation (SV) is the yearly change of the core field, which is
also accounted in the WMM by a linear model. Due to unpredictable changes in
the core field, the values of the WMM coefficients are updated every five
years. The most recent version is valid from 2020 to 2024.

The geomagnetic field vector B is described by 7 elements:

+---------+-----------------------------------------------+--------+----------------+
|         |                                               |        | Range          |
| Element | Definition                                    | Units  +--------+-------+
|         |                                               |        | Min    | Max   |
+=========+===============================================+========+========+=======+
| X       | Northerly intensity                           | nT     | -17000 | 43000 |
| Y       | Easterly intensity                            | nT     | -18000 | 17000 |
| Z       | Vertical intensity (Positive downwards)       | nT     | -67000 | 62000 |
| H       | Horizontal intensity                          | nT     |      0 | 43000 |
| F       | Total intensity                               | nT     |  23000 | 67000 |
| I       | Inclination angle (a.k.a. dip angle)          | degree |    -90 | 90    |
| D       | Declination angle (a.k.a. magnetic variation) | degree |   -180 | 180   |
+---------+-----------------------------------------------+--------+--------+-------+

The quantities X, Y and Z are perpendicular vectors and can be used to
determine the quantities F, I and D, and viceversa.

The vertical direction is perpendicular to the horizontal plane of the WGS 84
ellipsoid model of the Earth.

At a location on the plane of a chosen horizontal coordinate system, grivation
is the angle between grid north and magnetic north, i.e., the angle measured
clockwise from the direction parallel to the grid's Northing axis to the
horizontal component of the magnetic field at the observer's location.

Grivation is useful for local surveys, where location is given by grid
coordinates rather than by longitude and latitude. It is dependent on the map
projection used to define the grid coordinates. In general, it is estimated as:

    GV = D - C

where C is the "convergence-of-meridians" defined as the clockwise angle from
the northward meridional arc to the grid Northing direction.

The WMM requires a set of time-dependent Gauss coefficients to estimate the
magnetic field elements. These coefficients are provided by the NCEI
Geomagnetic Modeling Team and British Geological Survey in a file with
extension COF.

The WMM was developed jointly by the National Centers for Environmental
Information (NCEI, Boulder CO, USA) (formerly National Geophysical Data Center
(NGDC)) and the British Geological Survey (BGS, Edinburgh, Scotland). As part
of the regular update cycle of the World Magnetic Model both institutions have
released the latest model on December 10th, 2019.

This script is based on the originally conceived one by Christopher Weiss
(cmweiss@gmail.com), who adapted it from the geomagc software and World
Magnetic Model of the NOAA Satellite and Information Service, National
Geophysical Data Center.

License
-------
The WMM source code and binaries are in the public domain and not licensed or
under copyright. The information and software may be used freely by the public.
As required by 17 U.S.C. 403, third parties producing copyrighted works
consisting predominantly of the material produced by U.S. government agencies
must provide notice with such work(s) identifying the U.S. Government material
incorporated and stating that such material is not subject to copyright
protection.

References
----------
.. [1] The World Magnetic Model (https://www.ngdc.noaa.gov/geomag/WMM/DoDWMM.shtml)
.. [2] Chulliat, A., W. Brown, P. Alken, C. Beggan, M. Nair, G. Cox, A. Woods,
    S. Macmillan, B. Meyer and M. Paniccia, The US/UK World Magnetic Model for
    2020­-2025: Technical Report, National Centers for Environmental
    Information, NOAA, doi:10.25923/ytk1-yx35, 2020.
    (https://www.ngdc.noaa.gov/geomag/WMM/data/WMM2020/WMM2020_Report.pdf)
.. [3] WMM2020 Model values: NCEI Geomagnetic Modeling Team and British
    Geological Survey. 2019. World Magnetic Model 2020. NOAA National Centers
    for Environmental Information. doi: 10.25921/11v3-da71, 2020.
.. [4] Christopher Weiss' GeoMag repository (https://github.com/cmweiss/geomag)
.. [5] World Geodetic System 84 (https://en.wikipedia.org/wiki/World_Geodetic_System#A_new_World_Geodetic_System:_WGS_84)
.. [6] W. A. Heiskanen and H. Moritz. Physical Geodesy. TU Graz reprint. 1993.
.. [7] R. A. Langel and W. J. Hinze. The Magnetic Field of Earth's Lithosphere:
    The Satellite Perspective. Cambridge University Press. 1998.
.. [8] A. Muksin and R. Triharjanto. Implementing the 2015-2020 Earth's
    Geomagnetic Model for Satellite Simulator Base on 12th Generation Data.
.. [9] L. Tauxe. Essentials of Paleomagnetism: Fifth Web Edition. Scripps
    Institution of Oceanography. (https://earthref.org/MagIC/books/Tauxe/Essentials/)
.. [10] James R. Wertz. Spacecraft Attitude Determination and Control. Kluwer
    Academics. 1978.

"""

import unittest
import datetime
import numpy as np

EQUATOR_RADIUS = 6_378_137.0      # Semi-major radius of Earth, in meters (Equatorial Radius)
POLAR_RADIUS = 6_356_752.314245   # Semi-minor radius of Earth, in meters (Polar Radius)
MEAN_EARTH_RADIUS = 6_371_200     # Mean of Earth's radii, in meters
DEG2RAD = np.pi/180.0
RAD2DEG = 180.0/np.pi

def geodetic2spherical(lat, lon, h, a: float = EQUATOR_RADIUS/1000.0, b: float = POLAR_RADIUS/1000.0) -> tuple:
    """Transform geodetic coordinates into spherical geocentric coordinates

    The transformation cannot be a simple cylindric to spherical conversion, as
    we must also consider a planet's ellipsoid form. With the aid of its
    pre-defined flatness and eccentricity, we can better approximate the values
    of the conversion.

    In this function the Earth's major and minor semi-axis are considered.
    However, we can convert the coordinates of different ellipsoidal bodies, by
    giving the dimensions of its semi-axes.

    Notice that the longitude between both systems remains the same.

    Parameters
    ----------
    lat : float
        Latitude, in radians, of point in geodetic coordinates
    lon : float
        Longitude, in radians, of point in geodetic coordinates
    h : float
        Height, in kilometers, of point in geodetic coordinates
    a : float, default: 6378.137
        Major semi-axis dimension, in kilometers. Defaults to Earth's equatorial radius
    b : float, default: 6356.752314245
        Minor semi-axis dimension, in kilometers. Defaults to Earth's polar radius

    Returns
    -------
    lat_spheric : float
        Latitude of point in spherical coordinates.
    lon : float
        Longitue of point in spherical coordinates. Same as geodetic.
    r : float
        Radial distance of point in spherical coordinates.
    """
    # Transform geodetic coordinates into spherical geocentric coordinates
    f = (a-b)/a                             # Flatness
    e2 = f*(2.0-f)                          # First Eccentricity
    #########
    Rc = a/np.sqrt(1.0-e2*np.sin(lat)**2)   # Radius of curvature of prime vertical
    rho = (Rc+h)*np.cos(lat)
    z = (Rc*(1-e2)+h)*np.sin(lat)
    r = np.linalg.norm([rho, z])            # Radial distance
    lat_spheric = np.arcsin(z/r)            # Spherical latitude
    return lat_spheric, lon, r

class WMM:
    """Top class for the World Magnetic Model

    This class is mainly used to compute all elements of the World Magnetic
    Model (WMM) at a given point.

    The main magnetic field :math:`B_m` is a potential field written in
    geocentric spherical coordinates (longitude, latitude and radius) as
    the negative spatial gradient of a scalar potential. This potential can
    be expanded in terms of spherical harmonics:

    .. math::

        V(\\lambda, \\phi', r, t) = a\\sum_{n=1}^{N}(\\frac{a}{r})^{n+1}\\sum_{m=0}^{n}f(n, m, \\lambda, t)P_n^m(\\phi')

    where

    .. math::

        f(n, m, \\lambda, t) = g_n^m(t) \\cos(m\\lambda) + h_n^m(t) \\sin(m\\lambda)

    and the Schmidt semi-normalized associated Legendre functions :math:`P_n^m(\\phi')`
    are defined as:

        P_n^m(\\mu) = \\left\\{
        \\begin{array}{ll}
            \\sqrt{2\\frac{(n-m)!}{(n+m)!}}P_{n, m}(\\mu) & \\mathrm{if} m > 0
            \\P_{n, m}(\\mu) & \\mathrm{if} m = 0
        \\end{array}
        \\right.

    with :math:`P_{n, m}(\\mu) = (-1)^m P_n^m(\\mu)`

    Attributes
    ----------
    date : datetime.date, default: datetime.date.today()
        Desired date to estimate
    date_dec : float
        Desired date to estimate as decimal.
    epoch : float
        Initial time of model in decimal years.
    model : str
        WMM Model identificator
    modeldate : str
        Release date of the WMM Model

    Examples
    --------
    >>> wmm = WMM()         # Magnetic model today (Mid May 2020)
    >>> wmm.magnetic_field(10.0, -20.0)      # latitude = 10 deg, longitude = -20 deg
    >>> wmm.D               # Magnetic declination [degrees]
    -9.122361367239034
    >>> wmm.magnetic_field(10.0, -20.0, h=10.5)     # 10.5 km above sea level
    >>> wmm.D
    -9.128404039098971
    >>> wmm.magnetic_field(10.0, -20.0, h=10.5, date=datetime.date(2017, 5, 12))    # on 12th May, 2017
    >>> wmm.D
    -9.73078560629778

    All other main values are also computed (including grivation)

    >>> wmm.X           # Northerly intensity [nT]
    30499.640469609083
    >>> wmm.Y           # Easterly intensity [nT]
    -5230.267158472566
    >>> wmm.Z           # Vertical intensity [nT]
    -1716.633311360368
    >>> wmm.H           # Horizontal intensity [nT]
    30944.850352270452
    >>> wmm.F           # Total intensity [nT]
    30992.427998627096
    >>> wmm.I           # Inclination angle [nT]
    -3.1751692563622993
    >>> wmm.GV          # Grivation [degrees]
    -9.73078560629778

    """
    def __init__(self, date: datetime.date = None):
        """
        Parameters
        ----------
        date : datetime.date, int or float, default: present day
            Date of desired magnetic field estimation.
        """
        self.reset_coefficients(date)

    def reset_coefficients(self, date: datetime.date = None) -> None:
        """Reset Gauss coefficients to given date

        Parameters
        ----------
        date : datetime.date, int or float, default: current day
            Date of desired magnetic field estimation.
        """
        self.set_date(date)
        self.__dict__.update(self.get_properties(self.wmm_filename))
        self.c, self.cd = self.load_coefficients(self.wmm_filename)
        self.dims = len(self.c)
        self.denormalize_coefficients()

    def load_coefficients(self, cof_file: str) -> tuple:
        """Return model coefficients in NumPy array

        The model coefficients, also referred to as Gauss coefficients, are
        listed in a COF file. These coefficients can be used to copmute values
        for the fields elements and their annual rates of change at any
        location near the surface of the Earth.

        The COF file has 6 columns:

        1 : `n` is the degree.
        2 : `m` is the order.
        3 : `g` is a time-dependent Gauss coefficient of degree `n` and order `m`.
        4 : `h` is a time-dependent Gauss coefficient of degree `n` and order `m`.
        5 : `gd` is a secular variation coefficient.
        6 : `hd` is a secular variation coefficient.

        The units are nT for the main field, and nT per year for the secular
        variation.

        The Gauss coefficients :math:`g_n^m(t_0)`, :math:`h_n^m(t_0)`, :math:`\\dot{g}_n^m(t_0)`
        and :math:`\\dot{h}_n^m(t_0)` are defined for a time :math:`t` as:

        .. math::

            \\begin{eqnarray}
            g_n^m(t) & = & g_n^m(t_0) + (t-t_0) \\dot{g}_n^m(t_0) \\\\
            h_n^m(t) & = & h_n^m(t_0) + (t-t_0) \\dot{h}_n^m(t_0)
            \\end{eqnarray}

        where time is given in decimal years and :math:`t_0` corresponds to the
        epoch read from the corresponding COF file.

        Parameters
        ----------
        cof_file : str
            Path to COF file with the coefficients of the WMM

        Returns
        -------
        data : NumPy array
            N-by-6 array with the WMM coefficients.

        """
        if not cof_file.endswith(".COF"):
            raise TypeError("File must have extension 'COF'")
        data = np.genfromtxt(cof_file, comments="999999", skip_header=1)
        maxord = int(data[-1, 0])
        dims = maxord+1

        c = np.zeros((dims, dims))
        cd = np.zeros((dims, dims))
        for row in data:
            n, m = row[:2].astype(int)
            c[m, n] = row[2]           # g_n^m
            cd[m, n] = row[4]          # g_n^m secular
            if m != 0:
                c[n, m-1] = row[3]     # h_n^m
                cd[n, m-1] = row[5]    # h_n^m secular
        return c, cd

    def get_properties(self, cof_file: str) -> dict:
        """Return dictionary of WMM properties from COF file

        Three properties are read and return in a dictionary:

        1. `epoch` is the initial time t_0 as a float.
        2. `model` is the lustrum model used for the period to estimate.
        3. `modeldate` is the desired date for magnetic properties to estimate.

        Parameters
        ----------
        cof_file : str
            Path to COF file with the coefficients of the WMM

        Returns
        -------
        properties : dictionary
            Dictionary with the three WMM properties.

        """
        if not cof_file.endswith(".COF"):
            raise TypeError("File must have extension 'COF'")
        with open(cof_file, 'r') as f:
            line = f.readline()
        v = line.strip().split()
        properties = dict(zip(["model", "modeldate"], v[1:]))
        properties.update({"epoch": float(v[0])})
        return properties

    def set_date(self, date: datetime.date) -> None:
        """Set date to use with the model.

        Set the WMM to a given date. This date can be given as an instance of
        `datetime.date` or as a decimalized date of the format `YYYY.d`, where
        the value `d` is the fraction of the year.

        If None is given it sets the date to the current day. In addition, the
        corresponding COF file is also set.

        Parameter
        ---------
        date : datetime.date, int or float, default: current day
            Date of desired magnetic field estimation.
        """
        if date is None:
            self.date = datetime.date.today()
            self.date_dec = self.date.year + self.date.timetuple().tm_yday/365.0
        if isinstance(date, (int, float)):
            self.date_dec = float(date)
            self.date = datetime.date.fromordinal(round(datetime.date(int(date), 1, 1).toordinal() + (self.date_dec-int(self.date_dec))*365))
        if isinstance(date, datetime.date):
            self.date = date
            self.date_dec = self.date.year + self.date.timetuple().tm_yday/365.0
        if self.date.year < 2015:
            raise ValueError("No available coefficients for dates before 2015.")
        self.wmm_filename = './WMM2015/WMM.COF' if self.date_dec < 2020.0 else './WMM2020/WMM.COF'

    def denormalize_coefficients(self) -> None:
        """Denormalize Schmidt Gauss coefficients
        """
        snorm = np.identity(self.dims)
        self.k = np.zeros((self.dims, self.dims))
        for n in range(1, self.dims):
            snorm[0, n] = snorm[0, n-1]*(2.0*n-1)/n
            j = 2.0         # Kronecker delta
            for m in range(n+1):
                self.k[m, n] = ((n-1)**2-m**2) / ((2*n-1)*(2*n-3))
                if m>0:
                    snorm[m, n] = snorm[m-1, n] * np.sqrt(j*(n-m+1.0)/(n+m))
                    self.c[n, m-1] *= snorm[m, n]
                    self.cd[n, m-1] *= snorm[m, n]
                    j = 1.0
                self.c[m, n] *= snorm[m, n]
                self.cd[m, n] *= snorm[m, n]

    def magnetic_field(self, lat: float, lon: float, h: float = 0.0, date = datetime.date.today()) -> None:
        """Calculate the magnetic field elements for a single point.

        This method will estimate the following attributes:

        - X : Northerly intensity [nT]
        - Y : Easterly intensity [nT]
        - Z : Vertical intensity (Positive downwards) [nT]
        - H : Horizontal intensity [nT]
        - F : Total intensity [nT]
        - I : Inclination angle (a.k.a. dip angle) [deg]
        - D : Declination angle (a.k.a. magnetic variation) [deg]
        - GV : Grivation [deg]

        The code includes comments with references to equation numbers
        corresponding to the ones in the official report.

        Parameters
        ----------
        dlat : float
            Latitude in decimal degrees
        dlan : float
            Longitude in decimal degrees
        h : float, default: 0.0
            Mean Sea Level Height in kilometers
        date : datetime.date, default: datetime.date.today()
            Desired date to estimate
        """
        if date is not None:
            self.reset_coefficients(date)
        self.latitude = lat
        self.longitude = lon
        lat *= DEG2RAD
        lon *= DEG2RAD
        # Transform geodetic coordinates into spherical geocentric coordinates
        lat_prime, lon, radius = geodetic2spherical(lat, lon, h)
        # Compute cos(m*phi') and sin(m*phi') for all m values
        self.sp = np.zeros(self.dims)                   # sin(m*phi')
        self.cp = np.ones(self.dims+1)                  # cos(m*phi')
        self.sp[1] = np.sin(lon)
        self.cp[1] = np.cos(lon)
        for m in range(2, self.dims):
            self.sp[m] = self.sp[1]*self.cp[m-1] + self.cp[1]*self.sp[m-1]
            self.cp[m] = self.cp[1]*self.cp[m-1] - self.sp[1]*self.sp[m-1]
        dt = round(self.date_dec, 1) - self.epoch       # t - t_0
        a = MEAN_EARTH_RADIUS/1000.0                    # Mean earth radius in km
        ar = a/radius
        cpr = np.cos(lat_prime)                         # cos(phi')
        spr = np.sin(lat_prime)                         # sin(phi')
        self.P = np.identity(self.dims+1)
        self.dP = np.zeros((self.dims+1, self.dims))
        self.gh = np.zeros((self.dims+1, self.dims))
        Zp = Xp = Yp = Bp = 0.0
        # Spherical Harmonics (eq. 4)
        for n in range(1, self.dims):
            arn2 = ar**(n+2)
            x_p = y_p = z_p = 0.0
            for m in range(n+1):
                # ESTIMATE ASSOCIATED LEGENDRE POLYNOMIALS AND DERIVATIVES VIA RECURSION RELATIONS
                if n==m:
                    self.P[m, n] = cpr*self.P[m-1, n-1]
                    self.dP[m, n] = cpr*self.dP[m-1, n-1] + spr*self.P[m-1, n-1]
                else:
                    self.P[m, n] = spr*self.P[m, n-1]
                    self.dP[m, n] = spr*self.dP[m, n-1] - cpr*self.P[m, n-1]
                    if (n>1 and n!=m):
                        if m>n-2:
                            self.P[m, n-2] = 0.0
                            self.dP[m, n-2] = 0.0
                        self.P[m, n] -= self.k[m, n]*self.P[m, n-2]
                        self.dP[m, n] -= self.k[m, n]*self.dP[m, n-2]
                # Time adjusting Gauss coefficients (eq. 9)
                self.gh[m, n] = self.c[m, n] + dt*self.cd[m, n]
                if m!=0:
                    self.gh[n, m-1] = self.c[n, m-1] + dt*self.cd[n, m-1]
                # Accumulate terms of spherical harmonic expansions
                gchs = self.gh[m, n]*self.cp[m]         # g(t)cos(ml)
                gshc = self.gh[m, n]*self.sp[m]         # g(t)sin(ml)
                if m!=0:
                    gchs += self.gh[n, m-1]*self.sp[m]  # g(t)cos(ml) + h(t)sin(ml)
                    gshc -= self.gh[n, m-1]*self.cp[m]  # g(t)sin(ml) - h(t)cos(ml)
                x_p += gchs*self.dP[m, n]
                y_p += m*gshc*self.P[m, n]
                z_p += gchs*self.P[m, n]
                # SPECIAL CASE: NORTH/SOUTH GEOGRAPHIC POLES
                if (cpr==0.0 and m==1):
                    Bp += arn2*gshc
                    if n!=1:
                        Bp *= spr - self.k[m, n]
            Xp += arn2 * x_p                            # (eq. 10)
            Yp += arn2 * y_p                            # (eq. 11)
            Zp -= (n+1) * arn2 * z_p                    # (eq. 12)
        Yp = Bp if cpr==0.0 else Yp/cpr
        # ROTATE MAGNETIC VECTOR COMPONENTS FROM SPHERICAL TO GEODETIC COORDINATES (eq. 17)
        self.X = Xp*np.cos(lat_prime-lat) - Zp*np.sin(lat_prime-lat)
        self.Y = Yp
        self.Z = Xp*np.sin(lat_prime-lat) + Zp*np.cos(lat_prime-lat)
        # COMPUTE DECLINATION, INCLINATION AND TOTAL INTENSITY (eq. 19)
        self.H = np.linalg.norm([self.X, self.Y])
        self.F = np.linalg.norm([self.H, self.Z])
        self.I = RAD2DEG*np.arctan2(self.Z, self.H)
        self.D = RAD2DEG*np.arctan2(self.Y, self.X)
        # COMPUTE GRIVATION IF CURRENT GEODETIC POSITION IS IN THE POLAR AREAS (eq. 1)
        self.GV = self.D.copy()
        if self.latitude>55.0:
            self.GV -= self.longitude
        if self.latitude<-55.0:
            self.GV += self.longitude


class GeoMagTest(unittest.TestCase):
    """Test Magnetic Field estimation with provided values

    WMM 2015 uses a CSV test file with values split with semicolons, whereas
    the WMM 2020 uses a TXT file with values split with spaces. The position of
    their values is different. The following table shows their differences:

    +-------+-------------------+-------------------+
    | Index | CSV File (WM2015) | TXT File (WM2020) |
    +=======+===================+===================+
    | 0     | date              | date              |
    | 1     | height (km)       | height (km)       |
    | 2     | latitude (deg)    | latitude (deg)    |
    | 3     | longitude (deg)   | longitude (deg)   |
    | 4     | X (nT)            | D (deg)           |
    | 5     | Y (nT)            | I (deg)           |
    | 6     | Z (nT)            | H (nT)            |
    | 7     | H (nT)            | X (nT)            |
    | 8     | F (nT)            | Y (nT)            |
    | 9     | I (deg)           | Z (nT)            |
    | 10    | D (deg)           | F (nT)            |
    | 11    | GV (deg)          | dD/dt (deg/year)  |
    | 12    | Xdot (nT/yr)      | dI/dt (deg/year)  |
    | 13    | Ydot (nT/yr)      | dH/dt (nT/year)   |
    | 14    | Zdot (nT/yr)      | dX/dt (nT/year)   |
    | 15    | Hdot (nT/yr)      | dY/dt (nT/year)   |
    | 16    | Fdot (nT/yr)      | dZ/dt (nT/year)   |
    | 17    | dI/dt (deg/year)  | dF/dt (nT/year)   |
    | 18    | dD/dt (deg/year)  |                   |
    +-------+-------------------+-------------------+

    Besides using a different order, the newest format prescinds from grid
    variation (GV)
    """
    def _load_test_values(self, filename: str) -> np.ndarray:
        """Load test values from file.

        Parameters
        ----------
        filename : str
            Path to file with test values.

        Returns
        -------
        data : ndarray
            NumPy array with the test values.
        """
        if filename.endswith('.csv'):
            data = np.genfromtxt(filename, delimiter=';', skip_header=1)
            if data.shape[1]<19:
                raise ValueError("File has incomplete data")
            keys = ["date", "height", "latitude", "longitude", "X", "Y", "Z", "H", "F", "I", "D", "GV",
                "dX", "dY", "dZ", "dH", "dF", "dI", "dD"]
            return dict(zip(keys, data.T))
        if filename.endswith('.txt'):
            data = np.genfromtxt(filename, skip_header=1, comments='#')
            if data.shape[1]<18:
                raise ValueError("File has incomplete data")
            keys = ["date", "height", "latitude", "longitude", "D", "I", "H", "X", "Y", "Z", "F",
                "dD", "dI", "dH", "dX", "dY", "dZ", "dF"]
            return dict(zip(keys, data.T))
        raise ValueError("File type is not supported. Try a csv or txt File.")

    def test_wmm2015(self):
        """Test WMM 2015
        """
        wmm = WMM()
        test_values = self._load_test_values("./WMM2015/WMM2015_test_values.csv")
        num_tests = len(test_values['date'])
        for i in range(num_tests):
            wmm.magnetic_field(test_values['latitude'][i], test_values['longitude'][i], test_values['height'][i], date=test_values['date'][i])
            self.assertAlmostEqual(test_values['X'][i], wmm.X, 1, 'Expected {:.1f}, result {:.1f}'.format(test_values['X'][i], wmm.X))
            self.assertAlmostEqual(test_values['Y'][i], wmm.Y, 1, 'Expected {:.1f}, result {:.1f}'.format(test_values['Y'][i], wmm.Y))
            self.assertAlmostEqual(test_values['Z'][i], wmm.Z, 1, 'Expected {:.1f}, result {:.1f}'.format(test_values['Z'][i], wmm.Z))
            self.assertAlmostEqual(test_values['I'][i], wmm.I, 2, 'Expected {:.2f}, result {:.2f}'.format(test_values['I'][i], wmm.I))
            self.assertAlmostEqual(test_values['D'][i], wmm.D, 2, 'Expected {:.2f}, result {:.2f}'.format(test_values['D'][i], wmm.D))
            self.assertAlmostEqual(test_values['GV'][i], wmm.GV, 2, 'Expected {:.2f}, result {:.2f}'.format(test_values['GV'][i], wmm.GV))
        del wmm

    def test_wmm2020(self):
        """Test WMM 2020
        """
        wmm = WMM()
        test_values = self._load_test_values("./WMM2020/WMM2020_TEST_VALUES.txt")
        num_tests = len(test_values['date'])
        for i in range(num_tests):
            wmm.magnetic_field(test_values['latitude'][i], test_values['longitude'][i], test_values['height'][i], date=test_values['date'][i])
            self.assertAlmostEqual(test_values['X'][i], wmm.X, 1, 'Expected {:.1f}, result {:.1f}'.format(test_values['X'][i], wmm.X))
            self.assertAlmostEqual(test_values['Y'][i], wmm.Y, 1, 'Expected {:.1f}, result {:.1f}'.format(test_values['Y'][i], wmm.Y))
            self.assertAlmostEqual(test_values['Z'][i], wmm.Z, 1, 'Expected {:.1f}, result {:.1f}'.format(test_values['Z'][i], wmm.Z))
            self.assertAlmostEqual(test_values['I'][i], wmm.I, 2, 'Expected {:.2f}, result {:.2f}'.format(test_values['I'][i], wmm.I))
            self.assertAlmostEqual(test_values['D'][i], wmm.D, 2, 'Expected {:.2f}, result {:.2f}'.format(test_values['D'][i], wmm.D))
        del wmm

if __name__ == '__main__':
    unittest.main()
