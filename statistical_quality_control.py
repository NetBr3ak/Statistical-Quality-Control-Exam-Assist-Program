import math
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

defective_counts = [45, 29, 33, 43, 21, 65, 39, 28, 55, 44]
sample_size = 150
p_bar = 0.25
significance_level = 0.01


def p_control_chart_analysis(x_data=defective_counts, n=sample_size, p_bar=p_bar, alpha=significance_level):

    sigma_p = math.sqrt(p_bar * (1 - p_bar) / n)
    z_alpha_2 = stats.norm.ppf(1 - alpha/2)

    UCL = p_bar + z_alpha_2 * sigma_p
    LCL = max(0, p_bar - z_alpha_2 * sigma_p)
    CL = p_bar

    sample_proportions = np.array([xi / n for xi in x_data])

    out_of_control_points = []
    for i, p_hat in enumerate(sample_proportions):
        if p_hat > UCL or p_hat < LCL:
            out_of_control_points.append({
                'sample': i + 1,
                'proportion': p_hat,
                'z_score': (p_hat - p_bar) / sigma_p,
                'violation': 'UCL' if p_hat > UCL else 'LCL'
            })

    fig, ax = plt.subplots(figsize=(12, 8))
    sample_indices = np.arange(1, len(x_data) + 1)

    ax.plot(sample_indices, sample_proportions, 'o-', color='#1f77b4',
            linewidth=2, markersize=8, markerfacecolor='white',
            markeredgewidth=2, markeredgecolor='#1f77b4',
            label=r'$\hat{p}_i$ (Sample Proportions)')

    ax.axhline(y=UCL, color='red', linestyle='--', linewidth=2,
               label=f'UCL = {UCL:.4f}')
    ax.axhline(y=CL, color='green', linestyle='-', linewidth=2.5,
               label=rf'$\bar{{p}}$ = {CL:.4f}')
    ax.axhline(y=LCL, color='red', linestyle='--', linewidth=2,
               label=f'LCL = {LCL:.4f}')

    ax.fill_between(sample_indices, LCL, UCL, alpha=0.1, color='lightblue',
                    label='Control Region')

    if out_of_control_points:
        ooc_samples = [pt['sample'] for pt in out_of_control_points]
        ooc_proportions = [pt['proportion'] for pt in out_of_control_points]
        ax.scatter(ooc_samples, ooc_proportions, color='red', s=150,
                   marker='X', linewidths=3, edgecolors='darkred',
                   label='Out of Control Points', zorder=5)

    ax.set_title(rf'P-Chart: Proportion Control Chart ($\alpha$ = {alpha})',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Sample Number (i)', fontsize=12)
    ax.set_ylabel(r'Sample Proportion ($\hat{p}_i$)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', frameon=True)
    ax.set_xticks(sample_indices)

    plt.tight_layout()
    plt.savefig('p_control_chart.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("=" * 60)
    print("P-CHART STATISTICAL PROCESS CONTROL ANALYSIS")
    print("=" * 60)
    print(f"Sample size (n):                    {n}")
    print(f"Process mean proportion (p̄):        {p_bar:.6f}")
    print(f"Standard error (σₚ):                {sigma_p:.6f}")
    print(f"Significance level (α):             {alpha}")
    print(f"Critical z-value (z_{alpha/2:.3f}):           {z_alpha_2:.3f}")
    print(f"Upper Control Limit (UCL):          {UCL:.6f}")
    print(f"Center Line (CL):                   {CL:.6f}")
    print(f"Lower Control Limit (LCL):          {LCL:.6f}")
    print("-" * 60)

    if not out_of_control_points:
        print("✓ PROCESS STATUS: IN STATISTICAL CONTROL")
        print("  All sample proportions fall within 3σ control limits")

        sample_mean = np.mean(sample_proportions)
        sample_std = np.std(sample_proportions, ddof=1)

        print(f"\nProcess Performance Metrics:")
        print(f"Sample mean (p̂):                   {sample_mean:.6f}")
        print(f"Sample standard deviation (s):      {sample_std:.6f}")
        print(f"Theoretical std deviation (σₚ):     {sigma_p:.6f}")

    else:
        print("⚠ PROCESS STATUS: OUT OF STATISTICAL CONTROL")
        print(f"  {len(out_of_control_points)} point(s) exceed control limits")
        print("\nOut-of-Control Point Analysis:")

        for point in out_of_control_points:
            print(f"  Sample {point['sample']:2d}: p̂ = {point['proportion']:.6f} "
                  f"(z = {point['z_score']:+.3f}, violates {point['violation']})")

        actual_alpha = len(out_of_control_points) / len(sample_proportions)
        print(f"\nObserved out-of-control rate:       {actual_alpha:.4f}")
        print(f"Expected false alarm rate (α):      {alpha:.4f}")


if __name__ == "__main__":
    p_control_chart_analysis()
