import re
import csv
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from os import listdir
from os.path import isfile, join
from sklearn.utils import resample
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, MinMaxScaler


DATA_PATH = '../data'
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

N_COMPONENTS = 2
MAX_ITER = 500
K_VALUE = 6

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

def plotAllAU(data,s):
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
    #n_samples = getMinLen(data)
    n_samples = 100
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
    return df_means

def getMinLen(data):
    min_len = len(data[0])
    for df in data:
        if len(df) < min_len:
            min_len = len(df)
    return min_len
        
def plotMeansScaled(data,s):
    n_samples = 100
    df_means = pd.DataFrame()
    fig, axes = plt.subplots(2,4,figsize=(20,10),sharey=True)
    row = 0
    col = 0
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
        sns.lineplot(df, ax=axes[row,col], dashes=False, palette=sns.color_palette(['#b5b5b5'],len(all_p)), legend=False)
        axes[row,col].set(title=au)
        sns.lineplot(df.mean(axis=1), ax=axes[row,col], linewidth=3)
        # plt.plot(df_means[au], linewidth=3)
        if col < 3:
            col += 1
        else:
            row += 1
            col = 0

    fig.savefig(join(FIGURE_PATH,"mean_aus_"+s), bbox_inches='tight')
    return df_means

def pca(data):
    num_cols = data.shape[1]-1
    # get how many features
    pca = PCA()
    y = pca.fit_transform(data)
    print(pca.explained_variance_ratio_)

    # we know that its 2 from ^
    model = PCA(n_components=2).fit(data)
    pred = model.transform(data)
    n_pcs = model.components_.shape[0]

    # get the index of the most important feature on EACH component
    most_important = [np.abs(model.components_[i]).argmax() for i in range(n_pcs)]
    print(abs(model.components_))

    # get the names
    most_important_names = [AUS_SYM["happy"][most_important[i]] for i in range(n_pcs)]
    dic = {'PC{}'.format(i): most_important_names[i] for i in range(n_pcs)}
    # build the dataframe
    df = pd.DataFrame(dic.items())
    print('most important feature is')
    print(df.head(2))
    
    # with open('./output/pca_results.csv', 'w', newline='') as f:
    #     writer = csv.writer(f, delimiter=',')

    #     writer.writerow(pca.explained_variance_ratio_)
    #     for row in abs(pca.components_):
    #         writer.writerow(row)


def k_means(data, n_clusters, N_COMPONENTS):
    # run PCA to reduce the number of dimensions used
    preprocessor = Pipeline([
        ("scaler", MinMaxScaler()),
        ("pca", PCA(n_components=N_COMPONENTS, random_state=42)),
    ])

    clusterer = Pipeline([(
        "kmeans",
        KMeans( n_clusters=n_clusters,
                init="k-means++",
                n_init=50,
                max_iter=MAX_ITER,
                random_state=42,
            ),
    ),])

    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("clusterer", clusterer)
    ])
    pipe.fit(data)

    pcadf = pd.DataFrame(
        pipe["preprocessor"].transform(data),
        columns=["component_1", "component_2"],
    )

    pcadf["predicted_cluster"] = pipe["clusterer"]["kmeans"].labels_
    if n_clusters == K_VALUE:
            pcadf["predicted_cluster"].to_csv('predicted_classes_k_'+str(K_VALUE)+'.csv', encoding='utf-8')
    plt.style.use("fivethirtyeight")
    plt.figure(figsize=(8, 8))

    scat = sns.scatterplot(
        data=pcadf,
        x="component_1",
        y="component_2",
        hue="predicted_cluster",
        palette="Set2"
    )

    scat.set_title("k="+str(n_clusters))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.savefig('./output/k_'+str(n_clusters), bbox_inches='tight')

def plotMeans(df, s):
    facs_plot = sns.lineplot(df, dashes=False)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    facs_plot.figure.savefig(join(FIGURE_PATH,"means_"+s), bbox_inches='tight')
    plt.clf()

if __name__ == "__main__":
    # happy
    data = getData("happy")
    # plot each AU scaled
    # df_means = plotScaled(data,"happy")
    # plot each participant seperately
    #plotAUs(data,"happy")

    # SUBPLOT versions
    # plotAllAU(data,"happy")
    df_means = plotMeansScaled(data,"happy")
    plt.close()
    # plot all means one one graph
    plotMeans(df_means,"happy")
    plt.close()
    # group similar points together
    pca(df_means)
    for k in range(1,9):
        # print('running k='+str(k))
        k_means(df_means,k,N_COMPONENTS)