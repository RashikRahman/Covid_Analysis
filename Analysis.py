import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

# import urllib #to download the csv file
# url = "https://covid.ourworldindata.org/data/ecdc/full_data.csv"
# urllib.request.urlretrieve (url, "covid19.csv")

# CVD = pd.read_csv('https://covid.ourworldindata.org/data/ecdc/full_data.csv') #directly read from url
data = pd.read_csv('covid19.csv')
# print(data.head())
# print(data.dtypes)

data.date=pd.to_datetime(data.date)
# print(data.dtypes)
# print(data.groupby('location')['location'].agg('count'))

# countries=['United States', 'Spain', 'Italy', 'Bangladesh']
countries=['Bangladesh', 'India']
CVD_country = data[data.location.isin(countries)]
# print(CVD_country)

CVD_country.set_index('date', inplace=True)
# print( CVD_country.loc['2020-02-15':'2020-03-22'])
CVD_country['mortality_rate'] = CVD_country.total_deaths/CVD_country.total_cases
# print(CVD_country)

'''
#Plotting
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(14,14))

CVD_country.groupby('location')['new_cases'].plot(ax=axes[0,0], legend=True) #for log scale add logy=True
CVD_country.groupby('location')['new_deaths'].plot(ax=axes[0,1], legend=True)
CVD_country.groupby('location')['total_cases'].plot(ax=axes[1,0], legend=True)
CVD_country.groupby('location')['total_deaths'].plot(ax=axes[1,1], legend=True)
CVD_country.groupby('location')['mortality_rate'].plot(ax=axes[2,0], legend=True)
#CVD_country.to_csv('data/output.csv')

axes[0, 0].set_title("New Cases")
axes[0, 1].set_title("New Deaths")
axes[1, 0].set_title("Total Cases")
axes[1, 1].set_title("Total Deaths")
axes[1, 1].set_title("Total Deaths")
axes[2, 0].set_title("Mortality Rate")

fig.tight_layout() 
plt.show()
'''

# print(data.isnull().sum())
#Change column titles to something appropriate
data.columns = ['Date', 'Country', 'New Cases', 'New deaths', 'Total Cases', 'Total Deaths']
CVD_no_china = data.loc[~(data['Country'].isin(["China", "World"]))]
# print(CVD_no_china)

CVD_no_china = pd.DataFrame(CVD_no_china.groupby(['Country', 'Date'])['Total Cases', 'Total Deaths'].sum()).reset_index()
print(CVD_no_china)
#
CVD_no_china = CVD_no_china.sort_values(by = ['Country','Date'], ascending=True)
print(CVD_no_china)

import seaborn as sns
def plot_bar(feature, value, title, df, size):
    f, ax = plt.subplots(1,1, figsize=(4*size,4))
    df = df.sort_values([value], ascending=False).reset_index(drop=True)
    g = sns.barplot(df[feature][0:10], df[value][0:10], palette='Set3')
    g.set_title("Number of {} - highest 10 values".format(title))
#    ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
    plt.show()

filtered_CVD_no_china = CVD_no_china.drop_duplicates(subset = ['Country'], keep='first')
plot_bar('Country', 'Total Cases', 'Total cases in the World except China', filtered_CVD_no_china, size=4)
plot_bar('Country', 'Total Deaths', 'Total deaths in the World except China', filtered_CVD_no_china, size=4)

#Plot world aggregate numbers for total cases and deaths.
def plot_world_aggregate(df, title='Aggregate plot', size=1):
    f, ax = plt.subplots(1,1, figsize=(4*size,2*size))
    g = sns.lineplot(x="Date", y='Total Cases', data=df, color='blue', label='Total Cases')
    g = sns.lineplot(x="Date", y='Total Deaths', data=df, color='red', label='Total Deaths')
    plt.xlabel('Date')
    plt.ylabel(f'Total {title} cases')
    plt.xticks(rotation=90)
    plt.title(f'Total {title} cases')
    ax.grid(color='black', linestyle='dotted', linewidth=0.75)
    plt.show()

#Group by dates.
#Reset index because groupby by default makes grouped columns indices
#Sum values from all countries per given date
CVD_no_china_aggregate = CVD_no_china.groupby(['Date']).sum().reset_index()
print(CVD_no_china_aggregate)

plot_world_aggregate(CVD_no_china_aggregate, 'Rest of the World except China', size=4)
#################################################

#Plot aggregate numbers for total cases and deaths for select countries.
#Starting from Feb 15th

def plot_aggregate_countries(df, countries, case_type='Total Cases', size=3, is_log=False):
    f, ax = plt.subplots(1,1, figsize=(4*size, 3*size))
    for country in countries:
        df_ = df[(df['Country']==country) & (df['Date'] > '2020-02-15')]
        g = sns.lineplot(x="Date", y=case_type, data=df_,  label=country)
        ax.text(max(df_['Date']), max(df_[case_type]), str(country))
    plt.xlabel('Date')
    plt.ylabel(f' {case_type} ')
    plt.title(f' {case_type} ')
    plt.xticks(rotation=90)
    if(is_log):
        ax.set(yscale="log")
    ax.grid(color='black', linestyle='dotted', linewidth=0.75)
    plt.show()

CVD_country_aggregate = CVD_no_china.groupby(['Country', 'Date']).sum().reset_index()

countries = ["Bangladesh"]
plot_aggregate_countries(CVD_country_aggregate, countries, case_type = 'Total Cases', size=4)

plot_aggregate_countries(CVD_country_aggregate, countries, case_type = 'Total Deaths', size=4)

#log scale
plot_aggregate_countries(CVD_country_aggregate, countries, case_type = 'Total Cases', size=4, is_log=True)

##############################################################
#Calculate MORTALITY and plot

def plot_mortality(df, title='Mainland China', size=1):
    f, ax = plt.subplots(1,1, figsize=(4*size,2*size))
    g = sns.lineplot(x="Date", y='Mortality (Deaths/Cases)', data=df, color='blue', label='Mortality (Deaths / Total Cases)')
    plt.xlabel('Date')
    plt.ylabel(f'Mortality {title} [%]')
    plt.xticks(rotation=90)
    plt.title(f'Mortality percent {title}\nCalculated as Deaths/Confirmed cases')
    ax.grid(color='black', linestyle='dashed', linewidth=1)
    plt.show()

CVD_no_china_aggregate['Mortality (Deaths/Cases)'] = CVD_no_china_aggregate['Total Deaths'] / CVD_no_china_aggregate['Total Cases'] * 100
plot_mortality(CVD_no_china_aggregate, title = ' - Rest of the World except China', size = 3)