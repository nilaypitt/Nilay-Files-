from datascience import *
import numpy as np

1. Bangladesh ¶
In the population table, the geo column contains three-letter codes established by the International Organization for Standardization (ISO) in the Alpha-3 standard. We will begin by taking a close look at Bangladesh. Inspect the standard to find the 3-letter code for Bangladesh.

Question 1. Create a table called b_pop that has two columns labeled time and population_total. The first column should contain the years from 1970 through 2015 (including both 1970 and 2015) and the second should contain the population of Bangladesh in each of those years.

b_pop = population.where('geo', are.equal_to('bgd')).where('time', are.between(1970,2016)).drop('geo')
b_pop

Run the following cell to create a table called b_five that has the population of Bangladesh every five years. At a glance, it appears that the population of Bangladesh has been growing quickly indeed!
b_pop.set_format('population_total', NumberFormatter)

fives = np.arange(1970, 2016, 5) # 1970, 1975, 1980, ...
b_five = b_pop.sort('time').where('time', are.contained_in(fives))
b_five

Question 2. Assign b_1970_through_2010 to a table that has the same columns as b_five and has one row for every five years from 1970 through 2010 (but not 2015).
Then, use that table to assign initial to an array that contains the population for every five year interval from 1970 to 2010. Finally, assign changed to an array that
contains the population for every five year interval from 1975 to 2015.

b_1970_through_2010 = b_five.exclude(len(b_five.column(0))-1)
initial = b_1970_through_2010.column('population_total')
changed = b_five.exclude(0).column('population_total')

Question 3. Perhaps population is growing more slowly because people aren't living as long. Use the life_expectancy table to draw a line graph with the years 1970 and later on the horizontal axis that shows how the life expectancy at birth has changed in Bangladesh.

life_expectancy.where('time', are.above_or_equal_to(1970)).where('geo', are.equal_to('bgd')).plot('time', 'life_expectancy_years')

Write a function fertility_over_time that takes the Alpha-3 code of a country and a start year. It returns a two-column table with labels Year and Children per woman that can be used to generate a line chart of the country's fertility rate each year, starting at the start year. The plot should include the start year and all later years that appear in the fertility table.
Then, in the next cell, call your fertility_over_time function on the Alpha-3 code for Bangladesh and the year 1970 in order to plot how Bangladesh's fertility rate has changed since 1970.

def fertility_over_time(country, start):
    """Create a two-column table that describes a country's total fertility rate each year."""
    country_fertility = fertility.where('geo', are.equal_to(country)).drop('geo')
    country_fertility_after_start = country_fertility.where('time', are.above(start-1)).relabel('time', 'Year').relabel('children_per_woman_total_fertility', 'Children per woman')
    return country_fertility_after_start

    bangladesh_code = 'bgd'
fertility_over_time(bangladesh_code, 1970).plot(0, 1)

Question 7. Using both the fertility and child_mortality tables, draw a scatter diagram with one point for each year, starting with 1970, that has Bangladesh's total fertility on the horizontal axis and its child mortality on the vertical axis.
Create a table called post_1969_fertility_and_child_mortality with the appropriate column labels and data in order to generate the chart correctly. Use the label Children per woman to describe total fertility and the label Child deaths per 1000 born to describe child mortality.

bgd_fertility = fertility.where('geo', are.equal_to('bgd')).drop('geo')
bgd_child_mortality = child_mortality.where('geo', are.equal_to('bgd')).drop('geo')
fertility_and_child_mortality = bgd_fertility.join('time', bgd_child_mortality)
post_1969_fertility_and_child_mortality = fertility_and_child_mortality.where('time', are.above(1969)).relabel('children_per_woman_total_fertility', 'Children per woman').relabel('child_mortality_under_5_per_1000_born', 'Child deaths per 1000 born')

post_1969_fertility_and_child_mortality.scatter('Children per woman', 'Child deaths per 1000 born')

Question 11. Create a function stats_for_year that takes a year and returns a table of statistics. The table it returns should have four columns: geo, population_total, children_per_woman_total_fertility, and child_mortality_under_5_per_1000_born. Each row should contain one Alpha-3 country code and three statistics: population, fertility rate, and child mortality for that year from the population, fertility and child_mortality tables. Only include rows for which all three statistics are available for the country and year.

In addition, restrict the result to country codes that appears in big_50, an array of the 50 most populous countries in 2010. This restriction will speed up computations later in the project.

def stats_for_year(year):
    """Return a table of the stats for each country that year."""
    p = population_of_big_50.where('time', year).drop('time')
    f = fertility.where('time', year).drop('time')
    c = child_mortality.where('time', year).drop('time')
    return p.join('geo', f).join('geo', c)

Question 12. Create a table called pop_by_decade with two columns called decade and population. It has a row for each year since 1960 that starts a decade. The population column contains the total population of all countries included in the result of stats_for_year(year) for the first year of the decade. For example, 1960 is the first year of the 1960's decade. You should see that these countries contain most of the world's population.

def pop_for_year(year):
    pop = population_of_big_50.where('time', are.equal_to(year)).drop('time')
    return sum(pop.column('population_total'))

Question 13. Create a table called region_counts that has two columns, region and count. It should describe the count of how many countries in each region appear in the result of stats_for_year(1960).

countries_1960 = countries.where('country', are.contained_in(stats_for_year(1960).column('geo')))
region_counts = countries_1960.group('world_6region').relabel('world_6region', 'region')
region_counts


2. Global Poverty ¶
In 1800, 85% of the world's 1 billion people lived in extreme poverty, defined by the United Nations as "a condition characterized by severe deprivation of basic human needs, including food, safe drinking water, sanitation facilities, health, shelter, education and information." A common measure of extreme poverty is a person living on less than $1.25 per day.

In 2018, the proportion of people living in extreme poverty was estimated to be 8%. Although the world rate of extreme poverty has declined consistently for hundreds of years, the number of people living in extreme poverty is still over 600 million. The United Nations recently adopted an ambitious goal: "By 2030, eradicate extreme poverty for all people everywhere." In this section, we will examine extreme poverty trends around the world.

First, load the population and poverty rate by country and year and the country descriptions. While the population table has values for every recent year for many countries, the poverty table only includes certain years for each country in which a measurement of the rate of extreme poverty was available.

population = Table.read_table('population.csv')
countries = Table.read_table('countries.csv').where('country', are.contained_in(population.group('geo').column(0)))
poverty = Table.read_table('poverty.csv')
poverty.show(3)
geo	time	extreme_poverty_percent_people_below_125_a_day
alb	1996	0.2
alb	2002	0.73
alb	2004	0.53
... (1096 rows omitted)

Question 1. Assign latest_poverty to a three-column table with one row for each country that appears in the poverty table. The first column should contain the 3-letter code for the country. The second column should contain the most recent_poverty_total year for which an extreme poverty rate is available for the country. The third column should contain the poverty rate in that year.

def first(values):
    return values.item(0)

latest_poverty = poverty.sort('time', descending=True).group('geo', first)
latest_poverty.relabel(0, 'geo').relabel(1, 'time').relabel(2, 'poverty_percent')

Question 3. Assuming that the poverty_total numbers in the recent_poverty_total table describe all people in 2010 living in extreme poverty, assign the name poverty_percent to the known percentage of the world's 2010 population that were living in extreme poverty.

people_in_poverty = sum(recent_poverty_total.column(3))
world_pop_2010 = sum(population.where('time', are.equal_to(2010)).column('population_total'))
poverty_percent = people_in_poverty / world_pop_2010 * 100
poverty_percent

Question 4. Using both countries and recent_poverty_total, create a five-column table called poverty_map with one row for every country in recent_poverty_total. The four columns should have the following labels and contents:

a)latitude contains the country's latitude,
b)longitude contains the country's longitude,
c)name contains the country's name,
d)region contains the country's region from the world_4region column of countries,
e)poverty_total contains the country's poverty total.

poverty_map = countries.join('country', recent_poverty_total, 'geo').select('latitude', 'longitude', 'name', 'world_4region', 'poverty_total').relabel('world_4region', 'region')
poverty_map

Question 5. Assign largest to a two-column table with the name (not the 3-letter code) and poverty_total of the 10 countries with the largest number of people living in extreme poverty.

largest = poverty_map.sort('poverty_total', descending=True).select('name', 'poverty_total').take(np.arange(0,10))
largest

Question 6. Write a function called poverty_timeline that takes the name of a country as its argument. It should draw a line plot of the number of people living in poverty in that country with time on the horizontal axis. The line plot should have a point for each row in the poverty table for that country. To compute the population living in poverty from a poverty percentage, multiply by the population of the country in that year.

def population_for_country_in_year(row_of_poverty_table):
    """Optional: Define a function to return the population
    of a country in a year using a row from the poverty table."""
    population_for_country = population.where('time', row_of_poverty_table.item('time')).where('geo', row_of_poverty_table.item('geo'))
    return population_for_country.column('population_total').item(0)

def poverty_timeline(country):
    """Draw a timeline of people living in extreme poverty in a country."""
    geo = countries.where('name', country).column('country').item(0)
    country_poverty = poverty.where('geo', geo)
    timeline = Table().with_columns(
        'Year', country_poverty.column(1), 'Number in poverty',
        country_poverty.column(2) / 100 * country_poverty.apply(population_for_country_in_year))
    timeline.plot(0, 1)
