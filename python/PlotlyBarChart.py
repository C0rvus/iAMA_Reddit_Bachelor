# Tutorials used within this class:
# 1. (29.03.2016 @ 04:45) -
# https://plot.ly/python/bar-charts/
# 1. (29.03.2016 @ 06:18) -
# https://plot.ly/javascript/hover-text-and-formatting/

import time                         # Necessary to calculate the current time
import plotly
# noinspection PyUnresolvedReferences
from plotly.graph_objs import *


class PlotlyBarChart:
    """The class to create a stacked bar chart.
        This class is heavily modified because it pyplot normally is not designed to run offline this way..

    Args:
        -
    Returns:
        -
    """

    time_now_date = time.strftime("%d.%m.%Y")
    time_now_time = time.strftime("%H:%M:%S")

    bar_x_axis_text = 'Chart creation date: ' + str(time_now_date) + " @ " + str(time_now_time) + '<br>' + \
                      'IAMA db creation date: ' + '17.02.2016' + '<br>' + \
                      'IAMA db MD5 hash: 7C3058809C20C087C97F9DECF6244620'
    chart_title = ""

    # Contains values what the chart is about..
    bar_value_description = []
    bar_x_axis_values = []

    # i.e. (amount answered questions || amount of tier 1 questions)
    bar_y_axis_first_values = []

    # i.e. (amount unanswered questions || amount of questions on any tier)
    bar_y_axis_second_values = []

    # i.e. (answered / unanswered questions || amount of questions on tier 1 / any)
    bar_first_n_second_values_percentage = []

    def __init__(self):
        """Instanciates the class

        Args:
            -
        Returns:
            -
        """

        print('... Initializing plotly bar chart ...')

    def main_method(self, list_of_calculated_data):
        """Sequential fills the necessary varibales for the graph
        Structure of list_of_calculated_data:

        [ "sorting", [year, answered, unanswered], [year, answered, unanswered], ... ]
        i.e. ["top",
              [2009, 900, 1536],
              [2010, 500, 500],
              [2011, 300, 700]
              ]

        Args:
            list_of_calculated_data (list): Contains sorting method, and the years data
        Returns:
            -
        """

        self.fill_x_axis_list(list_of_calculated_data)
        self.fill_y_axis_answered_list(list_of_calculated_data)
        self.fill_y_axis_unanswered_list(list_of_calculated_data)
        self.fill_bar_percentages_values(list_of_calculated_data)
        self.fill_chart_title_n_bar_description(list_of_calculated_data)
        self.fill_bar_description(list_of_calculated_data)
        self.generate_chart()

    @staticmethod
    def fill_x_axis_list(list_of_calculated_data):
        """Fills the "x axis" with the values of the years

        Args:
            list_of_calculated_data (list) : Will be iterated to gain necessary values
        Returns:
            -
        """

        print(".. filling x_axis with year data now")

        # Adds the years to the x-axis list
        for i in range(1, len(list_of_calculated_data)):
            PlotlyBarChart.bar_x_axis_values.append(list_of_calculated_data[i][0])

    @staticmethod
    def fill_y_axis_answered_list(list_of_calculated_data):
        """Fills an bar within the chart with values of the amount of unanswered questions

        Args:
            list_of_calculated_data (list) : Will be iterated to gain necessary values
        Returns:
            -
        """

        print(".. filling y_axis_answered list now")

        # Adds the amount of answered questions to the graph
        for i in range(1, len(list_of_calculated_data)):
            PlotlyBarChart.bar_y_axis_first_values.append(list_of_calculated_data[i][1])

    @staticmethod
    def fill_y_axis_unanswered_list(list_of_calculated_data):
        """Fills an bar within the chart with values of the amount of unanswered questions

        Args:
            list_of_calculated_data (list) : Will be iterated to gain necessary values
        Returns:
            -
        """

        print(".. filling y_axis_unanswered list now")

        # Adds the amount of unanswered questions to the graph
        for i in range(1, len(list_of_calculated_data)):
            PlotlyBarChart.bar_y_axis_second_values.append(list_of_calculated_data[i][2])

    @staticmethod
    def fill_bar_percentages_values(list_of_calculated_data):
        """Calculates percentages to be shown within the graph..
            This is not supported within pyplot under normal circumstances.. so we're tricking the HTML settings

        Args:
            list_of_calculated_data (list) : Will be iterated to gain necessary values
        Returns:
            -
        """

        print(".. filling bar_percentages_values now")

        # Calculates the percentage amount of questions answered / not answered
        for i in range(1, len(list_of_calculated_data)):

            answered_per_iteration = list_of_calculated_data[i][1]
            unanswered_per_iteration = list_of_calculated_data[i][2]
            amount_of_questions = answered_per_iteration + unanswered_per_iteration
            amount_of_percentage_unanswered = (unanswered_per_iteration / amount_of_questions) * 100

            # Shortens huge percentage numbers by rounding them..
            amount_of_percentage_unanswered = float('%.2f' % amount_of_percentage_unanswered)
            amount_of_percentage_answered = float('%.2f' % (100 - amount_of_percentage_unanswered))

            text_to_be_appended = '' + str(amount_of_percentage_answered) + "%" + \
                                  '<br><br>' + str(amount_of_percentage_unanswered) + "%"

            # The amount of answered questions in percentage will be calculated here
            PlotlyBarChart.bar_first_n_second_values_percentage.append(text_to_be_appended)

    @staticmethod
    def fill_chart_title_n_bar_description(list_of_calculated_data):
        """Defines the chart title in dependence to sorting method and processed years

        Args:
            list_of_calculated_data (list) : Will be accessed to gain necessary values
        Returns:
            -
        """

        print(".. defining plot title now")

        top_worst_string = list_of_calculated_data[0][1]

        first_year = list_of_calculated_data[1][0]
        last_year = list_of_calculated_data[len(list_of_calculated_data) - 1][0]

        # Whenever a_question_Answered_Yes_No.py has been executed
        if list_of_calculated_data[0][0] == "q_answered_y_n":

            amount_of_questions = list_of_calculated_data[1][1] + list_of_calculated_data[1][2]

            PlotlyBarChart.chart_title += "Question answering status <br>" + top_worst_string.upper() + \
                                          " " + str(amount_of_questions) + " <br>"

        # Whenever a_question_Tier_Distribution.py has been executed
        elif list_of_calculated_data[0][0] == "q_tier_dist":

            PlotlyBarChart.chart_title += "Question tier distribution <br>"

        else:
            print("could not find parameter")

        PlotlyBarChart.chart_title += "[" + str(first_year) + " - " + str(last_year) + "]"

    @staticmethod
    def fill_bar_description(list_of_calculated_data):
        """Defines the bar description in dependence to given parameters list_of_calculated_data[0][0]

        Args:
            list_of_calculated_data (list) : Will be accessed to gain necessary values
        Returns:
            -
        """

        print(".. defining bar description now")

        if list_of_calculated_data[0][0] == "q_answered_y_n":
            PlotlyBarChart.bar_value_description.append(['Not answered'])
            PlotlyBarChart.bar_value_description.append(['Answered'])

        elif list_of_calculated_data[0][0] == "q_tier_dist":
            PlotlyBarChart.bar_value_description.append(['Other tiers'])
            PlotlyBarChart.bar_value_description.append(['Tier 1'])
        else:
            print("could not find parameter")

    @staticmethod
    def generate_chart():
        """Generates the chart "temp-plot.html" which will be automatically opened within the browser

        Args:
            -
        Returns:
            -
        """
        print(".. generating chart now!")

        # noinspection PyUnresolvedReferences
        plotly.offline.plot({

            "data": [
                Bar(x=PlotlyBarChart.bar_x_axis_values,
                    y=PlotlyBarChart.bar_y_axis_second_values,
                    name=PlotlyBarChart.bar_value_description[0],
                    marker=dict(
                        color='rgba(255, 0, 0, 0.7)',
                        line=dict(
                            color='rgba(165, 42, 42, 1.0)',
                            width=2,
                        )
                    )
                    ),
                Bar(x=PlotlyBarChart.bar_x_axis_values,
                    y=PlotlyBarChart.bar_y_axis_first_values,
                    name=PlotlyBarChart.bar_value_description[1],
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
                                            PlotlyBarChart.bar_y_axis_second_values,
                                            PlotlyBarChart.bar_first_n_second_values_percentage)]
            )
        })
