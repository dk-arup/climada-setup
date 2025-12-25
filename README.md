# CLIMADA Setup

A comprehensive setup for working with [CLIMADA](https://climada-python.readthedocs.io/) (CLIMate ADAptation), an open-source Python platform for climate risk analysis developed by ETH Zurich.

## Overview

CLIMADA is a probabilistic natural catastrophe impact modeling platform that combines:
- **Hazard** data (storms, floods, droughts, etc.)
- **Exposure** data (assets, population, infrastructure)
- **Vulnerability** functions (impact models)

This repository provides a ready-to-use environment setup, example workflows, and integration scripts for climate risk analysis projects.

## Features

- Pre-configured conda/mamba environment with CLIMADA and dependencies
- Example workflows for common climate risk analysis tasks
- Modular scripts for exposure, hazard, and vulnerability data integration
- Scenario development tools for climate impact assessment
- Jupyter notebooks for interactive analysis

## Installation

### Prerequisites

- [Conda](https://docs.conda.io/en/latest/) or [Mamba](https://mamba.readthedocs.io/) (recommended)
- Python 3.11 (recommended) or 3.10-3.12
- At least 4GB of free disk space

### Quick Start

#### Option 1: Using Mamba (Recommended)

Mamba is a faster alternative to conda. Install Miniforge (includes Mamba):

**macOS & Linux:**
```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

**Windows:**
Download and run the [Miniforge installer](https://github.com/conda-forge/miniforge/releases/latest), then open "Miniforge Prompt".

**Create and activate the environment:**
```bash
# Clone this repository
git clone https://github.com/dk-arup/climada-setup.git
cd climada-setup

# Create environment from environment.yml
mamba env create -f environment.yml

# Activate the environment
mamba activate climada_env
```

#### Option 2: Using Conda

```bash
# Clone this repository
git clone https://github.com/dk-arup/climada-setup.git
cd climada-setup

# Create environment from environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate climada_env
```

#### Option 3: Using pip (Not Recommended)

⚠️ **Warning:** CLIMADA has complex dependencies. Using pip alone may not resolve all requirements. Conda/Mamba is strongly recommended.

```bash
pip install -r requirements.txt
```

### Verify Installation

After activating the environment, verify CLIMADA is installed correctly:

```bash
python -c "import climada; print(f'CLIMADA version: {climada.__version__}')"
```

Expected output (version may vary):
```
CLIMADA version: 6.1.0
```

## Project Structure

```
climada-setup/
├── README.md                     # This file
├── environment.yml               # Conda/Mamba environment specification
├── requirements.txt              # Pip requirements (fallback)
├── workflows/                    # Example workflow scripts
│   ├── 01_basic_risk_assessment.py
│   ├── 02_exposure_integration.py
│   ├── 03_hazard_integration.py
│   ├── 04_vulnerability_functions.py
│   └── 05_scenario_development.py
├── data/                         # Data directory (add your datasets here)
│   ├── exposure/                 # Exposure data
│   ├── hazard/                   # Hazard data
│   └── vulnerability/            # Vulnerability/impact functions
├── docs/                         # Additional documentation
│   ├── getting_started.ipynb     # Jupyter notebook tutorial
│   └── quick_reference.md        # Quick reference guide
├── config.py                     # Project configuration
├── run_all_workflows.py          # Script to run all workflows
└── CONTRIBUTING.md               # Contribution guidelines
```

## Usage

### Quick Test

Run all example workflows at once:

```bash
python run_all_workflows.py
```

Note: This script checks if CLIMADA is installed and provides helpful error messages if not.

### Getting Started with Jupyter

Launch Jupyter Lab to explore the interactive tutorial:

```bash
jupyter lab docs/getting_started.ipynb
```

### Running Example Workflows

The `workflows/` directory contains Python scripts demonstrating key CLIMADA functionality:

1. **Basic Risk Assessment** (`01_basic_risk_assessment.py`)
   - Load exposure and hazard data
   - Define impact functions
   - Calculate risk metrics

2. **Exposure Integration** (`02_exposure_integration.py`)
   - Work with population and asset data
   - Use LitPop for economic exposure
   - Custom exposure data integration

3. **Hazard Integration** (`03_hazard_integration.py`)
   - Load historical hazard events
   - Generate probabilistic event sets
   - Work with different hazard types

4. **Vulnerability Functions** (`04_vulnerability_functions.py`)
   - Define impact functions
   - Calibrate functions with observed data
   - Customize vulnerability curves

5. **Scenario Development** (`05_scenario_development.py`)
   - Run climate change scenarios (SSPs/RCPs)
   - Compare current vs. future risk
   - Assess adaptation measures

Run any workflow script:
```bash
python workflows/01_basic_risk_assessment.py
```

## Data Requirements

CLIMADA can work with:
- Built-in demo datasets (automatic download)
- Global datasets from CLIMADA's API
- Custom local datasets (place in `data/` directories)

For large datasets, consider using CLIMADA's data API or downloading from:
- [CLIMADA Data Portal](https://climada.ethz.ch/)
- [Natural Earth Data](https://www.naturalearthdata.com/)
- [ECMWF Climate Data Store](https://cds.climate.copernicus.eu/)

## Configuration

Key CLIMADA configurations can be set via environment variables or Python:

```python
from climada.util.config import CONFIG

# Set data directory
CONFIG['local_data']['system'] = '/path/to/your/data'

# Configure logging
CONFIG['logging']['level'] = 'INFO'
```

See [CLIMADA configuration docs](https://climada-python.readthedocs.io/en/stable/user-guide/configuration.html) for more options.

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add new workflow'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Documentation

- [CLIMADA Official Documentation](https://climada-python.readthedocs.io/en/stable/)
- [CLIMADA Tutorials](https://climada-python.readthedocs.io/en/stable/user-guide/)
- [CLIMADA GitHub Repository](https://github.com/CLIMADA-project/climada_python)
- [CLIMADA @ ETH Zurich](https://climada.ethz.ch/)
- [Scientific Publication](https://gmd.copernicus.org/articles/12/3085/2019/)

## Support

- **Issues:** Report bugs or request features via [GitHub Issues](https://github.com/dk-arup/climada-setup/issues)
- **CLIMADA Support:** Visit [CLIMADA Discussions](https://github.com/CLIMADA-project/climada_python/discussions)
- **Documentation:** Refer to the [official CLIMADA docs](https://climada-python.readthedocs.io/)

## License

This repository is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Important:** This license applies to the setup scripts, documentation, and configuration files in this repository. CLIMADA itself is licensed under GPLv3. When using CLIMADA, you must comply with its license terms. See the [CLIMADA license](https://github.com/CLIMADA-project/climada_python/blob/main/LICENSE) for details.

## Acknowledgments

- CLIMADA is developed and maintained by the [Weather and Climate Risks Group](https://wcr.ethz.ch/) at ETH Zurich
- This setup repository is created to facilitate easier onboarding and usage of CLIMADA

## Version History

- **v1.0.0** (2025-12-25): Initial setup with CLIMADA 6.x support
  - Environment configuration
  - Example workflows
  - Documentation