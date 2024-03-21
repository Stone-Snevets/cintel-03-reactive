
# Imports
import palmerpenguins as pp
import plotly.express as px
import seaborn as sns
from shiny import reactive, render, req
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
        "checked_species",
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
        href="https://github.com/Stone-Snevets/cintel-03-reactive",
        target="_blank"
    )

# Layout multiple columns
with ui.layout_columns():

    # Data Table
    @render.data_frame
    def penguins_dt():
        return render.DataTable(filtered_data())

    # Data Grid
    @render.data_frame
    def penguins_dg():
        return render.DataGrid(filtered_data())
    
    # Histogram with Plotly
    @render_widget
    def plotly_histogram():
        return px.histogram(data_frame = filtered_data(),
                           x = input.field(),
                           nbins = input.num_bins_plotly()
                           )

    # Histogram with Seaborn
    @render.plot(alt = 'Seaborn Histogram of Palmers Penguins')
    def sns_histogram():
        return sns.histplot(data = filtered_data(),
                            x = input.field(),
                            bins = input.num_bins_sns()
                           )

# Create a Card for Scatterplot
with ui.card(full_screen=True):
    ui.card_header('Plotly Scatterplot: Species')
    
    # Scatterplot with Plotly
    @render_plotly
    def plotly_scatterplot():
        return px.scatter(data_frame = filtered_data(),
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
    # Make sure at least one species is selected
    req(input.checked_species())
    # Return User's Species Selection
    select_species = penguins_df['species'].isin(input.checked_species())
    return penguins_df[select_species]
