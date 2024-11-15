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
        
        .normal_text_two {
            font-size: 30x;
            color: #333333;
            padding-bottom: 15px;
        }
        
        .normal_text_three {
            font-size: 30x;
            color: #333333;
            padding-bottom: 40px;
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

    current_tab = st.segmented_control(label="Select your options", options=["Visualisation Magic", "Peak Wizard", "More analysis"], label_visibility="hidden", default=None)
    
    st.markdown("<br>" * 1, unsafe_allow_html=True)  # Adds line breaks

    if current_tab == None:
        st.plotly_chart(plot_graph(data=data), use_container_width=True)

    if current_tab == "Visualisation Magic":
        graph_placeholder = st.empty()

        col1, col2, col3 = st.columns(3)

        # Toggle options, choose colors, ...
        show_xgrid = col1.toggle("Show vertical gridlines", value=False)
        main_color = col2.color_picker("Main NMR color (default #1f77b4)", value="#1f77b4")
        peak_color = col3.color_picker("Peaks color (default #d62728)", value="#d62728")

        # Graph with all the options
        graph_placeholder.plotly_chart(plot_graph(data=data, main_color=main_color, show_xgrid=show_xgrid),
                                                    use_container_width=True)

    if current_tab == "Peak Wizard":

        st.markdown('<div class="normal_text_two">Find peaks by adjusting the minimum <strong>height</strong> and/or <strong>prominence</strong> using the sliders below.</div>', unsafe_allow_html=True)
        st.markdown('<div class="normal_text">&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp<strong>Height</strong>: gives you a minimum intensity value that your peak needs to be above.</div>', unsafe_allow_html=True)
        st.markdown('<div class="normal_text_two">&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp<strong>Prominence</strong>: determines the minimum height necessary to descend to get from the peak to any higher terrain.</div>', unsafe_allow_html=True)
        st.markdown('<div class="normal_text_three"><strong>Scroll down</strong> and you will see the an updated plot with the peaks, and a table of all the relevant peak values (both δ and <i>I</i>). You can then choose whether or not you want to see the checmical shift of the peaks, and if you want vertical gridlines. Of course, you can modify the color of your traces.</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            height = st.slider("Minimum height of the peaks", min_value=1, max_value=find_second_heighest_peak(data)+1, value=1, step=1)
        with col2:
            prominence = st.slider("How much do you want your peaks to stand out?", min_value=1, max_value=int(find_second_heighest_peak(data)/10), value=int(find_second_heighest_peak(data)/20), step=1)
        
        col1, col2 = st.columns([2.2, 1])

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
            peaks = find_peaks(data=data, height=height, prominence=prominence)
            st.dataframe(peaks, width=400, hide_index=True)
        
        with col1:
            graph_placeholder = st.empty()

            col1, col2, col3, col4 = st.columns(4)

            # Toggle options, choose colors, ...
            show_peaks = col1.toggle("Show peaks", value=True)
            PPM_on = col1.toggle("Show PPM values of peaks", value=False)
            show_xgrid = col4.toggle("Show vertical gridlines", value=False)
            main_color = col2.color_picker("Main NMR color (default #1f77b4)", value="#1f77b4")
            peak_color = col3.color_picker("Peaks color (default #d62728)", value="#d62728")

        # Graph with all the options
        graph_placeholder.plotly_chart(plot_graph_with_peaks(data=data, peaks=peaks, show_peak_labels=PPM_on,main_color=main_color,
                                                            peak_color=peak_color, show_peaks=show_peaks, show_xgrid=show_xgrid),
                                                            use_container_width=True)
        
