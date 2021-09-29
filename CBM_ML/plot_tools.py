from sklearn.metrics import roc_auc_score, roc_curve
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from numpy import sqrt, log, argmax
import itertools

"""
A receiver operating characteristic (ROC), or simply ROC curve, is a graphical plot which illustrates the performance of a binary classifier system as its
discrimination threshold is varied. This function requires the true binary value and the target scores, which can either be probability estimates of
the positive class, confidence values, or binary decisions.
The function roc_auc_score computes Area Under the Receiver Operating Characteristic Curve (ROC AUC) from prediction scores.

To find the best threshold which results more signal to background ratio for lambda candidates we use the parameter S0 called the approximate median significance
by the higgs boson  ML challenge (http://higgsml.lal.in2p3.fr/documentation,9.)
"""
def AMS(y_true, y_predict, y_true1, y_predict1):
    roc_auc=roc_auc_score(y_true, y_predict)
    fpr, tpr, thresholds = roc_curve(y_true, y_predict,drop_intermediate=False ,pos_label=1)
    S0 = sqrt(2 * ((tpr + fpr) * log((1 + tpr/fpr)) - tpr))
    S0 = S0[~np.isnan(S0)]
    xi = argmax(S0)
    S0_best_threshold = (thresholds[xi])
    if S0_best_threshold>1:
        S0_best_threshold = 1- S0_best_threshold

    roc_auc1=roc_auc_score(y_true1, y_predict1)
    fpr1, tpr1, thresholds1 = roc_curve(y_true1, y_predict1,drop_intermediate=False ,pos_label=1)
    S01 = sqrt(2 * ((tpr1 + fpr1) * log((1 + tpr1/fpr1)) - tpr1))
    S01 = S01[~np.isnan(S01)]
    xi1 = argmax(S01)
    S0_best_threshold1 = (thresholds[xi1])
    if S0_best_threshold1>1:
        S0_best_threshold1 = 1- S0_best_threshold1

    fig, ax = plt.subplots(figsize=(12, 8), dpi = 100)
    plt.plot(fpr, tpr, linewidth=3 ,linestyle=':',color='darkorange',label='ROC curve train (area = %0.4f)' % roc_auc)
    plt.plot(fpr1, tpr1, color='green',label='ROC curve test (area = %0.4f)' % roc_auc1)
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--', label='Random guess')
    #plt.scatter(fpr[xi], tpr[xi], marker='o', color='black', label= 'Best Threshold train set = '+"%.4f" % S0_best_threshold +'\n AMS = '+ "%.2f" % S0[xi])
    plt.scatter(fpr1[xi1], tpr1[xi1], marker='o', s=80, color='blue', label= 'Best Threshold test set = '+"%.4f" % S0_best_threshold1 +'\n AMS = '+ "%.2f" % S01[xi1])
    plt.xlabel('False Positive Rate', fontsize = 18)
    plt.ylabel('True Positive Rate', fontsize = 18)
    plt.legend(loc="lower right", fontsize = 18)
    plt.title('Receiver operating characteristic', fontsize = 18)
    ax.tick_params(axis='both', which='major', labelsize=18)
    plt.xlim([-0.01, 1.0])
    plt.ylim([0, 1.02])
    #axs.axis([-0.01, 1, 0.9, 1])
    fig.tight_layout()
    fig.savefig('hists.png')
    plt.show()
    return S0_best_threshold, S0_best_threshold1



"""
To visualize true MC signal in the probability distribution returned by XGB classifier for a train-test data-set, the preds_prob function can be used.
Its input are a data-frame, predictions of the classifier (probabilities) and the target in the data-frame, and shows how the True signal is present 
inside this probability.
"""

def preds_prob(df,preds,true,df1,preds1, true1):
    fig, ax = plt.subplots(figsize=(12, 8))
    bins1=100
    TP = df[(df[true]==1)]
    TN = df[(df[true]==0)]
    
    plt.hist(TN[preds], bins=bins1,facecolor='blue',alpha = 0.3, label='background in train')
    plt.hist(TP[preds], bins=bins1,facecolor='red',alpha = 0.3, label='signal in train')
    
    
    TP1 = df1[(df1[true1]==1)]
    TN1 = df1[(df1[true1]==0)]
    
    hist1, bins1 = np.histogram(TN1[preds1], bins=bins1)
    err1 = np.sqrt(hist1)
    center1 = (bins1[:-1] + bins1[1:]) / 2
    plt.errorbar(center1, hist1, yerr=err1, fmt='o',
                 c='blue', label='signal in test')
    
    hist, bins = np.histogram(TP1[preds1], bins=bins1)
    err = np.sqrt(hist)
    center = (bins[:-1] + bins[1:]) / 2
    plt.errorbar(center, hist, yerr=err, fmt='o',
                 c='red', label='background in test')
    
    #ax.annotate('cut on probability', xy=(0, 90),  xycoords='data',xytext=(0.25,0.5), textcoords='axes fraction',
                #fontsize=15,arrowprops=dict(facecolor='black', shrink=0.05),horizontalalignment='right', verticalalignment='top')
    

    
    if df[true].unique().shape[0]>2:
        TP2= df[df[true]>1]
        plt.hist(TP2[preds], bins=bins1,facecolor='green',alpha = 0.3, label='secondaries in train')
        TP2= df1[df1[true1]>1]
        hist2, bins2 = np.histogram(TP2[preds1], bins=bins1)
        center2 = (bins2[:-1] + bins2[1:]) / 2
        err2 = np.sqrt(hist2)
        plt.errorbar(center2, hist2,yerr=err2, fmt='o',c='green',label='secondaries in test')

    
    ax.set_yscale('log')
    ax.set_xlabel('Probability',fontsize=18)
    plt.ylabel('Counts', fontsize=18)
    ax.set_xticks(np.arange(0,1.1,0.1))
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.tick_params(axis='both', which='minor', labelsize=16)
    plt.legend(fontsize=18)
    fig.show()
    fig.tight_layout()
    return fig, ax

    
"""
A **Confusion Matrix** $C$ is such that $C_{ij}$ is equal to the number of observations known to be in group $i$ and predicted to be in group $j$.
 Thus in binary classification, the count of true positives is $C_{00}$, false negatives $C_{01}$,false positives is $C_{10}$, and true neagtives is $C_{11}$.

If $ y^{'}_{i} $ is the predicted value of the $ i$-th sample and $y_{i}$ is the corresponding true value, then the fraction of correct predictions over
$ n_{samples}$ is defined as 
$$
True \: positives (y,y^{'}) =  \sum_{i=1}^{n_{samples} } 1 (y^{'}_{i} = y_{i}=1)
$$ 

The following function prints and plots the confusion matrix. Normalization can be applied by setting `normalize=True`.
"""

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label',fontsize = 15)
    plt.xlabel('Predicted label',fontsize = 15)


"""
The function comparison compares the results of XGB and KFPF (manual selection cuts)
"""

def comaprison_XGB_KFPF(XGB_mass,KFPF_mass):
    range1= (1.0999, 1.17)
    fig, axs = plt.subplots(2, 1,figsize=(15,10), sharex=True,  gridspec_kw={'width_ratios': [10],
                           'height_ratios': [8,4]})

    ns, bins, patches=axs[0].hist((XGB_mass),bins = 300, range=range1, facecolor='red',alpha = 0.3)
    ns1, bins1, patches1=axs[0].hist((KFPF_mass),bins = 300, range=range1,facecolor='blue',alpha = 0.3)

    axs[0].set_ylabel("counts", fontsize = 15)
    axs[0].legend(('XGBoost Selected $\Lambda$s','KFPF selected $\Lambda$s'), fontsize = 15, loc='upper right')

    #plt.rcParams["legend.loc"] = 'upper right'
    axs[0].set_title("The lambda's Invariant Mass histogram with KFPF and XGB selection criteria on KFPF variables", fontsize = 15)
    axs[0].grid()
    axs[0].tick_params(axis='both', which='major', labelsize=15)


    hist1, bin_edges1 = np.histogram(XGB_mass,range=(1.09, 1.17), bins=300)
    hist2, bin_edges2 = np.histogram(KFPF_mass,range=(1.09, 1.17), bins=300)

    #makes sense to have only positive values 
    diff = (hist1 - hist2)
    axs[1].bar(bins[:-1],     # this is what makes it comparable
        ns / ns1, # maybe check for div-by-zero!
        width=0.001)
    plt.xlabel("Mass in $\dfrac{GeV}{c^2}$", fontsize = 15)
    axs[1].set_ylabel("XGB / KFPF", fontsize = 15)
    axs[1].grid()
    axs[1].tick_params(axis='both', which='major', labelsize=15)

    plt.show()
    fig.tight_layout()


"""
Function that plots signal and background in the train-test data set 
"""
def plt_sig_back(df):
    range1 = (1.077, 1.18)
    fig, axs = plt.subplots(figsize=(10, 6))
    #df_scaled['mass'].plot.hist(bins = 300, range=range1,grid=True,sharey=True)
    (df[df['issignal']==0])['mass'].plot.hist(bins = 300, facecolor='yellow',grid=True,range=range1, label='Background')
    (df[df['issignal']==1])['mass'].plot.hist(bins = 300, facecolor='magenta',grid=True, range=range1, label ='Signal')
    #plt.vlines(x=1.108,ymin=-1,ymax=48000, color='black', linestyle='-')
    #plt.vlines(x=1.1227,ymin=-1,ymax=48000, color='black', linestyle='-')
    plt.ylabel("Counts (log scale)", fontsize=15)
    plt.xlabel("Mass in GeV/$c^2$", fontsize= 15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    #plt.title('Test and Train Lambda Invariant Mass', fontsize = 15)
    plt.legend( fontsize = 15)
    axs.tick_params(axis='both', which='major', labelsize=18)
    plt.yscale("log")
    fig.tight_layout()
    fig.savefig("hists.png")
    

    
# The following function will display the inavriant mass histogram of the original 10k event set along with the mass histoigram after we apply a cut
# on the probability prediction of xgb
def cut_visualization(df, variable,cut, range1=(1.09, 1.19), bins1= 300 ):
    mask1 = df[variable]>cut
    df3=df[mask1]
    
    fig, ax2 = plt.subplots(figsize=(12, 8), dpi = 300)
    color = 'tab:blue'
    ax2.hist(df['mass'],bins = bins1, range=range1, facecolor='blue' ,alpha = 0.35, label='before selection')
    ax2.set_ylabel('Counts', fontsize = 15, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend( fontsize = 15, loc='upper left')
    ax2.tick_params(axis='both', which='major', labelsize=15)
    ax2.grid()
    ax2.set_xlabel("Mass (GeV/${c^2}$)", fontsize = 18)
    
    
    
    color = 'tab:red'
    ax1 = ax2.twinx()
    ax1.hist(df3['mass'], bins = bins1, range=range1, facecolor='red',alpha = 0.35, label="XGB (with a cut > %.2f"%cut+')')
    ax1.set_xlabel('Mass in GeV', fontsize = 15)
    ax1.set_ylabel('Counts ', fontsize = 15, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.tick_params(axis='both', which='major', labelsize=15)
    ax1.legend( fontsize = 18,loc='upper right' )

    plt.title("The original sample's Invariant Mass along with mass after selection of XGB", fontsize = 15)
    #plt.text(0.02, 0.1, r'cut > %.4f'%cut, fontsize=15)
    plt.show()
    fig.tight_layout()
    fig.savefig("test_best.png")
