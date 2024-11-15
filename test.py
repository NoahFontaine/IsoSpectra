import plotly.graph_objects as go
import pandas as pd

def plot_graph(data: pd.DataFrame, color="blue"):

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.iloc[:,0], y=data.iloc[:,1], name="NMR Trace"))
    fig.update_layout(xaxis=dict(range=[data.iloc[-1,0], data.iloc[0,0]]), xaxis_title=r"Chemical shift $\delta$ to TMS (PPM)", yaxis_title=r"Relative Signal Intensity $I$ (a.u.)", height=600)

    fig.show()


plot_graph(data=pd.read_csv("CA step 1 product + pt2 crude nmr.csv"))