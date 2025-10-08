import math
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

# Your data here - change these values for your specific problem
defective_counts = [45, 29, 33, 43, 21, 65, 39,
                    28, 55, 44]  # number of defects per sample
sample_size = 150  # how many items in each sample
target_proportion = 0.25  # expected proportion of defects (p-bar or smth)
alpha = 0.01  # significance level (usually 0.01 or 0.05)


def create_p_chart(data=defective_counts, n=sample_size, p_target=target_proportion, sig_level=alpha):
    # Step 1: Calculate standard error (how much variation we expect)
    std_error = math.sqrt(p_target * (1 - p_target) / n)

    # Step 2: Get the z-value for our confidence level
    z_value = stats.norm.ppf(1 - sig_level/2)

    # Step 3: Calculate control limits
    upper_limit = p_target + z_value * std_error  # UCL i guesss
    # LCL (can't be negative)
    lower_limit = max(0, p_target - z_value * std_error)
    center_line = p_target  # CL

    # Step 4: Convert defect counts to proportions
    proportions = np.array([defects / n for defects in data])

    # Step 5: Find which samples are out of control
    problem_samples = []
    for i, proportion in enumerate(proportions):
        if proportion > upper_limit or proportion < lower_limit:
            problem_samples.append({
                'sample_number': i + 1,
                'proportion': proportion,
                'z_score': (proportion - p_target) / std_error,
                'limit_violated': 'UCL' if proportion > upper_limit else 'LCL'
            })

    # Step 6: Create the chart
    fig, ax = plt.subplots(figsize=(12, 8))
    sample_numbers = np.arange(1, len(data) + 1)

    # Plot the actual sample proportions
    ax.plot(sample_numbers, proportions, 'o-', color='#1f77b4',
            linewidth=2, markersize=8, markerfacecolor='white',
            markeredgewidth=2, markeredgecolor='#1f77b4',
            label='Sample Proportions')

    # Draw control limit lines
    ax.axhline(y=upper_limit, color='red', linestyle='--', linewidth=2,
               label=f'UCL = {upper_limit:.4f}')
    ax.axhline(y=center_line, color='green', linestyle='-', linewidth=2.5,
               label=f'Target = {center_line:.4f}')
    ax.axhline(y=lower_limit, color='red', linestyle='--', linewidth=2,
               label=f'LCL = {lower_limit:.4f}')

    # Shade the "in control" area
    ax.fill_between(sample_numbers, lower_limit, upper_limit, alpha=0.1, color='lightblue',
                    label='Control Region')

    # Mark problem samples with red X's
    if problem_samples:
        bad_sample_nums = [pt['sample_number'] for pt in problem_samples]
        bad_proportions = [pt['proportion'] for pt in problem_samples]
        ax.scatter(bad_sample_nums, bad_proportions, color='red', s=150,
                   marker='X', linewidths=3, edgecolors='darkred',
                   label='Out of Control', zorder=5)

    # Chart labels and formatting
    ax.set_title(f'P-Chart: Process Control (α = {sig_level})',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Sample Number', fontsize=12)
    ax.set_ylabel('Proportion Defective', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', frameon=True)
    ax.set_xticks(sample_numbers)

    # Save and show the chart
    plt.tight_layout()
    plt.savefig('p_control_chart.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Step 7: Print the results
    print("=" * 60)
    print("P-CHART ANALYSIS RESULTS")
    print("=" * 60)
    print(f"Sample size (n):                    {n}")
    print(f"Target proportion (p-bar):          {p_target:.6f}")
    print(f"Standard error:                     {std_error:.6f}")
    print(f"Significance level (alpha):         {sig_level}")
    print(f"Z-value used:                       {z_value:.3f}")
    print(f"Upper Control Limit (UCL):          {upper_limit:.6f}")
    print(f"Center Line (CL):                   {center_line:.6f}")
    print(f"Lower Control Limit (LCL):          {lower_limit:.6f}")
    print("-" * 60)

    # Check if process is in control
    if not problem_samples:
        print("✓ GOOD NEWS: Process is in control!")
        print("  All samples are within the control limits")

        # Calculate some basic stats
        actual_mean = np.mean(proportions)
        actual_std = np.std(proportions, ddof=1)

        print(f"\nActual Performance:")
        print(f"Actual mean proportion:             {actual_mean:.6f}")
        print(f"Actual standard deviation:          {actual_std:.6f}")
        print(f"Expected standard deviation:        {std_error:.6f}")

    else:
        print("⚠ WARNING: Process is OUT OF CONTROL!")
        print(f"  {len(problem_samples)} sample(s) are outside control limits")
        print("\nProblem Samples:")

        for sample in problem_samples:
            print(f"  Sample {sample['sample_number']:2d}: {sample['proportion']:.6f} "
                  f"(z-score: {sample['z_score']:+.3f}, violates {sample['limit_violated']})")

        # Calculate false alarm rate
        false_alarm_rate = len(problem_samples) / len(proportions)
        print(f"\nActual out-of-control rate:         {false_alarm_rate:.4f}")
        print(f"Expected false alarm rate:          {sig_level:.4f}")


# Run the analysis
if __name__ == "__main__":
    create_p_chart()
