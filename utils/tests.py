import pytest
import parser

def test_type_1():
    test_data =[" 1996  6 7 1325 29.2 L  59.846   5.130 12.0F TES 12 .60 1.9LTES 2.2CTES 2.0LNAO1",
         " 1996  6 7 1325 30.5 L  59.763   5.396 29.2  NAO  2 1.0                 2.0LNAO1"]
    expected = {"DateTime": "1996-06-07T13:25:29.200000", "Distance Indicator": "L", "Event ID": " ", 'Lat': 59.846, 'Long': 5.13,'Depth': 12.0, 'Agency': 'TES', 'Magnitudes': [{'M': ' 1.9', 'T': 'L'},{'M': ' 2.2', 'T': 'C'},{'M': ' 2.0', 'T': 'L'},{'M': ' 2.0', 'T': 'L'}]}

    _ret = parser.parse_type_1(test_data)
    for (k,v) in _ret.items():
        assert _ret[k] == expected[k]

def test_type_3():
    test_data = [" OP: CVUA-RM/RC                                                                3",
" STATUS: OK    SENTIDO                                                         3",
" SENTIDO: II/III  -Pico: S. Caetano                                            3",
" PUB: NAO                                                                      3",
" WEB: SIM                                                                      3",
" OBS: Por ordem do CT nao foi emitido novo comunicado                          3",
" OBS: Sismo sobreposto                                                         3",
" REGIAO: Pico,VZ14,SZ06,FE95 405                                               3"]

    _ret = parser.parse_type_3(test_data)
    assert len(_ret["Comments"]) == 8

def test_type_6():
    test_data = [" 1996-06-03-2002-18S.TEST__012                                                 6",
          " 1996-06-03-1917-52S.TEST__002                                                 6"]
    expected = {"Wave": ["1996-06-03-2002-18S.TEST__012", "1996-06-03-1917-52S.TEST__002"]}

    _ret = parser.parse_type_6(test_data)
    for (k,v) in _ret.items():
        assert _ret[k] == expected[k]

def test_type_i():
    test_data = [" ACTION:SPL 08-10-02 10:19 OP:jh   STATUS:               ID:19960603195540     I"]
    expected = {"Action": "SPL", "Action Extra": {"Date": '2008-10-02T10:19:00', "OP": "jh", "Status": "", "ID":19960603195540}}

    _ret = parser.parse_type_i(test_data)
    for (k,v) in _ret.items():
        assert _ret[k] == expected[k]

def test_type_e():
    test_data =[" GAP=348        2.88     999.9   999.9999.9 -0.1404E+08 -0.3810E+08  0.1205E+09E"]
    expected = {"Gap": 348, "Origin": 2.88, "Error_lat": 999.9, "Error_long": 999.9, "Error_depth": 999.9, "Cov_xy": -14040000.0, "Cov_xz": -38100000.0, "Cov_yz": 120500000.0}

    _ret = parser.parse_type_e(test_data)
    for (k,v) in _ret.items():
        assert _ret[k] == expected[k]

