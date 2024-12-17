import plotly.graph_objects as go
import pandas as pd
from scipy import signal

def read_file(data_path: str) -> pd.DataFrame:
    return pd.read_csv(data_path)

def find_nmr_domain(data: pd.DataFrame):
    return [min(data.iloc[:, 0]), max(data.iloc[:, 0])]


def plot_graph(data: pd.DataFrame, main_color="#1f77b4", show_xgrid=False):

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.iloc[:,0], y=data.iloc[:,1], name="NMR Trace", line=dict(color=main_color)))
    fig.update_layout(xaxis=dict(range=[data.iloc[-1,0], data.iloc[0,0]]), xaxis_title="Chemical shift δ to TMS (PPM)", yaxis_title="Relative Signal Intensity I (a.u.)", height=600)

    # Choose to show x_grid or not
    if show_xgrid == True:   
        fig.update_layout(xaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.1)', gridwidth=0.2))

    return fig


def find_peaks(data: pd.DataFrame, height: int, prominence: int):
    
    # peaks are the indices
    peaks, properties = signal.find_peaks(data.iloc[:,1], height=height, prominence=prominence)

    ppm_peaks = data.iloc[:,0][peaks]
    intensity_peaks = data.iloc[:,1][peaks]

    df_peaks = pd.DataFrame({'PPM values of the peaks': ppm_peaks, 'Relative Intensity of the peaks': intensity_peaks})

    return df_peaks


def find_second_heighest_peak(data: pd.DataFrame):

    peaks, properties = signal.find_peaks(data.iloc[:,1])

    # Sort the list in descending order and get the second element
    second_largest = sorted(data.iloc[:,1][peaks], reverse=True)[1]

    return int(second_largest)


def plot_graph_with_peaks(data: pd.DataFrame, peaks: pd.DataFrame, main_color="#1f77b4", peak_color="#ff7f0e", show_peak_labels=False, show_peaks=True, show_xgrid=False): # Original graph with the peaked colored

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.iloc[:,0], y=data.iloc[:,1], name="NMR Trace", line=dict(color=main_color)))
    if show_peaks == True:
        if show_peak_labels == False:
            fig.add_trace(go.Scatter(x=peaks["PPM values of the peaks"], y=peaks["Relative Intensity of the peaks"], name="Peaks", mode="markers",
                                marker=dict(color=peak_color, size=8, opacity=0.3)))
        else:
            fig.add_trace(go.Scatter(x=peaks["PPM values of the peaks"], y=peaks["Relative Intensity of the peaks"], name="Peaks", mode="markers+text", textposition="top center", text=round(peaks["PPM values of the peaks"], 2),
                                marker=dict(color=peak_color, size=8, opacity=0.3)))

    fig.update_layout(xaxis=dict(range=[data.iloc[-1,0], data.iloc[0,0]]), xaxis_title="Chemical shift δ to TMS (PPM)", yaxis_title="Relative Signal Intensity I (a.u.)", height=500)

    if show_xgrid == True:   
        fig.update_layout(xaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.1)', gridwidth=0.2))


    return fig


def plot_graph_with_prediction(data: pd.DataFrame, prediction: pd.DataFrame, scale: float, main_color="#1f77b4", prediction_color="#ff7f0e", show_predictions=True, show_xgrid=False):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.iloc[:,0], y=data.iloc[:,1], name="NMR Trace", line=dict(color=main_color)))
    if show_predictions == True:
        fig.add_trace(go.Scatter(x=prediction.iloc[:,0], y=prediction.iloc[:,1]*scale, name="Prediction", line=dict(color=prediction_color, width=0.5)))

    fig.update_layout(xaxis=dict(range=[data.iloc[-1,0], data.iloc[0,0]]), xaxis_title="Chemical shift δ to TMS (PPM)", yaxis_title="Relative Signal Intensity I (a.u.)", height=500)

    if show_xgrid == True:   
        fig.update_layout(xaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.1)', gridwidth=0.2))
    
    return fig