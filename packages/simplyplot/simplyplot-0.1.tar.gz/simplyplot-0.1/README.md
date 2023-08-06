# Simply Plot

Simply plot is a wrapper built around the matplotlib framework. The purpose of
this wrapper is to make it easier to create basic graphs with less lines of code.

## Installation
```bash
pip install simply-plot
```

## Dependicies

- matplotlib

# Example
## Bar chart
```language=python
import simply_plot

options = {
	'title': 'Sales 2005 - 2008',
	'x_axis_name': 'Month',
	'y_axis_name': 'Sales',
	'data': (2000, 1500, 2250, 1750),
	'labels': ('2005', '2006', '2007', '2008')
}

monthly_sales = simply_plot.BarChart(**options)

monthly_sales.show()
```

### Result

![Test](example_images/bar_chart_example.png)

## Line chart

```language=python
import simply_plot

options = {
	'title': 'Sales 2005 - 2008',
	'x_axis_name': 'Month',
	'y_axis_name': 'Sales',
	'data': (2000, 1500, 2250, 1750),
	'labels': ('2005', '2006', '2007', '2008')
}

monthly_sales = simply_plot.LineChart(**options)

monthly_sales.show()
```

### Result

![Test](example_images/line_chart_example.png)