from optel.datalake import descriptive_stats


def test_missing_values(me_df_timestamp):
    missing_obs = descriptive_stats.missing_values(me_df_timestamp)
    value = missing_obs.select("empty").collect()
    assert value[0][0] == 1.0


def test_describe(me_df_timestamp):
    columns = ['number']
    stats_desc = descriptive_stats.describe(me_df_timestamp, columns)
    value = stats_desc.select("number").collect()
    print(value)
    assert value[1][0] == '3.25'
