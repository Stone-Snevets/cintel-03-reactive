# Imports
import palmerpenguins as pp
import plotly.express as px
import seaborn as sns
from shiny import reactive, render
from shiny.express import input, ui
from shinywidgets import render_plotly, render_widget

# Load PalmerPenguins into a Dataframe
penguins_df = pp.load_penguins()

# Generate UI
ui.page_opts(title="Stevens: Penguin Data", fillable=True)

# Add a sidebar
with ui.sidebar(open="open"):
    # Add 2nd level header to sidebar
    ui.h2("Sidebar")

    # Create Dropdown Input for Attributes
    ui.input_selectize("field", "Select an Attribute", ['bill_depth_mm', 
                                                        'flipper_length_mm', 
                                                        'body_mass_g',  
                                                        'year'])

    # Create Numeric Input
    ui.input_numeric("num_bins_plotly", "Select Number of Plotly Bins:", 20)

    # Create Slider for number of Seaborn bins
    ui.input_slider("num_bins_sns", "Select Number of Seaborn Bins", 10, 100, 20)

    # Filter Species with Checkbox
    ui.input_checkbox_group(
        "checked",
        "Select Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected="Adelie",
        inline=True
    )

    # Add in Horizontal Rule
    ui.hr()

    # Add in Hyperlink
    ui.a(
        "GitHub Repository",
        href="https://github.com/Stone-Snevets/cintel-02-data",
        target="_blank"
    )

# Layout multiple columns
with ui.layout_columns():

    # Data Table
    @render.data_frame
    def penguins_dt():
        return render.DataTable(penguins_df)

    # Data Grid
    @render.data_frame
    def penguins_dg():
        return render.DataGrid(penguins_df)
    
    # Histogram with Plotly
    @render_widget
    def plotly_histogram():
        return px.histogram(data_frame = penguins_df,
                           x = input.field(),
                           nbins = input.num_bins_plotly()
                           )

    # Histogram with Seaborn
    @render.plot(alt = 'Seaborn Histogram of Palmers Penguins')
    def sns_histogram():
        return sns.histplot(data = penguins_df,
                            x = input.field(),
                            bins = input.num_bins_sns()
                           )

# Create a Card for Scatterplot
with ui.card(full_screen=True):
    ui.card_header('Plotly Scatterplot: Species')
    
    # Scatterplot with Plotly
    @render_plotly
    def plotly_scatterplot():
        return px.scatter(data_frame = penguins_df,
                          x = 'year',
                          y = 'body_mass_g',
                          color = 'species',
                          title = 'Penguin Age (yr) vs. Weight (g)',
                          labels = {'year': 'Year of Birth',
                                   'body_mass_g': 'Weight (g)'}
                         )


# Add Reactive Calculation
@reactive.calc
def filtered_data():
    return penguins_df
