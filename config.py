"""
Configuration file for CLIMADA setup project.

This file contains project-specific settings and paths.
Adjust these settings according to your environment and requirements.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

# Data directories
DATA_DIR = PROJECT_ROOT / 'data'
EXPOSURE_DIR = DATA_DIR / 'exposure'
HAZARD_DIR = DATA_DIR / 'hazard'
VULNERABILITY_DIR = DATA_DIR / 'vulnerability'

# Output directories
OUTPUT_DIR = PROJECT_ROOT / 'outputs'
RESULTS_DIR = OUTPUT_DIR / 'results'
FIGURES_DIR = OUTPUT_DIR / 'figures'

# Create directories if they don't exist
for directory in [OUTPUT_DIR, RESULTS_DIR, FIGURES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# CLIMADA configuration
CLIMADA_CONFIG = {
    # Default reference year
    'reference_year': 2024,
    
    # Default value unit
    'value_unit': 'USD',
    
    # LitPop default resolution (arcsec)
    'litpop_resolution': 300,  # ~10km at equator
    
    # Default countries for examples (ISO 3166 alpha-3)
    'example_countries': ['CHE', 'AUT', 'DEU'],
    
    # Tropical cyclone basins
    'tc_basins': {
        'NA': 'North Atlantic',
        'EP': 'East Pacific',
        'WP': 'West Pacific',
        'SI': 'South Indian',
        'NI': 'North Indian',
        'SP': 'South Pacific',
    },
    
    # Climate scenarios
    'rcps': ['RCP2.6', 'RCP4.5', 'RCP6.0', 'RCP8.5'],
    'ssps': ['SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'],
    
    # Default years for scenario analysis
    'scenario_years': [2030, 2050, 2100],
}

# Visualization settings
PLOT_CONFIG = {
    'figure_dpi': 150,
    'figure_format': 'png',
    'colormap_risk': 'YlOrRd',
    'colormap_hazard': 'plasma',
    'font_size': 11,
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
}

# API endpoints (if using external data sources)
API_CONFIG = {
    'climada_api': 'https://climada.ethz.ch/api',
    'timeout': 30,  # seconds
}

# Performance settings
PERFORMANCE_CONFIG = {
    # Number of parallel workers (None = auto-detect)
    'n_workers': None,
    
    # Memory limit for large computations (GB)
    'memory_limit_gb': 4,
    
    # Chunk size for processing large datasets
    'chunk_size': 1000,
}

def get_config():
    """
    Get the complete configuration dictionary.
    
    Returns:
        dict: Complete configuration
    """
    return {
        'project_root': PROJECT_ROOT,
        'data_dir': DATA_DIR,
        'output_dir': OUTPUT_DIR,
        'climada': CLIMADA_CONFIG,
        'plot': PLOT_CONFIG,
        'logging': LOGGING_CONFIG,
        'api': API_CONFIG,
        'performance': PERFORMANCE_CONFIG,
    }

def print_config():
    """Print the current configuration."""
    config = get_config()
    
    print("=" * 60)
    print("CLIMADA Setup Configuration")
    print("=" * 60)
    
    print(f"\nProject Root: {config['project_root']}")
    print(f"Data Directory: {config['data_dir']}")
    print(f"Output Directory: {config['output_dir']}")
    
    print("\nCLIMADA Settings:")
    for key, value in config['climada'].items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        elif isinstance(value, list):
            print(f"  {key}: {', '.join(map(str, value))}")
        else:
            print(f"  {key}: {value}")
    
    print("\nVisualization Settings:")
    for key, value in config['plot'].items():
        print(f"  {key}: {value}")
    
    print("\nLogging Level: {0}".format(config['logging']['level']))
    print("=" * 60)

if __name__ == "__main__":
    # Print configuration when run directly
    print_config()
