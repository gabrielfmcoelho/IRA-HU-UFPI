import icecream as ic
import numpy as np
import pandas as pd

def calculate_age( # Função para calcular idade a partir da data de nascimento e referência (data de internação)
    df: pd.DataFrame,
    birth: str='dt_nascimento',
    reference: str='dt_internacao',
    output: str='idade',
    ) -> pd.DataFrame: 
    """
    Function to calculate age from birth and reference date
    :param df: Dataframe to calculate age from
    :param birth: Birth date column
    :param reference: Reference date column
    :return: Dataframe with age column
    """
    df[output] = df.apply(lambda x: (x[reference].year - x[birth].year) - ((x[reference].month, x[reference].day) < (x[birth].month, x[birth].day)), axis=1)
    return df

def identify_hospitalization_time( # Função para identificar o número de internações de um paciente no momento da internação
    df: pd.DataFrame,
    uid: str='uid_prontuario_dt_internacao',
    hospitalization: str='dt_internacao',
    output: str='n_internacoes'
    ) -> pd.DataFrame: 
    """
    Function to identify the number of hospitalizations of a patient at the moment of hospitalization
    :param df: Dataframe to identify the number of hospitalizations from
    :param uid: Unique identifier column
    :param output: Output column
    :return: Dataframe with hospitalization time column
    """
    # TODO: LIMPAR CODIGOS COMENTADOS
    df[output] = df.groupby(uid)[hospitalization].rank(method='dense').astype(int)
    #df['n_internacoes'] = df.groupby(['prontuario', 'uid_prontuario_internacao']).cumcount() + 1
    return df

def identify_collection_time( # Função para identificar o número de coletas de um paciente no momento da coleta
    df: pd.DataFrame,
    uid: str='uid_prontuario_dt_internacao',
    dt_collection: str='dt_creatinina',
    output: str='n_coletas_creatinina'
    ) -> pd.DataFrame:
    """
    Function to identify the number of collections of a patient at the moment of collection
    :param df: Dataframe to identify the number of collections from
    :param uid: Unique identifier column
    :param dt_collection: Collection column
    :param output: Output column
    :return: Dataframe with collection time column
    """
    df[output] = df.groupby(uid)[dt_collection].cumcount()+1 # TODO: CUMCOUNT OU RANK?
    return df

def ira( # Função para identificar IRA de acordo com as regras de validação em pelo menos um dos periodos
    row: pd.Series,
    periods: int,
    ira_column: str='ira',
) -> int:
    """
    Function to verify if IRA occurred in at least one of the periods and aggregate in a single column
    :param row: Row to verify IRA from
    :param periods: Number of periods to calculate the variation
    :param ira_column: IRA column
    :return: 1 if IRA occurred in at least one of the periods, 0 otherwise
    """
    for period in range(1, periods+1): # Verifica se a IRA ocorreu em pelo menos um dos periodos e agrega em uma unica coluna
        if row[f'{ira_column}_{period}'] == 1:
            return 1
    return 0

def validation( # Função para rotular a ocorrencia de IRA
    row: pd.Series, 
    period: int, 
    time_diff: int,
    time_diff_threshold: int, 
    value_threshold: float,
    time_diff_collection_column: str='diff_entre_dt_creatinina',
    value_variation_collection_column: str='varicao_valor_creatinina',
    ) -> int:
    """
    Function to label the IRA occurrence according to validation rules
    :param row: Row to label the IRA from
    :param period: Period to calculate the variation
    :param time_diff: Min time difference between collections
    :param time_diff_threshold: Max time difference between collections
    :param value_threshold: Value threshold
    :param time_diff_collection_column: Time difference between collections column
    :param value_variation_collection_column: Value variation between collections column
    :return: 1 if IRA occurred, 0 otherwise
    """
    if (
        (row[f'{time_diff_collection_column}_{period}'] >= pd.Timedelta(hours=time_diff)) and  # limite inferior de tempo entre as coletas
        (row[f'{time_diff_collection_column}_{period}'] < pd.Timedelta(hours=time_diff_threshold)) and # limite superior de tempo entre as coletas
        (abs(row[f'{value_variation_collection_column}_{period}']) >= value_threshold) # limite de variação do valor entre as coletas
    ):
        return 1 # IRA
    else:
        return 0 # Não IRA

def identify_ira( # Função para identificar ocorrencia de IRA de acordo com as regras de validação
    df: pd.DataFrame,
    periods: int=1 # Janela de tempo de 2 coletas
    ) -> pd.DataFrame: 
    """
    Function to identify IRA occurrence according to validation rules
    :param df: Dataframe to identify IRA from
    :param periods: Number of periods to calculate the variation
    :return: Dataframe with IRA column
    """
    periods_rules = {
        1: {
            "name" : "24h",
            "time_diff": 20, # No HU-UFPI o exame que representa 24 horas ocorre a partir de 20 horas está sendo considerado o limite de no maximo 40 horas de diferença entre as coletas
            "time_diff_threshold": 40,
            "value_threshold": 0.3,
        },
        2: {
            "name" : "48h",
            "time_diff": 40, # No HU-UFPI o exame que representa 48 horas ocorre a partir de 40 horas está sendo considerado o limite de no maximo 72 horas de diferença entre as coletas
            "time_diff_threshold": 72,
            "value_threshold": 0.3,
        }
    }
    for period in range(1, periods+1):
        df[f'ira_{period}'] = df.apply(lambda x: validation(x, period, periods_rules[period+1]['time_diff'], periods_rules[period+1]['time_diff_threshold'], periods_rules[period]['value_threshold']), axis=1)
    df['ira'] = df.apply(lambda x: ira(x, periods=periods), axis=1)
    return df

def label_target( # Função para rotular a feature alvo designada
    df: pd.DataFrame,
    target: str, # ira OU valor_creatinina
    uid: str='uid_prontuario_dt_internacao',
    fill: float=None,
    output_type: str=None, # float OU int
    ) -> pd.DataFrame:
    """
    Function to label the designated target feature
    :param df: Dataframe to label the target from
    :param uid: Unique identifier column
    :param target: Target column
    :param fill: Fill NaN values with
    :param output_type: Output type
    :return: Dataframe with target column, output name will be 'apresentara_{target}'
    """
    output_types = {
        'float': float,
        'int': int
    }
    output = f'apresentara_{target}'
    df[output] = df.groupby(uid)[target].shift(-1)
    if fill:
        df[output] = df[output].fillna(fill)
    if output_type:
        df[output] = df[output].astype(output_types[output_type])
    return df