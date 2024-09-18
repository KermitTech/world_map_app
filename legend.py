from shiny import ui
from branca.colormap import linear
import numpy as np

def create_legend(mapping):

    colormap=linear.Paired_03
    min_val, max_val = min(mapping.values()), max(mapping.values())

    num_bins = 5
    step = np.round((max_val - min_val) / num_bins, decimals = 0)
    step = int(step)
    # print(range(num_bins))

    legend_ui = ui.div(
        ui.h4("Number of Peace Agreements", class_= "legend-title"), 
        class_= "legend-container"
    )


    for i in range(num_bins):
        bin_min = min_val + (i * step)

        if i != num_bins -1:
            bin_max = min_val + ((i + 1) * step)
        else: 
            bin_max = max_val

        color = colormap(bin_min / max_val)  # Normalize value to the colormap

        legend_ui.children.append(
            ui.div(
                ui.div(
                    "", # empty string for the color block
                    class_= "legend-color-block",
                    style= f"background-color: {color};"
                ),
                ui.span(f"{round(bin_min, 2)} - {round(bin_max, 2)}", class_="legend-text"),
                class_= "legend-row"
            )
        )

    return legend_ui

















# def create_legend(mapping):

#     colormap=linear.Paired_03
#     min_val, max_val = min(mapping.values()), max(mapping.values())

#     num_bins = 5
#     step = np.round((max_val - min_val) / num_bins, decimals = 0)
#     # print(range(num_bins))

#     legend_html = """
#     <div style='padding: 10px; background-color: white; border: 2px solid grey;'>
#         <h4>No. of peace agreements</h4>"""

#     for i in range(num_bins):
#         bin_min = min_val + (i * step)

#         if i != num_bins -1:
#             bin_max = min_val + ((i + 1) * step)
#         else: 
#             bin_max = max_val

#         color = colormap(bin_min / max_val)  # Normalize value to the colormap

#         legend_html += f"""
#         <div style='display: flex; align-items: center; margin-bottom: 5px;'>
#             <div style='background-color: {color}; width: 20px; height: 10px; margin-right: 5px;'></div>
#             <span>{round(bin_min, 2)} - {round(bin_max, 2)}</span>
#         </div>
#         """

#     legend_html += "</div>"

#     return legend_html