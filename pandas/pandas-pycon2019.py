# Best Practices
# https://www.youtube.com/watch?v=dPwLlJkSHLo

'''
Best of the Best Practices
- Use count with mean, to look for meaningless means
'''

import ast  # module stands for Abstract Syntax Tree
import pandas as pd
import matplotlib.pyplot as plt


data = '/mnt/HD-Shared/work/data-sets/ted.csv'
ted = pd.read_csv(data)

ted.head()
ted.shape
ted.dtypes  # object type can be string, python objects (lists, dicts)
ted.isna().sum()  # checking for missing values

# 2. Which talks provoke the most online discussion?

# might think to look at the most number of comments
ted.sort_values('comments').tail()
# this doesn't look at sub/nested comments
# or how long these talks have been online
# correct for this bias by normalizing it by views


ted['comments_per_view'] = ted.comments / ted.views
ted.sort_values('comments_per_view').tail()

# interpretting the result 0.002 as for every view of this talk, there are 0.002 comments
# better intpretation taking the inverse

ted['views_per_comment'] = ted.views / ted.comments
ted.sort_values('views_per_comment').head()  # now we want lowest number
# interpret result 450 as it takes 450 views to generate a comment, or 1/450 people leave a comment

''' Lessons
- Consider limitations and biases of your data when analyzing it
- Make your results understandable
'''

# 3. Visualize the distribution of comments

ted.comments.plot()  # line plot, x is index, y is value of the comments
# line plot is for measuring something over time
# Want frequency distribution which typically is histogram type

ted.comments.plot(kind='hist')
# huge amount of outliers
# first bin is a lot of talks with between 0 and 600 comments, it does not represent a lot of comments in a single talk
# want to know what the distribution looks like within the first bin
# filter it down, this is filtering the dataframe before selecting the comments column
ted[ted.comments < 1000].comments.plot(kind='hist')
# how much data was lost from filtering
ted[ted.comments >= 1000].shape  # only 32 rows

# Alternative and recommended syntax, explicity what rows and what columns to choose.
ted.loc[ted.comments < 1000, 'comments'].plot(kind='hist')

# see finer grain detail with greater number of bins
ted.loc[ted.comments < 1000, 'comments'].plot(kind='hist', bins=20)

''' Lessons
- choose your plot type based on the questions your answers, and the data types you're working with
- use pandas one-liners to iterate through plots quickly
- try modifying the plot defaults
- creating plots involves decision making
'''

# 4. Plot the number of talks that took place each year
# exploring
ted.event.value_counts()  # count of each category
ted.event.value_counts().count()  # count of how many categories
ted.event.sample(10)  # can see some end with a number and some don't

ted.film_date.head()  # see date in Unix timestamp
# auto-magically converts successfully usually but not this time
pd.to_datetime(ted.film_date)
ted['film_datetime'] = pd.to_datetime(ted.film_date, unit='s')
# checking that the conversion is right
ted[['event', 'film_datetime']].sample(5)

ted.film_datetime.dt.year  # can access datetime methods on datetime columns
ted.film_datetime.dt.dayofyear

ted.event.str.lower()  # can access string methods on string based columns

ted.film_datetime.dt.year.value_counts().plot(kind='bar')
# problem  with bar plot is it's excluding all the years that are not in the data
ted.film_datetime.dt.year.value_counts().plot()
# what went wrong here is a sorting issue
ted.film_datetime.dt.year.value_counts().sort_index().plot()
ted.film_datetime.max()  # last year in the data set

''' Lessons
- read the documentation
- use datetime data type when you have dates and times
- check your work as you go
- instead of looking at head or tail, use a random sample
- consider excluding data if it might not be relevant
'''

# 5. What were the best events in Ted history to attend
ted.event.value_counts().head()  # number of talks

# Need to aggregate based on event
# Groupby syntax is: For each event, do aggregation on specified column
ted.groupby('event').views.mean().sort_values().tail()
# However, some of these events only have a small number of talks in them which should be relevant for defining Best

# how many talks were at each event?
# can do multiple aggregations within a groupby by passing a list of agg functions whose results will each be their own column

# this is now a DF so need to specify what to sort on
ted.groupby('event').views.agg(['count', 'mean']).sort_values('mean').tail()
# so what previously looked like the best event actually only had one talk in that event
ted.groupby('event').views.agg(
    ['count', 'mean', 'sum']).sort_values('sum').tail()

''' Lessons
- Think creatively for how you can use the data available to answer your question
- Watch out for small sample sizes 'Use count with mean, to look for meaningless means'
'''

# 6. Unpack the ratings data
ted.ratings.head()
ted.loc[0, 'ratings']
ted.ratings[0]
type(ted.ratings[0])  # this is a stringified list of dictionaries

ast.literal_eval('[1,2,3]')
# will evaluate a string that looks like a python literal or container
ast.literal_eval(ted.ratings[0])  # got list of ratings for a single talk

# custom function


def str_to_list(ratings_str):
    return ast.literal_eval(ratings_str)


# want to apply this function to every element in the ratings Series
ted.ratings.apply(str_to_list).head()
# can also
ted.ratings.apply(ast.literal_eval).head()
# where x represents each element in the Series
ted.ratings.apply(lambda x: ast.literal_eval(x))

ted['ratings_list'] = ted.ratings.apply(str_to_list)

''' Lessons
- Pay attention to data types in pandas to not miss out on what functions you can use on a column
- Use apply any time it is necessary, it's slow so reach for it last if there is better
'''

# 7. Count the total number of ratings received by each talk put it into new column named num_ratings

# Piecewise example of building up a function


def get_num_ratings(list_of_dicts):
    return list_of_dicts[0]


get_num_ratings(ted.ratings_list[0])


def get_num_ratings(list_of_dicts):
    return list_of_dicts[0]['count']


get_num_ratings(ted.ratings_list[0])


def get_num_ratings(list_of_dicts):
    num = 0
    for d in list_of_dicts:
        num = num + d['count']
    return num


get_num_ratings(ted.ratings_list[0])

ted['num_ratings'] = ted.ratings_list.apply(get_num_ratings)
ted.num_ratings.describe()  # checking that results make sense

# Alternative method from the audience
pd.DataFrame(ted.ratings_list[0])['count'].sum()

''' Lessons
- write code in small chunks and check as you go
- Lambda is best for simple functions
'''

# 8. Which occupations deliver the funniest tedtalks on average
# There is more than one way to do this, no single correct way
# Step 1, count the number of funny ratings
ted.ratings_list.head()
ted.ratings.str.contains('Funny').value_counts()
# No false means that "Funny' always exists as an option


def get_funny_ratings(list_of_dicts):
    for d in list_of_dicts:
        if d['name'] == 'Funny':
            return d['count']


ted['funny_ratings'] = ted.ratings_list.apply(get_funny_ratings)

# Step 2 Percentage of ratings which were funny
ted['funny_rate'] = ted.funny_ratings / ted.num_ratings
# how to gut check that this metric makes sense?
# see if the funniest rating to speaker occupation matches human intuition
ted.sort_values('funny_rate').speaker_occupation.tail(20)

# Step 3
# Analyze the funny rate by occupation
# Again groupby is "for each something, I want to do agg on some column"
ted.groupby('speaker_occupation').funny_rate.mean().sort_values().tail()
# problem though, many of these occupations have a very small sample size

# Step 4
# Focus on occupations that are well represented in the data

occupation_counts = ted.speaker_occupation.value_counts()
top_occupations = occupation_counts[occupation_counts >= 5].index
type(top_occupations)  # index data type can be treated like a list

ted_top_occupations = ted[ted.speaker_occupation.isin(top_occupations)]
ted_top_occupations.shape
ted_top_occupations.groupby(
    'speaker_occupation').funny_rate.mean().sort_values().tail()
# weaknessess, 5 is still a small sample size
# some of the occupations were all the same person multiple times
# some of the occupations have multiple listed together

''' Lessons
- check your assumptions about the data, like if funny exists or not in all observations
- check for reasonable results, like the numerical results
- take of advantage of how pandas results often output a dataframe or series
- watch out for small sample sizes
- consider impact of missing data, pandas often ignores missing values by default
'''
