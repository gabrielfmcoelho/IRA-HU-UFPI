import icecream as ic
import numpy as np
import pandas as pd

def fill_collection_of_type_elimination( # Função para preencher valor da coleta que do tipo eliminação com 1
    df: pd.DataFrame,
    type_column: str='tipo_controle',
    elimination_types: list=['Eliminação urinária', 'Fezes', 'Vômitos'],
    value_column: str='valor_controle',
    ) -> pd.DataFrame:
    """
    Function to fill the value of the collection which type is elimination with 1
    :param df: Dataframe to fill the value from
    :param type_column: Type column
    :param elimination_types: List of elimination types
    :param value_column: Value column
    :return: Dataframe with value column filled
    """
    df.loc[df[type_column].isin(elimination_types), value_column] = 1
    return df

def drop_null_values_that_are_not_type_elimination( # Função para remover linhas com valor nulo que não sejam do tipo eliminação
    df: pd.DataFrame,
    type_column: str='tipo_controle',
    elimination_types: list=['Eliminação urinária', 'Fezes', 'Vômitos'],
    value_column: str='valor_controle',
    ) -> pd.DataFrame:
    """
    Function to remove null values that are not elimination type
    :param df: Dataframe to remove null values from
    :param type_column: Type column
    :param elimination_types: List of elimination types
    :param value_column: Value column
    :return: Dataframe without null values that are not elimination type
    """
    index_to_drop = df.loc[(~(df[type_column].isin(elimination_types)) & (df[value_column].isnull()))].index
    return df.drop(index_to_drop).reset_index(drop=True)

def keep_only_selected_types( # Função para manter apenas os tipos de controle curados
    df: pd.DataFrame,
    type_column: str='tipo_controle',
    values_to_keep: list=[
        'Pressão Arterial Sistólica', # ok
        'Pressão Arterial Diastólica', # ok
        'Frequência Cardíaca', # ok
        'Frequência Respiratória', # ok
        'Temperatura  Axilar', # "ok" atenção ao duplo espaço entre as palavras
        ],
    ) -> pd.DataFrame:
    """
    Function to keep only selected types
    :param df: Dataframe to keep only selected types from
    :param type_column: Type column
    :param values_to_keep: List of values to keep
    :return: Dataframe with only selected types
    """
    return df.loc[df[type_column].isin(values_to_keep)].reset_index(drop=True)

def pivot( # Função para pivotar o dataframe
    df: pd.DataFrame,
    index_columns: list=['uid_prontuario_dt_internacao', 'prontuario', 'dt_internacao', 'dt_controle_date', 'dt_controle', 'alta'],
    target_column: str='tipo_controle',
    values_columns: list=['grupo_controle', 'valor_controle', 'diff_dt_controle_dt_internacao', 'diff_entre_dt_controle_1', 'diff_entre_dt_controle_2', 'variacao_valor_controle_1', 'variacao_valor_controle_2'],
    aggfunc: str='max'
    ) -> pd.DataFrame:
    """
    Function to pivot a dataframe
    :param df: Dataframe to pivot
    :param index_columns: Index columns
    :param target_column: Target column
    :param values_columns: Values columns
    :param aggfunc: Aggregation function
    :return: Dataframe pivoted
    """
    df_pivoted = df.pivot_table(index=index_columns,
                        columns=target_column,
                        values=values_columns,
                        aggfunc=aggfunc)
    df_pivoted.columns = ['_'.join(col) for col in df_pivoted.columns]
    return df_pivoted.reset_index()

    # fill float columns with 0
    # fill NaT columns with pd.Timedelta(seconds=0)

    #float_columns = [column for column in df_pivoted.columns if (column.startswith('valor_controle') or column.startswith('variacao_contr'))]
    #nat_columns = [column for column in df_pivoted.columns if column.startswith('diff_dt_')]
    
    #df_pivoted[float_columns] = df_pivoted[float_columns].fillna(0)
    #df_pivoted[nat_columns] = df_pivoted[nat_columns].fillna(pd.Timedelta(seconds=0))

def iqr_n_coletas_cre(
    df: pd.DataFrame
    ) -> pd.DataFrame:
    # calculate the interquartile range of the number of collections of creatinine
    q1, q3 = np.percentile(df['n_coletas_cre'], [25, 75])
    ic(q1, q3)
    # keep only uid_prontuario_internacao that the max n_coletas_cre is (igual or greater than q1) and (less or igual than q3)
    df_temp = df.groupby('uid_prontuario_internacao')['n_coletas_cre'].max().reset_index()
    df_temp = df_temp[(df_temp['n_coletas_cre'] >= q1) & (df_temp['n_coletas_cre'] <= q3)]
    uid_prontuario_dt_internacao_to_keep = list(df_temp['uid_prontuario_internacao'].unique())
    # keep only the uid_prontuario_internacao that are in uid_prontuario_dt_internacao_to_keep
    df = df[df['uid_prontuario_internacao'].isin(uid_prontuario_dt_internacao_to_keep)]
    df = df.reset_index(drop=True)
    # remove the row of the last n_coletas_cre for each uid_prontuario_internacao
    df = df.groupby('uid_prontuario_internacao').apply(lambda x: x.iloc[:-1])
    return df.reset_index(drop=True)



