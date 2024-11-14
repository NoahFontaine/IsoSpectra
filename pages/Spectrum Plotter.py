from functions.plotting import plot_graph, find_peaks, read_file, find_second_heighest_peak, plot_graph_with_peaks
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
    # Explanation
    st.markdown('<div class="normal_text">Simply drag and drop your .csv file of your spectrum, and a Plotly plot will generate. On the top write you can zoom in, out, choose your window, or even save it. </div>', unsafe_allow_html=True)

with col2:
    # File uploader widget
    uploaded_file = st.file_uploader("Choose a CSV file to input", type="csv")

if uploaded_file is not None:

    data = read_file(uploaded_file)
    
    # Placeholder for the plot
    graph_placeholder = st.empty()

    # Initialize session state variable for active tab
    if 'active_tab' not in st.session_state:
        st.session_state['active_tab'] = "Tab 1"  # Default tab

    tab1, tab2, tab3, tab4 = st.tabs(["Original Plot", "Visualisation editor", "Find peaks", "More analysis"])

    with tab1:
        st.session_state['active_tab'] = "Tab 1" 
        print(st.session_state['active_tab'])
        graph_placeholder.plotly_chart(plot_graph(data=data), use_container_width=True)

    with tab3:
        st.session_state['active_tab'] = "Tab 3"
        print(st.session_state['active_tab'])

        st.markdown('<div class="normal_text">Find peaks by adjusting <strong>height</strong> and <strong>distance</strong> using the sliders bellow.. Note that <strong>height</strong> and <strong>distance</strong>.</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            height = st.slider("Minimum height of the peaks", min_value=1, max_value=find_second_heighest_peak(data)+1, value=None, step=1)
        
        with col2:
            # Center the df and the titles
            st.markdown("""
                <style>
                    .stDataFrame {
                        display: flex;
                        justify-content: center;
                    }
                
                    .stDataFrame thead th {
                        text-align: center;
                        font-weight: bold;
                    }

                </style>
                """, unsafe_allow_html=True)

            # Table of peaks
            peaks = find_peaks(data=data, height=height)
            st.dataframe(peaks, width=500, hide_index=True)
            # For Tab 3, use the plot with peaks
            if st.session_state['modify_graph']:
                graph_placeholder.plotly_chart(plot_graph_with_peaks(data=data, peaks=peaks), use_container_width=True)
