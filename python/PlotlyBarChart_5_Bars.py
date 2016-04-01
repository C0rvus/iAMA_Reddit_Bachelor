# Tutorials used within this class:
# 1. (29.03.2016 @ 04:45) -
# https://plot.ly/python/bar-charts/
# 1. (29.03.2016 @ 06:18) -
# https://plot.ly/javascript/hover-text-and-formatting/

import time                         # Necessary to calculate the current time
import plotly                       # The plotting library we misuse for offline usage
# noinspection PyUnresolvedReferences
from plotly.graph_objs import *


class PlotlyBarChart5Bars:
    """The class to create a stacked bar chart.
        This class is heavily modified because it pyplot normally is not designed to run offline this way..

    Args:
        -
    Returns:
        -
    """

    color_1 = 'rgba(255, 114, 86, 1.0)'
    color_1_border = 'rgba(238, 106, 80, 1.0)'

    color_2 = 'rgba(238, 118, 0, 1.0)'
    color_2_border = 'rgba(205, 102, 0, 1.0)'

    color_3 = 'rgba(0, 201, 87, 1.0)'
    color_3_border = 'rgba(0, 139, 0, 1.0)'

    color_4 = 'rgba(0, 205, 205, 1.0)'
    color_4_border = 'rgba(0, 139, 139, 1.0)'

    color_5 = 'rgba(137, 104, 205, 1.0)'
    color_5_border = 'rgba(39, 71, 139, 1.0)'

    time_now_date = time.strftime("%d.%m.%Y")
    time_now_time = time.strftime("%H:%M:%S")

    bar_x_axis_text = 'Chart creation date: ' + str(time_now_date) + " @ " + str(time_now_time) + '<br>' + \
                      'IAMA db creation date: ' + '17.02.2016' + '<br>' + \
                      'IAMA db MD5 hash: 7C3058809C20C087C97F9DECF6244620'
    chart_title = ""

    # Contains values what the chart is about..
    bar_value_description = []

    bar_x_axis_values = []

    bar_y_axis_first_values = []
    bar_y_axis_second_values = []
    bar_y_axis_third_values = []
    bar_y_axis_fourth_values = []
    bar_y_axis_fifth_values = []

    # i.e. (answered / unanswered questions || amount of questions on tier 1 / any)
    bar_percentages_values_1 = []
    bar_percentages_values_2 = []
    bar_percentages_values_3 = []
    bar_percentages_values_4 = []
    bar_percentages_values_5 = []

    annotations_1 = []
    annotations_2 = []
    annotations_3 = []
    annotations_4 = []
    annotations_5 = []
    annotations_all = []

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
        self.fill_y_axis_values(list_of_calculated_data)
        self.fill_bar_percentages_values(list_of_calculated_data)
        self.fill_chart_title_description(list_of_calculated_data)
        self.fill_bar_description(list_of_calculated_data)
        self.fill_bar_annotations()
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
            PlotlyBarChart5Bars.bar_x_axis_values.append(list_of_calculated_data[i][0])

    @staticmethod
    def fill_y_axis_values(list_of_calculated_data):
        """Fills an bar within the chart with values of the amount of unanswered questions

        Args:
            list_of_calculated_data (list) : Will be iterated to gain necessary values
        Returns:
            -
        """

        print(".. filling 'bar_y_axis_first_values' now")

        # Adds the amount of answered questions to the graph
        for i in range(1, len(list_of_calculated_data)):
            PlotlyBarChart5Bars.bar_y_axis_first_values.append(list_of_calculated_data[i][1])
            PlotlyBarChart5Bars.bar_y_axis_second_values.append(list_of_calculated_data[i][2])
            PlotlyBarChart5Bars.bar_y_axis_third_values.append(list_of_calculated_data[i][3])
            PlotlyBarChart5Bars.bar_y_axis_fourth_values.append(list_of_calculated_data[i][4])
            PlotlyBarChart5Bars.bar_y_axis_fifth_values.append(list_of_calculated_data[i][5])

    @staticmethod
    def fill_bar_percentages_values(list_of_calculated_data):
        """Calculates percentages to be shown within the graph..
            This is not supported within pyplot under normal circumstances.. so we're tricking the HTML settings

        Args:
            list_of_calculated_data (list) : Will be iterated to gain necessary values
        Returns:
            -
        """

        print(".. calculating percentage distribution now")

        # Calculates the percentage amount of questions answered / not answered
        for i in range(1, len(list_of_calculated_data)):

            first_value = list_of_calculated_data[i][1]
            second_value = list_of_calculated_data[i][2]
            third_value = list_of_calculated_data[i][3]
            fourth_value = list_of_calculated_data[i][4]
            fifth_value = list_of_calculated_data[i][5]

            # The total amount of all values.. needed for corect percentage calculation
            total_amount_of_values = first_value + second_value + third_value + fourth_value + fifth_value

            percentage_amount_first_value = (first_value / total_amount_of_values) * 100
            percentage_amount_second_value = (second_value / total_amount_of_values) * 100
            percentage_amount_third_value = (third_value / total_amount_of_values) * 100
            percentage_amount_fourth_value = (fourth_value / total_amount_of_values) * 100
            percentage_amount_fifth_value = (fifth_value / total_amount_of_values) * 100

            # Rounds the values for smooth display
            percentage_amount_first_value = float('%.2f' % percentage_amount_first_value)
            percentage_amount_second_value = float('%.2f' % percentage_amount_second_value)
            percentage_amount_third_value = float('%.2f' % percentage_amount_third_value)
            percentage_amount_fourth_value = float('%.2f' % percentage_amount_fourth_value)
            percentage_amount_fifth_value = float('%.2f' % percentage_amount_fifth_value)

            # Appends the values to each bars corresponding value list
            PlotlyBarChart5Bars.bar_percentages_values_1.append('' + str(percentage_amount_first_value) + '%')
            PlotlyBarChart5Bars.bar_percentages_values_2.append('' + str(percentage_amount_second_value) + '%')
            PlotlyBarChart5Bars.bar_percentages_values_3.append('' + str(percentage_amount_third_value) + '%')
            PlotlyBarChart5Bars.bar_percentages_values_4.append('' + str(percentage_amount_fourth_value) + '%')
            PlotlyBarChart5Bars.bar_percentages_values_5.append('' + str(percentage_amount_fifth_value) + '%')

    @staticmethod
    def fill_chart_title_description(list_of_calculated_data):
        """Defines the chart title in dependence to sorting method and processed years

        Args:
            list_of_calculated_data (list) : Will be accessed to gain necessary values
        Returns:
            -
        """

        print(".. defining plot title now")

        first_year = list_of_calculated_data[1][0]
        last_year = list_of_calculated_data[len(list_of_calculated_data) - 1][0]

        if list_of_calculated_data[0][0] == "t_life_span" and list_of_calculated_data[0][1] == "minutes":
            PlotlyBarChart5Bars.chart_title += "Thread life span in minutes <br>"

        elif list_of_calculated_data[0][0] == "t_life_span" and list_of_calculated_data[0][1] == "hours":
            PlotlyBarChart5Bars.chart_title += "Thread life span in hours <br>"

        elif list_of_calculated_data[0][0] == "t_life_span" and list_of_calculated_data[0][1] == "days":
            PlotlyBarChart5Bars.chart_title += "Thread life span in days <br>"

        elif list_of_calculated_data[0][0] == "t_comment_time" and list_of_calculated_data[0][1] == "minutes":
            PlotlyBarChart5Bars.chart_title += "Average comment reaction time in minutes <br>"

        elif list_of_calculated_data[0][0] == "t_comment_time" and list_of_calculated_data[0][1] == "hours":
            PlotlyBarChart5Bars.chart_title += "Average comment reaction time in hours <br>"

        elif list_of_calculated_data[0][0] == "t_comment_time" and list_of_calculated_data[0][1] == "days":
            PlotlyBarChart5Bars.chart_title += "Average comment reaction time in days <br>"


        else:
            print("could not find parameter")
            PlotlyBarChart5Bars.chart_title += "Error in parsing arguments ... please check again ! <br>"

        PlotlyBarChart5Bars.chart_title += "[" + str(first_year) + " - " + str(last_year) + "]"

    @staticmethod
    def fill_bar_description(list_of_calculated_data):
        """Defines the bar description in dependence to given parameters list_of_calculated_data[0][0]

        Args:
            list_of_calculated_data (list) : Will be accessed to gain necessary values
        Returns:
            -
        """

        print(".. defining bar description now")

        if (list_of_calculated_data[0][0] == "t_life_span" or list_of_calculated_data[0][0] == "t_comment_time") and \
                        list_of_calculated_data[0][1] == "minutes":
            PlotlyBarChart5Bars.bar_value_description.append(['0 - 14 minutes'])
            PlotlyBarChart5Bars.bar_value_description.append(['15 - 29 minutes'])
            PlotlyBarChart5Bars.bar_value_description.append(['30 - 59 minutes'])
            PlotlyBarChart5Bars.bar_value_description.append(['60 - 119 minutes'])
            PlotlyBarChart5Bars.bar_value_description.append(['>= 120 minutes'])

        elif (list_of_calculated_data[0][0] == "t_life_span" or list_of_calculated_data[0][0] == "t_comment_time") and \
                        list_of_calculated_data[0][1] == "hours":
            PlotlyBarChart5Bars.bar_value_description.append(['0 - 1 hours'])
            PlotlyBarChart5Bars.bar_value_description.append(['2 - 5 hours'])
            PlotlyBarChart5Bars.bar_value_description.append(['6 - 10 hours'])
            PlotlyBarChart5Bars.bar_value_description.append(['11 - 23 hours'])
            PlotlyBarChart5Bars.bar_value_description.append(['>= 24 hours'])

        elif (list_of_calculated_data[0][0] == "t_life_span" or list_of_calculated_data[0][0] == "t_comment_time") and \
                        list_of_calculated_data[0][1] == "days":
            PlotlyBarChart5Bars.bar_value_description.append(['0 - 1 days'])
            PlotlyBarChart5Bars.bar_value_description.append(['2 - 4 days'])
            PlotlyBarChart5Bars.bar_value_description.append(['5 - 8 days'])
            PlotlyBarChart5Bars.bar_value_description.append(['9 - 13 days'])
            PlotlyBarChart5Bars.bar_value_description.append(['>= 14 days'])

        else:
            print("could not find parameter")

    @staticmethod
    def fill_bar_annotations():

        PlotlyBarChart5Bars.annotations_1 = [dict(
            x=x - 0.325,
            y=y,
            text=text,
            xanchor='auto',
            yanchor='auto',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40,
            bordercolor=PlotlyBarChart5Bars.color_1_border,
            borderwidth=2,
            borderpad=4,
            bgcolor=PlotlyBarChart5Bars.color_1_border,
            opacity=0.8,
            font=dict(family='Arial', size=14, color='rgba(0, 0, 0, 1)')
        )for x, y, text in zip(PlotlyBarChart5Bars.bar_x_axis_values, PlotlyBarChart5Bars.bar_y_axis_first_values,
                               PlotlyBarChart5Bars.bar_percentages_values_1)]

        PlotlyBarChart5Bars.annotations_2 = [dict(
            x=x - 0.1625,
            y=y,
            text=text,
            xanchor='auto',
            yanchor='auto',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40,
            bordercolor=PlotlyBarChart5Bars.color_2_border,
            borderwidth=2,
            borderpad=4,
            bgcolor=PlotlyBarChart5Bars.color_2_border,
            opacity=0.8,
            font=dict(family='Arial', size=14, color='rgba(0, 0, 0, 1)')
        )for x, y, text in zip(PlotlyBarChart5Bars.bar_x_axis_values, PlotlyBarChart5Bars.bar_y_axis_second_values,
                               PlotlyBarChart5Bars.bar_percentages_values_2)]

        PlotlyBarChart5Bars.annotations_3 = [dict(
            x=x,
            y=y,
            text=text,
            xanchor='auto',
            yanchor='auto',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40,
            bordercolor=PlotlyBarChart5Bars.color_3_border,
            borderwidth=2,
            borderpad=4,
            bgcolor=PlotlyBarChart5Bars.color_3_border,
            opacity=0.8,
            font=dict(family='Arial', size=14, color='rgba(0, 0, 0, 1)')
        )for x, y, text in zip(PlotlyBarChart5Bars.bar_x_axis_values, PlotlyBarChart5Bars.bar_y_axis_third_values,
                               PlotlyBarChart5Bars.bar_percentages_values_3)]

        PlotlyBarChart5Bars.annotations_4 = [dict(
            x=x + 0.1625,
            y=y,
            text=text,
            xanchor='auto',
            yanchor='auto',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40,
            bordercolor=PlotlyBarChart5Bars.color_4_border,
            borderwidth=2,
            borderpad=4,
            bgcolor=PlotlyBarChart5Bars.color_4_border,
            opacity=0.8,
            font=dict(family='Arial', size=14, color='rgba(0, 0, 0, 1)')
        )for x, y, text in zip(PlotlyBarChart5Bars.bar_x_axis_values, PlotlyBarChart5Bars.bar_y_axis_fourth_values,
                               PlotlyBarChart5Bars.bar_percentages_values_4)]

        PlotlyBarChart5Bars.annotations_5 = [dict(
            x=x + 0.325,
            y=y,
            text=text,
            xanchor='auto',
            yanchor='auto',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40,
            bordercolor=PlotlyBarChart5Bars.color_5_border,
            borderwidth=2,
            borderpad=4,
            bgcolor=PlotlyBarChart5Bars.color_5_border,
            opacity=0.8,
            font=dict(family='Arial', size=14, color='rgba(0, 0, 0, 1)')
        )for x, y, text in zip(PlotlyBarChart5Bars.bar_x_axis_values, PlotlyBarChart5Bars.bar_y_axis_fifth_values,
                               PlotlyBarChart5Bars.bar_percentages_values_5)]

        PlotlyBarChart5Bars.annotations_all = PlotlyBarChart5Bars.annotations_1 + PlotlyBarChart5Bars.annotations_2 + \
                                              PlotlyBarChart5Bars.annotations_3 + PlotlyBarChart5Bars.annotations_4 + \
                                              PlotlyBarChart5Bars.annotations_5

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
                Bar(x=PlotlyBarChart5Bars.bar_x_axis_values,
                    y=PlotlyBarChart5Bars.bar_y_axis_first_values,
                    name=PlotlyBarChart5Bars.bar_value_description[0],
                    marker=dict(
                        color=PlotlyBarChart5Bars.color_1,
                        line=dict(
                            color=PlotlyBarChart5Bars.color_1_border,
                            width=2,
                        )
                    )
                    ),
                Bar(x=PlotlyBarChart5Bars.bar_x_axis_values,
                    y=PlotlyBarChart5Bars.bar_y_axis_second_values,
                    name=PlotlyBarChart5Bars.bar_value_description[1],
                    marker=dict(
                        color=PlotlyBarChart5Bars.color_2,
                        line=dict(
                            color=PlotlyBarChart5Bars.color_2_border,
                            width=2,
                        )
                    )
                    ),
                Bar(x=PlotlyBarChart5Bars.bar_x_axis_values,
                    y=PlotlyBarChart5Bars.bar_y_axis_third_values,
                    name=PlotlyBarChart5Bars.bar_value_description[2],
                    marker=dict(
                        color=PlotlyBarChart5Bars.color_3,
                        line=dict(
                            color=PlotlyBarChart5Bars.color_3_border,
                            width=2,
                        )
                    )
                    ),
                Bar(x=PlotlyBarChart5Bars.bar_x_axis_values,
                    y=PlotlyBarChart5Bars.bar_y_axis_fourth_values,
                    name=PlotlyBarChart5Bars.bar_value_description[3],
                    marker=dict(
                        color=PlotlyBarChart5Bars.color_4,
                        line=dict(
                            color=PlotlyBarChart5Bars.color_4_border,
                            width=2,
                        )
                    )
                    ),
                Bar(x=PlotlyBarChart5Bars.bar_x_axis_values,
                    y=PlotlyBarChart5Bars.bar_y_axis_fifth_values,
                    name=PlotlyBarChart5Bars.bar_value_description[4],
                    marker=dict(
                        color=PlotlyBarChart5Bars.color_5,
                        line=dict(
                            color=PlotlyBarChart5Bars.color_5_border,
                            width=2,
                        )
                    )
                    )],
            "layout": Layout(
                title=PlotlyBarChart5Bars.chart_title,
                xaxis=dict(title=PlotlyBarChart5Bars.bar_x_axis_text),
                barmode='group',
                annotations=PlotlyBarChart5Bars.annotations_all
            )
        })
