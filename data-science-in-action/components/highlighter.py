def highlight_better_row(row):
    new_row = []
    for i, val in enumerate(row):
        metric_name = row.name

        higher_is_better = [
            'Average Monthly Salary (€)',
            'GDP per Capita (€)',
            'Working Age Population (Count)',
            'Air Quality Index',
            'Green Space Index',
            'Health Care Index',
            'Life Expectancy (Years)',
            'Public Transport Satisfaction'
        ]

        if metric_name in higher_is_better:
            color = "background-color: lightgreen" if val == row.max() else "background-color: lightcoral"
        else:
            color = "background-color: lightgreen" if val == row.min() else "background-color: lightcoral"
        new_row.append(color)
    return new_row

def air_pollution(row):
    new_row = []
    for val in row:
        if val == 'good':
            color = 'background-color: darkgreen'
        elif val == 'fair':
            color = 'background-color: green'
        elif val == 'moderate':
            color = 'background-color: yellow'
        elif val == 'poor':
            color = 'background-color: red'
        elif val == 'very poor':
            color = 'background-color: purple'
        else:
            color = 'background-color: transparent'
        new_row.append(color)
    return new_row
