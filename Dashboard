import pandas as pd 
import plotly.express as px
import streamlit as st
from PIL import Image

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'
st.set_page_config(page_title="GHOST Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide",
                   initial_sidebar_state=st.session_state.sidebar_state
)


# ----GHOST Logo----

image = Image.open('GHOST_LOGO.png')
st.image(image)
st.markdown("""---""")

# ---- READ EXCEL ----

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="GHOST_case.xlsx",
        engine="openpyxl",
        sheet_name="Sample_inventory",
        skiprows=3,
        usecols="B:L",
        nrows=88,
    )
    return df

df = get_data_from_excel()

# ---- SLIDE BAR ----

st.sidebar.header("Filters:")
state = st.sidebar.multiselect(
    "State:",
    options=df["State"].unique(),
    default=df["State"].unique()
)

result = st.sidebar.multiselect(
    "Result:",
    options=df["Result"].unique(),
    default=df["Result"].unique()
)

user = st.sidebar.multiselect(
    "User Name:",
    options=df["User"].unique(),
    default=df["User"].unique()
)

userID = st.sidebar.multiselect(
    "User ID:",
    options=df["UserID"].unique(),
    default=df["UserID"].unique()
)

month = st.sidebar.multiselect(
    "Receiving date:",
    options=df["Month"].unique(),
    default=df["Month"].unique(),
)

df_selection = df.query(
    "State == @state & Result == @result & User == @user & UserID == @userID & Month ==@month "
)

# ---- MAINPAGE ----

st.title(":bar_chart: Dashboard")
st.markdown("##")

# ----INDICATORS----

samples_processed = int(df_selection["Result"].str.count("Po|Ne|Un").sum())
positive_samples = int(df_selection["Result"].str.count("Positive").sum())
negative_samples = int(df_selection["Result"].str.count("Negative").sum())
negative_samples = int(df_selection["Result"].str.count("Undetermined").sum())

first_column, second_column, third_column, forth_column = st.columns(4)
with first_column:
    st.subheader("Samples tested:")
    st.markdown(f":red[Year 2023:\t{samples_processed:,}]")
with second_column:
    st.subheader("Positive Samples:")
    st.markdown(f":red[Total:\t{positive_samples:,}]")
with third_column:
    st.subheader("Negative Samples:")
    st.markdown(f":red[Total:\t{negative_samples}]")
with forth_column:
    st.subheader("Negative Samples:")
    st.markdown(f":red[Total:\t{negative_samples}]")

st.markdown("""---""")

# SAMPLES BY STATE [CHART]

samples_by_state = (
    df_selection.groupby(by=["State", "Result"]).size().to_frame('Results').reset_index()
)
fig_samples_by_state = px.bar(
    samples_by_state,
    x="Result",
    y="State",
    orientation="h",
    title="<b>Samples by State</b>",
    color_discrete_sequence=["#0083B8"] * len(samples_by_state),
    template="plotly_white",
)
fig_samples_by_state.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SAMPLES BY MONTH [CHART]

samples_by_month = df_selection.groupby(by=["State", "Month"]).size().to_frame('Months').reset_index()
fig_samples_by_month = px.bar(
    samples_by_month,
    x="State",
    y="Month",
    title="<b>Monthly</b>",
    color_discrete_sequence=["#0083B8"] * len(samples_by_month),
    template="plotly_white",
)
fig_samples_by_month.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

#---- RADIO BUTTONS ----
display_sections = ['Full List', 'State', 'Buble Graph']
selection_buttons = st.radio("Make a selection:", display_sections)
st.markdown("###")

if selection_buttons == 'Full List':
    st.dataframe(df)

if selection_buttons == 'State':
    if st.button('Show/hide sidebar'):
        st.session_state.sidebar_state = 'expanded' if st.session_state.sidebar_state == 'collapsed' else 'collapsed'
        st.experimental_rerun()    
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_samples_by_state, use_container_width=True)
    right_column.plotly_chart(fig_samples_by_month, use_container_width=True)

if selection_buttons == 'Buble Graph':
    df = px.data.gapminder()

    fig = px.scatter(
        df.query("year==2007"),
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=60,
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

#---- HIDE STREAMLIT STYLE ----

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
