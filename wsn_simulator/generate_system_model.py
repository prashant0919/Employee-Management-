import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as pe

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 11)
ax.axis('off')

def draw_box(ax, x, y, width, height, text, bg_color='#E8F0FE'):
    rect = patches.FancyBboxPatch((x, y), width, height,
                                  boxstyle="round,pad=0.1",
                                  linewidth=1.5, edgecolor='black', facecolor=bg_color)
    ax.add_patch(rect)
    ax.text(x + width/2, y + height/2, text, ha='center', va='center', fontsize=11, wrap=True, weight='bold')

def draw_arrow(ax, x1, y1, x2, y2, text=None):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor='black', shrink=0.01, width=2, headwidth=10))
    if text:
        ax.text((x1+x2)/2 + 0.2, (y1+y2)/2, text, fontsize=10, weight='bold', color='red')

# Nodes
draw_box(ax, 3, 9.5, 4, 1, "Sensing Field:\nN Sensor Nodes", '#FFE0B2')
draw_box(ax, 2.5, 7.5, 5, 1, "Network Energy Variance Trigger?", '#C8E6C9')

draw_box(ax, 7, 6, 2.5, 1, "Continue Previous\nRound Protocol", '#BBDEFB')
draw_box(ax, 2.5, 5.5, 5, 1, "Extract Multivariate Tensor:\n[E_res, C_prox, P_BS]", '#BBDEFB')

draw_box(ax, 2.5, 3.5, 5, 1, "Adaptive K-Means Clustering\n(Evaluate Silhouette Score)", '#BBDEFB')
draw_box(ax, 2.5, 1.5, 5, 1, "Isolate 'Optimal' Tier\n& Calculate Fairness Score", '#BBDEFB')

draw_box(ax, 3, -0.5, 4, 1, "Rotate Cluster Heads\n& Route to Base Station", '#FFE0B2')

# Arrows main pipeline
draw_arrow(ax, 5, 9.5, 5, 8.5)
draw_arrow(ax, 5, 7.5, 5, 6.5, "Yes")
draw_arrow(ax, 5, 5.5, 5, 4.5)
draw_arrow(ax, 5, 3.5, 5, 2.5)
draw_arrow(ax, 5, 1.5, 5, 0.5)

# Trigger 'No' condition path
ax.annotate('', xy=(8.25, 7), xytext=(7.5, 8),
            arrowprops=dict(facecolor='black', shrink=0.01, width=2, headwidth=10))
ax.text(6.5, 8.2, 'No', fontsize=10, weight='bold', color='red')

# Loop back arrow from Continue block to Rotate CH
ax.annotate('', xy=(7.5, 0), xytext=(8.25, 6),
            arrowprops=dict(facecolor='black', shrink=0.01, width=2, headwidth=10))

plt.title("System Flowchart: Energy-Variance-Triggered\nAdaptive K-Means Capability Classifier", fontsize=15, weight='bold', pad=10)
plt.tight_layout()
plt.savefig('results/plots/system_model_diagram.png', dpi=300, bbox_inches='tight')
print("Diagram saved successfully.")
