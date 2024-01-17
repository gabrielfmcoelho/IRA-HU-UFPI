import icecream as ic
import numpy as np
import pandas as pd



def merge_cre_contr(
    df_left: pd.DataFrame,
    df_right: pd.DataFrame,
    uid: str='uid_prontuario_dt_internacao',
    date_column: str='dt_coleta_date',
    ) -> pd.DataFrame:
    """
    Function to merge creatinine and control dataframes
    :param df_left: Creatinine dataframe
    :param df_right: Control dataframe
    :param uid: Unique identifier column
    :param date_column: Date column
    :return: Dataframe merged
    """
    list_uids_cre = list(df_left[uid].unique())
    list_uids_contr = list(df_right[uid].unique())
    list_uids = list(set(list_uids_cre).intersection(set(list_uids_contr)))

    df_left = df_left[df_left[uid].isin(list_uids)]
    df_right = df_right[df_right[uid].isin(list_uids)]
    df = pd.merge(df_left, df_right, on=[uid, date_column], how='left')
    return df.sort_values(by=[uid, date_column]).reset_index(drop=True)
