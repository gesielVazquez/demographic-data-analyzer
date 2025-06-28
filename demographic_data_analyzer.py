import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(df.loc[df['sex'] == 'Male', 'age'].mean(),1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((df.loc[df['education'] == 'Bachelors', 'education'].count() * 100)/df['education'].count(),1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    adv_edu_filt = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    adv_edu_tab = df[adv_edu_filt]
    adv_more_50K = adv_edu_tab.loc[adv_edu_tab['salary'] == '>50K', 'education'].count()

    low_edu_tab = df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    low_more_50K = low_edu_tab.loc[low_edu_tab['salary'] == '>50K', 'education'].count()
    
    higher_education = adv_edu_tab['education'].count()
    lower_education = low_edu_tab['education'].count()

    # percentage with salary >50K
    higher_education_rich = round((adv_more_50K * 100)/higher_education,1)
    lower_education_rich = round((low_more_50K * 100)/lower_education,1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_work_hours = df['hours-per-week'].min()
    num_min_workers = df.loc[df['hours-per-week'] == min_work_hours, 'education'].count()
    min_work_tab = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = round((min_work_tab.loc[min_work_tab['salary'] == '>50K', 'education'].count()*100)/num_min_workers,1)

    # What country has the highest percentage of people that earn >50K?

    people_per_country = df['native-country'].value_counts()
    people_per_country_df = people_per_country.to_frame()

    ppc_df_index = people_per_country_df.reset_index()
    ppc_df_rename = ppc_df_index.rename(columns={'native-country': 'country', 'count': 'total_num'})

    people_per_country_more50k = df[df['salary'] == '>50K']
    more50k_counts = people_per_country_more50k['native-country'].value_counts().to_frame().reset_index()
    more50k_counts_rename = more50k_counts.rename(columns={'native-country': 'country', 'count': 'filter_num'})

    merged_tab = pd.merge(left=ppc_df_rename,right=more50k_counts_rename, left_on='country', right_on='country')
    merged_tab['percentage'] = round((merged_tab['filter_num']*100)/merged_tab['total_num'],1)

    top_percentage = merged_tab['percentage'].max()
    pre_highest = merged_tab.loc[merged_tab['percentage'] == top_percentage, 'country']


    highest_earning_country = pre_highest.to_string(index=False)
    highest_earning_country_percentage = merged_tab['percentage'].max()

    # Identify the most popular occupation for those who earn >50K in India.

    people_per_country_more50k = df[df['salary'] == '>50K']
    indian_more50k = people_per_country_more50k.loc[people_per_country_more50k['native-country'] == 'India']
    count_indian_ocupation = indian_more50k['occupation'].value_counts().to_frame().reset_index()
    filter_indian_occupation = count_indian_ocupation.loc[count_indian_ocupation['count'] == count_indian_ocupation['count'].max(), 'occupation']

    top_IN_occupation = filter_indian_occupation.to_string(index=False)

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

