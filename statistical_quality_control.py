import math
import matplotlib.pyplot as plt

# Constants for data input (you can tweak these as needed)
DATA = [45, 29, 33, 43, 21, 65, 39, 28, 55, 44]  # Sample data
SAMPLE_SIZE = 150  # Total sample size
P0 = 0.25  # Expected proportion of defects
ALPHA = 0.01  # Significance level


def optimized_control_chart_analysis(
    data=DATA, sample_size=SAMPLE_SIZE, p0=P0, alpha=ALPHA
):
    # Calculate important parameters based on the input
    sigma_p = math.sqrt(
        p0 * (1 - p0) / sample_size
    )  # Standard deviation of proportions
    z = 2.576  # z-score for alpha = 0.01 (two-tailed)
    UCL = p0 + z * sigma_p  # Upper Control Limit
    LCL = p0 - z * sigma_p  # Lower Control Limit

    # Calculate the proportions of defects for each sample
    p_values = [d / sample_size for d in data]

    # Identify which samples are out of control limits
    out_of_control = [(i + 1, p) for i, p in enumerate(p_values) if p > UCL or p < LCL]

    # Create a control chart visualization
    samples = list(range(1, len(data) + 1))
    plt.figure(figsize=(10, 6))
    plt.plot(samples, p_values, marker="o", linestyle="-", color="blue")
    plt.axhline(y=UCL, color="r", linestyle="--", label="Upper Control Limit (UCL)")
    plt.axhline(y=p0, color="g", linestyle="-", label="Center = $p_0$")
    plt.axhline(y=LCL, color="r", linestyle="--", label="Lower Control Limit (LCL)")
    plt.fill_between(samples, LCL, UCL, color="yellow", alpha=0.3)
    plt.title("Proportion Control Chart (p)")
    plt.xlabel("Sample Number")
    plt.ylabel("Proportion of Defects")
    plt.xticks(samples)
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()

    # Save the chart as an image
    plt.savefig("control_chart.png")

    # Provide a concise and engaging description
    description = ""
    if not out_of_control:
        description += "The process is in control and performing well."
    else:
        samples_out = ", ".join(str(sample[0]) for sample in out_of_control)
        description += f"The process is out of control! Deviations were spotted in samples {samples_out}."
        for sample, p in out_of_control:
            if p < LCL:
                description += f" In sample {sample}, the value dipped below the Lower Control Limit."
            else:
                description += (
                    f" In sample {sample}, the value shot past the Upper Control Limit."
                )
        description += (
            f" The chance of a false alarm is quite low, not exceeding {alpha/2}."
        )
    print(description)

optimized_control_chart_analysis()
