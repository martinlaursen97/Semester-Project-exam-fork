import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

INPUT_BASE_PATH = "rpg_api/tests/locust/reports/spike_test/"

# Load CSV data
stats = pd.read_csv(f"{INPUT_BASE_PATH}data/locust_report_stats.csv")
history = pd.read_csv(f"{INPUT_BASE_PATH}data/locust_report_stats_history.csv")

# Check the column names in the 'history' DataFrame
print(history.columns)

fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot Requests/s on the primary y-axis
ax1.set_xlabel("Timestamp")
ax1.set_ylabel(
    "Requests/s", color="tab:green"
)  # We already handled the x-label with ax1
ax1.plot(history["Timestamp"], history["Requests/s"], color="tab:green")
ax1.tick_params(axis="y", labelcolor="tab:green")


# Add a second y-axis sharing the same x-axis to plot User count
ax2 = ax1.twinx()
ax2.set_ylabel("User Count", color="tab:blue")
ax2.plot(history["Timestamp"], history["User Count"], color="tab:blue")
ax2.tick_params(axis="y", labelcolor="tab:blue")

# Synchronize y-axes
y_min = min(ax1.get_ylim()[0], ax2.get_ylim()[0])
y_max = max(ax1.get_ylim()[1], ax2.get_ylim()[1])
ax1.set_ylim(y_min, y_max)
ax2.set_ylim(y_min, y_max)

fig.tight_layout()  # To ensure the layout is neat
plt.title("Metrics Over Time")
plt.savefig(f"{INPUT_BASE_PATH}data/combined_metrics_plot.png")

# Create PDF
pdf = canvas.Canvas(f"{INPUT_BASE_PATH}locust_report.pdf", pagesize=letter)
pdf.drawString(72, 720, "Locust Test Report")

# Add plots and other data
pdf.drawImage(
    f"{INPUT_BASE_PATH}data/combined_metrics_plot.png",
    72,
    500,
    width=400,
    height=200,
)

pdf.save()
