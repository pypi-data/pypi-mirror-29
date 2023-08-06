from pyspark.sql import SparkSession


def get_spark(name):
    """
    Get a Spark session by name.

    The Spark session is reused if it already exists.

    Args:
        name (str): The name of the Spark session.

    Returns:
        pyspark.sql.SparkSession: Ready to use session.
    """
    spark = SparkSession \
        .builder \
        .appName(name) \
        .getOrCreate()
    return spark


def default_spark():
    """
    Provide the default Spark session.

    Returns:
        pyspark.sql.SparkSession: A Spark session named *Optel Data Lake*.
    """
    return get_spark('Optel Data Lake')
