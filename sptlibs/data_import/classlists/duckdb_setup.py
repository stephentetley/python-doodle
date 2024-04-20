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

def setup_tables(*, con: duckdb.DuckDBPyConnection) -> None:
    con.execute('CREATE SCHEMA IF NOT EXISTS s4_classlists;')
    con.execute(floc_characteristics_ddl)
    con.execute(equi_characteristics_ddl)
    con.execute(floc_enums_ddl)
    con.execute(equi_enums_ddl)
    con.execute(vw_refined_characteristic_defs_ddl)

floc_characteristics_ddl = """
    CREATE OR REPLACE TABLE s4_classlists.floc_characteristics(
        class_name TEXT NOT NULL,
        char_name TEXT NOT NULL,
        class_description TEXT,
        char_description TEXT,
        char_type TEXT,
        char_length INTEGER,
        char_precision INTEGER,
        PRIMARY KEY(class_name, char_name)
    );
"""

equi_characteristics_ddl = """
    CREATE OR REPLACE TABLE s4_classlists.equi_characteristics(
        class_name TEXT NOT NULL,
        char_name TEXT NOT NULL,
        class_description TEXT,
        char_description TEXT,
        char_type TEXT,
        char_length INTEGER,
        char_precision INTEGER,
        PRIMARY KEY(class_name, char_name)
    );
"""

floc_enums_ddl = """
    -- Dont bother with primary key as it is a 3-tuple.
    CREATE OR REPLACE TABLE s4_classlists.floc_enums(
        class_name TEXT NOT NULL,
        char_name TEXT NOT NULL,
        enum_value TEXT NOT NULL,
        enum_description TEXT
    );
    """

equi_enums_ddl = """
    -- Dont bother with primary key as it is a 3-tuple.
    CREATE OR REPLACE TABLE s4_classlists.equi_enums(
        class_name TEXT NOT NULL,
        char_name TEXT NOT NULL,
        enum_value TEXT NOT NULL,
        enum_description TEXT
    );
    """

vw_refined_characteristic_defs_ddl = """
 CREATE OR REPLACE VIEW s4_classlists.vw_refined_characteristic_defs AS
    SELECT 
        '002' AS class_type, 
        cd.class_name AS class_name,
        cd.char_name AS char_name, 
        cd.class_description AS class_description,
        cd.char_description AS char_description,
        cd.char_type AS s4_char_type,
        cd.char_length AS char_len,
        cd.char_precision AS char_precision,
        CASE 
            WHEN cd.char_type = 'CHAR' THEN 'TEXT'
            WHEN cd.char_type = 'NUM' AND cd.char_precision = 0 THEN 'INTEGER'
            WHEN cd.char_type = 'NUM' AND cd.char_precision > 0 THEN 'DECIMAL'
            ELSE cd.char_type
        END AS refined_char_type,
        CASE 
            WHEN cd.char_type = 'CHAR' THEN format('VARCHAR({})', cd.char_length)
            WHEN cd.char_type = 'NUM' AND cd.char_precision = 0 THEN 'INTEGER'
            WHEN cd.char_type = 'NUM' AND cd.char_precision > 0 THEN format('DECIMAL({}, {})', cd.char_length, cd.char_precision)
            ELSE cd.char_type
        END AS ddl_data_type
    FROM s4_classlists.equi_characteristics  cd;
"""    