import pandas as pd

#In this exercise, we're going to create a program that allows us do 
#cross-cultural cinematic research. A tool that prints the percentage of movie
#descriptions containing a certain word (scraped from Wikipedia),
#for different cultures. First we will practice a little with Pandas.
#Then, follow the steps to create the program.

#As a challenge, you can also ignore these steps and code it without help.

#1. First, download the movie_plots.csv file from Canvas and open it

data_location = "python\data_wrangling_2\movie_plots.csv"
df = pd.read_csv(data_location, sep=",", encoding="ISO-8859-1", on_bad_lines='skip')

#2. Let's inspect the data. Display the first rows and get the summary (.info)
print(df.loc[0])
print(df.info)

#3. Print out the number of movies for each Origin/Ethnicity
def get_number_of_origins(df): 
    """
    Returns a sorted dictionary with the number of movies with each origin
    
    Example code:
    for i in get_number_of_origins(df):
        print(i)
    """
    origins = {}
    for index, row in df.iterrows():
        current_origin = row['Origin/Ethnicity']
        if current_origin in origins:
            origins[current_origin] += 1
        else:
            origins[current_origin] = 1
    sorted_dict = dict(sorted(origins.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_dict

for i in get_number_of_origins(df):
        print(i)

#4. Subsetting: select only the rows with Bollywood movies
print(df.loc[df['Origin/Ethnicity'] == 'Bollywood'])

#5. Subsetting: select only the rows with Turkish movies released after 2000
print(df.loc[(df['Origin/Ethnicity'] == 'Turkish') & (df['Release Year'] > 2000)])

#6. Subsetting: create a new df with only Title, Release Year, Origin/Ethnicity, Plot
new_df = df[['Title', 'Release Year', 'Origin/Ethnicity', 'Plot']]
print(new_df)

#7. Change the column names to Title, Year, Origin, Plot. Find online how to this.
new_df = new_df.rename(columns={'Release Year': 'Year', 'Origin/Ethnicity': 'Origin'})
print(new_df.columns)

##This is where the basic section ends.##
##Advanced section: for a more challenging assignment, try (some of) the steps below##

#8. Create a new column "kimono" that is True if the Plot contains the word "kimono"
#and false if not (tip: find a suitable Pandas string method).
#Tip: use Pandas .astype(int) to convert the resulting Boolean in 0 or 1.
def add_word_present(expected_str, target_df = new_df, new_column_name = "", type = bool, literal = False):
    """
    Adds a new column, based on whether the plot contains the target string
    
    New column name defaults to expected_str if not explicitely set

    Example code:
    has_gun_df = add_word_present("gun", new_df, "has_gun", int, True)
    """
    if new_column_name == "": # if left empty
        new_column_name = expected_str

    if literal: #Adds word termination markers, to check for exclusively the full word
        expected_str = f"\b{expected_str}\b"

    target_df[new_column_name] = target_df["Plot"].str.contains(expected_str, na=False).astype(type) # Defaults to FALSE
    return target_df

kimono_df = add_word_present("kimono", new_df)
print(kimono_df)

#9. Using your new column, pd.groupby() and another Pandas function, count the number of movies
#with "kimono" in the plot, for the different origins.

def compare_column(target_column, group_column, target_df = new_df):
    """
    Counts how many entries are True/False in target_column, in rows with specific group_column values
    
    Example code:
    origins = count_true_false_by_origin("kimono", 'Origin', my_df)
    """
    groups = {} # One entry per group_column value
    for country, group in target_df.groupby(group_column): # Pandas group is NOT my group
        column_series = group[target_column]
        groups[country] = int(column_series.sum())

    sorted_groups = dict(sorted(groups.items(), key=lambda item: item[1], reverse=True))
    return sorted_groups
    

origins = compare_column("kimono", 'Origin')
print(origins)


#10. Using your earlier code, create a function add_word_present() with one argument (word),
#that adds a column df[word] with a 1 if the word occurs in the plot,
#and 0 if not.
#Extra challenge: make sure that it's not counted if it's inside another word.
has_gun_df = add_word_present("gun", new_df, "has_gun", int, True)
print(has_gun_df.loc[0])

#11. Write another function compare_origins() with one argument (word), that:
#1. adds a column to your data frame (simply call your earlier function)
#2. prints the proportion of movies for different origins containing that word
def compare_origins(word):
    worded_df = add_word_present(word)
    origins = compare_column(word, 'Origin', worded_df)
    for country in origins:
        print(f"{country}: {origins[country]}")

compare_origins("gun")

#12. We need one more tweak: to really compare different cultures,
#we need to account for the fact that the total number of movies is not the same.
#Write another, better function that calculates a percentage rather than a count.
#Hint: note that df.groupby(["Origin"])[word].count() will get you the number of movies, grouped by origin.
#Also sort the result so that the percentage is descending.
#Finally, make it user-friendly: print the word and what the numbers mean
def percentage_of_movies(word):
    """
    Prints the percentage of each country's movies containing the target word

    Example code:
    percentage_of_movies("gun")
    """
    percentages = {}
    worded_df = add_word_present(word)
    origins = compare_column(word, 'Origin', worded_df)
    total_movie_numbers = worded_df.groupby(["Origin"])[word].count().to_dict()
    for country in origins:
        percentages[country] = origins[country] / total_movie_numbers[country]
    
    percentages = dict(sorted(percentages.items(), key=lambda item: item[1], reverse=True))

    print(f"Percentage of movies whose plot contain the word: {word}")
    for country in percentages:
        current_percent = round((percentages[country] * 100), 2)
        print(f"{country}: {current_percent}%")

percentage_of_movies("gun")

#You're done! Try out your function and paste your most interesting result
#as a comment

"""
American: 18.79%
Japanese: 12.54%
Australian: 12.15%
Hong Kong: 11.5%
Canadian: 10.79%
Punjabi: 10.71%
British: 10.3%
Filipino: 9.38%
Malaysian: 8.57%
Bollywood: 7.88%
Russian: 7.33%
Chinese: 7.13%
South_Korean: 5.36%
Bengali: 5.23%
Tamil: 4.96%
Telugu: 4.81%
Malayalam: 3.93%
Bangladeshi: 3.45%
Turkish: 2.86%
Marathi: 2.13%
Kannada: 2.03%
Egyptian: 1.49%
Assamese: 0.0%
Maldivian: 0.0%
"""