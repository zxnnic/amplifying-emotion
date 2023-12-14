import pandas as pd
from os import listdir
from os.path import isfile, join

import seaborn as sns
import matplotlib.pyplot as plt

DATA_PATH = "./"

pd.options.display.float_format = "{:,.2f}".format

def load_data(fname, study_codes):
    df = pd.read_csv(fname)
    df.replace(study_codes,inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    # drop_col_names = ['Select the face that looks happier:.'+str(n) for n in range(1,31)]
    # drop_col_names += ['Timestamp', 'Select the face that looks happier:', 'Score', 'Email Address']
    # drop_col_names = ['Timestamp']
    # print(df.columns)
    # for col in drop_col_names:
    #     if col in df.columns:
    #         df.drop(index=col, axis=1, inplace=True)
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
    sns.violinplot(data=data,palette='hls',width=0.2)
    plt.show()


if __name__ == "__main__":
    study_codes = load_study_codes()
    data = load_data("study_data.csv", study_codes)
    # get the preferences overall
    print('Preference based on realism overall')
    total_count = data.apply(pd.Series.value_counts, axis=0).sum(axis=1)
    print(total_count)
    print()
    # get preferences by person
    person_count = data.apply(pd.Series.value_counts, axis=1).divide(12)
    person_count.to_csv('output_person_ratio.csv')
    # plot the mean
    plot_violin(person_count)