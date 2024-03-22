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
    #-> Number of Bins for Plotly Histogram
    ui.input_numeric("num_bins_plotly", "Select Number of Plotly Bins:", 20)

    # Create Slider
    #-> Number of Bins for Seaborn Histogram
    ui.input_slider("num_bins_sns", "Select Number of Seaborn Bins", 10, 100, 20)

    # Create Checkboxes
    #-> Filter Species
    ui.input_checkbox_group(
        "checked_species",
        "Select Species",
        ["Adelie", "Chinstrap", "Gentoo"],
        selected="Adelie",
        inline=True
    )
    #-> Filter Island
    ui.input_checkbox_group(
        'checked_island',
        'Select Island',
        ['Biscoe', 'Dream', 'Torgersen'],
        selected='Biscoe',
        inline=True
    )
    #-> Filter Gender
    ui.input_checkbox_group(
        'checked_gender',
        'Select Gender',
        ['female', 'male'],
        selected = 'female',
        inline=True
    )

    # Add in Horizontal Rule
    ui.hr()

    # Add in Hyperlink to GitHub Repository
    ui.a(
        "GitHub Repository",
        href="https://github.com/Stone-Snevets/cintel-03-reactive",
        target="_blank"
    )


# Generate Output Layout having Multiple Columns
with ui.layout_columns():

    # Create Data Table
    @render.data_frame
    def penguins_dt():
        return render.DataTable(filtered_data())

    # Create Data Grid
    @render.data_frame
    def penguins_dg():
        return render.DataGrid(filtered_data())
    
    # Create Plotly Histogram
    @render_widget
    def plotly_histogram():
        return px.histogram(data_frame = filtered_data(),
                           x = input.field(),
                           nbins = input.num_bins_plotly()
                           )

    # Create Seaborn Histogram
    @render.plot(alt = 'Seaborn Histogram of Palmers Penguins')
    def sns_histogram():
        return sns.histplot(data = filtered_data(),
                            x = input.field(),
                            bins = input.num_bins_sns()
                           )


# Generate a Card for Scatterplot
with ui.card(full_screen=True):
    ui.card_header('Plotly Scatterplot: Species')
    
    # Create Scatterplot
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
    # Make sure at least one island is selected
    req(input.checked_island())
    # Make sure at least one gender is selected
    req(input.checked_gender())
    
    # Select Species from Penguins Dataframe
    select_species = penguins_df['species'].isin(input.checked_species())
    # Select Island from Penguins Dataframe
    select_island = penguins_df['island'].isin(input.checked_island())
    # Select Gender from Penguins Dataframe
    select_gender = penguins_df['sex'].isin(input.checked_gender())

    # Return Filtered Dataframe
    return penguins_df[select_species & select_island & select_gender]
