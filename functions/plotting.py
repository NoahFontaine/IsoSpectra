import plotly.graph_objects as go
import pandas as pd
from scipy import signal

def read_file(data_path: str) -> pd.DataFrame:
    return pd.read_csv(data_path)


def plot_graph(data: pd.DataFrame):

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.iloc[:,0], y=data.iloc[:,1]))
    fig.update_layout(xaxis=dict(range=[data.iloc[-1,0], data.iloc[0,0]]), xaxis_title="", yaxis_title="", height=600)

    return fig


def find_peaks(data: pd.DataFrame, height: int):
    
    # peaks are the indices
    peaks, properties = signal.find_peaks(data.iloc[:,1], height=height)

    ppm_peaks = data.iloc[:,0][peaks]
    intensity_peaks = data.iloc[:,1][peaks]

    df_peaks = pd.DataFrame({'PPM values of the peaks': ppm_peaks, 'Relative Intensity of the peaks': intensity_peaks})

    return df_peaks


def find_second_heighest_peak(data: pd.DataFrame):

    peaks, properties = signal.find_peaks(data.iloc[:,1])

    # Sort the list in descending order and get the second element
    second_largest = sorted(data.iloc[:,1][peaks], reverse=True)[1]

    return int(second_largest+1)


def plot_graph_with_peaks(data: pd.DataFrame, peaks: pd.DataFrame): # Original graph with the peaked colored

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.iloc[:,0], y=data.iloc[:,1]))
    fig.add_trace(go.Scatter(x=peaks["PPM values of the peaks"], y=peaks["Relative Intensity of the peaks"], mode="markers"))

    fig.update_layout(xaxis=dict(range=[data.iloc[-1,0], data.iloc[0,0]]), xaxis_title="", yaxis_title="", height=600)

    return fig