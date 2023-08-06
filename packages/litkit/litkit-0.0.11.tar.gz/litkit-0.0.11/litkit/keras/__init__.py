import plotly.offline as py
import plotly.graph_objs as go


def plot_history(history):
    history = history.history

    py.plot([go.Scatter(x=list(range(len(history[k]))), y=history[k], name=k, mode='line') for k in history.keys()], filename='/tmp/history.html')
