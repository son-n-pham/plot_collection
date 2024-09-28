import json
import matplotlib.pyplot as plt
import numpy as np
import io
import base64


def plot_doc_chart(rop_min, rop_max, rpm_min, rpm_max, doc_value, text_above_line, text_below_line, font_size=20):
    # Create arrays for RPM and ROP
    rpm = np.linspace(rpm_min, rpm_max, 1000)
    rop = np.linspace(rop_min, rop_max, 1000)

    # Create a meshgrid
    RPM, ROP = np.meshgrid(rpm, rop)

    # Calculate DOC (inches/revolution), avoiding division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        DOC = np.where(RPM != 0, (ROP * 12) / (RPM * 60), np.inf)

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot the contour
    levels = [0, doc_value, np.max(DOC[np.isfinite(DOC)])]
    contour = ax.contourf(RPM, ROP, DOC, levels=levels,
                          colors=['yellow', 'limegreen'], alpha=0.8, extend='both')

    # Add contour line for the specific DOC value
    doc_contour = ax.contour(RPM, ROP, DOC, levels=[
                             doc_value], colors='black', linestyles='solid')

    # Customize the plot
    ax.set_xlabel('Rotary Speed (RPM)', fontsize=font_size)
    ax.set_ylabel('Rate of Penetration (ft/hr)', fontsize=font_size)
    ax.set_title(f'DOC Chart (DOC = {doc_value} in/rev)', fontsize=font_size+2)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Get the path of the DOC contour line
    path = doc_contour.collections[0].get_paths()[0]
    vertices = path.vertices

    # Find points for text placement
    mid_point = vertices[len(vertices)//2]
    end_point = vertices[-1]

    # Calculate text positions based on plot dimensions
    plot_height = rop_max - rop_min
    plot_width = rpm_max - rpm_min

    # Add text annotations with dynamic positioning
    upper_text_y = rop_max - plot_height * 0.2
    lower_text_y = plot_height * 0.2

    ax.text(plot_width * 0.3, upper_text_y,
            text_above_line,
            ha='center', va='center', fontsize=font_size,
            bbox=dict(facecolor='limegreen', alpha=0.8, edgecolor='black'))

    ax.text(plot_width * 0.7, lower_text_y,
            text_below_line,
            ha='center', va='center', fontsize=font_size,
            bbox=dict(facecolor='yellow', alpha=0.8, edgecolor='black'))

    # Add DOC value annotation outside the plot area
    ax.annotate(f'{doc_value} in/rev', xy=(end_point[0], end_point[1]),
                xytext=(5, 0), textcoords='offset points',
                ha='left', va='center', fontsize=font_size,
                bbox=dict(boxstyle='round,pad=0.5',
                          fc='white', ec='gray', alpha=0.8),
                annotation_clip=False)

    # Adjust layout to make room for annotation
    plt.tight_layout()

    # Set axis limits to remove white space
    ax.set_xlim(rpm_min, rpm_max)
    ax.set_ylim(rop_min, rop_max)

    # Show the plot
    plt.show()


def lambda_handler(event, context):
    rop_min = event['rop_min']
    rop_max = event['rop_max']
    rpm_min = event['rpm_min']
    rpm_max = event['rpm_max']
    doc_value = event['doc_value']
    text_above_line = event['text_above_line']
    text_below_line = event['text_below_line']
    font_size = event.get('font_size', 20)

    plot_doc_chart(rop_min, rop_max, rpm_min, rpm_max, doc_value,
                   text_above_line, text_below_line, font_size)

    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'image/png'},
        'body': image_base64,
        'isBase64Encoded': True
    }
