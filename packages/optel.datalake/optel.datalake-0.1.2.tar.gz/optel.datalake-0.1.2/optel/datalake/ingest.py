from optel.datalake.config.sparksession import default_spark


def load_sql_tables(database, tables, server, username, password, spark=None):
    """
    Load one table or a table schema from SQL server.

    Args:
        database (str): Database from which to fetch tables.
        tables (list): A list of tables to fetch.
        server (str): The server from which to fetch data.
        username (str): The username used to connect to the server.
        password (str): The password of the aforementioned username.
        spark (pyspark.sql.SparkSession): Optional Spark session to use.  This
            will default to the session provided by
            :func:`optel.datalake.config.sparksession.default_spark`

    Returns:
        dict: Data frames keyed by table name
    """
    spark = spark or default_spark()
    dic_of_df = dict()
    for table in tables:
        spark_df = spark.read \
            .format("jdbc") \
            .option("url", server) \
            .option("databaseName", database) \
            .option("dbtable", table) \
            .option("user", username) \
            .option("password", password) \
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
            .option("header", "true") \
            .option("nullValue", "0") \
            .option("encrypt", "false") \
            .load()
        dic_of_df[table] = spark_df

    return dic_of_df


def write_to_elastic(table, destination, nodes, username, password):
    """
    Write table to Elastic search.

    Args:
        table (pyspark.sql.DataFrame): The name of the spark dataframe that
            will be written to Elastic.
        destination (str): The name of the index under which the dataframe
            will be written.
        nodes (str): Elastic search nodes where to write table.
        username (str): Elasticsearch user with write access.
        password (str): Elasticsearch user password.
    """
    resource_name = '{}/table'.format(destination)
    table.write \
        .format("org.elasticsearch.spark.sql") \
        .option("es.mapping.date.rich", "true") \
        .mode("overwrite") \
        .option("es.index.auto.create", "true") \
        .option("es.resource", resource_name) \
        .option("es.nodes", nodes) \
        .option("es.net.ssl.protocol", "true") \
        .option("es.nodes.wan.only", "true") \
        .option("es.net.http.auth.user", username) \
        .option("es.field.read.empty.as.null", "yes") \
        .option("es.net.http.auth.pass", password) \
        .save()


def read_from_elastic(index, nodes, username, password, spark=None):
    """
    Read a table from Elasic Search.

    Args:
        index (str): The name of the elastic search index to read.
        spark (pyspark.sql.SparkSession): Optional Spark session to use.  This
            will default to the session provided by
            :func:`optel.datalake.config.sparksession.default_spark`
    """
    spark = spark or default_spark()
    loaded_es_index = spark.read \
        .format("org.elasticsearch.spark.sql") \
        .option("es.nodes", nodes) \
        .option("es.net.ssl.protocol", "true") \
        .option("es.nodes.wan.only", "true") \
        .option("es.net.http.auth.user", username) \
        .option("es.net.http.auth.pass", password) \
        .load(index + "/table")
    return loaded_es_index


def write_csv(df, destination):
    """
    Write a csv table to a destination.

    Args:
        df (pyspark.sql.DataFrame): TODO
        destination (str): CSV file path.
    """
    df.write \
        .format("csv") \
        .mode("overwrite") \
        .option("header", "true") \
        .option("inferSchema", "true")\
        .csv(destination)


def write_parquet(df, destination):
    """
    Write a Spark dataframe to a parket file.

    Args:
        df (pyspark.sql.DataFrame): The name of the Spark dataframe.
        destination (str): The destination file path where to write the
            dataframe *parquet* file.
    """
    df.write \
        .mode("overwrite") \
        .parquet(destination)


def read_csv(source, spark=None):
    spark = spark or default_spark()
    df = spark.read \
        .format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .load(source)
    return df


def read_parquet(source, spark=None):
    """
    Read parquet files into a spark dataframe.

    Args:
        source (str): Source *parquet* file.
        spark (pyspark.sql.SparkSession): Optional Spark session to use.  This
            will default to the session provided by
            :func:`optel.datalake.config.sparksession.default_spark`

    Returns:
        pyspark.sql.DataFrame: Properly initialized data frame.
    """
    spark = spark or default_spark()
    result_df = spark.read.parquet(source)
    return result_df


def get_df_from_source(base_source, tables):
    """
    Make data frames from a folder of *parquet* files.

    Args:
        base_source (str): Path to the folder containing *parquet* files.
        tables: List of parquet file names.

    Returns:
        dict: Mapping of :class:`pyspark.sql.DataFrame` objects indexed by
            file name.
    """
    dic_of_df = {}
    for table in tables:
        source = (base_source + table)
        dic_of_df[table] = read_parquet(source)
    dic_of_df[table].show(n=2)
    return dic_of_df
