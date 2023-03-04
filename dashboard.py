import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'
st.set_page_config(page_title="GHOST Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide",
                   initial_sidebar_state=st.session_state.sidebar_state
)

# ----Horizontal radios-----

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)

st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:regular;padding-left:2px;}</style>', unsafe_allow_html=True)

# ----GHOST Logo----
left, center, right = st.alignment(3)
image = Image.open('GHOST_LOGO.png')
with center:
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
        usecols="B:P",
        nrows=626,
    )
    return df


df = get_data_from_excel()

# ---- SORTING THE DATA ----
months = {'Jan':1,'Feb':2,'Mar':3, 
          'Apr':4, 'May':5, 'Jun':6, 
          'Jul':7, 'Aug':8, 'Sep':9, 
          'Oct':10, 'Nov':11, 'Dec':12}

df = df.sort_values('Month', key = lambda x: x.apply(lambda x:months[x]))

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

month = st.sidebar.multiselect(
    "Receiving date:",
    options=df["Month"].unique(),
    default=df["Month"].unique(),
)


df_selection = df.query(
    "State == @state & Result == @result & User == @user & Month ==@month "
)

# ---- MAINPAGE ----

st.title(":bar_chart: Dashboard")
st.markdown("##")

# ----INDICATORS----

samples_processed = int(df_selection["Result"].str.count("Po|Ne|Un").sum())
positive_samples = int(df_selection["Result"].str.count("Positive").sum())
negative_samples = int(df_selection["Result"].str.count("Negative").sum())
undetermined_samples = int(df_selection["Result"].str.count("Undetermined").sum())

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
    st.subheader("Undetermined Samples:")
    st.markdown(f":red[Total:\t{undetermined_samples}]")

st.markdown("""---""")

# SAMPLES BY STATE [CHART]

samples_by_state = df_selection.groupby(by=["State", "Result"]).size().to_frame('Results').reset_index()
results = samples_by_state['Result'].unique()
states = samples_by_state['State'].unique()

bars_objects = []
for state in states: 
    bar = go.Bar(name=state, y=results, orientation='h',
                 x=samples_by_state.query("State == @state")['Results']
                 )
    bars_objects.append(bar)
    
fig_samples_by_state = go.Figure(bars_objects)
fig_samples_by_state.update_traces(hovertemplate='Samples: %{x}') ## Add whatever text you want
fig_samples_by_state.update_layout(barmode='stack')

# SAMPLES BY MONTH [CHART]

samples_by_month = df_selection.groupby(by=["State", "Month"]).size().to_frame('Months').reset_index()
monthly = samples_by_month['Month'].unique()
states = samples_by_month['State'].unique()

ordered_months = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"]

bars_objects = []
for state in states: 
    bar = go.Bar(name=state, x=ordered_months,
                 y=samples_by_month.query("State == @state")['Months']
                 )
    bars_objects.append(bar)
    
fig_samples_by_month = go.Figure(bars_objects)
fig_samples_by_month.update_traces(hovertemplate='Samples: %{y}') ## Add whatever text you want
fig_samples_by_month.update_layout(barmode='stack')

#---- MISEQ GRAPHS ----

miseq_performance1 = df.groupby(['Result','Instrument'])['Result'].count().to_frame('Count').reset_index()
miseq_performance1 = miseq_performance1[miseq_performance1['Instrument'].str.contains('MiSeq-1')]
fig_miseq_performance1 = px.pie(miseq_performance1, values='Count', names='Result')
fig_miseq_performance1.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
fig_miseq_performance1.update_layout(title_text='MiSeq-1', title_x=0.5)

miseq_performance2 = df.groupby(['Result','Instrument'])['Result'].count().to_frame('Count').reset_index()
miseq_performance2 = miseq_performance2[miseq_performance2['Instrument'].str.contains('MiSeq-2')]
fig_miseq_performance2 = px.pie(miseq_performance2, values='Count', names='Result')
fig_miseq_performance2.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
fig_miseq_performance2.update_layout(title_text='MiSeq-2', title_x=0.5)

miseq_performance3 = df.groupby(['Result','Instrument'])['Result'].count().to_frame('Count').reset_index()
miseq_performance3 = miseq_performance3[miseq_performance3['Instrument'].str.contains('MiSeq-3')]
fig_miseq_performance3 = px.pie(miseq_performance3, values='Count', names='Result')
fig_miseq_performance3.update_traces(textposition='inside', textinfo='percent+label')
fig_miseq_performance3.update_layout(title_text='MiSeq-3', title_x=0.5)


#---- BUBBLE GRAPHS ----

df_1 = px.data.gapminder()
fig_Bubble = px.scatter(
    df_1.query("year==2007"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)

#---- RADIO BUTTONS ----
display_sections = ['Sample Search', 'Monthly Search', 'Genotype Search', 'Cluster Identification', 'Instrument', 'Sequence Query','Full List', 'State', 'Buble Graph']
selection_buttons = st.radio("Make a selection:", display_sections)
st.markdown("###")
col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1]) 

if selection_buttons == 'Sample Search':
    specimen = col1.text_input('Please enter specimen ID:', 'Exact sample ID')
    sample_search = df[df['Sample ID'] == (specimen)]
    st.dataframe(sample_search)

if selection_buttons == 'Monthly Search':
    month_input = col1.text_input('Please enter month:', 'Three letter code')
    month_search = df[df['Month'].str.contains(month_input.capitalize())]
    st.dataframe(month_search)  
    
if selection_buttons == 'Genotype Search':
    genotype = col1.text_input('Please enter genotype:', '1a, 1b, 3a, etc')
    genotype_search = df[df['Genotype'] == (genotype)]
    st.dataframe(genotype_search) 
    
if selection_buttons == 'Cluster Identification':
    cluster = col1.text_input('Please enter cluster ID:', 'Cluster-ID')
    cluster_id = df[df['Cluster'] == (cluster)]
    st.dataframe(cluster_id) 
    
if selection_buttons == 'Instrument':
    miseq = col1.text_input('Please enter instrument number:', 'MiSeq-1, MiSeq-2, etc')
    miseq_report = df[df['Instrument'] == (miseq)]
    st.dataframe(miseq_report)
    left_fig, center_fig, right_fig = st.columns(3)
    left_fig.plotly_chart(fig_miseq_performance1, theme="streamlit", use_container_width=True)
    center_fig.plotly_chart(fig_miseq_performance2, theme="streamlit", use_container_width=True)
    right_fig.plotly_chart(fig_miseq_performance3, theme="streamlit", use_container_width=True)

if selection_buttons == 'Sequence Query':
    sequence = st.text_input('Please enter nucleotyde sequence:', 'Only DNA sequences allowed')
    sequence_query = df[df['Sequence'].str.contains(sequence)]
    st.dataframe(sequence_query) 
    
if selection_buttons == 'Full List':
    df_sorted = df.sort_index()
    st.dataframe(df_sorted)

if selection_buttons == 'State':
    if st.button('Show/hide filter menu'):
        st.session_state.sidebar_state = 'expanded' if st.session_state.sidebar_state == 'collapsed' else 'collapsed'
        st.experimental_rerun()    
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_samples_by_state, theme="streamlit", use_container_width=True)
    right_column.plotly_chart(fig_samples_by_month, theme="streamlit", use_container_width=True)

if selection_buttons == 'Buble Graph':
    st.plotly_chart(fig_Bubble, theme="streamlit", use_container_width=True)

#---- HIDE STREAMLIT STYLE ----

hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
