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

s4_fd_classes_ddl = """
    -- Same table for classequi and classfloc
    CREATE OR REPLACE TABLE s4_fd_classes(
        entity_id TEXT NOT NULL,
        class_name TEXT NOT NULL,
        class_type TEXT,
    );
    """

s4_fd_char_values_ddl = """
    -- No primary key
    CREATE OR REPLACE TABLE s4_fd_char_values(
        entity_id TEXT NOT NULL,
        char_name TEXT NOT NULL,
        char_desc TEXT,
        char_text_value TEXT,
        class_type TEXT,
        int_counter_value TEXT,
        value_from DECIMAL(26, 6),
        value_to DECIMAL(26,6),
    );
"""

vw_fd_equi_decimal_values_ddl = """
    CREATE OR REPLACE VIEW vw_fd_equi_decimal_values AS
    SELECT 
        sfcv.entity_id AS entity_id,
        sfcv.class_type AS class_type,
        sem.object_type AS object_type,
        scd.char_precision AS decimal_precision,
        sfc.class_name AS class_name,
        sfcv.char_name AS char_name,
        sfcv.int_counter_value AS int_counter_value,
        CAST(sfcv.value_from AS DECIMAL(26,6)) AS decimal_value,
    FROM s4_fd_char_values sfcv
    JOIN s4_equipment_masterdata sem ON sem.equi_id = sfcv.entity_id
    JOIN s4_fd_classes sfc ON sfc.entity_id = sfcv.entity_id
    JOIN s4_characteristic_defs scd ON scd.char_name = sfcv.char_name AND scd.class_name = sfc.class_name AND scd.class_type = sfcv.class_type
    WHERE scd.char_type = 'NUM'
    AND scd.char_precision > 0;
    """

vw_fd_equi_integer_values_ddl = """
    CREATE OR REPLACE VIEW vw_fd_equi_integer_values AS
    SELECT 
        sfcv.entity_id AS entity_id,
        sfcv.class_type AS class_type,
        sem.object_type AS object_type,
        sfc.class_name AS class_name,
        sfcv.char_name AS char_name,
        sfcv.int_counter_value AS int_counter_value,
        CAST(sfcv.value_from AS INTEGER) AS integer_value,
    FROM s4_fd_char_values sfcv         -- base table
    JOIN s4_equipment_masterdata sem ON sem.equi_id = sfcv.entity_id
    JOIN s4_fd_classes sfc ON sfc.entity_id = sfcv.entity_id
    JOIN s4_characteristic_defs scd ON scd.char_name = sfcv.char_name AND scd.class_name = sfc.class_name AND scd.class_type = sfcv.class_type
    WHERE scd.char_type = 'NUM'
    AND scd.char_precision = 0;
    """

vw_fd_equi_text_values_ddl = """
    CREATE OR REPLACE VIEW vw_fd_equi_text_values AS
    SELECT 
        sfcv.entity_id AS entity_id,
        sfcv.class_type AS class_type,
        sem.object_type AS object_type,
        sfc.class_name AS class_name,
        sfcv.char_name AS char_name,
        sfcv.int_counter_value AS int_counter_value,
        sfcv.char_text_value AS text_value,
    FROM s4_fd_char_values sfcv         -- base table
    JOIN s4_equipment_masterdata sem ON sem.equi_id = sfcv.entity_id
    JOIN s4_fd_classes sfc ON sfc.entity_id = sfcv.entity_id
    JOIN s4_characteristic_defs scd ON scd.char_name = sfcv.char_name AND scd.class_name = sfc.class_name AND scd.class_type = sfcv.class_type
    WHERE scd.char_type = 'CHAR';
    """

def query_sqlite_schema_tables(*, sqlite_path: str) -> str:
    return f"""
    SELECT 
        name
    FROM 
        sqlite_scan('{sqlite_path}', 'sqlite_schema')
    WHERE 
        type ='table' AND 
        name NOT LIKE 'sqlite_%';
    """

def s4_funcloc_masterdata_insert(*, sqlite_path: str) -> str: 
    return f"""
    INSERT INTO s4_funcloc_masterdata BY NAME
    SELECT 
        f.funcloc AS functional_location,
        f.adrnr AS address_ref,
        f.bukrsfloc AS company_code,
        TRY_CAST(f.baumm AS INTEGER) AS construction_month,
        TRY_CAST(f.baujj AS INTEGER) AS construction_year,
        f.kokr_floc AS controlling_area,
        f.kost_floc AS cost_center,
        f.txtmi AS description,
        f.usta_floc AS user_status,
        f.fltyp AS category,
        IF(f.iequi = 'X', true, false) AS installation_allowed,
        f.stor_floc AS location,
        f.gewrkfloc AS main_work_center,
        f.swerk_fl AS maintenance_plant,
        f.eqart AS object_type,
        f.jobjn_fl AS object_number,
        f.plnt_floc AS planning_plant,
        f.beber_fl AS plant_section,
        TRY_CAST(f.posnr AS INTEGER) AS display_position,
        IF(f.inbdt IS NOT NULL, strptime(f.inbdt, '%d.%m.%Y'), NULL) AS startup_date,
        f.tplkz_flc AS structure_indicator,
        f.tplma AS superior_funct_loc,
    FROM sqlite_scan('{sqlite_path}', 'funcloc_floc1') f;
    """

def s4_equipment_masterdata_insert(*, sqlite_path: str) -> str: 
    return f"""
    INSERT INTO s4_equipment_masterdata BY NAME
    SELECT 
        e.equi AS equi_id,
        e.rbnr_eeqz AS catalog_profile,
        e.bukr_eilo AS company_code,
        e.baumm_eqi AS construction_month,
        e.baujj AS construction_year,
        e.kokr_eilo AS controlling_area,
        e.kost_eilo AS cost_center,
        e.txtmi AS description,
        e.tpln_eilo AS functional_location,
        e.brgew AS gross_weight,
        e.stor_eilo AS location,
        e.arbp_eeqz AS main_work_center,
        e.swer_eilo AS maintenance_plant,
        e.serge AS serial_number,
        e.mapa_eeqz AS manufact_part_number,
        e.herst AS manufacturer,
        e.typbz AS model_number,
        e.eqart_equ AS object_type,
        e.ppla_eeqz AS planning_plant,
        e.bebe_eilo AS plant_section,
        e.heqn_eeqz AS display_position,
        IF(e.inbdt IS NOT NULL, strptime(e.data_eeqz, '%d.%m.%Y'), NULL) AS startup_date,
        e.hequ_eeqz AS  superord_id,
        e.tidn_eeqz AS technical_ident_number,
        e.gewei AS unit_of_weight,
        IF(e.data_eeqz IS NOT NULL, strptime(e.data_eeqz, '%d.%m.%Y'), NULL) AS valid_from,
        e.adrnr AS address_ref
    FROM sqlite_scan('{sqlite_path}', 'equi_equi1') e;
    """

def s4_fd_classfloc_insert(*, sqlite_path: str) -> str: 
    return f"""
    INSERT INTO s4_fd_classes BY NAME
    SELECT 
        c.funcloc AS entity_id,
        c.class AS class_name,
        c.classtype AS class_type
    FROM sqlite_scan('{sqlite_path}', 'classfloc_classfloc1') c;
    """

def s4_fd_classequi_insert(*, sqlite_path: str, ) -> str: 
    return f"""
    INSERT INTO s4_fd_classes BY NAME
    SELECT 
        c.equi AS entity_id,
        c.class AS class_name,
        c.classtype AS class_type
    FROM sqlite_scan('{sqlite_path}', 'classequi_classequi1') c;
    """

def s4_fd_char_valuafloc_insert(*, sqlite_path: str) -> str: 
    return f"""
    INSERT INTO s4_fd_char_values BY NAME
    SELECT 
        v.funcloc AS entity_id,
        v.charid AS char_name,
        v.atnam AS char_desc,
        v.atwrt AS char_text_value,
        v.classtype AS class_type,
        v.valcnt AS int_counter_value,
        v.atflv AS value_from,
        v.atflb AS value_to
    FROM sqlite_scan('{sqlite_path}', 'valuafloc_valuafloc1') v;
    """

def s4_fd_char_valuaequi_insert(*, sqlite_path: str) -> str: 
    return f"""
    INSERT INTO s4_fd_char_values BY NAME
    SELECT 
        v.equi AS entity_id,
        v.charid AS char_name,
        v.atnam AS char_desc,
        v.atwrt AS char_text_value,
        v.classtype AS class_type,
        v.valcnt AS int_counter_value,
        v.atflv AS value_from,
        v.atflb AS value_to
    FROM sqlite_scan('{sqlite_path}', 'valuaequi_valuaequi1') v;
    """

def s4_classlists_table_copy(*, classlists_duckdb_path: str) -> str: 
    return f"""
        ATTACH '{classlists_duckdb_path}' AS classlists_db;
        INSERT INTO s4_characteristic_defs SELECT * FROM classlists_db.s4_characteristic_defs;
        INSERT INTO s4_enum_defs SELECT * FROM classlists_db.s4_enum_defs;
        DETACH classlists_db;
    """
