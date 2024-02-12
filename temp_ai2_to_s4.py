# polars is in my (base) env

from sptlibs.ai2_eav.gen_duckdb import GenDuckdb
from sptlibs.xlsx_source import XlsxSource

parents_source = XlsxSource('g:/work/2024/ai2_to_s4/ai2-magflow-meter-parents-export.xlsx', 'Sheet1')


gen_duckdb = GenDuckdb(duckdb_output_path='g:/work/2024/ai2_to_s4/magflow.db')
gen_duckdb.add_parents_source(source=parents_source)
gen_duckdb.gen_duckdb()


# df = pl.read_excel(
#     source="g:/work/2024/ai2_to_s4/ai2-magflow-meter-parents-export.xlsx",
#     sheet_name="Sheet1",
# )

# print(df)

# def get_parent_data(df: pl.DataFrame) -> pl.DataFrame:
#     df1 = df.select(pl.col("Reference", "Common Name"))
#     df2 = df1.rename({"Reference" : "sai_num", "Common Name": "common_name"})
#     return df2


# con = duckdb.connect('g:/work/2024/ai2_to_s4/magflow.db', read_only=False)
# con.execute("CREATE SCHEMA IF NOT EXISTS ai2_raw_data;")
# polars_import_utils.duckdb_import_sheet(parents_source, table_name='ai2_raw_data.parent_flocs', con=con, df_trafo=get_parent_data)

# con.close()

