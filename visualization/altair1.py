# https://altair-viz.github.io/getting_started/starting.html
# https://altair-viz.github.io/altair-tutorial/notebooks/Index.html


from vega_datasets import data
import altair as alt
import pandas as pd
data = pd.DataFrame({'a': list('CCCDDDEEE'),
                     'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})

chart = alt.Chart(data)

chart.mark_point().encode(x='a', y='b')

chart.mark_point().encode(x='a', y='average(b)')

# THE IMPORTANT LINE TO HANDLE LARGE FILES
alt.data_transformers.enable('json')

chart.mark_bar().encode(x='a', y='average(b)')

alt.Chart(data).mark_bar().encode(
    y='a',
    x='average(b)'
)

alt.Chart(data).mark_bar().encode(
    alt.Y('a', type='nominal'),
    alt.X('b', type='quantitative', aggregate='average')
)

chart = alt.Chart(data).mark_bar().encode(
    x='a',
    y='average(b)',
)
chart.save('chart.html')

# Pycon https://www.youtube.com/watch?v=ms29ZPUKxbU

iris = data.iris()
alt.Chart(iris).mark_point().encode(
    x='petalLength',
    y='sepalWidth',
    color='species',
    column='species'
)
