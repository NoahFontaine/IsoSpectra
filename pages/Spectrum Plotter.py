from functions.plotting import plot_graph, find_peaks
import streamlit as st

st.set_page_config(layout="wide", page_title="1D Spectra Plotter", page_icon="🔬")

# Custom CSS for the title
st.markdown("""
    <style>
        .title {
            font-size: 50px;
            font-weight: bold;
            color: #2D3E50;
            text-align: center;
            padding-bottom: 40px;
        }
            
        .normal_text {
            font-size: 30x;
            color: #333333;
        }      

    </style>
""", unsafe_allow_html=True)


col1, col2 = st.columns([1.2, 1])

with col1:
    # Title
    st.markdown('<div class="title">1D NMR Spectra Plotter</div>', unsafe_allow_html=True)
    # Explaination
    st.markdown('<div class="normal_text">Simply drag and drop your .csv file of your spectrum, and a Plotly plot will generate. On the top write you can zoom in, out, choose your window, or even save it. </div>', unsafe_allow_html=True)

with col2:
    # File uploader widget
    uploaded_file = st.file_uploader("Choose a CSV file to input", type="csv")

if uploaded_file is not None:
    st.plotly_chart(plot_graph(data_path=uploaded_file), use_container_width=True)
#find_peaks(data_path=uploaded_file, height=10, distance=10)