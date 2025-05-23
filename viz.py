import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Slider, HoverTool
from bokeh.layouts import column
from bokeh.models import (ColumnDataSource, DataTable, HoverTool, IntEditor,
                          NumberEditor, NumberFormatter, SelectEditor,
                          StringEditor, StringFormatter, TableColumn)
from bokeh.io import curdoc

# Load dataset
df = pd.read_csv('gapminder.txt')

# Filter years and Asian regions
df = df[(df['Year'] >= 2000) & (df['Year'] <= 2013)]
asian_df = df[df['Region'].str.contains('Asia')].copy()

# Create a data dictionary by year
data_by_year = {}
years = sorted(asian_df['Year'].unique())

for year in years:
    year_data = asian_df[asian_df['Year'] == year]
    data_by_year[year] = {
        'x': year_data['Fertility'],
        'y': year_data['lifeExp'],
        'country': year_data['Country'],
        'pop': year_data['pop'] / 1e6,  # Convert to millions
        'region': year_data['Region']
    }
# Create ColumnDataSource for the first year
initial_year = years[0]
source = ColumnDataSource(data=data_by_year[initial_year])

# Set up the figure
p = figure(
    title=f"Fertility vs Life Expectancy in Asia ({initial_year})",
    x_axis_label='Fertility Rate (children per woman)',
    y_axis_label='Life Expectancy (years)',
    x_range=(0, 8),
    y_range=(50, 90),
    height=600, width=800,
    tools="pan,wheel_zoom,box_zoom,reset"
)

# Draw the bubbles
p.circle('x', 'y', size='pop', source=source, fill_alpha=0.3, line_color='black', legend_field='region')

# Add Hover Tool
hover = HoverTool(tooltips=[
    ("Country", "@country"),
    ("Fertility", "@x"),
    ("Life Expectancy", "@y"),
    ("Population (M)", "@pop"),
])
p.add_tools(hover)

# Create the Slider and Callback
slider = Slider(start=years[0], end=years[-1], value=years[0], step=1, title="Year")

def update_plot(attr, old, new):
    year = slider.value
    new_data = data_by_year[year]
    source.data = new_data
    p.title.text = f"Fertility vs Life Expectancy in Asia ({year})"

slider.on_change('value', update_plot)

# Combine into a layout
layout = column(slider, p)
curdoc().add_root(layout)
