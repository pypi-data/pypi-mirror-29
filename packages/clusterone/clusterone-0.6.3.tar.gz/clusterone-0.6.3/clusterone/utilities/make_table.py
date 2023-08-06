"""
blah blah blah
"""

from clusterone.utils import render_table

def main(_data, header=None):
    #TODO: Pull the code from render_table here and refactor it, then test
    table_data = [header]

    for row in _data:
        table_data.append(row)

    table = render_table(table_data, 36).table
    return table

