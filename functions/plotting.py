import plotly.graph_objects as go
import pandas as pd
from scipy import signal

def plot_graph(data_path: str):
    data = pd.read_csv(data_path)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.iloc[:,0], y=data.iloc[:,1]))
    fig.update_layout(xaxis=dict(range=[data.iloc[-1,0], data.iloc[0,0]]), xaxis_title="", yaxis_title="", height=600)

    return fig


def find_peaks(data_path: str, height: int, distance: int):
    data = pd.read_csv(data_path)
    print(data)
    # peaks are the indices
    peaks, properties = signal.find_peaks(data.iloc[:,1], height=height, distance=distance)

    ppm_peaks = data.iloc[:,0][peaks]
    intensity_peaks = data.iloc[:,1][peaks]

    return ppm_peaks