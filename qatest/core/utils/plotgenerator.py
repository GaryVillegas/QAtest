import pandas as pd
from plotly.offline import plot
import plotly.express as px
from plotly.offline import plot

def generate_plot_analista(casos):
    casos_data = [{
        'estado': caso.estado_display,
        'titulo': caso.project.name
    } for caso in casos]
    df = pd.DataFrame(casos_data)
    if df.empty:
        return '<div>No hay datos disponibles para generar el gráfico.</div>'
    colors = {
        'Sin Ejecutar': '#808080',
        'Aprobado': '#4CAF50',
        'Bloqueado': '#FFEB3B',
        'Retesteado': '#FF9800',
        'Fallido': '#F44336',
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
        'Sin Ejecutar': '#808080',
        'Aprobado': '#4CAF50',
        'Bloqueado': '#FFEB3B',
        'Retesteado': '#FF9800',
        'Fallido': '#F44336',
    }
    fig = px.pie(df, names='estado', title='Estado de los Casos', color='estado', color_discrete_map=colors)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    return plot(fig, output_type='div')

def generate_plot_test(qs):
    casos_data = [{
        'estado': x.estado_display,
        'proyecto': x.project.name
    } for x in qs]
    df = pd.DataFrame(casos_data)
    
    if df.empty:
        return '<div>No hay datos disponibles para generar el gráfico.</div>'
    
    colors = {
        'Sin Ejecutar': '#808080',
        'Aprobado': '#4CAF50',
        'Bloqueado': '#FFEB3B',
        'Retesteado': '#FF9800',
        'Fallido': '#F44336',
    }
    
    fig = px.bar(df, x='proyecto', color='estado', title='Estado de los Casos por Proyecto',
                 color_discrete_map=colors, category_orders={'estado': list(colors.keys())})
    
    fig.update_layout(
        bargap=0.2,
        bargroupgap=0.1,
        legend_title_text='Estado',
        xaxis_title='Proyecto',
        yaxis_title='Número de Casos',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    fig.update_xaxes(tickangle=-45)
    
    return plot(fig, output_type='div', include_plotlyjs=False)