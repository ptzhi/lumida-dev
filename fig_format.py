
###############################################################################
# Uniform Figure Properties
###############################################################################

# Uniform X axes properties for time series graphs
xaxis = dict(
    showspikes=True, spikemode='across', spikesnap='cursor', spikedash='dot',spikethickness=-1, spikecolor='rgba(0, 0, 0, 1)',
    # showline=True,
    showgrid=True,
    rangeslider_visible=False,
    # rangeslider=dict(
    #     thickness=0.1,
        # autorange=False,
        # range=[
        #     '2019-01-01',
        #     '2022-11-01',
        # ],
    # ),
    rangeselector=dict(
        # activecolor='rgb(80,103,132)',
        bgcolor='rgba(0,0,0,0)',
        xanchor='left', x=0.022,
        yanchor='top', y=1.08,
        buttons=[
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            # dict(count=2, label="2y", step="year", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(step="all")
        ],
    ),
)

# Uniform Y axes y_properties
yaxis= dict(
    zeroline=True, zerolinewidth=0.15, zerolinecolor='rgba(135, 135, 135, 0.46)',
)

# Uniform layout
layout=dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=True,
    hovermode='x unified',
    hoverlabel=dict(
        bgcolor='rgba(235, 235, 235, 0.85)'),
    spikedistance=-1,
    # margin=dict(l=25, r=25, t=80, b=70),
    margin=dict(l=0, r=0, t=80, b=70),
    title={
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    },
    title_font=dict(
        color='#787b7e',
        size=16,
        family='Nunito Sans'
    ),
    title_pad=dict(
        t=20,
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5
    )
)
