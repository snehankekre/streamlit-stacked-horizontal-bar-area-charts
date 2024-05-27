# streamlit-simple-chart-axis-labels

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stack-horizontal-bar-area-charts-poc.streamlit.app)

Streamlit's [st.bar_chart](https://docs.streamlit.io/develop/api-reference/charts/st.bar_chart) and [st.area_chart](https://docs.streamlit.io/develop/api-reference/charts/st.area_chart) have `horizontal` and `stack` parameters to control the orientation of the charts and the stacking of the data.


### `st.bar_chart`

| Parameter | Description |
| --- | --- |
| `horizontal` *(bool)* | Determines the orientation of the chart: ``True``: Displays the chart horizontally, with the x-axis and y-axis swapped. ``False``: Displays the chart vertically (default). |
| `stack` *(bool, "normalize", "zero", or "center"*) | Determines how the bars are stacked: True: Stacks the bars on top of each other (default). "normalize": Stacks and normalizes the bars to 100%. "zero": Stacks the bars with the baseline set to 0. "center": Stacks the bars with the baseline set to the center of the bars.|

### `st.area_chart`

| Parameter | Description |
| --- | --- |
| `horizontal` *(bool)* | Determines the orientation of the chart: ``True``: Displays the chart horizontally, with the x-axis and y-axis swapped. ``False``: Displays the chart vertically (default). |
| `stack` *(bool, "normalize", "zero", or "center"*) | Determines how the data is stacked. If False (default), doesn't stack the data.  If True, stacks the data. If "normalize", normalizes the data. If "zero", stacks the data and sets the baseline to zero. If "center", stacks the data and sets the baseline to the middle of the y range. |



See the [PoC implementation](https://github.com/streamlit/streamlit/compare/develop...snehan/feature/chart-titles)