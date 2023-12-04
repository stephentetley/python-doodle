"""
Copyright 2023 Stephen Tetley

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import duckdb


def make_ih_char_and_classes(*, con: duckdb.DuckDBPyConnection) -> None:
    con.execute(normalize_column_name_macro)
    con.execute(valuaequi_tables_query)
    for row in con.fetchall():
         qualified_name = f'{row[0]}.{row[1]}'
         ins1 = s4_ih_classes_insert(qualified_table_name=qualified_name, class_type='002')
         con.execute(ins1)
         ins2= s4_ih_char_values_insert(qualified_table_name=qualified_name, class_type='002')
         con.execute(ins2)
    con.commit()


normalize_column_name_macro = """
    CREATE OR REPLACE MACRO normalize_column_name(name) AS regexp_replace(trim(regexp_replace(lower(name), '[\W+]', ' ', 'g')), '[\W]+', '_', 'g');
    """

valuaequi_tables_query = """
    SELECT DISTINCT
        dc.schema_name,
        dc.table_name AS table_name,
    FROM duckdb_columns() dc
    WHERE dc.schema_name = 's4_raw_data'
    AND dc.table_name LIKE 'valuaequi_%';
    """

def s4_ih_classes_insert(*, qualified_table_name: str, class_type: str) -> str:
     return f"""
    INSERT INTO s4_ih_classes BY NAME
    SELECT DISTINCT
        vals.entity_id AS entity_id,
        vals.class_name AS class_name,
        '{class_type}' AS class_type,
    FROM (UNPIVOT {qualified_table_name}
    ON COLUMNS(* EXCLUDE (entity_id, class_name))
    INTO 
        NAME attribute_name
        VALUE attribute_value) vals;
    """

def s4_ih_char_values_insert(*, qualified_table_name: str, class_type: str) -> str:
     return f"""
    INSERT INTO s4_ih_char_values BY NAME
    SELECT 
        vals.entity_id AS entity_id,
        vals.class_name AS class_name,
        '{class_type}' AS class_type,
        cd.char_name AS char_name,
        IF(cd.char_type != 'NUM', vals.attribute_value, NULL) AS text_value,
        IF(cd.char_type = 'NUM', TRY_CAST(vals.attribute_value AS NUMERIC) , NULL) AS numeric_value,
    FROM (UNPIVOT {qualified_table_name}
    ON COLUMNS(* EXCLUDE (entity_id, class_name))
    INTO 
        NAME attribute_name
        VALUE attribute_value) vals
    LEFT OUTER JOIN s4_classlists.characteristic_defs cd ON normalize_column_name(cd.char_description) = vals.attribute_name AND cd.class_name = vals.class_name
    WHERE cd.class_type = '{class_type}'
    ORDER BY entity_id;
    """