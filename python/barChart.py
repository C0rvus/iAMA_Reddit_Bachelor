# Source: https://plot.ly/python/bar-charts/
# Source: https://plot.ly/javascript/hover-text-and-formatting/

import plotly
from plotly.graph_objs import *

x_values = [2009, 2010, 2011, 2012]
y_answered = [4, 2, 3, 7]
percentage_values = ['30%<br><br>70%', '42%', '10%', '20%']

y_not_answered = [3, 1, 2, 5]

not_answered_text_values = ['31%', '42%', '11%', '23410%']

# noinspection PyUnresolvedReferences
plotly.offline.plot({


    "data": [
        Bar(x=x_values,
            y=y_not_answered,
            name='Not answered',
            marker=dict(
                color='rgba(255, 0, 0, 0.7)',
                line=dict(
                    color='rgba(165, 42, 42, 1.0)',
                    width=2,
                )
            )
            ),
        Bar(x=x_values,
            y=y_answered,
            name='Answered',
            marker=dict(
                color='rgba(50, 171, 96, 0.7)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=2,
                )
            )
            )

    ],
    "layout": Layout(
        title="Question status - X years",
        xaxis=dict(title="SACK"),
        barmode='stack',
        annotations=[
                dict(
                    x=x,
                    y=y,
                    text=text,
                    xanchor='center',
                    yanchor='center',
                    showarrow=False,
                    font=dict(family='Arial', size=14, color='rgba(0, 0, 0, 1)')
                ) for x, y, text in zip(x_values, y_not_answered, percentage_values)]
    )
})