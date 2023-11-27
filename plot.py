import re
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from os import listdir
from os.path import isfile, join
from sklearn.utils import resample

DATA_PATH = './data'
FIGURE_PATH = './figures'
DATA_FILES = [f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f))]

AUS = {
    "happy": ["CheekSquintRight", "CheekSquintLeft", "EyeSquintRight", "EyeSquintLeft", "MouthDimpleRight", "MouthDimpleLeft",
             "NoseSneerRight", "NoseSneerLeft", "MouthSmileRight", "MouthSmileLeft", "JawOpen", "MouthUpperUpRight", "MouthUpperUpLeft",
             "BrowDownRight", "BrowDownLeft"],
    "angry": []
}
# symmetry assumption
AUS_SYM = {
    "happy": ["CheekSquintRight", "EyeSquintRight", "MouthDimpleRight",
             "NoseSneerRight", "MouthSmileRight", "JawOpen", "MouthUpperUpRight", 
             "BrowDownRight"],
    "angry": []
}

def getData(s):
    data = []
    for f in DATA_FILES:
        if s in f:
            df = pd.read_csv(join(DATA_PATH,f))
            columns = df.columns.values.tolist()
            for col in columns:
                if col not in AUS_SYM[s]:
                    df = df.drop(col,axis=1)
            data.append(df)
    return data

def plotAUs(data,s):
    for p_num, df in enumerate(data):
        facs_plot = sns.lineplot(df, dashes=False)
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        facs_plot.figure.savefig(join(FIGURE_PATH,"p"+str(p_num)+"_"+s), bbox_inches='tight')
        plt.clf()

def plotEachAU(data,s):
    fig, axes = plt.subplots(2,4,figsize=(20,10),sharey=True)
    row = 0
    col = 0
    for au in AUS_SYM[s]:
        all_p = []
        for p_num,df in enumerate(data):
            all_p.append(df[au].rename('p'+str(p_num)))
        # turn all series into a dataframe
        df = pd.concat(all_p, axis=1)
        sns.lineplot(df, ax=axes[row,col],dashes=False)
        axes[row,col].set_title(au)
        if row == 1 and col == 3:
            plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        else:
            axes[row,col].get_legend().remove()

        if col < 3:
            col += 1
        else:
            row += 1
            col = 0
    fig.savefig(join(FIGURE_PATH,"facs_curves_"+s), bbox_inches='tight')

def plotScaled(data,s):
    n_samples = getMinLen(data)
    df_means = pd.DataFrame()
    for au in AUS_SYM[s]:
        all_p = []
        for p_num,df_p in enumerate(data):
            # downsample
            d = resample(df_p,
                         replace=True,
                         n_samples=n_samples,
                         random_state=42)
            d = d.sort_index().reset_index(drop=True)
            # append to dataframe
            all_p.append(d[au].rename('p'+str(p_num)))
        # turn all series into a dataframe
        df = pd.concat(all_p, axis=1)
        # make line for the mean
        df_means[au] = df.mean(axis=1)
        # plot it all
        facs_plot = sns.lineplot(df, dashes=False, palette=sns.color_palette(['#b5b5b5'],len(all_p)), legend=False)
        facs_plot.set(title=au)
        plt.plot(df_means[au], linewidth=3)
        facs_plot.figure.savefig(join(FIGURE_PATH, "AU_"+au+"_"+s), bbox_inches='tight')
        plt.clf()
    df_means.to_csv('mean_aus_scaled.csv', encoding='utf-8')

def getMinLen(data):
    min_len = len(data[0])
    for df in data:
        if len(df) < min_len:
            min_len = len(df)
    return min_len

if __name__ == "__main__":
    # happy
    data = getData("happy")
    # plot each AU scaled
    plotScaled(data,"happy")
    # plot each participant seperately
    # plotAUs(data,"happy")

    # # plot each person with a specific AU as subplots
    # plotEachAU(data,"happy")

    

    # angry