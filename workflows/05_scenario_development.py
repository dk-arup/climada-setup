#!/usr/bin/env python3
"""
Scenario Development with CLIMADA

This script demonstrates how to develop and analyze climate risk scenarios:
1. Current vs. future climate scenarios
2. Socioeconomic scenarios (SSPs)
3. Adaptation measure assessment
4. Scenario comparison and visualization

Author: CLIMADA Setup Project
Date: 2025-12-25
"""

import sys
from pathlib import Path

try:
    from climada.entity import Exposures, ImpactFuncSet, ImpactFunc
    from climada.hazard import Hazard
    from climada.engine import Impact, CostBenefit
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure CLIMADA is properly installed.")
    sys.exit(1)


def create_baseline_scenario():
    """
    Create a baseline (current climate) scenario.
    
    Returns:
        dict: Scenario data with exposure, hazard metadata
    """
    print("Creating baseline scenario (current climate, 2024)...")
    
    scenario = {
        'name': 'Baseline 2024',
        'description': 'Current climate and socioeconomic conditions',
        'year': 2024,
        'climate': 'historical',
        'ssp': None,
        'rcp': None,
        'population_growth': 1.0,  # No growth factor
        'economic_growth': 1.0,    # No growth factor
        'adaptation': 'current'
    }
    
    print(f"  Scenario: {scenario['name']}")
    print(f"  Year: {scenario['year']}")
    print(f"  Climate: {scenario['climate']}")
    
    return scenario


def create_future_scenario(year=2050, ssp='SSP2', rcp='RCP4.5'):
    """
    Create a future climate scenario.
    
    Args:
        year: Future year (e.g., 2050, 2100)
        ssp: Shared Socioeconomic Pathway (SSP1-SSP5)
        rcp: Representative Concentration Pathway (RCP2.6, RCP4.5, RCP8.5)
        
    Returns:
        dict: Future scenario data
    """
    print(f"\nCreating future scenario ({year}, {ssp}, {rcp})...")
    
    # SSP scenarios: socioeconomic development pathways
    ssp_descriptions = {
        'SSP1': 'Sustainability (low challenges)',
        'SSP2': 'Middle of the road (moderate challenges)',
        'SSP3': 'Regional rivalry (high challenges)',
        'SSP4': 'Inequality (unequal challenges)',
        'SSP5': 'Fossil-fueled development (high challenges)'
    }
    
    # RCP scenarios: greenhouse gas concentration trajectories
    rcp_descriptions = {
        'RCP2.6': 'Strong mitigation (2°C target)',
        'RCP4.5': 'Moderate mitigation',
        'RCP8.5': 'High emissions (business as usual)'
    }
    
    # Simplified growth factors (would be more detailed in practice)
    # Based on SSP projections
    years_ahead = year - 2024
    
    if ssp == 'SSP1':
        pop_growth = 1.0 + (0.01 * years_ahead)  # Slow growth
        econ_growth = 1.0 + (0.025 * years_ahead)  # Moderate economic growth
    elif ssp == 'SSP2':
        pop_growth = 1.0 + (0.015 * years_ahead)  # Moderate growth
        econ_growth = 1.0 + (0.02 * years_ahead)
    elif ssp == 'SSP3':
        pop_growth = 1.0 + (0.02 * years_ahead)  # Higher growth
        econ_growth = 1.0 + (0.015 * years_ahead)  # Lower economic growth
    elif ssp == 'SSP5':
        pop_growth = 1.0 + (0.015 * years_ahead)
        econ_growth = 1.0 + (0.035 * years_ahead)  # High economic growth
    else:
        pop_growth = 1.0 + (0.015 * years_ahead)
        econ_growth = 1.0 + (0.02 * years_ahead)
    
    scenario = {
        'name': f'{ssp}-{rcp} {year}',
        'description': f'{ssp_descriptions.get(ssp, "")}, {rcp_descriptions.get(rcp, "")}',
        'year': year,
        'climate': rcp,
        'ssp': ssp,
        'rcp': rcp,
        'population_growth': pop_growth,
        'economic_growth': econ_growth,
        'adaptation': 'baseline'  # Can be modified for adaptation scenarios
    }
    
    print(f"  Scenario: {scenario['name']}")
    print(f"  Description: {scenario['description']}")
    print(f"  Population growth factor: {pop_growth:.2f}x")
    print(f"  Economic growth factor: {econ_growth:.2f}x")
    
    return scenario


def create_adaptation_scenario(base_scenario, adaptation_measures):
    """
    Create a scenario with adaptation measures.
    
    Args:
        base_scenario: Base scenario dict
        adaptation_measures: Dict describing adaptation measures
        
    Returns:
        dict: Scenario with adaptation
    """
    print(f"\nCreating adaptation scenario based on {base_scenario['name']}...")
    
    adapted_scenario = base_scenario.copy()
    adapted_scenario['name'] = f"{base_scenario['name']} + Adaptation"
    adapted_scenario['adaptation'] = adaptation_measures
    
    print(f"  Scenario: {adapted_scenario['name']}")
    print(f"  Adaptation measures:")
    for measure, details in adaptation_measures.items():
        print(f"    - {measure}: {details}")
    
    return adapted_scenario


def apply_scenario_to_exposure(base_exposure, scenario):
    """
    Apply scenario adjustments to exposure data.
    
    Args:
        base_exposure: Baseline exposure data
        scenario: Scenario dict with growth factors
        
    Returns:
        Exposures: Adjusted exposure
    """
    print(f"\nApplying scenario adjustments to exposure...")
    
    # Create a copy
    adj_exposure = base_exposure.copy()
    
    # Apply economic growth
    adj_exposure.gdf['value'] = base_exposure.gdf['value'] * scenario['economic_growth']
    
    # Update reference year
    adj_exposure.ref_year = scenario['year']
    
    print(f"  Adjusted exposure to year {scenario['year']}")
    print(f"  Economic growth factor: {scenario['economic_growth']:.2f}x")
    print(f"  Original total value: ${base_exposure.gdf['value'].sum()/1e9:.2f}B")
    print(f"  Adjusted total value: ${adj_exposure.gdf['value'].sum()/1e9:.2f}B")
    
    return adj_exposure


def simulate_hazard_change(base_hazard, scenario):
    """
    Simulate hazard changes under climate scenario.
    
    In practice, this would use climate model outputs.
    Here we apply simplified adjustments for demonstration.
    
    Args:
        base_hazard: Baseline hazard
        scenario: Climate scenario
        
    Returns:
        Hazard: Adjusted hazard
    """
    print(f"\nSimulating hazard changes for {scenario['climate']}...")
    
    # Climate change intensity factors (simplified)
    # In practice, use downscaled climate model outputs
    intensity_factors = {
        'historical': 1.0,
        'RCP2.6': 1.1,   # 10% increase
        'RCP4.5': 1.2,   # 20% increase
        'RCP8.5': 1.4    # 40% increase
    }
    
    # Frequency factors (events may become more frequent)
    frequency_factors = {
        'historical': 1.0,
        'RCP2.6': 1.1,
        'RCP4.5': 1.3,
        'RCP8.5': 1.6
    }
    
    climate = scenario['climate']
    intensity_factor = intensity_factors.get(climate, 1.0)
    frequency_factor = frequency_factors.get(climate, 1.0)
    
    print(f"  Climate scenario: {climate}")
    print(f"  Intensity adjustment: {intensity_factor:.2f}x")
    print(f"  Frequency adjustment: {frequency_factor:.2f}x")
    print("  Note: Using simplified factors; use climate models for real analysis")
    
    # In a real implementation, would adjust the hazard data
    # For this demo, we just return metadata
    return {
        'scenario': scenario['name'],
        'intensity_factor': intensity_factor,
        'frequency_factor': frequency_factor
    }


def compare_scenarios(scenarios):
    """
    Compare multiple scenarios.
    
    Args:
        scenarios: List of scenario dicts
        
    Returns:
        pd.DataFrame: Comparison table
    """
    print("\n" + "=" * 60)
    print("Scenario Comparison")
    print("=" * 60)
    
    comparison_data = []
    
    for scenario in scenarios:
        comparison_data.append({
            'Scenario': scenario['name'],
            'Year': scenario['year'],
            'Climate': scenario['climate'],
            'SSP': scenario.get('ssp', 'N/A'),
            'Pop Growth': f"{scenario['population_growth']:.2f}x",
            'Econ Growth': f"{scenario['economic_growth']:.2f}x",
            'Adaptation': scenario['adaptation']
        })
    
    df = pd.DataFrame(comparison_data)
    print("\n", df.to_string(index=False))
    
    return df


def visualize_scenario_comparison(scenarios, risk_metrics):
    """
    Visualize comparison of scenarios.
    
    Args:
        scenarios: List of scenario dicts
        risk_metrics: Dict of scenario names to risk metrics
    """
    print("\nGenerating scenario comparison visualizations...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Risk comparison bar chart
    ax1 = axes[0, 0]
    scenario_names = [s['name'] for s in scenarios]
    # Simulate risk values (in real analysis, these would come from Impact calculations)
    baseline_risk = 100  # Million USD
    risk_values = [
        baseline_risk,
        baseline_risk * scenarios[1]['economic_growth'] * 1.2,  # Future scenario
        baseline_risk * scenarios[2]['economic_growth'] * 1.4,  # High emissions
        baseline_risk * scenarios[3]['economic_growth'] * 1.05  # With adaptation
    ]
    
    bars = ax1.bar(range(len(scenario_names)), risk_values, color=['green', 'yellow', 'red', 'blue'], alpha=0.7)
    ax1.set_xticks(range(len(scenario_names)))
    ax1.set_xticklabels(scenario_names, rotation=45, ha='right')
    ax1.set_ylabel('Average Annual Loss (Million USD)')
    ax1.set_title('Risk Comparison Across Scenarios')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, risk_values)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${val:.0f}M',
                ha='center', va='bottom', fontsize=9)
    
    # Plot 2: Growth factors
    ax2 = axes[0, 1]
    x_pos = np.arange(len(scenarios))
    width = 0.35
    
    pop_growth = [s['population_growth'] for s in scenarios]
    econ_growth = [s['economic_growth'] for s in scenarios]
    
    bars1 = ax2.bar(x_pos - width/2, pop_growth, width, label='Population', alpha=0.7)
    bars2 = ax2.bar(x_pos + width/2, econ_growth, width, label='Economic', alpha=0.7)
    
    ax2.set_xlabel('Scenario')
    ax2.set_ylabel('Growth Factor')
    ax2.set_title('Socioeconomic Growth Factors')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([s['name'] for s in scenarios], rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, linewidth=1)
    
    # Plot 3: Risk breakdown by component
    ax3 = axes[1, 0]
    components = ['Hazard\nIntensity', 'Hazard\nFrequency', 'Exposure\nValue', 'Net\nRisk']
    
    # Baseline (all = 1.0)
    baseline_components = [1.0, 1.0, 1.0, 1.0]
    # Future high emissions (example)
    future_components = [1.4, 1.6, scenarios[2]['economic_growth'], 
                        1.4 * 1.6 * scenarios[2]['economic_growth']]
    # With adaptation (reduced risk)
    adapted_components = [1.4, 1.6, scenarios[3]['economic_growth'],
                         1.4 * 1.6 * scenarios[3]['economic_growth'] * 0.75]  # 25% reduction
    
    x = np.arange(len(components))
    width = 0.25
    
    ax3.bar(x - width, baseline_components, width, label='Baseline', alpha=0.7)
    ax3.bar(x, future_components, width, label='Future High Emissions', alpha=0.7)
    ax3.bar(x + width, adapted_components, width, label='With Adaptation', alpha=0.7)
    
    ax3.set_xlabel('Risk Component')
    ax3.set_ylabel('Change Factor (relative to baseline)')
    ax3.set_title('Risk Component Breakdown')
    ax3.set_xticks(x)
    ax3.set_xticklabels(components)
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, linewidth=1)
    
    # Plot 4: Cost-benefit of adaptation
    ax4 = axes[1, 1]
    years = np.arange(2024, 2055, 5)
    
    # Cumulative costs and benefits
    adaptation_cost_annual = 5  # Million USD per year
    benefit_annual = (risk_values[2] - risk_values[3])  # Risk reduction
    
    cumulative_cost = (years - 2024) * adaptation_cost_annual
    cumulative_benefit = (years - 2024) * benefit_annual
    cumulative_net = cumulative_benefit - cumulative_cost
    
    ax4.plot(years, cumulative_cost, 'r-o', label='Adaptation Cost', linewidth=2)
    ax4.plot(years, cumulative_benefit, 'g-s', label='Avoided Losses', linewidth=2)
    ax4.plot(years, cumulative_net, 'b-^', label='Net Benefit', linewidth=2)
    ax4.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Cumulative Value (Million USD)')
    ax4.set_title('Cost-Benefit Analysis of Adaptation')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # Find break-even year
    if cumulative_net[-1] > 0:
        breakeven_idx = np.where(cumulative_net > 0)[0][0]
        breakeven_year = years[breakeven_idx]
        ax4.annotate(f'Break-even: {breakeven_year}',
                    xy=(breakeven_year, 0),
                    xytext=(breakeven_year+2, -50),
                    arrowprops=dict(arrowstyle='->', color='blue'),
                    fontsize=10, color='blue')
    
    plt.tight_layout()
    
    # Save figure
    output_dir = Path(__file__).parent.parent / 'data'
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / 'scenario_comparison.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"  Saved visualization to: {output_path}")
    
    plt.close()


def main():
    """Main workflow execution."""
    print("=" * 60)
    print("CLIMADA Scenario Development")
    print("=" * 60)
    
    try:
        # Create scenarios
        print("\n### Creating Scenarios ###")
        
        # 1. Baseline
        baseline = create_baseline_scenario()
        
        # 2. Future moderate scenario
        future_moderate = create_future_scenario(year=2050, ssp='SSP2', rcp='RCP4.5')
        
        # 3. Future high emissions scenario
        future_high = create_future_scenario(year=2050, ssp='SSP3', rcp='RCP8.5')
        
        # 4. Future with adaptation
        adaptation_measures = {
            'building_codes': 'Enhanced construction standards',
            'early_warning': 'Improved forecast and alert systems',
            'green_infrastructure': 'Natural flood barriers and cooling',
            'insurance': 'Expanded risk transfer mechanisms'
        }
        future_adapted = create_adaptation_scenario(future_high, adaptation_measures)
        
        # Compile scenarios
        scenarios = [baseline, future_moderate, future_high, future_adapted]
        
        # Compare scenarios
        comparison_df = compare_scenarios(scenarios)
        
        # Visualize
        risk_metrics = {}  # In real analysis, calculate from Impact objects
        visualize_scenario_comparison(scenarios, risk_metrics)
        
        print("\n" + "=" * 60)
        print("Scenario development workflow completed!")
        print("=" * 60)
        
        print("\nKey Insights:")
        print("  - Climate change increases both hazard intensity and frequency")
        print("  - Socioeconomic growth increases exposure value")
        print("  - Combined effect can significantly amplify future risk")
        print("  - Adaptation measures can substantially reduce future risk")
        print("  - Cost-benefit analysis helps prioritize adaptation investments")
        
        print("\nNext Steps:")
        print("1. Use actual climate model projections for hazard scenarios")
        print("2. Incorporate detailed SSP exposure projections")
        print("3. Define specific adaptation measures relevant to your context")
        print("4. Calculate impacts for each scenario using CLIMADA Impact class")
        print("5. Use CostBenefit class for detailed adaptation assessment")
        
        print("\nCommon Scenario Frameworks:")
        print("  - SSPs: Shared Socioeconomic Pathways (SSP1-SSP5)")
        print("  - RCPs: Representative Concentration Pathways (2.6, 4.5, 6.0, 8.5)")
        print("  - Combined: SSP-RCP scenarios (e.g., SSP2-4.5)")
        
        print("\nCLIMADA Scenario Resources:")
        print("  - Climate projections: CORDEX, CMIP6 datasets")
        print("  - Socioeconomic projections: IIASA SSP database")
        print("  - Adaptation options: CLIMADA CostBenefit module")
        
    except Exception as e:
        print(f"\nError during workflow execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
