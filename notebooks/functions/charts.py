from pandas import DataFrame, cut
from sklearn.metrics import roc_curve, auc, confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_boxplot_distant_and_close(df: DataFrame, column: str, title_reference: str = None, date_to_floor: str = None, size: set = (10, 4)) -> None:
    """
    Function to plot 2 boxplots of a column of a dataframe, one with outliers and other without outliers
    :param df: pandas.DataFrame: dataframe to be used
    :param column: str: column to be used
    :param title_reference: str: title of the plot
    :return: None
    """
    title_reference = title_reference if title_reference else column
    fig, ax = plt.subplots(1, 2, figsize=size)
    if date_to_floor:
        df[column] = df[column].dt.days
    sns.boxplot(x=df[column], ax=ax[0])
    sns.boxplot(x=df[column], ax=ax[1], showfliers=False)
    min_value = round(df[column].quantile(0.25) - 1.5 * (df[column].quantile(0.75) - df[column].quantile(0.25)), 2)
    max_value = round(df[column].quantile(0.75) + 1.5 * (df[column].quantile(0.75) - df[column].quantile(0.25)), 2)
    ax[1].set_xlim(min_value, max_value)
    ax[0].set_title(f'IQR { title_reference } com outliers')
    ax[1].set_title(f'IQR { title_reference } ampliado')
    ax[0].text(0.05, 0.95, f'Min: {df[column].min()}\nMax: {df[column].max()}', transform=ax[0].transAxes, fontsize=10, verticalalignment='top')
    ax[1].text(0.05, 0.95, f'Min IQR: {min_value}\nMax IQR: {max_value}', transform=ax[1].transAxes, fontsize=10, verticalalignment='top')
    fig.show()

def plot_boxplot(df: DataFrame, column: str, title_reference: str = None, min_max_global: bool = False) -> None:
    """
    Function to plot a boxplot of a column of a dataframe
    :param df: pandas.DataFrame: dataframe to be used
    :param column: str: column to be used
    :param title_reference: str: title of the plot
    :return: None
    """
    title_reference = title_reference if title_reference else column
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    if min_max_global:
        sns.boxplot(x=df[column], ax=ax, showfliers=True)
    else:
        sns.boxplot(x=df[column], ax=ax)
    ax.set_title(f'IQR { title_reference }')
    ax.text(0.05, 0.95, f'Q1: {df[column].quantile(0.25)}', transform=ax.transAxes, fontsize=10, verticalalignment='top')
    ax.text(0.05, 0.85, f'Q2: {df[column].quantile(0.5)}', transform=ax.transAxes, fontsize=10, verticalalignment='top')
    ax.text(0.05, 0.75, f'Q3: {df[column].quantile(0.75)}', transform=ax.transAxes, fontsize=10, verticalalignment='top')
    ax.text(0.05, 0.35, f'Min: {df[column].min()}', transform=ax.transAxes, fontsize=10, verticalalignment='top')
    ax.text(0.05, 0.25, f'Max: {df[column].max()}', transform=ax.transAxes, fontsize=10, verticalalignment='top')
    fig.show()

def plot_line_chart_count_by_date(df: DataFrame, date_column: str, y_column: str = None, title: str = None) -> None:
    """
    Function to plot a line chart with count of records by date
    :param df: pandas.DataFrame: dataframe to be used
    :param date_column: str: date column to be used
    :param title: str: title of the plot
    :return: None
    """
    title = title if title else date_column
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    if y_column:
        sns.lineplot(x=df[date_column], y=df[y_column])
    else:
        df[date_column].value_counts().sort_index().plot(kind='line', figsize=(10, 4))
    plt.title(title)
    plt.show() 

def plot_bar_chart_count_by_column(df: DataFrame, column: str, group_column: str = None, title: str = None) -> None:
    """
    Function to plot a bar chart with count of records by column
    :param df: pandas.DataFrame: dataframe to be used
    :param column: str: column to be used
    :param title: str: title of the plot
    :return: None
    """
    title = title if title else column
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    df = df.copy()
    if group_column:
        min_value = df[group_column].min()
        max_value = df[group_column].max()
        df[f'{group_column}_'] = cut(df[group_column], bins=5, labels=[f'{min_value} - {min_value+(max_value-min_value)/5}', f'{min_value+(max_value-min_value)/5} - {min_value+2*(max_value-min_value)/5}', f'{min_value+2*(max_value-min_value)/5} - {min_value+3*(max_value-min_value)/5}', f'{min_value+3*(max_value-min_value)/5} - {min_value+4*(max_value-min_value)/5}', f'{min_value+4*(max_value-min_value)/5} - {max_value}'])
        sns.countplot(x=column, data=df, hue=f'{group_column}_', ax=ax)
        ax.set_ylim(0, df.groupby(f'{group_column}_')[column].value_counts().max()+df.groupby(f'{group_column}_')[column].value_counts().max()*0.2)
    else:
        sns.countplot(x=column, data=df, ax=ax)
        ax.set_ylim(0, df[column].value_counts().max()+df[column].value_counts().max()*0.2)
    ax.set_title(title)
    #for p in ax.patches:
    #    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    plt.show()

def plot_histogram(df: DataFrame, column: str, title: str = None) -> None:
    """
    Function to plot a histogram of a column of a dataframe
    :param df: pandas.DataFrame: dataframe to be used
    :param column: str: column to be used
    :param title: str: title of the plot
    :return: None
    """
    title = title if title else column
    df[column].plot(kind='hist', bins=10, figsize=(10, 4))
    plt.ylabel('Frequência')
    plt.title(title)
    plt.show()

def plot_feature_importances(importances, features):
    plt.figure(figsize=(10, 8))
    plt.barh(range(len(features)), importances, align='center')
    plt.yticks(range(len(features)), features)
    plt.xlabel('Importância da feature')
    plt.ylabel('Feature')
    plt.title('Importância das features no modelo')
    plt.show()

def plot_scatter_real_vs_pred(y_real, y_pred, title='Real vs Predito', xlabel='Real', ylabel='Predito'):
    plt.figure(figsize=(10, 4))
    plt.scatter(y_real, y_pred, c=np.abs(y_real - y_pred), cmap='coolwarm', s=10)
    plt.plot([min(y_real), max(y_real)], [min(y_real), max(y_real)], 'k--', lw=2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def roc_curve_plot(y_true, y_pred, title='Curva ROC', xlabel='Taxa de Falso Positivo', ylabel='Taxa de Verdadeiro Positivo'):
    plt.figure(figsize=(10, 4))
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    plt.plot(fpr, tpr)
    auc_value = auc(fpr, tpr)
    plt.text(0.85, 0.03, f'AUC: {auc_value:.2f}', fontsize=8)
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def plot_confusion_matrix(y_true, y_pred, title='Matriz de confusão', cmap='Blues'):
    plt.figure(figsize=(10, 4))
    sns.heatmap(confusion_matrix(y_true, y_pred), annot=True, cmap=cmap, fmt='d')
    plt.xlabel('Predito')
    plt.ylabel('Real')
    plt.title(title)
    plt.show()

def plot_specificity_pie_chart(tn: int, fp: int, title: str = "Especificidade da inferência de IRA"):
    plt.figure(figsize=(10, 4))
    plt.title(title)
    plt.pie([tn, fp], labels=['IRA', 'Falso Negativo'], autopct='%1.1f%%', startangle=140, colors=['LightBlue', '#919999'])
    plt.show()