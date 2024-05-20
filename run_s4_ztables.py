"""
Copyright 2024 Stephen Tetley

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
import sptlibs.cmdline_utils as cmdline_utils
from sptlibs.xlsx_source import XlsxSource
import sptlibs.data_import.ztables.duckdb_import as duckdb_import


def main(): 
    config = cmdline_utils.get_asset_data_config().get('s4_ztables', None)
    if config:
        eqobjl_src = cmdline_utils.get_expanded_path('eqobjl_src', config)
        flocdes_src = cmdline_utils.get_expanded_path('flocdes_src', config)
        floobjl_src = cmdline_utils.get_expanded_path('floobjl_src', config)
        manuf_model_src = cmdline_utils.get_expanded_path('manuf_model_src', config)
        objtype_src = cmdline_utils.get_expanded_path('objtype_src', config)
        output_path = cmdline_utils.get_expanded_path('s4_ztables_outfile', config)

        conn = duckdb.connect(database=output_path)
        duckdb_import.init(con=conn)
        duckdb_import.import_eqobjl(XlsxSource(eqobjl_src, 'Sheet1'), con=conn)
        duckdb_import.import_flocdes(XlsxSource(flocdes_src, 'Sheet1'), con=conn)
        duckdb_import.import_floobjl(XlsxSource(floobjl_src, 'Sheet1'), con=conn)
        duckdb_import.import_manuf_model(XlsxSource(manuf_model_src, 'Sheet1'), con=conn)
        duckdb_import.import_objtype_manuf(XlsxSource(objtype_src, 'Sheet1'), con=conn)
        conn.close()
        print(f"Done - created: {output_path}")

main()


