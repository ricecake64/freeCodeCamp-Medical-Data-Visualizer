import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np

# import data and assign it to a df variable
df = pd.read_csv('medical_examination.csv')

# add an overweight column. if a person's BMI is over 25, they are overweight
df['overweight'] = np.where((df['weight'] / ((df['height'] / 100) ** 2)) > 25, 1, 0)

# Normalize data by making 0 always good and 1 always bad. If the value of cholesterol or gluc is 1, set the value to 0. If the value is more than 1, set the value to 1.
df['cholesterol'] = np.where((df['cholesterol']) > 1, 1, 0)
df['gluc'] = np.where((df['gluc']) > 1, 1, 0)

# create a cat plot
def draw_cat_plot():
    # create dataframe for the cat plot
    df_cat = pd.melt(df, id_vars=['id', 'cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'], var_name='variable', value_name='variable_value')

    # group the df by 'cardio' using the groupby function and then count the values for the groups. use reset_index to rename the column that is produced by size()
    grouped_df_cat = df_cat.groupby(['cardio', 'variable', 'variable_value']).size().reset_index(name='total')

    # create the cat plot
    fig = sns.catplot(
    grouped_df_cat,        # DataFrame or array
    x='variable',          # Categorical variable for x-axis
    y='total',             # Quantitative variable for y-axis
    hue='variable_value',  # Categorical variable for color grouping
    col='cardio',           # Facet variable for columns
    kind='bar',       
    height=5,           # Height of each facet
    aspect=1,           # Aspect ratio of each facet
)

    # 9
    fig.savefig('catplot.png')
    return fig


# create a heat map function
def draw_heat_map():
    # 11
    df_heat = df.drop(df.loc[df['ap_lo'] > df['ap_hi']].index)
    df_heat = df.drop(df.loc[(df['height'] < df['height'].quantile(0.025))].index)
    df_heat = df.drop(df.loc[(df['height'] > df['height'].quantile(0.975))].index)
    df_heat = df.drop(df.loc[(df['weight'] < df['weight'].quantile(0.025))].index)
    df_heat = df.drop(df.loc[(df['weight'] > df['weight'].quantile(0.975))].index)

    # create the correlation
    corr = df_heat.corr()

    # when visualizing heat maps, usually either the lower triangle or upper triangle (aka above or below the diagonal of 1's) is used
   
    # create a mask for the upper triangle
    mask = np.triu(np.ones(corr.shape)).astype(bool)

    # Apply the mask to the correlation matrix
    lower_triangle = round(corr.mask(mask),1)

    # set up matplot figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # plot correlation matrix
    sns.heatmap(
    lower_triangle,
    annot=True,
    fmt=".2f",
    cmap='coolwarm',
    cbar=True,
    square=True,
    ax=ax
)

    # 16
    fig.savefig('heatmap.png')
    return fig
