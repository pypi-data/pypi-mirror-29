import pyspark.sql.functions as sf
import logging


def missing_values(df):
    """
    Count percentage of missing values in each columns.

    .. todo:: This code is duplicated from sanity_checks

    Args:
        df (pyspark.sql.DataFrame): A spark dataframe.

    Return:
        pyspark.sql.DataFrame: A spark dataframe containing the percentage of
            missing values for each column of the input dataframe.
    """
    missing_obs = df.agg(
        *[(1 - (sf.count(c) / sf.count('*'))).
          alias(c) for c in df.columns])
    missing_obs.show()
    return missing_obs


def describe(df, columns):
    """
    Show a descriptive stats of numerical columns of a data frame.

    .. todo:: Do not write to *stdout* because it is rude.

    Args:
        df (pyspark.sql.DataFrame): A Spark Dataframe
        columns (list): A list of columns to extract descriptive stats from.

    Return:
        pyspark.sql.DataFrame: A spark Dataframe containing descriptive
            stats of the columns arg.
    """
    stats_desc = df.describe(columns)
    values = stats_desc.first()
    stats_desc_dic = values.asDict()
    logging.info("Descriptive stats of %s \n %s", df, stats_desc_dic)
    return stats_desc
