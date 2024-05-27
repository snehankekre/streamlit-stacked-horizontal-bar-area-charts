import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def data_one():
    return pd.DataFrame(
        {
            "category": ["A", "A", "B", "B"],
            "type": ["X", "Y", "X", "Y"],
            "value": [28, 55, 43, 91],
        }
    )


@st.cache_data
def data_two():
    return pd.DataFrame(
        {
            "col1": list(range(20)) * 3,
            "col2": np.random.randn(60),
            "col3": ["A"] * 20 + ["B"] * 20 + ["C"] * 20,
        }
    )


@st.cache_data
def data_three():
    return pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])


@st.cache_data
def data_four():
    return pd.DataFrame(
        np.random.randint(1, 101, size=(20, 3)), columns=["a", "b", "c"]
    )


def create_bar_chart(data, x, y, color, stack_option, orientation):
    if orientation == "vertical":
        if stack_option is None:
            return (
                alt.Chart(data)
                .mark_bar()
                .encode(
                    x=alt.X(x),
                    y=alt.Y(y),
                    color=alt.Color(color),
                    xOffset=alt.XOffset(color),
                )
            )
        else:
            return (
                alt.Chart(data)
                .mark_bar()
                .encode(
                    x=alt.X(x), y=alt.Y(y, stack=stack_option), color=alt.Color(color)
                )
            )
    else:
        if stack_option is None:
            return (
                alt.Chart(data)
                .mark_bar()
                .encode(
                    x=alt.X(y),
                    y=alt.Y(x),
                    color=alt.Color(color),
                    yOffset=alt.YOffset(color),
                )
            )
        else:
            return (
                alt.Chart(data)
                .mark_bar()
                .encode(
                    x=alt.X(y, stack=stack_option), y=alt.Y(x), color=alt.Color(color)
                )
            )


def create_area_chart(data, stack_option, orientation="vertical"):
    if orientation == "vertical":
        melted_data = pd.melt(data, id_vars=["index"])
        return (
            alt.Chart(melted_data)
            .mark_area()
            .encode(
                x=alt.X("index:O", title="Index"),
                y=alt.Y("value:Q", stack=stack_option),
                color=alt.Color("variable:N", title="Variable"),
            )
        )

    melted_data = pd.melt(data, id_vars=["index"])
    return (
        alt.Chart(melted_data)
        .mark_area()
        .encode(
            x=alt.X("value:Q", stack=stack_option),
            y=alt.Y("index:O", title="Index"),
            color=alt.Color("variable:N", title="Variable"),
        )
    )


qp = st.query_params.to_dict()

disabled_horizontal = False
disabled_orientation = False
disabled_stack = False
disabled_bar = False
disabled_area = False

if qp.get("type") == "area":
    disabled_horizontal = False
    disabled_bar = True
if qp.get("type") == "bar":
    # disabled_horizontal = False
    disabled_area = True
if qp.get("feature") == "stack":
    disabled_orientation = True
if qp.get("feature") == "horizontal":
    disabled_stack = True

tab1, tab2 = st.tabs(["Altair", "Streamlit ✨"])

# User input for chart orientation
orientation = st.sidebar.radio(
    "Chart orientation",
    ["vertical", "horizontal"] if not disabled_horizontal else ["vertical"],
    horizontal=True,
    disabled=disabled_orientation,
    help="Orientation option disabled"
    if disabled_orientation
    else "Select the orientation of the chart",
)

# User input for stack options
stacked = st.sidebar.radio(
    "Stack options",
    ["stacked", "not stacked", "normalize", "center"],
    disabled=disabled_stack,
    help="Select the stack option for the chart"
    if not disabled_stack
    else "Stack option disabled when viewing horizontal charts feature",
)

show_data = st.sidebar.toggle(
    "Show data", False, help="Show the data used to generate the charts"
)


# Define the data
data = data_one()
chart_data = data_two()
area_chart_one_data = data_three().reset_index()
area_chart_two_data = data_four().reset_index()

# Determine stack option for Vega-Lite
stack_option_map = {
    "stacked": "zero",
    "not stacked": None,
    "normalize": "normalize",
    "center": "center",
}
stack_option = stack_option_map[stacked]

with tab1:
    if show_data:
        col1, col2 = st.columns(2)
        if not disabled_horizontal and not disabled_bar:
            col1.dataframe(data, use_container_width=True)
            col1.dataframe(chart_data, use_container_width=True, height=300)

            col2.altair_chart(
                create_bar_chart(
                    data, "category:N", "value:Q", "type:N", stack_option, orientation
                ).properties(height=200),
                use_container_width=True,
            )
            col2.altair_chart(
                create_bar_chart(
                    chart_data, "col1:N", "col2:Q", "col3:N", stack_option, orientation
                ),
                use_container_width=True,
            )
        if not disabled_area:
            col1.dataframe(area_chart_one_data, use_container_width=True)
            col1.dataframe(area_chart_two_data, use_container_width=True, height=350)

            col2.altair_chart(
                create_area_chart(area_chart_one_data, stack_option),
                use_container_width=True,
            )
            col2.altair_chart(
                create_area_chart(area_chart_two_data, stack_option),
                use_container_width=True,
            )
    else:
        if not disabled_horizontal and not disabled_bar:
            st.altair_chart(
                create_bar_chart(
                    data, "category:N", "value:Q", "type:N", stack_option, orientation
                ),
                use_container_width=True,
            )
            st.altair_chart(
                create_bar_chart(
                    chart_data, "col1:N", "col2:Q", "col3:N", stack_option, orientation
                ),
                use_container_width=True,
            )
        if not disabled_area:
            st.altair_chart(
                create_area_chart(area_chart_one_data, stack_option),
                use_container_width=True,
            )
            st.altair_chart(
                create_area_chart(area_chart_two_data, stack_option),
                use_container_width=True,
            )
            st.altair_chart(
                create_area_chart(area_chart_one_data, stack_option, orientation),
                use_container_width=True,
            )
            st.altair_chart(
                create_area_chart(area_chart_two_data, stack_option, orientation),
                use_container_width=True,
            )

with tab2:
    area_chart_one_data = area_chart_one_data.set_index("index")
    area_chart_two_data = area_chart_two_data.set_index("index")
    if show_data:
        col1, col2 = st.columns(2)
        with col1:
            if not disabled_horizontal and not disabled_bar:
                st.dataframe(data, use_container_width=True)
                st.dataframe(chart_data, use_container_width=True, height=300)
            if not disabled_area:
                st.dataframe(area_chart_one_data, use_container_width=True)
                st.dataframe(area_chart_two_data, use_container_width=True, height=350)
        with col2:
            if not disabled_horizontal and not disabled_bar:
                st.bar_chart(
                    data,
                    x="category",
                    y="value",
                    color="type",
                    use_container_width=True,
                    stack=stack_option,
                    horizontal=orientation == "horizontal",
                    height=275,
                )
                st.bar_chart(
                    chart_data,
                    x="col1",
                    y="col2",
                    color="col3",
                    use_container_width=True,
                    stack=stack_option,
                    horizontal=orientation == "horizontal",
                )
            if not disabled_area:
                st.area_chart(area_chart_one_data, stack=stack_option)
                st.area_chart(area_chart_two_data, stack=stack_option)
    else:
        if not disabled_horizontal and not disabled_bar:
            st.bar_chart(
                data,
                x="category",
                y="value",
                color="type",
                use_container_width=True,
                stack=stack_option,
                horizontal=orientation == "horizontal",
                height=400,
            )
            st.bar_chart(
                chart_data,
                x="col1",
                y="col2",
                color="col3",
                use_container_width=True,
                stack=stack_option,
                horizontal=orientation == "horizontal",
            )
        if not disabled_area:
            st.area_chart(
                area_chart_one_data,
                stack=stack_option,
                horizontal=orientation == "horizontal",
            )
            st.area_chart(
                area_chart_two_data,
                stack=stack_option,
                horizontal=orientation == "horizontal",
            )
