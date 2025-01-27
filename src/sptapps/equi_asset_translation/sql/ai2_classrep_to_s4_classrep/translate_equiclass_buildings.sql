-- 
-- Copyright 2025 Stephen Tetley
-- 
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
-- 
-- http://www.apache.org/licenses/LICENSE-2.0
-- 
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
-- 

INSERT OR REPLACE INTO s4_classrep.equiclass_kiskki BY NAME
SELECT
    t.equipment_id AS equipment_id,  
    null AS location_on_site,
    udf_size_to_millimetres('METRES', t._kiosk_base_height_m) AS kisk_base_height_mm,
    udf_size_to_millimetres('METRES', t._kiosk_depth_m) AS kisk_depth_mm,
    udf_size_to_millimetres('METRES', t._kiosk_height_m) AS kisk_height_mm,
    udf_size_to_millimetres('METRES', t._kiosk_width_m) AS kisk_width_mm,
    t._kiosk_material AS kisk_material,
FROM ai2_classrep.equiclass_kiosk t;
