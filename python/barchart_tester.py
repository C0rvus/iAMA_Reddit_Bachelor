# noinspection PyUnresolvedReferences
from PlotlyBarChart import PlotlyBarChart

pbarchart = PlotlyBarChart()


# 1. year, 2. amount answered, 3. amount UNanswered

data_to_give = ["top",
                [2009, 900, 1536],
                [2010, 500, 500],
                [2011, 300, 700]
                ]


#        for i in range(1, len(list_of_calculated_data)):
#            print(list_of_calculated_data[i][0])
# Doku in analyze top 100 überarbeiten
# muss ich noch adden
pbarchart.main_method(data_to_give)
