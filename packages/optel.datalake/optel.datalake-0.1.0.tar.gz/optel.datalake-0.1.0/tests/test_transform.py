from optel.datalake import transform
from optel.datalake import descriptive_stats


def test_convert_ms_timestamp(me_df_timestamp):
    df_transformed = transform.convert_ms_timestamp(
        me_df_timestamp, ["date", "date2"])
    test_date = df_transformed.select("date").collect()[0][0]
    assert(str(test_date) == "2018-02-01 10:16:17")


def test_missing_values(me_df_timestamp):
    df = descriptive_stats.missing_values(me_df_timestamp)
    null_value = df.select("empty").collect()[0][0]
    assert(null_value == 1.0)
