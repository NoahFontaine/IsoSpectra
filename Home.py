from functions.weather import get_temperature, get_temperature_delta_from_Milan
import streamlit as st

#def show_Home():
st.set_page_config(layout="wide", page_title="Home Page", page_icon="🏠")

# Title of the app

# Custom CSS for the title
st.markdown("""
    <style>
        .title {
            font-family: 'Open Sans', sans-serif;
            font-size: 70px;
            font-weight: bold;
            color: #2D3E50;
            text-align: center;
            margin-top: 210px;
        }
            
        .for_sofia {
            font-family: 'Open Sans', sans-serif;
            font-size: 30x;
            color: #7D8A96;
            padding-bottom: 40px;
            text-align: center;
        }      
            
        .logo_home {
            font-family: 'Open Sans', sans-serif;
            font-size: 70px;
            color: #2D3E50;
            text-align: center;
            padding-bottom: 40px;

    </style>
""", unsafe_allow_html=True)

# Title with the custom CSS class
st.markdown('<div class="title">Welcome to IsoSpectra</div>', unsafe_allow_html=True)
st.markdown('<div class="logo_home">⚛</div>', unsafe_allow_html=True)

st.markdown('<div class="for_sofia">For my lovely Sofia ❤️. This is the homepage of IsoSpectra, a specialised app where you can visualise and analyse NMR spectra in an intuitive and beatiful way. Choose between a variety of options. </div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1])
with col4:
    st.page_link("pages/Spectrum Plotter.py", label="Plot basic 1D NMR spectra here", icon="🔬", use_container_width=True)

st.markdown("<br>" * 10, unsafe_allow_html=True)  # Adds 5 line breaks

st.metric(label="Temperature in Sofia's city", value=f"{get_temperature("London")} K", delta=f"{get_temperature_delta_from_Milan("London")} K")