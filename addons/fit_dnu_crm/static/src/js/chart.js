odoo.define('fit_dnu_crm.chart', function(require) {
    'use strict';

    const core = require('web.core');
    const QWeb = core.qweb;
    const AbstractAction = require('web.AbstractAction');

    const ChartAction = AbstractAction.extend({
        template: 'chart_template',

        start: function() {
            this._super.apply(this, arguments);
            this.renderChart();
        },

        renderChart: function() {
            const ctx = this.$el.find('#myChart');
            const myChart = new Chart(ctx, {
                type: 'bar', // Example chart type
                data: {
                    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                    datasets: [{
                        label: '# of Votes',
                        data: [12, 19, 3, 5, 2, 3],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    });

    core.action_registry.add('chart_action', ChartAction);
});
