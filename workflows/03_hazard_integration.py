#!/usr/bin/env python3
"""
Hazard Data Integration with CLIMADA

This script demonstrates how to work with hazard data:
1. Load historical hazard data from IBTrACS (tropical cyclones)
2. Create custom hazard event sets
3. Work with different hazard types
4. Visualize hazard footprints and intensity

Author: CLIMADA Setup Project
Date: 2025-12-25
"""

import sys
from pathlib import Path

try:
    from climada.hazard import TropCyclone, Hazard
    import matplotlib.pyplot as plt
    import numpy as np
    from datetime import datetime
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure CLIMADA is properly installed.")
    sys.exit(1)


def load_historical_tropical_cyclones(basin='NA', year_range=(2015, 2020)):
    """
    Load historical tropical cyclone data from IBTrACS.
    
    IBTrACS (International Best Track Archive for Climate Stewardship)
    provides global tropical cyclone track data.
    
    Args:
        basin: Basin code ('NA'=North Atlantic, 'EP'=East Pacific, 'WP'=West Pacific, etc.)
        year_range: Tuple of (start_year, end_year)
        
    Returns:
        TropCyclone: Tropical cyclone hazard
    """
    print(f"Loading historical tropical cyclones from IBTrACS...")
    print(f"  Basin: {basin}")
    print(f"  Years: {year_range[0]}-{year_range[1]}")
    
    try:
        # Load from IBTrACS
        # Note: This downloads data on first use
        tc_hazard = TropCyclone.from_ibtracs_netcdf(
            provider='official',
            basin=basin,
            year_range=year_range,
            estimate_missing=True
        )
        
        print(f"  Loaded {tc_hazard.size} storm events")
        print(f"  Date range: {tc_hazard.date[0]} to {tc_hazard.date[-1]}")
        
        return tc_hazard
        
    except Exception as e:
        print(f"  Error loading IBTrACS data: {e}")
        print("  Note: First run requires internet connection to download data")
        print("  Falling back to example hazard structure...")
        return create_example_hazard_structure()


def create_example_hazard_structure():
    """
    Create an example hazard structure for demonstration.
    
    This shows the basic structure of a CLIMADA hazard.
    In practice, use real data from IBTrACS or other sources.
    
    Returns:
        Hazard: Example hazard
    """
    print("\nCreating example hazard structure...")
    
    # Create a simple hazard
    hazard = TropCyclone()
    hazard.haz_type = 'TC'
    hazard.units = 'm/s'
    hazard.centroids.lat = np.array([25.0, 25.5, 26.0])
    hazard.centroids.lon = np.array([-80.0, -80.0, -80.0])
    
    print("  Example hazard structure created")
    print("  Note: Use real data (IBTrACS, etc.) for actual analysis")
    
    return hazard


def create_custom_hazard_event():
    """
    Create a custom hazard event.
    
    This demonstrates how to create a hazard from custom data,
    such as model outputs or scenario definitions.
    
    Returns:
        Hazard: Custom hazard event
    """
    print("\nCreating custom hazard event...")
    
    # Define a grid of centroids (locations)
    n_lat = 20
    n_lon = 20
    lat = np.linspace(25.0, 30.0, n_lat)
    lon = np.linspace(-82.0, -77.0, n_lon)
    lon_grid, lat_grid = np.meshgrid(lon, lat)
    
    # Create hazard
    hazard = Hazard('TC')
    hazard.centroids.lat = lat_grid.flatten()
    hazard.centroids.lon = lon_grid.flatten()
    hazard.units = 'm/s'
    
    # Create a synthetic wind field (example: circular pattern)
    center_lat, center_lon = 27.5, -79.5
    distances = np.sqrt(
        (hazard.centroids.lat - center_lat)**2 +
        (hazard.centroids.lon - center_lon)**2
    )
    
    # Wind speed decreases with distance from center
    max_wind = 70  # m/s (~156 mph, Category 5)
    intensity = max_wind * np.exp(-distances / 2.0)
    
    # Set hazard properties
    hazard.event_id = np.array([1])
    hazard.event_name = ['Synthetic Storm Alpha']
    hazard.date = np.array([datetime(2024, 9, 15).toordinal()])
    hazard.frequency = np.array([0.01])  # 1% annual probability
    hazard.orig = np.array([False])
    
    # Intensity matrix (events × centroids)
    from scipy.sparse import csr_matrix
    hazard.intensity = csr_matrix(intensity.reshape(1, -1))
    
    # Fraction matrix (fraction of centroid affected, usually 1.0)
    hazard.fraction = csr_matrix(np.ones((1, len(intensity))))
    
    print(f"  Created custom hazard with {len(intensity)} centroids")
    print(f"  Max wind speed: {intensity.max():.1f} m/s")
    print(f"  Event frequency: {hazard.frequency[0]:.2%} per year")
    
    return hazard


def analyze_hazard_statistics(hazard):
    """
    Analyze and print hazard statistics.
    
    Args:
        hazard: Hazard data
    """
    print("\nHazard Statistics:")
    print("-" * 40)
    
    try:
        print(f"  Hazard type: {hazard.haz_type}")
        print(f"  Intensity unit: {hazard.units}")
        print(f"  Number of events: {hazard.size}")
        print(f"  Number of centroids: {hazard.centroids.size}")
        
        if hazard.size > 0 and hasattr(hazard, 'intensity'):
            max_intensity = hazard.intensity.max()
            mean_intensity = hazard.intensity.mean()
            print(f"  Max intensity: {max_intensity:.2f} {hazard.units}")
            print(f"  Mean intensity: {mean_intensity:.2f} {hazard.units}")
            
            if hasattr(hazard, 'frequency'):
                total_freq = hazard.frequency.sum()
                print(f"  Total annual frequency: {total_freq:.3f}")
        
    except Exception as e:
        print(f"  Error analyzing hazard: {e}")


def visualize_hazard(hazard, event_idx=0, title="Hazard Intensity"):
    """
    Visualize hazard intensity footprint.
    
    Args:
        hazard: Hazard data
        event_idx: Index of event to visualize
        title: Plot title
    """
    print(f"\nGenerating hazard visualization for event {event_idx}...")
    
    try:
        if hazard.size == 0 or not hasattr(hazard, 'intensity'):
            print("  No intensity data to visualize")
            return
        
        # Extract intensity for selected event
        intensity = hazard.intensity[event_idx].toarray().flatten()
        
        # Create figure
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Spatial intensity map
        ax1 = axes[0]
        scatter = ax1.scatter(
            hazard.centroids.lon,
            hazard.centroids.lat,
            c=intensity,
            s=50,
            cmap='YlOrRd',
            alpha=0.7,
            edgecolors='black',
            linewidth=0.5
        )
        ax1.set_xlabel('Longitude')
        ax1.set_ylabel('Latitude')
        event_name = hazard.event_name[event_idx] if hasattr(hazard, 'event_name') else f"Event {event_idx}"
        ax1.set_title(f'{title}\n{event_name}')
        ax1.grid(True, alpha=0.3)
        cbar = plt.colorbar(scatter, ax=ax1, label=f'Intensity ({hazard.units})')
        
        # Plot 2: Intensity distribution
        ax2 = axes[1]
        # Filter out zero values for better visualization
        nonzero_intensity = intensity[intensity > 0]
        if len(nonzero_intensity) > 0:
            ax2.hist(nonzero_intensity, bins=30, edgecolor='black', alpha=0.7, color='coral')
            ax2.set_xlabel(f'Intensity ({hazard.units})')
            ax2.set_ylabel('Frequency')
            ax2.set_title('Intensity Distribution (non-zero values)')
            ax2.grid(True, alpha=0.3, axis='y')
            
            # Add statistics
            stats_text = f"Max: {nonzero_intensity.max():.1f}\n"
            stats_text += f"Mean: {nonzero_intensity.mean():.1f}\n"
            stats_text += f"Median: {np.median(nonzero_intensity):.1f}\n"
            stats_text += f"Affected: {len(nonzero_intensity)}/{len(intensity)}"
            ax2.text(0.98, 0.97, stats_text,
                     transform=ax2.transAxes,
                     verticalalignment='top',
                     horizontalalignment='right',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        else:
            ax2.text(0.5, 0.5, 'No non-zero intensity values',
                     transform=ax2.transAxes,
                     ha='center', va='center', fontsize=14)
            ax2.set_xlabel(f'Intensity ({hazard.units})')
            ax2.set_ylabel('Frequency')
            ax2.set_title('Intensity Distribution')
        
        plt.tight_layout()
        
        # Save figure
        output_dir = Path(__file__).parent.parent / 'data' / 'hazard'
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f'hazard_visualization_event_{event_idx}.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"  Saved visualization to: {output_path}")
        
        plt.close()
        
    except Exception as e:
        print(f"  Error visualizing hazard: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main workflow execution."""
    print("=" * 60)
    print("CLIMADA Hazard Data Integration")
    print("=" * 60)
    
    try:
        # Example 1: Custom hazard event
        print("\n### Example 1: Custom Hazard Event ###")
        custom_hazard = create_custom_hazard_event()
        analyze_hazard_statistics(custom_hazard)
        visualize_hazard(custom_hazard, event_idx=0, title="Custom Hazard Event")
        
        # Example 2: Historical data (commented out to avoid data download during demo)
        print("\n### Example 2: Historical Tropical Cyclones (Optional) ###")
        print("  To load historical cyclone data, uncomment the following line:")
        print("  tc_hazard = load_historical_tropical_cyclones('NA', (2017, 2018))")
        print("  Note: This requires internet connection for first-time data download")
        
        # Uncomment to try loading real data:
        # tc_hazard = load_historical_tropical_cyclones('NA', (2017, 2018))
        # if tc_hazard and tc_hazard.size > 0:
        #     analyze_hazard_statistics(tc_hazard)
        #     # Visualize first event
        #     visualize_hazard(tc_hazard, event_idx=0, title="Historical Tropical Cyclone")
        
        print("\n" + "=" * 60)
        print("Hazard integration workflow completed!")
        print("=" * 60)
        print("\nNext Steps:")
        print("1. Load real historical data from IBTrACS")
        print("2. Create scenario-based hazards for climate projections")
        print("3. Combine hazard with exposure data for risk calculation")
        print("4. Explore other hazard types (floods, droughts, etc.)")
        print("\nAvailable Hazard Types:")
        print("  - TC: Tropical Cyclones")
        print("  - RF: River Floods")
        print("  - WF: Wildfires")
        print("  - HS: Heat Stress")
        print("  - DR: Droughts")
        print("  - And many more...")
        
    except Exception as e:
        print(f"\nError during workflow execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
