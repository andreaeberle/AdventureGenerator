vectors_fully_in = [
                    [0,0],  #0 #center
                    [-1,0], #1 #left 1
                    [-2,0], #2 #left 2
                    [1,0],  #3 #right 1
                    [2,0],  #4 #right 2
                    [0,1],  #5 #up 1 (up is up-right because b1_center is always odd)
                    [-1,1], #6 #up 1, left 1
                    [-2,1], #7 #up 1, left 2
                    [-3,1], #8 #up 1, left 3
                    [1,1],  #9 #up 1, right 1
                    [2,1],  #10 #up 1, right 2
                    [0,2],  #11 #up 2
                    [-1,2], #12 #up 2, left 1
                    [-2,2], #13 #up 2, left 2
                    [1,2],  #14 #up 2, right 1
                    [2,2],  #15 #up 2, right 2
                    [0,3],  #16 #up 3
                    [-1,3], #17 #up 3, left 1
                    [0,-1], #18 #down 1 (down is down-right because b1_center is always odd)
                    [-1,-1],#19 #down 1, left 1
                    [-2,-1],#20 #down 1, left 2
                    [-3,-1],#21 #down 1, left 3
                    [1,-1], #22 #down 1, right 1
                    [2,-1], #23 #down 1, right 2
                    [0,-2], #24 #down 2
                    [-1,-2],#25 #down 2, left 1
                    [-2,-2],#26 #down 2, left 2
                    [1,-2], #27 #down 2, right 1
                    [2,-2], #28 #down 2, right 2
                    [0,-3], #29 #down 3
                    [-1,-3],#30 #down 3, left 1
                   ]

vectors_partial_left = [
                    [-3,0], #left 3
                    [-3,2], #up 2, left 3
                    [-2,3], #up 3, left 2
                    [-3,-2], #down 2, left 3
                    [-2,-3], #down 3, left 2
                   ]

vectors_partial_right = [
                    [3,0], #right 3
                    [3,2], #up 2, right 3
                    [2,3], #up 3, right 2
                    [3,-2], #down 2, right 3
                    [2,-3], #down 3, right 2
                   ]

vectors_partial_updown = [
                    [0,4], #up 4
                    [0,-4], #down 4
                   ]



import pandas as pd
import numpy as np

def generate_constants(W0,H0):
    M0 = W0*H0
    W1 = 6*W0+4
    H1 = 6*H0+4
    M1 = W1*H1
    m0 = np.arange(M0)
    m1 = np.arange(M1)
    a0 = m0%W0
    b0 = m0//W0
    a1_center = 6*a0-3*(b0%2)+6
    b1_center = 6*b0+5
    
    to_ret = {}
    to_ret['W0'] = W0
    to_ret['H0'] = H0
    to_ret['M0'] = M0
    to_ret['W1'] = W1
    to_ret['H1'] = H1
    to_ret['M1'] = M1
    to_ret['m0'] = m0
    to_ret['m1'] = m1
    to_ret['a0'] = a0
    to_ret['b0'] = b0
    to_ret['a1_center'] = a1_center
    to_ret['b1_center'] = b1_center
    return to_ret

def add_vectors(a1_center,b1_center,vectors,M0,W1):
    n = len(vectors)
    xvectors = np.tile(np.array(vectors)[:,0],(M0,1))
    yvectors = np.tile(np.array(vectors)[:,1],(M0,1))
    a1 = np.tile(a1_center,(n,1)).T+xvectors
    b1 = np.tile(b1_center,(n,1)).T+yvectors
    m1 = a1+(W1*b1)
    return m1

def perform_melt(rollup,all_df,which):
    if which == 'inside':
        start = 0
        stop = len(vectors_fully_in)
        df = rollup.iloc[:,start:stop]
    elif which == 'left':
        start = len(vectors_fully_in)
        stop = len(vectors_fully_in)+len(vectors_partial_left)
        df = rollup.iloc[:,start:stop]
    elif which == 'right':
        start = len(vectors_fully_in)+len(vectors_partial_left)
        stop = len(vectors_fully_in)+len(vectors_partial_left)+len(vectors_partial_right)
        df = rollup.iloc[:,start:stop]
    elif which == 'updown':
        start = len(vectors_fully_in)+len(vectors_partial_left)+len(vectors_partial_right)
        stop = len(vectors_fully_in)+len(vectors_partial_left)+\
                len(vectors_partial_right)+len(vectors_partial_updown)
        df = rollup.iloc[:,start:stop]
    c = df.columns
    df = df.reset_index()
    df = pd.melt(df, id_vars='index', value_vars=range(start,stop))
    df = df.set_index('value',verify_integrity=True)
    df.index.name = None
    df = df.sort_index()
    all_df.loc[df.index,which] = df['index']

def roll_up_resolution(constants):
    M0 = constants['M0']
    W1 = constants['W1']
    a1_center = constants['a1_center']
    b1_center = constants['b1_center']
    m1_fully_in = add_vectors(a1_center,b1_center,vectors_fully_in,M0,W1)
    m1_partial_left = add_vectors(a1_center,b1_center,vectors_partial_left,M0,W1)
    m1_partial_right = add_vectors(a1_center,b1_center,vectors_partial_right,M0,W1)
    m1_partial_updown = add_vectors(a1_center,b1_center,vectors_partial_updown,M0,W1)
    rollup_array = np.concatenate([m1_fully_in,m1_partial_left,m1_partial_right,m1_partial_updown],axis = 1)
    rollup = pd.DataFrame(rollup_array)
    return rollup

def roll_down_resolution(constants,rollup):
    M1 = constants['M1']
    columns = ['inside','left','right','updown']
    all_df_ary = np.zeros((M1,4))+np.nan
    all_df = pd.DataFrame(all_df_ary,columns = columns)
    for which in columns:
        perform_melt(rollup,all_df,which)
    return all_df