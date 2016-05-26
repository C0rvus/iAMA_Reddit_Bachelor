// Data gathered from http://populationpyramid.net/germany/2015/
$(function () {
    // Age categories
    var categories = ['0-4', '5-9', '10-14', '15-19'];
    $(document).ready(function () {
        $('#container_example_3').highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: 'Population pyramid for Germany, 2015'
            },
            subtitle: {
                text: 'Source: <a href="http://populationpyramid.net/germany/2015/">Population Pyramids of the World from 1950 to 2100</a>'
            },
            xAxis: [{
                categories: categories,
                reversed: false,
                labels: {
                    step: 1
                }
            }, { // mirror axis on right side
                opposite: true,
                reversed: false,
                categories: categories,
                linkedTo: 0,
                labels: {
                    step: 1
                }
            }],
            yAxis: {
                title: {
                    text: null
                },
                labels: {
                    formatter: function () {
                        return Math.abs(this.value) + '%';
                    }
                }
            },

            plotOptions: {
                series: {
                    stacking: 'normal'
                }
            },

            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + ', age ' + this.point.category + '</b><br/>' +
                        'Population: ' + Highcharts.numberFormat(Math.abs(this.point.y), 0);
                }
            },

            series: [{
                name: 'Male',
                data: [-2.2, -2.2, -2.3, -2.5]
            }, {
                name: 'Female',
                data: [2.1, 2.0, 2.2, 2.4]
            }]
        });
    });

});