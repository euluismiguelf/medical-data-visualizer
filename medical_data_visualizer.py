import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Importante: las funciones deben devolver el objeto fig para que las pruebas automaticas funcionen.

def draw_cat_plot():
    # 1) Importar los datos
    df = pd.read_csv('medical_examination.csv')

    # 2) Añadir la columna 'overweight'
    # BMI = weight (kg) / (height (m))^2
    bmi = df['weight'] / ((df['height'] / 100) ** 2)
    df['overweight'] = (bmi > 25).astype(int)

    # 3) Normalizar 'cholesterol' y 'gluc' (0 = bueno, 1 = malo)
    df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
    df['gluc'] = (df['gluc'] > 1).astype(int)

    # 4) Crear DataFrame para el cat plot usando pd.melt
    df_cat = pd.melt(df,
                     id_vars=['cardio'],
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
                    )

    # 5) No hace falta renombrar columnas en este caso; sns.catplot con kind='count' funciona con el DataFrame 'melted'
    # Pero para claridad, aseguramos nombres esperados: variable, value, cardio (pd.melt ya los deja así)

    # 6) Dibujar el catplot usando seaborn
    # Usamos kind='count' para contar valores 0/1 por variable, separados por cardio
    catplot = sns.catplot(
        data=df_cat,
        kind='count',
        x='variable',
        hue='value',
        col='cardio'
    )

    fig = catplot.fig
    # Ajustes estéticos
    fig.subplots_adjust(top=0.85)
    fig.suptitle('Categorical Plot of Medical Features by Cardio', fontsize=14)

    # No modificar las siguientes 2 líneas
    fig.savefig('catplot.png')
    return fig


def draw_heat_map():
    # 1) Importar datos
    df = pd.read_csv('medical_examination.csv')

    # 2) Añadir la columna 'overweight'
    bmi = df['weight'] / ((df['height'] / 100) ** 2)
    df['overweight'] = (bmi > 25).astype(int)

    # 3) Normalizar 'cholesterol' y 'gluc'
    df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
    df['gluc'] = (df['gluc'] > 1).astype(int)

    # 4) Limpiar datos para df_heat:
    # - ap_lo <= ap_hi
    # - height entre 2.5 y 97.5 percentiles
    # - weight entre 2.5 y 97.5 percentiles
    df_heat = df.copy()

    df_heat = df_heat[df_heat['ap_lo'] <= df_heat['ap_hi']]

    h_low = df_heat['height'].quantile(0.025)
    h_high = df_heat['height'].quantile(0.975)
    df_heat = df_heat[(df_heat['height'] >= h_low) & (df_heat['height'] <= h_high)]

    w_low = df_heat['weight'].quantile(0.025)
    w_high = df_heat['weight'].quantile(0.975)
    df_heat = df_heat[(df_heat['weight'] >= w_low) & (df_heat['weight'] <= w_high)]

    # 5) Calcular matriz de correlación
    corr = df_heat.corr()

    # 6) Generar máscara para la mitad superior
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 7) Configurar figura
    fig, ax = plt.subplots(figsize=(12, 10))

    # 8) Dibujar el heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.1f',
        vmax=0.3,
        center=0,
        square=True,
        linewidths=.5,
        cbar_kws={'shrink': .5},
        ax=ax
    )

    # No modificar las siguientes 2 líneas
    fig.savefig('heatmap.png')
    return fig
