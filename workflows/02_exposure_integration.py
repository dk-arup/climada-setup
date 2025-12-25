#!/usr/bin/env python3
"""
Exposure Data Integration with CLIMADA

This script demonstrates how to work with exposure data:
1. Generate exposure using LitPop (Lit population, economic production)
2. Load custom exposure from CSV
3. Aggregate and analyze exposure data
4. Visualize spatial distribution

Author: CLIMADA Setup Project
Date: 2025-12-25
"""

import sys
from pathlib import Path

try:
    from climada.entity import Exposures
    from climada.entity.exposures import LitPop
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure CLIMADA is properly installed.")
    sys.exit(1)


def generate_litpop_exposure(country='CHE', resolution=150):
    """
    Generate exposure using LitPop methodology.
    
    LitPop combines nightlight intensity (Lit) and GDP/capita (Pop)
    to estimate economic exposure at high resolution.
    
    Args:
        country: ISO 3166 alpha-3 country code (e.g., 'CHE' for Switzerland)
        resolution: Resolution in arcsec (default: 150 = ~5km at equator)
        
    Returns:
        Exposures: Generated exposure data
    """
    print(f"Generating LitPop exposure for {country}...")
    print(f"  Resolution: {resolution} arcsec (~{resolution/30:.1f} km at equator)")
    
    try:
        # Generate LitPop exposure
        # This will download required data on first run
        exposure = LitPop.from_countries(
            countries=[country],
            res_arcsec=resolution,
            reference_year=2020
        )
        
        print(f"  Generated {len(exposure.gdf)} exposure points")
        print(f"  Total value: ${exposure.gdf['value'].sum()/1e9:.2f} billion")
        print(f"  Value unit: {exposure.value_unit}")
        
        return exposure
        
    except Exception as e:
        print(f"  Error generating LitPop data: {e}")
        print("  Note: First run requires data download from CLIMADA servers")
        return None


def create_custom_exposure_example():
    """
    Create a custom exposure dataset from scratch.
    
    This demonstrates the required structure for custom exposure data.
    In practice, you would load this from your own data sources.
    
    Returns:
        Exposures: Custom exposure data
    """
    print("\nCreating custom exposure dataset...")
    
    # Create exposure object
    exposure = Exposures()
    
    # Define exposure data
    # Required columns: latitude, longitude, value
    data = {
        'latitude': [47.3769, 47.5596, 46.9480, 46.5197, 47.4239],
        'longitude': [8.5417, 7.5886, 7.4474, 6.6323, 9.3770],
        'value': [5e8, 2e8, 1.5e8, 1e8, 3e8],  # Asset values in USD
        'region_id': [1, 2, 3, 4, 5],
        'asset_type': ['residential', 'commercial', 'industrial', 'residential', 'commercial']
    }
    
    # Create GeoDataFrame
    exposure.gdf = pd.DataFrame(data)
    
    # Set metadata
    exposure.ref_year = 2024
    exposure.value_unit = 'USD'
    exposure.description = 'Custom exposure dataset - Swiss cities example'
    
    # Assign impact function IDs (used in risk calculation)
    exposure.gdf['impf_TC'] = 1  # Tropical cyclone impact function ID
    exposure.gdf['impf_RF'] = 1  # River flood impact function ID
    
    # Validate exposure data
    exposure.check()
    
    print(f"  Created exposure with {len(exposure.gdf)} locations")
    print(f"  Total value: ${exposure.gdf['value'].sum()/1e6:.1f} million")
    print(f"  Columns: {list(exposure.gdf.columns)}")
    
    return exposure


def load_exposure_from_csv(csv_path):
    """
    Load exposure from a CSV file.
    
    CSV should contain at minimum: latitude, longitude, value
    Optional columns: region_id, asset_type, impf_*, etc.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        Exposures: Loaded exposure data
    """
    print(f"\nLoading exposure from CSV: {csv_path}")
    
    try:
        # Read CSV
        df = pd.read_csv(csv_path)
        
        # Create exposure object
        exposure = Exposures()
        exposure.gdf = df
        
        # Set metadata (adjust as needed)
        exposure.ref_year = 2024
        exposure.value_unit = 'USD'
        
        # Validate
        exposure.check()
        
        print(f"  Loaded {len(exposure.gdf)} exposure points")
        print(f"  Total value: ${exposure.gdf['value'].sum():,.0f}")
        
        return exposure
        
    except FileNotFoundError:
        print(f"  File not found: {csv_path}")
        print("  Creating example CSV template...")
        create_exposure_csv_template(csv_path)
        return None
    except Exception as e:
        print(f"  Error loading CSV: {e}")
        return None


def create_exposure_csv_template(output_path):
    """
    Create an example CSV template for exposure data.
    
    Args:
        output_path: Where to save the template
    """
    template_data = {
        'latitude': [47.3769, 47.5596, 46.9480],
        'longitude': [8.5417, 7.5886, 7.4474],
        'value': [1000000, 2000000, 1500000],
        'region_id': [1, 2, 3],
        'asset_type': ['residential', 'commercial', 'industrial']
    }
    
    df = pd.DataFrame(template_data)
    df.to_csv(output_path, index=False)
    print(f"  Created template at: {output_path}")


def aggregate_exposure_by_region(exposure):
    """
    Aggregate exposure data by region.
    
    Args:
        exposure: Exposure data
        
    Returns:
        pd.DataFrame: Aggregated results
    """
    print("\nAggregating exposure by region...")
    
    if 'region_id' not in exposure.gdf.columns:
        print("  No region_id column found, skipping aggregation")
        return None
    
    # Group by region and sum values
    regional_agg = exposure.gdf.groupby('region_id').agg({
        'value': 'sum',
        'latitude': 'mean',
        'longitude': 'mean'
    }).reset_index()
    
    regional_agg.columns = ['region_id', 'total_value', 'center_lat', 'center_lon']
    
    print(f"  Aggregated to {len(regional_agg)} regions")
    print("\n  Regional summary:")
    for _, row in regional_agg.iterrows():
        print(f"    Region {row['region_id']}: ${row['total_value']/1e6:.1f}M")
    
    return regional_agg


def visualize_exposure(exposure, title="Exposure Distribution"):
    """
    Visualize exposure spatial distribution.
    
    Args:
        exposure: Exposure data
        title: Plot title
    """
    print("\nGenerating exposure visualization...")
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Spatial distribution
    ax1 = axes[0]
    scatter = ax1.scatter(
        exposure.gdf['longitude'],
        exposure.gdf['latitude'],
        s=exposure.gdf['value'] / exposure.gdf['value'].max() * 500,
        c=exposure.gdf['value'],
        cmap='YlOrRd',
        alpha=0.6,
        edgecolors='black',
        linewidth=0.5
    )
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.set_title(f'{title} - Spatial Distribution')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax1, label=f'Asset Value ({exposure.value_unit})')
    
    # Plot 2: Value distribution histogram
    ax2 = axes[1]
    ax2.hist(exposure.gdf['value'], bins=30, edgecolor='black', alpha=0.7)
    ax2.set_xlabel(f'Asset Value ({exposure.value_unit})')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Exposure Value Distribution')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add statistics
    stats_text = f"Total: ${exposure.gdf['value'].sum()/1e9:.2f}B\n"
    stats_text += f"Mean: ${exposure.gdf['value'].mean()/1e6:.1f}M\n"
    stats_text += f"Median: ${exposure.gdf['value'].median()/1e6:.1f}M\n"
    stats_text += f"Count: {len(exposure.gdf):,}"
    ax2.text(0.98, 0.97, stats_text,
             transform=ax2.transAxes,
             verticalalignment='top',
             horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    
    # Save figure
    output_dir = Path(__file__).parent.parent / 'data' / 'exposure'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / 'exposure_visualization.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"  Saved visualization to: {output_path}")
    
    plt.close()


def main():
    """Main workflow execution."""
    print("=" * 60)
    print("CLIMADA Exposure Data Integration")
    print("=" * 60)
    
    try:
        # Example 1: Custom exposure dataset
        print("\n### Example 1: Custom Exposure Dataset ###")
        custom_exp = create_custom_exposure_example()
        if custom_exp:
            visualize_exposure(custom_exp, "Custom Exposure")
            aggregate_exposure_by_region(custom_exp)
        
        # Example 2: CSV loading
        print("\n### Example 2: Load from CSV ###")
        csv_path = Path(__file__).parent.parent / 'data' / 'exposure' / 'exposure_template.csv'
        csv_exp = load_exposure_from_csv(csv_path)
        
        # Example 3: LitPop (commented out as it requires data download)
        print("\n### Example 3: LitPop Exposure (Optional) ###")
        print("  To generate LitPop exposure, uncomment the following line:")
        print("  litpop_exp = generate_litpop_exposure('CHE', resolution=300)")
        print("  Note: This requires internet connection for data download")
        
        # Uncomment to try LitPop (will download data):
        # litpop_exp = generate_litpop_exposure('CHE', resolution=300)
        # if litpop_exp:
        #     visualize_exposure(litpop_exp, "LitPop Exposure - Switzerland")
        
        print("\n" + "=" * 60)
        print("Exposure integration workflow completed!")
        print("=" * 60)
        print("\nNext Steps:")
        print("1. Load your own exposure data from CSV/database")
        print("2. Try LitPop for country-level economic exposure")
        print("3. Combine exposure with hazard data (see 03_hazard_integration.py)")
        print("4. Assign appropriate impact function IDs for risk calculation")
        
    except Exception as e:
        print(f"\nError during workflow execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
