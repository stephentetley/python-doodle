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
    con.execute('CREATE SCHEMA IF NOT EXISTS s4_fd_raw_data;')
    con.execute(funcloc_floc1_ddl)
    con.execute(equi_equi1_ddl)
    con.execute(classfloc_classfloc1_ddl)
    con.execute(classequi_classequi1_ddl)
    con.execute(valuafloc_valuafloc1_ddl)
    con.execute(valuaequi_valuaequi1_ddl)

funcloc_floc1_ddl = """
    CREATE OR REPLACE TABLE s4_fd_raw_data.funcloc_floc1 (
        funcloc VARCHAR,
        abckzfloc VARCHAR,
        abckzi VARCHAR,
        answt VARCHAR,
        ansdt VARCHAR,
        deact VARCHAR,
        anln1_fl VARCHAR,
        anlnri VARCHAR,
        einzli VARCHAR,
        begrui VARCHAR,
        begru VARCHAR,
        cgwldt_fl VARCHAR,
        vgwldt_fl VARCHAR,
        gsbe_floc VARCHAR,
        gsberi VARCHAR,
        rbnr_floc VARCHAR,
        bukrsi VARCHAR,
        bukrsfloc VARCHAR,
        submti VARCHAR,
        baumm VARCHAR,
        submtiflo VARCHAR,
        baujj VARCHAR,
        kokrsi VARCHAR,
        kokr_floc VARCHAR,
        kost_floc VARCHAR,
        kostli VARCHAR,
        herld VARCHAR,
        waers VARCHAR,
        lvorm VARCHAR,
        txtmi VARCHAR,
        usta_floc VARCHAR,
        vtweg VARCHAR,
        spart VARCHAR,
        iequii VARCHAR,
        equi_floc VARCHAR,
        fltyp VARCHAR,
        brgew VARCHAR,
        cgaerb_fl VARCHAR,
        vgaerb_fl VARCHAR,
        iequi VARCHAR,
        invnr VARCHAR,
        liznr VARCHAR,
        stor_floc VARCHAR,
        storti VARCHAR,
        gewrkfloc VARCHAR,
        ingr_floc VARCHAR,
        rbnr_i VARCHAR,
        ingrpi VARCHAR,
        swerki VARCHAR,
        swerk_fl VARCHAR,
        serge VARCHAR,
        mapar VARCHAR,
        herst VARCHAR,
        floc_ref VARCHAR,
        cmganr_fl VARCHAR,
        vmganr_fl VARCHAR,
        typbz VARCHAR,
        objidfloc VARCHAR,
        objtyfloc VARCHAR,
        eqart VARCHAR,
        jobjn_fl VARCHAR,
        ppsidi VARCHAR,
        plnt_floc VARCHAR,
        beber_fl VARCHAR,
        beberi VARCHAR,
        wergwfloc VARCHAR,
        iwerki VARCHAR,
        posnr VARCHAR,
        trpnr1 VARCHAR,
        trpnr VARCHAR,
        msgrp VARCHAR,
        msgrpi VARCHAR,
        vkorg VARCHAR,
        vkgrp VARCHAR,
        vkbur VARCHAR,
        vkorgi VARCHAR,
        aufn_floc VARCHAR,
        aufnri VARCHAR,
        iflot_srt VARCHAR,
        einzl VARCHAR,
        groes VARCHAR,
        eqfnr VARCHAR,
        dauf_floc VARCHAR,
        daufni VARCHAR,
        inbdt VARCHAR,
        stattext VARCHAR,
        stsm_floc VARCHAR,
        ustw_floc VARCHAR,
        uswo_floc VARCHAR,
        tplkz_flc VARCHAR,
        anla_fl VARCHAR,
        tplma1 VARCHAR,
        tplma VARCHAR,
        gewei VARCHAR,
        sttxu VARCHAR,
        datbi_flo VARCHAR,
        proi_floc VARCHAR,
        proidi VARCHAR,
        cgwlen_fl VARCHAR,
        vgwlen_fl VARCHAR,
        cwaget_fl VARCHAR,
        vwaget_fl VARCHAR,
        arbplfloc VARCHAR,
        lgwidi VARCHAR,
        modeldesc VARCHAR,
        modelname VARCHAR,
        modelref VARCHAR,
        modelrver VARCHAR,
        modelver VARCHAR,
        adrnr VARCHAR,
        adrnri VARCHAR,
        geo_exist VARCHAR,
        alkey VARCHAR,
        modelext VARCHAR
    );
"""

equi_equi1_ddl = """
    CREATE OR REPLACE TABLE s4_fd_raw_data.equi_equi1 (
        equi VARCHAR,
        abck_eilo VARCHAR,
        abckzi VARCHAR,
        answt VARCHAR,
        ansdt VARCHAR,
        deact VARCHAR,
        anl1_eilo VARCHAR,
        begrui VARCHAR,
        begru VARCHAR,
        char2equi VARCHAR,
        cgwldt_eq VARCHAR,
        vgwldt_eq VARCHAR,
        gsbe_eilo VARCHAR,
        gsberi VARCHAR,
        rbnr_eeqz VARCHAR,
        zzclass VARCHAR,
        bukrsi VARCHAR,
        bukr_eilo VARCHAR,
        kmatn VARCHAR,
        baumm_eqi VARCHAR,
        subm_eeqz VARCHAR,
        baujj VARCHAR,
        kokrsi VARCHAR,
        kokr_eilo VARCHAR,
        kost_eilo VARCHAR,
        kostli VARCHAR,
        herld VARCHAR,
        waers VARCHAR,
        kunde_eq VARCHAR,
        kunde VARCHAR,
        kun1_eeqz VARCHAR,
        gewrki VARCHAR,
        lvorm_eqi VARCHAR,
        auldt_eqi VARCHAR,
        txtmi VARCHAR,
        usta_equi VARCHAR,
        vtweg VARCHAR,
        spart VARCHAR,
        kun2_eeqz VARCHAR,
        eqtyp VARCHAR,
        tplnr_i VARCHAR,
        tpln_eilo VARCHAR,
        brgew VARCHAR,
        cgaerb_eq VARCHAR,
        vgaerb_eq VARCHAR,
        invnr VARCHAR,
        eqasp VARCHAR,
        lsernr VARCHAR,
        liznr VARCHAR,
        stor_eilo VARCHAR,
        storti VARCHAR,
        eq_ltext VARCHAR,
        arbp_eeqz VARCHAR,
        ingr_eeqz VARCHAR,
        rbnr_i VARCHAR,
        ingrpi VARCHAR,
        swerki VARCHAR,
        swer_eilo VARCHAR,
        serge VARCHAR,
        mapa_eeqz VARCHAR,
        herst VARCHAR,
        cmganr_eq VARCHAR,
        vmganr_eq VARCHAR,
        mat2equi VARCHAR,
        mat2equic VARCHAR,
        mat_equ VARCHAR,
        sernr VARCHAR,
        typbz VARCHAR,
        obji_eilo VARCHAR,
        objt_equi VARCHAR,
        eqart_equ VARCHAR,
        kun3_eeqz VARCHAR,
        ppsidi VARCHAR,
        ppla_eeqz VARCHAR,
        werk_equi VARCHAR,
        bebe_eilo VARCHAR,
        beberi VARCHAR,
        wergw_eqi VARCHAR,
        iwerki VARCHAR,
        heqn_eeqz VARCHAR,
        krfkz VARCHAR,
        msgr_eilo VARCHAR,
        msgrpi VARCHAR,
        vkorg VARCHAR,
        vkgrp VARCHAR,
        vkbur VARCHAR,
        vkorgi VARCHAR,
        gernr VARCHAR,
        aufn_eilo VARCHAR,
        aufnri VARCHAR,
        groes_equ VARCHAR,
        eqfn_eilo VARCHAR,
        eqfnri VARCHAR,
        dauf_eilo VARCHAR,
        daufni VARCHAR,
        inbdt VARCHAR,
        stattext VARCHAR,
        stsm_equi VARCHAR,
        ustw_equi VARCHAR,
        uswo_equi VARCHAR,
        lager_eqi VARCHAR,
        anl2_eilo VARCHAR,
        hequ_eeqz VARCHAR,
        tidn_eeqz VARCHAR,
        gewei VARCHAR,
        data_eeqz VARCHAR,
        datb_eeqz VARCHAR,
        datbi_eil VARCHAR,
        elief_eqi VARCHAR,
        proi_eilo VARCHAR,
        proidi VARCHAR,
        cgwlen_eq VARCHAR,
        vgwlen_eq VARCHAR,
        cwaget_eq VARCHAR,
        vwaget_eq VARCHAR,
        arbp_eilo VARCHAR,
        aineq_ind VARCHAR,
        modelid VARCHAR,
        ain_equnr VARCHAR,
        adrnr VARCHAR,
        adrnri VARCHAR,
        copy_from VARCHAR,
        instime VARCHAR,
        insdate VARCHAR,
        frcrmv VARCHAR,
        frcfit VARCHAR,
        funcid VARCHAR,
        geo_exist VARCHAR,
        iuid_type VARCHAR,
        uii_agen VARCHAR,
        is_model VARCHAR,
        ppeguid VARCHAR,
        uii_plant VARCHAR,
        uii VARCHAR
    );
"""

classfloc_classfloc1_ddl = """
    CREATE OR REPLACE TABLE s4_fd_raw_data.classfloc_classfloc1 (
        funcloc VARCHAR,
        class VARCHAR,
        classtype VARCHAR,
        clint VARCHAR,
        clstatus1 VARCHAR,
        lkenz_cla VARCHAR
    );
"""

classequi_classequi1_ddl = """
    CREATE OR REPLACE TABLE s4_fd_raw_data.classequi_classequi1 (
        equi VARCHAR,
        class VARCHAR,
        classtype VARCHAR,
        clint VARCHAR,
        clstatus1 VARCHAR,
        lkenz_cla VARCHAR
    );
"""

valuafloc_valuafloc1_ddl = """
    CREATE OR REPLACE TABLE s4_fd_raw_data.valuafloc_valuafloc1 (
        funcloc VARCHAR,
        ataw1 VARCHAR,
        atawe VARCHAR,
        ataut VARCHAR,
        charid VARCHAR,
        atnam VARCHAR,
        atwrt VARCHAR,
        classtype VARCHAR,
        atcod VARCHAR,
        atvglart VARCHAR,
        textbez VARCHAR,
        atzis VARCHAR,
        valcnt VARCHAR,
        atimb VARCHAR,
        atsrt VARCHAR,
        atflv VARCHAR,
        atflb VARCHAR
    );
"""

valuaequi_valuaequi1_ddl = """
    CREATE OR REPLACE TABLE s4_fd_raw_data.valuaequi_valuaequi1 (
        equi VARCHAR,
        ataw1 VARCHAR,
        atawe VARCHAR,
        ataut VARCHAR,
        charid VARCHAR,
        atnam VARCHAR,
        atwrt VARCHAR,
        classtype VARCHAR,
        atcod VARCHAR,
        atvglart VARCHAR,
        textbez VARCHAR,
        atzis VARCHAR,
        valcnt VARCHAR,
        atimb VARCHAR,
        atsrt VARCHAR,
        atflv VARCHAR,
        atflb VARCHAR
    );
"""
