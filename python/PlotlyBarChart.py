# Source: https://plot.ly/python/bar-charts/
# Source: https://plot.ly/javascript/hover-text-and-formatting/

import time                         # Necessary to calculate the current time
import plotly
# noinspection PyUnresolvedReferences
from plotly.graph_objs import *


class PlotlyBarChart:
    time_now_date = time.strftime("%d.%m.%Y")
    time_now_time = time.strftime("%H:%M:%S")

    bar_x_axis_text = 'Chart creation date: ' + str(time_now_date) + " @ " + str(time_now_time) + '<br>' + \
                      'IAMA db creation date: ' + '17.02.2016' + '<br>' + \
                      'IAMA db MD5 hash: 7C3058809C20C087C97F9DECF6244620'
    chart_title = ""

    bar_x_axis_values = []
    bar_y_axis_answered_values = []
    bar_y_axis_unanswered_values = []
    bar_answered_percentage_values = []

    def __init__(self):
        print('... Initializing plotly bar chart ...')

    def main_method(self, list_of_calculated_data):

        self.fill_x_axis_list(list_of_calculated_data)
        self.fill_y_axis_answered_list(list_of_calculated_data)
        self.fill_y_axis_unanswered_list(list_of_calculated_data)
        self.fill_bar_percentages_values(list_of_calculated_data)
        self.fill_chart_title(list_of_calculated_data)
        self.generate_chart()

    @staticmethod
    def fill_x_axis_list(list_of_calculated_data):
        print(".. filling x_axis with year data now")

        # Adds the years to the x-axis list
        for i in range(1, len(list_of_calculated_data)):
            PlotlyBarChart.bar_x_axis_values.append(list_of_calculated_data[i][0])

    @staticmethod
    def fill_y_axis_answered_list(list_of_calculated_data):
        print(".. filling y_axis_answered list now")

        # Adds the amount of answered questions to the graph
        for i in range(1, len(list_of_calculated_data)):
            PlotlyBarChart.bar_y_axis_answered_values.append(list_of_calculated_data[i][1])


    @staticmethod
    def fill_y_axis_unanswered_list(list_of_calculated_data):
        print(".. filling y_axis_unanswered list now")

        # Adds the amount of unanswered questions to the graph
        for i in range(1, len(list_of_calculated_data)):
            PlotlyBarChart.bar_y_axis_unanswered_values.append(list_of_calculated_data[i][2])

    @staticmethod
    def fill_bar_percentages_values(list_of_calculated_data):
        print(".. filling bar_percentages_values now")

        # Calculates the percentage amount of questions answered / not answered
        for i in range(1, len(list_of_calculated_data)):

            answered_per_iteration = list_of_calculated_data[i][1]
            unanswered_per_iteration = list_of_calculated_data[i][2]
            amount_of_questions = answered_per_iteration + unanswered_per_iteration
            amount_of_percentage_unanswered = (unanswered_per_iteration / amount_of_questions) * 100

            # Shortens huge percentage numbers by rounding them..
            amount_of_percentage_unanswered = float('%.2f' % amount_of_percentage_unanswered)
            amount_of_percentage_answered = 100 - amount_of_percentage_unanswered

            text_to_be_appended = '' + str(amount_of_percentage_answered) + \
                                  '<br><br>' + str(amount_of_percentage_unanswered)

            # The amount of answered questions in percentage will be calculated here
            PlotlyBarChart.bar_answered_percentage_values.append(text_to_be_appended)

    @staticmethod
    def fill_chart_title(list_of_calculated_data):
        print(".. defining plot title now")

        top_worst_string = list_of_calculated_data[0]

        first_year = list_of_calculated_data[1][0]
        last_year = list_of_calculated_data[len(list_of_calculated_data) - 1][0]
        amount_of_questions = list_of_calculated_data[1][1] + list_of_calculated_data[1][2]

        PlotlyBarChart.chart_title = "Question answering status in % <br>" + \
                                     top_worst_string.upper() + " " + str(amount_of_questions) + " <br>" + \
                                     "[" + str(first_year) + " - " + str(last_year) + "]"

    @staticmethod
    def generate_chart():
        print(".. generating chart now!")

        # noinspection PyUnresolvedReferences
        plotly.offline.plot({

            "data": [
                Bar(x=PlotlyBarChart.bar_x_axis_values,
                    y=PlotlyBarChart.bar_y_axis_unanswered_values,
                    name='Not answered',
                    marker=dict(
                        color='rgba(255, 0, 0, 0.7)',
                        line=dict(
                            color='rgba(165, 42, 42, 1.0)',
                            width=2,
                        )
                    )
                    ),
                Bar(x=PlotlyBarChart.bar_x_axis_values,
                    y=PlotlyBarChart.bar_y_axis_answered_values,
                    name='Answered',
                    marker=dict(
                        color='rgba(50, 171, 96, 0.7)',
                        line=dict(
                            color='rgba(50, 171, 96, 1.0)',
                            width=2,
                        )
                    )
                    )],
            "layout": Layout(
                title=PlotlyBarChart.chart_title,
                xaxis=dict(title=PlotlyBarChart.bar_x_axis_text),
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
                    ) for x, y, text in zip(PlotlyBarChart.bar_x_axis_values,
                                            PlotlyBarChart.bar_y_axis_unanswered_values,
                                            PlotlyBarChart.bar_answered_percentage_values)]
            )
        })
