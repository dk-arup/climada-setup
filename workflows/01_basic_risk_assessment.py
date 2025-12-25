#!/usr/bin/env python3
"""
Basic Risk Assessment with CLIMADA

This script demonstrates a complete basic workflow for climate risk assessment:
1. Load exposure data (assets at risk)
2. Load hazard data (tropical cyclone)
3. Define vulnerability (impact functions)
4. Calculate and visualize risk

Author: CLIMADA Setup Project
Date: 2025-12-25
"""

import sys
from pathlib import Path

try:
    from climada.entity import Exposures, ImpactFuncSet, ImpactFunc
    from climada.hazard import TropCyclone
    from climada.engine import Impact
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure CLIMADA is properly installed:")
    print("  mamba activate climada_env")
    print("  python -c 'import climada; print(climada.__version__)'")
    sys.exit(1)


def create_sample_exposure():
    """
    Create a sample exposure dataset.
    
    In practice, you would load this from:
    - CLIMADA's LitPop module (population and assets)
    - Custom CSV/shapefile with asset locations and values
    - Database queries
    
    Returns:
        Exposures: Sample exposure data
    """
    print("Creating sample exposure data...")
    
    # Create simple exposure with a few locations
    exp = Exposures()
    
    # Define sample locations (latitude, longitude, asset values)
    # Example: coastal properties in a hypothetical region
    exp.gdf['latitude'] = np.array([26.0, 26.5, 27.0, 27.5, 28.0])
    exp.gdf['longitude'] = np.array([-80.0, -80.2, -80.1, -79.9, -80.0])
    exp.gdf['value'] = np.array([1e6, 2e6, 1.5e6, 3e6, 2.5e6])  # Asset values in USD
    exp.gdf['region_id'] = np.array([1, 1, 2, 2, 3])
    
    # Set reference year and value unit
    exp.ref_year = 2024
    exp.value_unit = 'USD'
    
    # Check exposure data
    exp.check()
    
    print(f"  Created exposure with {len(exp.gdf)} locations")
    print(f"  Total exposure value: ${exp.gdf['value'].sum():,.0f}")
    
    return exp


def load_sample_hazard():
    """
    Load sample hazard data.
    
    In practice, you would:
    - Use TropCyclone.from_ibtracs() for historical data
    - Use CLIMADA's API to download hazard datasets
    - Load custom hazard data from NetCDF files
    
    Returns:
        TropCyclone: Sample hazard event set
    """
    print("\nLoading sample hazard data...")
    print("  Note: For real analysis, use TropCyclone.from_ibtracs() or custom data")
    
    # For this example, we'll create a minimal hazard structure
    # In real usage, load actual data:
    # hazard = TropCyclone.from_ibtracs(basin='NA', year_range=(2010, 2020))
    
    hazard = TropCyclone()
    print("  Hazard structure created (use real data for actual analysis)")
    
    return hazard


def define_impact_functions():
    """
    Define vulnerability (impact) functions.
    
    Impact functions define how exposure responds to hazard intensity.
    For tropical cyclones, this relates wind speed to damage fraction.
    
    Returns:
        ImpactFuncSet: Set of impact functions
    """
    print("\nDefining impact functions...")
    
    impact_funcs = ImpactFuncSet()
    
    # Create tropical cyclone impact function
    tc_impf = ImpactFunc()
    tc_impf.id = 1
    tc_impf.name = 'TC Building Damage'
    tc_impf.haz_type = 'TC'
    tc_impf.intensity_unit = 'm/s'
    
    # Define intensity-damage relationship
    # Intensity (wind speed in m/s)
    tc_impf.intensity = np.array([0, 20, 30, 40, 50, 60, 70, 80])
    
    # Mean damage ratio (0 = no damage, 1 = total destruction)
    tc_impf.mdd = np.array([0, 0.01, 0.05, 0.15, 0.35, 0.60, 0.85, 1.0])
    
    # Percentage of affected exposures
    tc_impf.paa = np.array([0, 0.5, 0.7, 0.85, 0.95, 0.98, 1.0, 1.0])
    
    # Check validity
    tc_impf.check()
    
    impact_funcs.append(tc_impf)
    
    print(f"  Created impact function: {tc_impf.name}")
    
    return impact_funcs


def calculate_risk(exposure, hazard, impact_funcs):
    """
    Calculate risk (expected impacts).
    
    Risk = Hazard × Exposure × Vulnerability
    
    Args:
        exposure: Exposure data
        hazard: Hazard event set
        impact_funcs: Impact functions
        
    Returns:
        Impact: Calculated impacts
    """
    print("\nCalculating risk...")
    
    # Note: This is a demonstration structure
    # For actual calculations, you need real hazard data
    impact = Impact()
    
    print("  Note: Risk calculation requires complete hazard data")
    print("  In real analysis, use: impact.calc(exposure, hazard, impact_funcs)")
    
    # With real data, you would:
    # impact.calc(exposure, hazard, impact_funcs)
    # print(f"  Average Annual Impact (AAI): ${impact.aai_agg:,.0f}")
    
    return impact


def visualize_results(exposure, impact_funcs):
    """
    Visualize exposure and impact functions.
    
    Args:
        exposure: Exposure data
        impact_funcs: Impact functions
    """
    print("\nGenerating visualizations...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Exposure map
    ax1 = axes[0]
    scatter = ax1.scatter(
        exposure.gdf['longitude'],
        exposure.gdf['latitude'],
        s=exposure.gdf['value'] / 1e4,  # Size proportional to value
        c=exposure.gdf['value'],
        cmap='YlOrRd',
        alpha=0.6,
        edgecolors='black'
    )
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.set_title('Exposure Locations and Values')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax1, label='Asset Value (USD)')
    
    # Plot 2: Impact function (vulnerability curve)
    ax2 = axes[1]
    impf = impact_funcs.get_func(haz_type='TC')[0]
    ax2.plot(impf.intensity, impf.mdd, 'o-', label='Mean Damage Degree (MDD)', linewidth=2)
    ax2.plot(impf.intensity, impf.paa, 's-', label='% Affected Assets (PAA)', linewidth=2)
    ax2.set_xlabel('Wind Speed (m/s)')
    ax2.set_ylabel('Damage Ratio / Affected Fraction')
    ax2.set_title('Tropical Cyclone Impact Function')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_ylim(-0.05, 1.05)
    
    plt.tight_layout()
    
    # Save figure
    output_dir = Path(__file__).parent.parent / 'data'
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / 'basic_risk_assessment.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"  Saved visualization to: {output_path}")
    
    # plt.show()  # Uncomment to display interactively
    plt.close()


def main():
    """Main workflow execution."""
    print("=" * 60)
    print("CLIMADA Basic Risk Assessment Workflow")
    print("=" * 60)
    
    try:
        # Step 1: Create/load exposure data
        exposure = create_sample_exposure()
        
        # Step 2: Load hazard data
        hazard = load_sample_hazard()
        
        # Step 3: Define impact functions
        impact_funcs = define_impact_functions()
        
        # Step 4: Calculate risk
        impact = calculate_risk(exposure, hazard, impact_funcs)
        
        # Step 5: Visualize results
        visualize_results(exposure, impact_funcs)
        
        print("\n" + "=" * 60)
        print("Workflow completed successfully!")
        print("=" * 60)
        print("\nNext Steps:")
        print("1. Use real hazard data: TropCyclone.from_ibtracs()")
        print("2. Use LitPop for exposure: Exposures.from_litpop()")
        print("3. Run full impact calculation with complete data")
        print("4. Explore other workflow scripts in this directory")
        
    except Exception as e:
        print(f"\nError during workflow execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
