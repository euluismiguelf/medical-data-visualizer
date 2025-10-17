from medical_data_visualizer import draw_cat_plot, draw_heat_map

if __name__ == "__main__":
    print("Generando catplot...")
    fig1 = draw_cat_plot()
    print("Se guardó catplot.png")

    print("Generando heatmap...")
    fig2 = draw_heat_map()
    print("Se guardó heatmap.png")
