import pandas as pd
import os
from glob import glob
import numpy as np
import pandas as pd


def organise_behav(df, ID, cond, stored, cond_name, behavs = ['pup sniff', 'pup groom', 'aborted retrieval', 'nest time','retrieval to nest', 'overall retrieval', 'crouching', 'nest building']):
    '''
    Organizes behavioural data and calculates latency and duration of behaviour, for illustration purposes. If a specific behaviour was not performed by the animal, its latency is set to the max.
    This function was written for BORIS files. In order to use with EthoVision files, the number of rows to be deleted at the beginning may differ (line 26), and line 30 might need to be modified as well. 
    
    Args:
        df: dataframe where your dataset is stored
        ID: list; list of your animals IDs
        cond: list; conditions of the experiment (e.g. time)
        stored: pd.Dataframe; 2D tabular data, where rows correspond to individual behaviours and columns correspond to         ID, condition, latency, duration
        cond_name: str; name of your condition (e.g. time)
        behavs: list; list of annotated behaviours
    
    Returns:
        stored: pd.Dataframe; 2D tabular data, where rows correspond to different behaviours and columns correspond to         ID, condition, latency, duration
    '''
    #organises imported dataframe (remove empty rows at the top of the df, rename columns appropriately, assign float       type to 'time') 
    df = df.iloc[14:, :]
    columns = list(df.iloc[0])
    df.columns = columns
    df = df.iloc[1:, :] 
    df["Time"] = df["Time"].astype(float)
    
    # define time of pup intro
    intro = df[df.Behavior == "pup intro"].Time.iloc[0]

    # extract behaviours, calculate latency and duration
    for behav in behavs:
        if behav == 'overall retrieval':
            df.loc[df.Behavior.isin(['aborted retrieval', 'retrieval to nest']), 'Behavior'] = 'overall retrieval'
        behav_df = df[df.Behavior == behav]
        
        if behav_df.empty:
            latency = 900
        else:
            latency = float(behav_df.iloc[0].Time) - float(intro)

        starts = behav_df[behav_df.Status == "START"].reset_index(drop = True).Time
        stops = behav_df[behav_df.Status == "STOP"].reset_index(drop = True).Time

        duration = sum(stops - starts)

        # create dictionary for each individual behaviour
        behaviour = {}
        behaviour["ID"] = ID
        behaviour[cond_name] = cond
        behaviour["behaviour"] = behav
        behaviour["latency"] = latency
        behaviour["duration"] = duration

        # turn dictionary for each behaviour into df, and concatenate dfs
        behaviour = pd.DataFrame(behaviour, index = [0])
        stored = pd.concat([stored, behaviour])
              
    
    stored = stored.reset_index(drop = True)          
    
    return stored



def organise_behav_new(df, ID, cond, stored, cond_name, behavs = ['pup sniff', 'pup groom', 'aborted retrieval', 'nest time','retrieval to nest', 'overall retrieval', 'crouching', 'nest building']):
    '''
    Organizes behavioural data and calculates latency and duration of behaviour, for illustration purposes. If a specific behaviour was not performed by the animal, its latency is set to the max.
    This function was written for BORIS files. In order to use with EthoVision files, the number of rows to be deleted at the beginning may differ (line 26), and line 30 might need to be modified as well. 
    
    Args:
        df: dataframe where your dataset is stored
        ID: list; list of your animals IDs
        cond: list; conditions of the experiment (e.g. time)
        stored: pd.Dataframe; 2D tabular data, where rows correspond to individual behaviours and columns correspond to         ID, condition, latency, duration
        cond_name: str; name of your condition (e.g. time)
        behavs: list; list of annotated behaviours
    
    Returns:
        stored: pd.Dataframe; 2D tabular data, where rows correspond to different behaviours and columns correspond to         ID, condition, latency, duration
    '''
    #organises imported dataframe (remove empty rows at the top of the df, rename columns appropriately, assign float       type to 'time') 
    df = df.rename(columns={"Behavior type": "Status"})
    df["Time"] = df["Time"].astype(float)
    
    # define time of pup intro
    intro = df[df.Behavior == "pup intro"].Time.iloc[0]

    # extract behaviours, calculate latency and duration
    for behav in behavs:
        if behav == 'overall retrieval':
            df.loc[df.Behavior.isin(['aborted retrieval', 'retrieval to nest']), 'Behavior'] = 'overall retrieval'
        behav_df = df[df.Behavior == behav]
        
        if behav_df.empty:
            latency = 900
        else:
            latency = float(behav_df.iloc[0].Time) - float(intro)

        starts = behav_df[behav_df.Status == "START"].reset_index(drop = True).Time
        stops = behav_df[behav_df.Status == "STOP"].reset_index(drop = True).Time

        duration = sum(stops - starts)

        # create dictionary for each individual behaviour
        behaviour = {}
        behaviour["ID"] = ID
        behaviour[cond_name] = cond
        behaviour["behaviour"] = behav
        behaviour["latency"] = latency
        behaviour["duration"] = duration

        # turn dictionary for each behaviour into df, and concatenate dfs
        behaviour = pd.DataFrame(behaviour, index = [0])
        stored = pd.concat([stored, behaviour])
              
    
    stored = stored.reset_index(drop = True)          
    
    return stored