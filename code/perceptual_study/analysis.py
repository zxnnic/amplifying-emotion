import pandas as pd
from os import listdir
from os.path import isfile, join

import seaborn as sns
import matplotlib.pyplot as plt
import statistics as stat
import math

DATA_PATH = "./"
STUDY_DATA = "study_data.csv"
NUM_QUESTIONS = 12

pd.options.display.float_format = "{:,.2f}".format

def load_data(fname, study_codes):
    df = pd.read_csv(fname)
    df.replace(study_codes,inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    return df

def load_study_codes():
    study_codes = {}
    for fname in listdir(DATA_PATH):
        if isfile(join(DATA_PATH, fname)) and "studycode" in fname:
            df = pd.read_csv(fname)
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            codes = pd.Series(df.Condition.values,index=df.Name).to_dict()
            study_codes.update(codes)
    return study_codes
    
def plot_violin(data):
    print('{:7}{:>6}{:>6}'.format('','AMP','LIN'))  
    print('{:7}{:6.2}{:6.2}'.format('mean', stat.mean(data['AMP']), stat.mean(data['LIN'])))
    print('{:7}{:6.2}{:6.2}'.format('median', stat.median(data['AMP']), stat.median(data['LIN'])))
    print('{:7}{:6.2}{:6.2}'.format('std', stat.stdev(data['AMP']), stat.stdev(data['LIN'])))

    sns.violinplot(data=data,palette='hls',width=0.5)
    plt.show()

def plot_boxplot(data):
    sns.boxplot(data=data,palette='hls',width=0.2)
    plt.show()

if __name__ == "__main__":
    study_codes = load_study_codes()
    data = load_data(STUDY_DATA, study_codes)
    # get the preferences overall
    print('Preference based on realism overall')
    total_count = data.apply(pd.Series.value_counts, axis=0)
    total_count.to_csv("output_per_question_preferences.csv")
    print()
    # get preferences by person
    person_count = data.apply(pd.Series.value_counts, axis=1).divide(NUM_QUESTIONS)
    person_count = person_count.sort_values(by='AMP', ascending=False)
    person_count.to_csv('output_person_ratio_decrease.csv')
    # plot the mean
    plot_violin(person_count)