import icecream as ic
import numpy as np
import pandas as pd
import operator

def parse_datetime( # Função para converter colunas de data e hora para o formato datetime
    df_column: pd.Series,
    column: str
    ) -> pd.DataFrame: 
    """
    Funtion to parse datetime columns from dataframe
    :param df: Dataframe to parse datetime columns
    :param columns: List of columns to parse
    :return: Dataframe with parsed datetime columns
    """
    df_column = df_column.astype(str)
    df_column = df_column.apply(lambda x: x[:19] if len(x) > 19 else x) # Remove milissegundos, se houver
    return pd.to_datetime(df_column, format='%Y-%m-%d %H:%M:%S') # Converte para datetime no formato Ano-Mes-Dia Hora:Minuto:Segundos

def split_datetime( # Função para extrair data da coluna de data e hora
    df: pd.DataFrame
    ) -> pd.DataFrame: 
    """
    Function to split date fom datetime columns, they should start with 'dt_'
    :param df: Dataframe to split datetime columns
    :return: Dataframe with splitted datetime columns, each column will have the suffix '_date'
    """
    columns = [column for column in df.columns if column.startswith('dt_')] # Por design todas as colunas de data e hora começam com 'dt_'
    for column in columns:
        df[f'{column}_date'] = df[column].dt.date
    return df

def count_unique_uids( # Função para contar uid's únicos e prontuarios
    df: pd.DataFrame,
    uid: str='uid_prontuario_dt_internacao',
    patient: str='prontuario'
    ) -> tuple:
    """
    Function to count unique uid's and patients
    :param df: Dataframe to count unique uid's and patients from
    :param uid: Unique identifier column
    :param patient: Patient column
    :return: Tuple with unique uid's and patients
    """
    unique_uids = df[uid].unique()
    unique_patients = df[patient].unique()
    print(f'[count_unique_uids] unique uid: {len(unique_uids)}')
    print(f'[count_unique_uids] unique patients: {len(unique_patients)}')
    return unique_uids, unique_patients

def create_uid( # Função para criar uid de prontuario e data de internação
    df: pd.DataFrame,
    first: str='prontuario',
    second: str='dt_internacao'
    ) -> pd.DataFrame: 
    """
    Function to create uid from the combination of two columns
    :param df: Dataframe to create uid from
    :param first: First column to combine
    :param second: Second column to combine
    :return: Dataframe with uid column, it will have the name 'uid_{first}_{second}'
    """
    uid = f'uid_{first}_{second}'
    df[uid] = df.apply(lambda x: f"{x[first]}_{x[second]}", axis=1)
    count_unique_uids(df)
    return df

def keep_only_valid_records( # Função para eliminar registros de eventos que ocorreram antes da internação
    df: pd.DataFrame,
    first: str,
    operation: str,
    second: str | int,
    second_is_constant: bool=False,
    patient: str='prontuario',
    dt_hospitalization: str='dt_internacao'
    ) -> pd.DataFrame:
    """
    Function to eliminate records of events that occurred before hospitalization
    :param df: Dataframe to eliminate records from
    :param dt_collection: Some collection column
    :param hospitalization: Hospitalization column
    :return: Dataframe without records of events that occurred before hospitalization
    """

    operations = {
        '>=': operator.ge,
        '>': operator.gt,
        '<=': operator.le,
        '<': operator.lt,
        '==': operator.eq, 
        '!=': operator.ne
    }
    second_term = second if second_is_constant else df[second]

    df_temporary = df.copy()
    print('--Before--')
    df_temporary = create_uid(df_temporary)
    uids_to_drop = df_temporary.loc[~(operations[operation](df_temporary[first], second_term)), 'uid_prontuario_dt_internacao'].unique()
    index_from_uids_to_drop = df_temporary.loc[df_temporary['uid_prontuario_dt_internacao'].isin(uids_to_drop)].index
    print('--after--')
    count_unique_uids(df_temporary.loc[~(df_temporary.index.isin(index_from_uids_to_drop))])
    return df.loc[~(df.index.isin(index_from_uids_to_drop))].reset_index(drop=True)

def time_diff_collection_and_hospitalization( # Função para calcular a diferença, em tempo, entre alguma coleta e a internação
    df: pd.DataFrame,
    dt_collection: str, # dt_creatinina OU dt_controle
    hospitalization: str='dt_internacao',
    ) -> pd.DataFrame:
    """
    Function to calculate the difference, in time, between some collection and hospitalization
    :param df: Dataframe to calculate the difference from
    :param dt_collection: Some collection column
    :param hospitalization: Hospitalization column
    :return: Dataframe with difference column, output name will be 'diff_{dt_collection}_{hospitalization}'
    """
    output_name = f'diff_{dt_collection}_{hospitalization}'
    df[output_name] = df[dt_collection] - df[hospitalization]
    return df

def time_diff_between_collections( # Função para calcular a diferença, em tempo, entre coletas em determinado intervalo de tempo    
    df: pd.DataFrame,
    dt_collection: str, # dt_creatinina OU dt_controle
    uid: str='uid_prontuario_dt_internacao',
    periods: int=2, # Janela de tempo de 2 coletas
    group_by_tags: list=[],
    ) -> pd.DataFrame:
    """
    Function to calculate the difference, in time, between collections in a given time interval
    :param df: Dataframe to calculate the difference from
    :param uid: Unique identifier column
    :param collection: Collection column
    :param periods: Number of periods to calculate the difference
    :return: Dataframe with difference columns, output name will be 'diff_entre_{collection}_{period}'
    """
    df = df.sort_values(by=[uid]+group_by_tags+[dt_collection], ascending=True).reset_index(drop=True)
    for period in range(1, periods+1):
        output = f'diff_entre_{dt_collection}_{period}'
        df[output] = df.groupby([uid]+group_by_tags)[dt_collection].diff(period)
    return df

def value_variation_between_collections( # Função para calcular a variação, em valor, entre coletas em determinado intervalo de tempo
    df: pd.DataFrame,
    collection: str, # valor_creatinina OU valor_controle
    dt_collection: str, # dt_creatinina OU dt_controle
    uid: str='uid_prontuario_dt_internacao',
    periods: int=2, # Janela de tempo de 2 coletas
    group_by_tags: list=[],
    ) -> pd.DataFrame:
    """
    Function to calculate the variation, in value, between collections in a given time interval
    :param df: Dataframe to calculate the variation from
    :param uid: Unique identifier column
    :param collection: Collection column
    :param periods: Number of periods to calculate the variation
    :return: Dataframe with variation columns, output name will be 'variacao_{collection}_{period}'
    """
    df = df.sort_values(by=[uid]+group_by_tags+[dt_collection], ascending=True).reset_index(drop=True)
    for period in range(1, periods+1):
        output = f'variacao_{collection}_{period}'
        denominator = df.groupby([uid]+group_by_tags)[collection].shift(period)
        df[output] = np.where(denominator.notna(), (df[collection] - denominator) / (denominator + 1e-8), np.nan)
    return df

def drop_variation_and_diff_null_values(
    df: pd.DataFrame,
    starting_prefix: list=['diff_', 'variacao_'],
    ) -> pd.DataFrame:
    """
    Function to drop null values from variation and diff columns
    :param df: Dataframe to drop null values from
    :param starting_prefix: List of prefixes to drop null values from
    :return: Dataframe without null values from variation and diff columns
    """
    for prefix in starting_prefix:
        columns = [column for column in df.columns if column.startswith(prefix)]
        df = df.dropna(subset=columns).reset_index(drop=True)
    return df