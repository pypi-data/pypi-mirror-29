from pyspark.sql import functions as sf
from pyspark.sql.types import DecimalType
from tzlocal import get_localzone


def convert_ms_timestamp(table, date_columns):
    """
    Convert unix timestamp (ms) to date.

    Args:
        table (str): Spark dataframe
        date_columns (list): A list of columns to convert
    """
    localtz = get_localzone()
    for date_column in date_columns:
        df_tmp = table.withColumn(
            date_column, (sf.col(date_column)/1000).cast(DecimalType(12, 0)))
        df_tmp = df_tmp.withColumn(
            date_column, df_tmp[date_column].cast('timestamp'))
        df_tmp = df_tmp.withColumn(date_column, sf.to_utc_timestamp(
            df_tmp[date_column], str(localtz)))
        table = df_tmp
    return df_tmp


def find_key(dic, val):
    """
    Return the key of dictionary dic given the value.

    Args:
        dic (dict): A dictionary.
        val (str): A string to search for in the dictionary.

    Returns:
        list: A list of keys (columns) containing a
            specified value (val).
    """
    empty_cols = []
    for key, value in dic.items():
        if value == val:
            empty_cols.append(key)
        else:
            pass
    return empty_cols
