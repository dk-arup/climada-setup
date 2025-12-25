# CLIMADA Quick Reference Guide

A quick reference for common CLIMADA operations and patterns.

## Installation & Setup

```bash
# Install with Mamba (recommended)
mamba env create -f environment.yml
mamba activate climada_env

# Verify installation
python -c "import climada; print(climada.__version__)"
```

## Common Imports

```python
# Core modules
from climada.entity import Exposures, ImpactFunc, ImpactFuncSet
from climada.hazard import TropCyclone, Hazard
from climada.engine import Impact, CostBenefit

# Exposure generation
from climada.entity.exposures import LitPop

# Utilities
from climada.util.config import CONFIG
```

## Exposure Data

### Create Exposure from Scratch

```python
from climada.entity import Exposures
import numpy as np

exp = Exposures()
exp.gdf['latitude'] = np.array([lat1, lat2, ...])
exp.gdf['longitude'] = np.array([lon1, lon2, ...])
exp.gdf['value'] = np.array([val1, val2, ...])  # Asset values
exp.ref_year = 2024
exp.value_unit = 'USD'
exp.check()
```

### Load Exposure from CSV

```python
import pandas as pd

df = pd.read_csv('exposure_data.csv')
exp = Exposures()
exp.gdf = df
exp.ref_year = 2024
exp.value_unit = 'USD'
exp.check()
```

### Generate LitPop Exposure

```python
from climada.entity.exposures import LitPop

exp = LitPop.from_countries(
    countries=['CHE'],      # ISO 3166 alpha-3 code
    res_arcsec=300,         # Resolution (~10km at equator)
    reference_year=2020
)
```

## Hazard Data

### Load Tropical Cyclones from IBTrACS

```python
from climada.hazard import TropCyclone

tc_hazard = TropCyclone.from_ibtracs_netcdf(
    provider='official',
    basin='NA',              # North Atlantic
    year_range=(2010, 2020)
)
```

### Create Custom Hazard

```python
from climada.hazard import Hazard
from scipy.sparse import csr_matrix
import numpy as np

hazard = Hazard('TC')
hazard.centroids.lat = np.array([...])
hazard.centroids.lon = np.array([...])
hazard.units = 'm/s'
hazard.event_id = np.array([1, 2, 3])
hazard.date = np.array([date1, date2, date3])
hazard.frequency = np.array([0.1, 0.05, 0.02])
hazard.intensity = csr_matrix(intensity_matrix)
hazard.fraction = csr_matrix(fraction_matrix)
```

## Impact Functions

### Define Impact Function

```python
from climada.entity import ImpactFunc

impf = ImpactFunc()
impf.id = 1
impf.name = 'TC Buildings'
impf.haz_type = 'TC'
impf.intensity_unit = 'm/s'

# Intensity thresholds
impf.intensity = np.array([0, 20, 40, 60, 80])

# Mean Damage Degree (0=no damage, 1=total loss)
impf.mdd = np.array([0, 0.05, 0.30, 0.70, 1.0])

# Percentage of Affected Assets
impf.paa = np.array([0, 0.5, 0.9, 1.0, 1.0])

impf.check()
```

### Create Impact Function Set

```python
from climada.entity import ImpactFuncSet

impf_set = ImpactFuncSet()
impf_set.append(impf1)
impf_set.append(impf2)

# Or load defaults
impf_set.from_tc_default()
```

## Risk Calculation

### Calculate Impact

```python
from climada.engine import Impact

impact = Impact()
impact.calc(exposure, hazard, impf_set)

# Results
print(f"Average Annual Impact: ${impact.aai_agg:,.0f}")
print(f"Total events: {impact.size}")

# Event-specific impacts
max_event = impact.at_event.argmax()
print(f"Maximum single event loss: ${impact.at_event[max_event]:,.0f}")
```

### Visualize Results

```python
# Exceedance frequency curve (return period)
impact.plot_exceedance()

# Impact map
impact.plot_map()

# Impact per exposure point
impact.plot_scatter_eai_exposure()
```

## Scenario Analysis

### Future Exposure Scenario

```python
# Adjust exposure for future scenario
future_exp = exposure.copy()
future_exp.gdf['value'] *= 1.5  # 50% economic growth
future_exp.ref_year = 2050
```

### Climate Scenarios

```python
# Load future climate hazard
# (Use climate model outputs, not shown here)
future_hazard = load_climate_projection('RCP8.5', 2050)

# Calculate future impact
future_impact = Impact()
future_impact.calc(future_exp, future_hazard, impf_set)

# Compare
print(f"Current AAI: ${impact.aai_agg:,.0f}")
print(f"Future AAI: ${future_impact.aai_agg:,.0f}")
print(f"Increase: {(future_impact.aai_agg / impact.aai_agg - 1) * 100:.1f}%")
```

## Adaptation Analysis

### Cost-Benefit Analysis

```python
from climada.engine import CostBenefit

# Define adaptation measure
adapt_measure = {
    'name': 'Building Codes',
    'cost': 10e6,  # One-time cost
    'maint_cost': 0.5e6,  # Annual maintenance
    'hazard_freq_cutoff': 0.01  # Reduces impacts for events < 1/100 year
}

# Run cost-benefit analysis
cb = CostBenefit()
cb.calc(
    hazard=hazard,
    exposure=exposure,
    impf_set=impf_set,
    adapt_measure=adapt_measure
)

# Results
cb.plot()
```

## Configuration

### Set Data Directory

```python
from climada.util.config import CONFIG

CONFIG['local_data']['system'] = '/path/to/data'
```

### Configure Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
CONFIG['logging']['level'] = 'INFO'
```

## Common Patterns

### Loop Over Multiple Countries

```python
countries = ['CHE', 'AUT', 'DEU']
results = {}

for country in countries:
    exp = LitPop.from_countries([country])
    impact = Impact()
    impact.calc(exp, hazard, impf_set)
    results[country] = impact.aai_agg
```

### Aggregate by Region

```python
# Add region_id to exposure
exposure.gdf['region_id'] = assign_regions(exposure.gdf)

# Calculate impacts
impact.calc(exposure, hazard, impf_set)

# Aggregate by region
regional_impacts = {}
for region_id in exposure.gdf['region_id'].unique():
    mask = exposure.gdf['region_id'] == region_id
    regional_impacts[region_id] = impact.eai_exp[mask].sum()
```

### Save and Load Results

```python
# Save exposure
exposure.write_hdf5('exposure.h5')

# Load exposure
exp_loaded = Exposures.from_hdf5('exposure.h5')

# Save hazard
hazard.write_hdf5('hazard.h5')

# Load hazard
haz_loaded = Hazard.from_hdf5('hazard.h5')
```

## Data Sources

### Built-in Data

- IBTrACS: Global tropical cyclone tracks
- LitPop: Population and economic data
- Natural Earth: Geographic boundaries

### External Data Sources

- [ECMWF Climate Data Store](https://cds.climate.copernicus.eu/): Climate projections
- [Natural Earth](https://www.naturalearthdata.com/): Geographic data
- [WorldPop](https://www.worldpop.org/): Population data
- [SEDAC](https://sedac.ciesin.columbia.edu/): Socioeconomic data

## Troubleshooting

### Import Errors

```python
# Check CLIMADA installation
import climada
print(climada.__version__)

# Check specific module
from climada.entity import Exposures
```

### Data Download Issues

```bash
# Check internet connection
# Check CLIMADA data directory
python -c "from climada.util.config import CONFIG; print(CONFIG['local_data']['system'])"

# Clear cache if corrupted
rm -rf ~/.climada/data
```

### Performance Issues

```python
# Reduce resolution for testing
exp = LitPop.from_countries(['USA'], res_arcsec=600)  # ~20km instead of ~5km

# Use fewer events for testing
hazard_subset = hazard.select(event_ids=[1, 2, 3])
```

## Resources

- **Documentation**: https://climada-python.readthedocs.io/
- **Tutorials**: https://climada-python.readthedocs.io/en/stable/user-guide/
- **GitHub**: https://github.com/CLIMADA-project/climada_python
- **Issues**: https://github.com/CLIMADA-project/climada_python/issues
- **Discussions**: https://github.com/CLIMADA-project/climada_python/discussions

## Hazard Type Abbreviations

| Code | Hazard Type |
|------|-------------|
| TC   | Tropical Cyclone |
| RF   | River Flood |
| CF   | Coastal Flood |
| WF   | Wildfire |
| HS   | Heat Stress |
| DR   | Drought |
| LS   | Landslide |
| EQ   | Earthquake |
| VO   | Volcanic Eruption |

---

For more details, see the [CLIMADA documentation](https://climada-python.readthedocs.io/).
