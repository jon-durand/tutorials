# https://altair-viz.github.io/getting_started/starting.html
# https://altair-viz.github.io/altair-tutorial/notebooks/Index.html


import pandas as pd
data = pd.DataFrame({'a': list('CCCDDDEEE'),
                     'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})

import altair as alt
chart = alt.Chart(data)

chart.mark_point().encode(x='a', y = 'b')

chart.mark_point().encode(x='a', y='average(b)')

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
