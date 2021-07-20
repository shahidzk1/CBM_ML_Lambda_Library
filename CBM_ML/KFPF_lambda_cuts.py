def KFPF_lambda_cuts(df):
    KFPF_lambda= df.copy()
    KFPF_lambda['new_signal']=0
    mask1 = (KFPF_lambda['chi2primpos'] > 18.4) & (KFPF_lambda['chi2primneg'] > 18.4)

    mask2 = (KFPF_lambda['ldl'] > 5) & (KFPF_lambda['distance'] < 1)

    mask3 = (KFPF_lambda['chi2geo'] < 3) & (KFPF_lambda['cosinepos'] > 0) & (KFPF_lambda['cosineneg'] > 0)

    KFPF_lambda = KFPF_lambda[(mask1) & (mask2) & (mask3)] 

    #After all these cuts, what is left is considered as signal, so we replace all the values in the 'new_signal'
    # column by 1
    KFPF_lambda['new_signal'] = 1
    return KFPF_lambda
