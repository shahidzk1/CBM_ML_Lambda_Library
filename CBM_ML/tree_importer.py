import uproot
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pandas as pd


"""
The tree_importer function takes in flat analysis tree and returns a pandas data-frame object. It has 3 inputs, the first one is
path of the analysis tree, the second one as the tree name and third one the number of CPU cores. The first and second input
should be inserted as strings i.e. path inside a single quotation '' or double quotations "". The third input should be a number. 
For example  tree_importer("/home/flat_trees/a.tree","PlainTree",4)
"""
def tree_importer(path,treename, n):    
    #The number of parallel processors
    executor = ThreadPoolExecutor(n)
    
    #To open the root file and convert it to a pandas dataframe
    file = uproot.open(path+':'+treename, library='pd', decompression_executor=executor,
                                  interpretation_executor=executor).arrays(library='np',decompression_executor=executor,
                                  interpretation_executor=executor)
    df= pd.DataFrame(data=file)
    return df


"""
The quality_cuts_plus_other_cuts function applies quality selection criteria with other selection criteria to reduce data size
"""
def quality_cuts_plus_other_cuts_lambda():
    #The following quality selection criteria is applied
    mass_cut = '('+labels[10]+' > 1.07) &'
    
    coordinate_cut = '('+labels[20]+'>-50) & ('+labels[20]+'<50) & ('+labels[21]+'>-50) & ('+labels[21]+'<50) & ('+labels[22]+'>-1) & ('+labels[22]+'<80) &'
    
    chi_2_positive_cut ='('+labels[0]+'>0) & ('+labels[8]+'>0) & ('+labels[2]+'>0) & ('+labels[1]+' > 0) &'
    
    distance_cut = '('+labels[4]+'>0) & ('+labels[5]+'<80) & ('+labels[3]+'>0) & ('+labels[3]+'<100) &'
    
    pz_cut = '('+labels[14]+'>0) & '
    #Other cuts
    pseudo_rapidity_cut_based_on_acceptance = '('+labels[19]+'>1) & ('+labels[19]+'<6.5) &'
    
    angular_cut = '('+labels[6]+'>0.1) & ('+labels[7]+'>0.1) &'
    
    data_reducing_cut = '('+labels[10]+'< 1.3) &  ('+labels[15]+'<20)  &   ('+labels[0]+' < 1000) &  ('+labels[2]+'<1e6) & ('+labels[1]+ '< 3e7) &  ('+labels[4]+'<5000) & ('+labels[8]+'< 100000)'

    cuts= mass_cut+coordinate_cut+chi_2_positive_cut+distance_cut+pz_cut+pseudo_rapidity_cut_based_on_acceptance+angular_cut+data_reducing_cut
    return cuts

"""
Selects the labels only required for lambda analysis
"""

def labels_lambda(file):
    find_labels = ['chi2_geo','prim_first','prim_second', 'distance','_dl','_l','cosine_first','cosine_second','chi2_topo','cosine_topo','_mass','_pT','_px','_py','_pz','_p','_phi','_rapidity','_pid','_eta','_x','_y','_z','_generation']
    labels = []
    for a in find_labels:
        for s in file.keys():
            if a in s:
                if 'err' not in s:
                    if s not in labels:
                        labels.append(s)
    return labels

"""
This tree_importer_with_cuts imports tree and also applies quality selection criteria on the data along with some further data reducing cuts.
"""

def tree_importer_with_cuts(path,treename, n):
    
    #This part changes the labels of the root tree's branches 
    
    new_labels=['chi2geo', 'chi2primneg','chi2primpos', 'distance', 'ldl','mass', 'pT', 'rapidity','issignal']
    
    #The number of parallel processors
    executor = ThreadPoolExecutor(n)
    
    #To open the 
    file = uproot.open(path+':'+treename, library='pd', decompression_executor=executor,
                                  interpretation_executor=executor)
    labels = labels_lambda(file)
    cuts = quality_cuts_plus_other_cuts_lambda(labels)
    select_labels = [labels[0],labels[1],labels[2],labels[3],labels[4],labels[10],labels[11],labels[18],labels[23]]

    np_arrays = file.arrays(select_labels, cuts, library='np',decompression_executor=executor,
                                  interpretation_executor=executor)
    df= pd.DataFrame(data=np_arrays)
    df.columns = new_labels
    #df['issignal']=((df['issignal']>0)*1)
    with pd.option_context('mode.use_inf_as_na', True):
        df = df.dropna()
    return df


