import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

INPUT_BASE_PATH = "rpg_api/tests/locust/reports/spike_test/"

# Load CSV data
stats = pd.read_csv(f"{INPUT_BASE_PATH}data/locust_report_stats.csv")
history = pd.read_csv(f"{INPUT_BASE_PATH}data/locust_report_stats_history.csv")

# Check the column names in the 'history' DataFrame
# print(history.columns)

# Create figure for Requests/s
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot Requests/s on the primary y-axis
ax1.set_xlabel("Timestamp")
ax1.set_ylabel("Requests/s", color="tab:green")
ax1.plot(history["Timestamp"], history["Requests/s"], color="tab:green")
ax1.tick_params(axis="y", labelcolor="tab:green")


# Add a second y-axis sharing the same x-axis to plot User count
ax2 = ax1.twinx()
ax2.set_ylabel("User Count", color="tab:blue")
ax2.plot(history["Timestamp"], history["User Count"], color="tab:blue")
ax2.tick_params(axis="y", labelcolor="tab:blue")


fig.tight_layout()  # To ensure the layout is neat
fig.subplots_adjust(top=0.85)  # Add some margin top
plt.title("Metrics Over Time")
plt.savefig(f"{INPUT_BASE_PATH}data/combined_metrics_plot.png")

# New figure for Failures/s
fig2, ax3 = plt.subplots(figsize=(12, 6))

# Plot Failures/s
ax3.set_xlabel("Timestamp")
ax3.set_ylabel("Failures/s", color="tab:red")
ax3.plot(history["Timestamp"], history["Failures/s"], color="tab:red")
ax3.tick_params(axis="y", labelcolor="tab:red")


# Add a second y-axis sharing the same x-axis to plot Requests/s
ax4 = ax3.twinx()
ax4.set_ylabel("Requests/s", color="tab:blue")
ax4.plot(history["Timestamp"], history["Requests/s"], color="tab:blue")
ax4.tick_params(axis="y", labelcolor="tab:blue")

fig2.tight_layout()
fig2.subplots_adjust(top=0.85)
plt.title("Failures Over Time")
plt.savefig(f"{INPUT_BASE_PATH}data/failures_over_time.png")

# Create PDF
pdf = canvas.Canvas(f"{INPUT_BASE_PATH}locust_report.pdf", pagesize=letter)
pdf.drawString(72, 720, "Locust Test Report")

# Add plots
pdf.drawImage(
    f"{INPUT_BASE_PATH}data/combined_metrics_plot.png",
    72,
    500,
    width=400,
    height=200,
)

pdf.drawImage(
    f"{INPUT_BASE_PATH}data/failures_over_time.png",
    72,
    300,
    width=400,
    height=200,
)


pdf.save()
