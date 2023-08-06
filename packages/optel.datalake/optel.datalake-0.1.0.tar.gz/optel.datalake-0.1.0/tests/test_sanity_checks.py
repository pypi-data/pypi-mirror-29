from optel.datalake import sanity_checks
import pyspark.sql.functions as sf


def test_real_dups(duplicates_df):
    dedup_df = sanity_checks.real_dups(duplicates_df)
    dedup_df.show()
    nb_rows = dedup_df.count()
    nb_distinct = dedup_df.distinct().count()
    nb_dups = nb_rows - nb_distinct
    assert nb_dups == 0


def test_empty_columns(me_df_timestamp):
    df_no_empty_cols = sanity_checks.empty_columns(me_df_timestamp)
    missing_obs = df_no_empty_cols.agg(*[(1 - (sf.count(c) / sf.count('*'))).
                                         alias(c) for c in df_no_empty_cols.columns])
    values = missing_obs.first()
    dict_values = values.asDict()
    assert 1.0 not in dict_values.values()
