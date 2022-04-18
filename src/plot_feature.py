#!/usr/bin python3.8.10
# -*- coding: utf-8 -*-

# third party import

# local import
import matplotlib.pyplot as plt


def bar_chart_plot(item_dict, file_name, x_rotate=False):
    items = item_dict['items']

    for item in items:
        extras = {}
        # Build extra parameters:
        if 'color' in item:
            extras['c'] = item['color']

        if item['type'] == 'scatter':
            plt.plot(item['x_axis'], item['y_axis'], '--o', label=item['label'], **extras)
            plt.legend(prop={'size': 6}, loc="lower left")
        elif item['type'] == 'plot':
            plt.plot(item['x_axis'], item['y_axis'], label=item['label'], **extras)
            plt.legend()
        elif item['type'] == 'bar':
            plt.bar(item['x_axis'], item['y_axis'])

    plt.xlabel(item_dict['xlabel'])
    plt.ylabel(item_dict['ylabel'])

    if 'yscale' in item_dict:
        plt.yscale(item_dict['yscale'])

    if 'x_rotate' in item_dict and item_dict['x_rotate']:
        plt.xticks(rotation=45)
        plt.gcf().subplots_adjust(bottom=0.20)

    if 'title' in item_dict:
        plt.title(item_dict['title'])

    if file_name is not None:
        plt.savefig(f'{file_name}.png', dpi=300)
        plt.clf()
