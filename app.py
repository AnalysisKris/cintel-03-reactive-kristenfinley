import plotly.express as px
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
import seaborn as sns
import matplotlib.pyplot as plt

# Load penguins dataset
penguins_df = load_penguins()

# Set up the UI page options
ui.page_opts(title="Kristen's Penguins Data", fillable=True)

# Create the sidebar for user interaction
with ui.sidebar(open="open"):
    ui.h2("Sidebar", style="font-size: 16px;")  # Adjusted size for header
    
    # Dropdown to select attribute
    ui.tags.div(
        ui.input_selectize(
            "selected_attribute",
            "Select Attribute",
            ["bill_length_mm", "flipper_length_mm", "body_mass_g"],
        ),
        style="font-size: 12px;"  # Smaller text for dropdown
    )
    
    # Numeric input for Plotly histogram bins
    ui.tags.div(
        ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 30),
        style="font-size: 12px;"
    )
    
    # Slider for Seaborn histogram bins
    ui.tags.div(
        ui.input_slider(
            "seaborn_bin_count",
            "Seaborn Bin Count",
            1,
            100,
            30,
        ),
        style="font-size: 12px;"
    )
    
    # Checkbox group for selecting species
    ui.tags.div(
        ui.input_checkbox_group(
            "selected_species_list",
            "Select Species",
            ["Adelie", "Gentoo", "Chinstrap"],
            selected=["Adelie"],
            inline=True,
        ),
        style="font-size: 12px;"
    )
    
    # Horizontal rule
    ui.hr()
    
    # Link to GitHub repo
    ui.tags.div(
        ui.a(
            "GitHub Code Repository",
            href="https://github.com/AnalysisKris/cintel-03-reactive-kristenfinley",
            target="_blank",
        ),
        style="font-size: 12px;"  # Smaller text for link
    )

# Layout columns for organizing content
with ui.layout_columns():
    # Data Table card
    with ui.card():
        ui.card_header("Data Table")

        @render.data_frame
        def penguin_datatable():
            return penguins_df

    # Data Grid card
    with ui.card():
        ui.card_header("Data Grid")

        @render.data_frame
        def penguin_datagrid():
            return penguins_df

# Add a reactive calculation to filter the data
@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list())]

# Layout columns for visualizations
with ui.layout_columns():
    # Tabbed tabset card for plots
    with ui.navset_card_tab(id="plot_tabs"):
        # Plotly Histogram tab
        with ui.nav_panel("Plotly Histogram"):

            @render_plotly
            def plotly_histogram():
                plotly_hist = px.histogram(
                    data_frame=filtered_data(),
                    x=input.selected_attribute(),
                    nbins=input.plotly_bin_count(),
                    color="species",
                    color_discrete_sequence=["#5e4b8a", "#a55e8b", "#d59b84"],  # Dark purple shades
                ).update_layout(
                    title="Plotly Penguins Data by Attribute",
                    xaxis_title="Selected Attribute",
                    yaxis_title="Count",
                    plot_bgcolor='#ffebee',  # Lighter pink background
                    paper_bgcolor='#ffebee',  # Lighter pink paper background
                )
                return plotly_hist

        # Seaborn Histogram tab
        with ui.nav_panel("Seaborn Histogram"):

            @render.plot
            def seaborn_histogram():
                plt.figure(facecolor='#ffebee')  # Set lighter pink background for Seaborn plots
                seaborn_hist = sns.histplot(
                    data=filtered_data(),
                    x=input.selected_attribute(),
                    bins=input.seaborn_bin_count(),
                    color="#5e4b8a",  # Dark purple color for Seaborn
                )
                seaborn_hist.set_title("Seaborn Penguin Data by Attribute")
                seaborn_hist.set_xlabel("Selected Attribute")
                seaborn_hist.set_ylabel("Count")
                plt.gca().set_facecolor('#ffebee')  # Set lighter pink background for the plot area
                plt.tight_layout()
                return seaborn_hist

        # Plotly Scatterplot tab
        with ui.nav_panel("Plotly Scatterplot"):

            @render_plotly
            def plotly_scatterplot():
                plotly_scatter = px.scatter(
                    filtered_data(),
                    x="bill_length_mm",
                    y="bill_depth_mm",
                    color="species",
                    size_max=8,
                    title="Plotly Scatterplot: Bill Depth and Length",
                    labels={
                        "bill_depth_mm": "Bill Depth (mm)",
                        "bill_length_mm": "Bill Length (mm)",
                    },
                    color_discrete_sequence=["#5e4b8a", "#a55e8b", "#d59b84"],  # Dark purple shades
                ).update_layout(
                    plot_bgcolor='#ffebee',  # Lighter pink background
                    paper_bgcolor='#ffebee',  # Lighter pink paper background
                )
                return plotly_scatter

        # Grouped Bar Plot tab
        with ui.nav_panel("Grouped Bar Plot"):

            @render_plotly
            def grouped_bar_plot():
                grouped_bar = px.bar(
                    filtered_data(),
                    x="island",
                    y="bill_length_mm",
                    color="species",
                    barmode="group",
                    title="Average Bill Length by Island",
                    labels={"bill_length_mm": "Average Bill Length (mm)"},
                    color_discrete_sequence=["#5e4b8a", "#a55e8b", "#d59b84"],  # Dark purple shades
                ).update_layout(
                    plot_bgcolor='#ffebee',  # Lighter pink background
                    paper_bgcolor='#ffebee',  # Lighter pink paper background
                )
                return grouped_bar
