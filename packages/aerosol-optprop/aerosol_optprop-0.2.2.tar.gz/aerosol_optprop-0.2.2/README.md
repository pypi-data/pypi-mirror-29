# Introduction

Simple package to help with calculation of aerosol optical properties and derived parameters. 
Currently two size distrubtions are supported:

#### Monodisperse
A 'distribution' with particles of a single radii. Can be convenient for
derived classes.


#### Lognormal
The equation describing the distribution is:

```math
\frac{dn}{dr} = \frac{n}{\sqrt{2\pi}r\ln\sigma_g}\exp\left(-\frac{(\ln(r)-\ln(r_g))^2}{2\ln^2\sigma_g}\right)
```

where $`r_g`$ is the median radius, and $`\sigma_g`$ is the width.

## Installation

You can dowload the package from pypi using

```
pip install aerosol_optprop
```

Or, if you'll be developing, then clone the repository and use

```
pip install -e .
```

## Example Usage

Cross section Calculations
```python
from aerosol_optprop import Lognormal

# create a lognormal distribution and compute the cross section
aerosol = Lognormal(median_radius=0.1, width=1.5)
print(aerosol.cross_section(wavelength=0.525))
```

Calculation of derived properties
```python
aerosol = Lognormal(median_radius=0.1, width=1.5, n=10)
print('extinction =', aerosol.extinction(wavelength=0.525), 'km^-1')
print('surface area density =', aerosol.surface_area_density, 'microns^2/cm^3')
print('volume density =', aerosol.volume_density, 'microns^3/cm^3')
```

Internally consistent parameters
```python
aerosol = Lognormal(median_radius=0.1, width=1.5, n=10)
aerosol.mode_radius = 0.1  # update the mode radius of the distribution
print('median radius is now =', aerosol.median_radius, 'microns')
```

Extinction can be kept constant if desired
```python
aerosol = Lognormal(median_radius=0.1, width=1.5)
aerosol.set_n_from_extinction(extinction=1e-3, wavelength=0.525, persistant=True)
print('old n =', aerosol.n, 'cm^-3')
aerosol.median_radius = 0.12
print('new n = ', aerosol.n, 'cm^-3')
```

Phase function calculations (these are a bit slow)
```python
import matplotlib.pyplot as plt

aerosol = Lognormal(median_radius=0.1, width=1.5, n=10)
theta = np.arange(0, 181)
p = aerosol.phase_function(wavelength=0.525, scattering_angles=theta)
plt.plot(theta, p)
plt.xlabel('scattering angle (deg)')
plt.ylabel('P')
```

# Details
The code uses the [miepython](https://github.com/scottprahl/miepython) implementation of the
Wiscombe code developed by Scott Prahl for the Mie calculations.

Optical properties are from Palmer and Williams between 0.36-25 microns and Beyer et al. between
0.214 and 0.36 microns, assuming 75% H<sub>2</sub>SO<sub>4</sub> and 25% H<sub>2</sub>O.
If you prefer to use your own refractive index data then this can be changed using the
`refractive_index_file` variable. Files should have three columns in the format

wavenumber \[cm^-1 \] | real refractive index | imaginary refractive index
--- | --- | ---
400 | 1.3 | 1e-8
450 | 1.4 | 1.3e-7
... | ... | ...

1. Optical Constants of Sulfuric Acid; Application to the Clouds of Venus?
Kent F. Palmer and Dudley Williams
Appl. Opt. 14, 208-219 (1975)

2. Measurements of UV refractive indices and densities of
H2SO4/H2O and H2SO4/HNO3/2:O solutions
Keith D. Beyer, A. R. Ravishankara, and Edward R. Lovejoy
J. Geophys. Res., 101, D9, 2156-2202, 1996
http://dx.doi.org/10.1029/96JD00937
