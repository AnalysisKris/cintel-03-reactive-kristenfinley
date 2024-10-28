# cintel-03-reactive-kristenfinley
CC3.1: Orient and Engage (Reactive Calcs, Filtering DataFrames)

## Goal
To get the charts to use the results of our `filtered_data()` function instead. To get started, at the end of `app.py`, add the following:

```python
# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input function used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df
