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

## Setup tables initially (ddl is autogenerated from examples)

def setup_views(*, con: duckdb.DuckDBPyConnection) -> None:
    con.execute('CREATE SCHEMA IF NOT EXISTS s4_sai_mapping;')
    con.execute(vw_s4_level1_worklist_ddl)
    con.execute(vw_level1_mapping_ddl)
    con.execute(vw_ai2_sites_ddl)
    con.execute(vw_ai2_installations_ddl)
    con.execute(vw_ai2_installation_type_codes_ddl)
    con.execute(vw_ai2_level1_kids_ddl)
    con.execute(vw_s4_level1_kids_ddl)
    con.execute(vw_level1_parent_child_results_ddl)
    con.execute(vw_level1_children_report_ddl)

vw_s4_level1_worklist_ddl = """
    CREATE OR REPLACE VIEW s4_sai_mapping.vw_s4_level1_worklist AS 
    SELECT *
    FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY t1.functional_location) AS row_number
    FROM sai_raw_data.s4_level_1_2 t1
    ) t
    WHERE t.row_number = 1
    AND t.functloccategory = 1
"""

vw_level1_mapping_ddl = """
    CREATE OR REPLACE VIEW s4_sai_mapping.vw_level1_mapping AS 
    SELECT DISTINCT 
        t.ai2_sitereference AS ai2_site_id,
        t.site_name AS ai2_site_name,
        t.s_4_hana_floc_lvl1_code AS s4_site_id,
        t.s_4_hana_floc_description AS s4_site_name,
    FROM sai_raw_data.site_mapping t;
"""

vw_ai2_sites_ddl = """
    CREATE OR REPLACE VIEW s4_sai_mapping.vw_ai2_sites AS 
    SELECT DISTINCT 
        ai2.sitereference as site_reference,
        ai2.sitecommonname as common_name,
    FROM sai_raw_data.ai2_data ai2
    WHERE ai2.siteassetid IS NOT NULL;
"""

vw_ai2_installations_ddl = """
    CREATE OR REPLACE VIEW s4_sai_mapping.vw_ai2_installations AS 
    (SELECT DISTINCT
        ai2.installationreference AS sai_num,
        ai2.installationcommonname AS common_name,
        ai2.installationstatus AS status,
        ai2.installationtypecode AS type_code,
        ai2.sitereference AS site_id,
    FROM sai_raw_data.ai2_data ai2
    WHERE ai2.siteassetid IS NOT NULL
    AND ai2.subinstallationassetid IS NULL)
    UNION
    (SELECT DISTINCT
        ai2.subinstallationreference AS sai_num,
        ai2.subinstallationcommonname AS common_name,
        ai2.subinstallationstatus AS status,
        ai2.subinstallationtypecode AS type_code,
        ai2.sitereference AS site_id,
    FROM sai_raw_data.ai2_data ai2
    WHERE ai2.siteassetid IS NOT NULL
    AND ai2.subinstallationassetid IS NOT NULL)
"""

vw_ai2_installation_type_codes_ddl = """
    CREATE OR REPLACE VIEW s4_sai_mapping.vw_ai2_installation_type_codes AS
    SELECT DISTINCT * FROM (
        (SELECT 
            t1.sai_num AS sai_num,
            t1.common_name AS common_name,
            t1.type_code AS type_code,
        FROM s4_sai_mapping.vw_ai2_installations t1)
        UNION
        (SELECT 
            t2.site_reference AS sai_num,
            t2.common_name AS common_name,
            'SITE' AS type_code,
        FROM s4_sai_mapping.vw_ai2_sites t2)
    );
"""

vw_ai2_level1_kids_ddl = """
    CREATE OR REPLACE VIEW s4_sai_mapping.vw_ai2_level1_kids AS
    (SELECT DISTINCT 
        sites.site_reference AS site_id,
        sites.common_name AS site_description,
        insts.sai_num AS child_id,
        s_to_a.s4_site_id AS s4_site_id,
        insts.status AS child_status,
    FROM s4_sai_mapping.vw_ai2_sites sites
    JOIN s4_sai_mapping.vw_ai2_installations insts ON insts.site_id = sites.site_reference
    JOIN s4_sai_mapping.vw_level1_mapping s_to_a ON s_to_a.ai2_site_id = sites.site_reference)
    UNION 
    (SELECT DISTINCT 
        sites.site_reference AS site_id,
        sites.common_name AS site_description,
        sites.site_reference AS child_id,
        s_to_a.s4_site_id AS s4_site_id,
        'SITE (no status)' AS child_status,
    FROM s4_sai_mapping.vw_ai2_sites sites
    JOIN s4_sai_mapping.vw_level1_mapping s_to_a ON s_to_a.ai2_site_id = sites.site_reference)
    ORDER BY site_description, site_id
"""

vw_s4_level1_kids_ddl = """
    CREATE OR REPLACE VIEW s4_sai_mapping.vw_s4_level1_kids AS
    SELECT DISTINCT 
        t.functional_location AS site_floc,
        t.description_of_functional_location AS site_description,
        t.ai2_aib_reference AS child_id,
    FROM sai_raw_data.s4_level_1_2 t
    WHERE t.functloccategory = 1
"""

vw_level1_parent_child_results_ddl = """
    CREATE OR REPLACE VIEW s4_sai_mapping.vw_level1_parent_child_results AS 
        (SELECT stbl.* FROM
            (SELECT DISTINCT
                t1.s4_site_id AS parent_id,
                t1.child_id AS child_id,
                'SAME' as status,
            FROM s4_sai_mapping.vw_ai2_level1_kids t1
            INTERSECT
            SELECT DISTINCT
                t2.site_floc AS parent_id,
                t2.child_id AS child_id,
                'SAME' as status,
            FROM s4_sai_mapping.vw_s4_level1_kids t2) stbl
        WHERE stbl.parent_id IS NOT NULL)
        UNION
        (SELECT mtbl.* FROM 
            (SELECT DISTINCT
                t1.s4_site_id AS parent_id,
                t1.child_id AS child_id,
                'MISSING' as status,
            FROM s4_sai_mapping.vw_ai2_level1_kids t1
            EXCEPT
            SELECT DISTINCT
                t2.site_floc AS parent_id,
                t2.child_id AS child_id,
                'MISSING' as status,
            FROM s4_sai_mapping.vw_s4_level1_kids t2) mtbl
        WHERE mtbl.parent_id IS NOT NULL)
        UNION
        (SELECT atbl.* FROM 
            (SELECT DISTINCT
                t2.site_floc AS parent_id,
                t2.child_id AS child_id,
                'ALIEN' as status,
            FROM s4_sai_mapping.vw_s4_level1_kids t2    
            EXCEPT
            SELECT DISTINCT
                t1.s4_site_id AS parent_id,
                t1.child_id AS child_id,
                'ALIEN' as status,
            FROM s4_sai_mapping.vw_ai2_level1_kids t1) atbl
        WHERE atbl.parent_id IS NOT NULL)
    ORDER BY parent_id, child_id;
"""

vw_level1_children_report_ddl = """
    CREATE OR REPLACE VIEW s4_sai_mapping.vw_level1_children_report AS 
    WITH cte_child_status AS (
        (SELECT 
            t1.child_id AS child_id,
            first(t1.child_status) AS asset_status,
        FROM s4_sai_mapping.vw_ai2_level1_kids t1
        GROUP BY t1.child_id)
        )
    (SELECT 
        t.functional_location AS funcloc,
        t.description_of_functional_location AS floc_name,
        ans.child_id AS child_id,
        tyco.common_name AS child_name,
        ans.status AS data_status,
        tyco.type_code AS type_code,
        IF (tyco.type_code NOT IN ('ADT', 'BIF', 'BUI', 'CRR', 'CRS', 'CRT', 'CSP', 'IVR', 'IVS', 'LMP', 'SPR', 'STR', 'STU', 'WFM'), '', 'type_code not migrated') AS type_code_migrated,
        cte.asset_status AS child_asset_status,
    FROM s4_sai_mapping.vw_s4_level1_worklist AS t
    JOIN s4_sai_mapping.vw_level1_parent_child_results ans ON ans.parent_id = t.functional_location 
    JOIN s4_sai_mapping.vw_ai2_installation_type_codes tyco ON tyco.sai_num = ans.child_id 
    JOIN cte_child_status cte ON cte.child_id = ans.child_id)
    ORDER BY funcloc, ans.child_id;
"""
