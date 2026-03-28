import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create a highly polished, high-resolution academic flowchart
fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 11)
ax.axis('off')

# Colors defining IEEE-compliant academic scheme
blue_fill = '#E3F2FD'
blue_edge = '#1E88E5'
green_fill = '#E8F5E9'
green_edge = '#43A047'
orange_fill = '#FFF3E0'
orange_edge = '#FB8C00'

def draw_box(x, y, text, fill, edge, w=5.4, h=0.9):
    # Professional corner rounding
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle="round,pad=0.1,rounding_size=0.2",
                                  linewidth=2.0, edgecolor=edge, facecolor=fill, zorder=3)
    ax.add_patch(rect)
    # Centered bold text
    ax.text(x, y, text, ha='center', va='center', fontsize=12, weight='bold', wrap=True, zorder=4)

def draw_arrow(x1, y1, x2, y2, text=None, tx=None, ty=None):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=2, color='black'), zorder=2)
    if text:
        tx = text_x if tx else (x1+x2)/2 + 0.3
        ty = text_y if ty else (y1+y2)/2
        ax.text(tx, ty, text, fontsize=11, weight='bold', color='darkred', 
                ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none', pad=1), zorder=4)

# Draw central column of algorithm methodology (Y goes from 10 down to 1)
draw_box(4.5, 9.8, "Network Initialization\n(N Sensor Nodes Deployed)", orange_fill, orange_edge)

# Draw regular arrow
draw_arrow(4.5, 9.25, 4.5, 8.55)

draw_box(4.5, 8.0, "Calculate Network\nEnergy Variance", blue_fill, blue_edge)

# Draw regular arrow
draw_arrow(4.5, 7.45, 4.5, 6.75)

draw_box(4.5, 6.2, "Variance > Threshold?", green_fill, green_edge)

# "Yes" Path arrow
ax.annotate('', xy=(4.5, 4.95), xytext=(4.5, 5.65), arrowprops=dict(arrowstyle="->", lw=2, color='black'), zorder=2)
ax.text(4.8, 5.3, "Yes", fontsize=11, weight='bold', color='darkred', va='center')

draw_box(4.5, 4.4, "Extract Multivariate Features\n[E_res, C_prox, P_BS]", blue_fill, blue_edge)
draw_arrow(4.5, 3.85, 4.5, 3.15)

draw_box(4.5, 2.6, "Adaptive K-Means Clustering\n(Identify Capability Tiers)", blue_fill, blue_edge)
draw_arrow(4.5, 2.05, 4.5, 1.35)

draw_box(4.5, 0.8, "Isolate 'Optimal' Tier\n& Calculate Fairness Score", blue_fill, blue_edge)
draw_arrow(4.5, 0.25, 4.5, -0.45)

draw_box(4.5, -1.0, "Role Rotation via Evaluation Metric\n(Determine Valid CHs)", orange_fill, orange_edge)

# "No" Path branch
draw_box(8.5, 6.2, "Retain Previous\nCluster Heads", blue_fill, blue_edge, w=1.8, h=0.9)
# Arrow to side
draw_arrow(7.3, 6.2, 7.5, 6.2) # To the box
ax.text(7.4, 6.4, "No", fontsize=11, weight='bold', color='darkred', ha='center')

# Orthogonal return arrow from Retain Previous to bottom Role Rotation
ax.plot([8.5, 8.5], [5.65, -1.0], lw=2, color='black', zorder=2)
ax.annotate('', xy=(7.3, -1.0), xytext=(8.5, -1.0),
            arrowprops=dict(arrowstyle="->", lw=2, color='black'), zorder=2)

plt.title("System Architecture: Energy-Variance-Triggered\nAdaptive K-Means Classifier", 
          fontsize=16, weight='bold', y=1.05)

# Adjust limits because we went slightly negative
ax.set_ylim(-1.6, 10.5)

plt.savefig('results/plots/better_system_model_diagram.png', dpi=400, bbox_inches='tight')
print("High-resolution diagram successfully saved to better_system_model_diagram.png")
