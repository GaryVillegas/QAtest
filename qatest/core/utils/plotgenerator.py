import pandas as pd
from plotly.offline import plot
import plotly.express as px

def generate_plot_analista(casos):
    casos_data = [{
        'estado': caso.estado_display,
        'titulo': caso.project.name
    } for caso in casos]
    df = pd.DataFrame(casos_data)
    if df.empty:
        return '<div>No hay datos disponibles para generar el gráfico.</div>'
    colors = {
        'Sin Ejecutar': 'grey',
        'Aprobado': 'green',
        'Bloqueado': 'yellow',
        'Retesteado': 'orange',
        'Fallido': 'red',
    }
    fig = px.pie(df, names='estado', title='Estado de los Casos', color='estado', color_discrete_map=colors)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    return plot(fig, output_type="div")

def generate_plot_admin(qs):
    casos_data = [{
        'estado': x.estado_display,
        'title': x.project.name
    } for x in qs]
    df = pd.DataFrame(casos_data)
    colors = {
        'Sin Ejecutar': 'grey',
        'Aprobado': 'green',
        'Bloqueado': 'yellow',
        'Retesteado': 'orange',
        'Fallido': 'red', 
    }
    fig = px.pie(df, names='estado', title='Estado de los Casos', color='estado', color_discrete_map=colors)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    return plot(fig, output_type='div')