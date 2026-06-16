"""Tests for column type/role inference."""

from pathlib import Path

from app.profiler import profile_columns, read_csv

CSV = """Company,Country,Founded,Description,Website
Isar Aerospace,Germany,2018,Spectrum small launcher built in Ottobrunn near Munich,isaraerospace.com
PLD Space,Spain,2011,Miura 1 suborbital and Miura 5 orbital launch vehicles,pldspace.com
Avio,Italy,,Vega-C operator and lead contractor for European solid motors,avio.com
Orbex,UK,2015,Prime microlauncher developed in Forres Scotland,orbex.space
RFA,Germany,2018,RFA ONE microlauncher built by the OHB group in Augsburg,rfa.space
Latitude,Spain,2019,Zephyr microlauncher developed for small satellite payloads,latitude.aero
HyImpulse,Germany,2018,Hybrid paraffin and liquid oxygen suborbital launch systems,hyimpulse.de
Sidereus,Italy,2019,Small reusable single stage to orbit launch vehicle EOS,sidereus.space
Skyrora,UK,2017,Skyrora XL orbital launch vehicle and hybrid space tug,skyrora.com
"""


def _profile(tmp_path: Path, text: str):
    f = tmp_path / "sample.csv"
    f.write_text(text)
    header, rows = read_csv(f)
    return {p.name: p for p in profile_columns(header, rows)}


def test_roles_and_types(tmp_path):
    cols = _profile(tmp_path, CSV)

    assert cols["Company"].role == "title"
    assert cols["Country"].type == "categorical"
    assert cols["Country"].role == "facet"
    assert cols["Founded"].type == "year"
    assert cols["Founded"].role == "metric"
    assert cols["Description"].type == "long_text"
    assert cols["Website"].type == "url"
    assert cols["Website"].role == "link"


def test_fill_rate_and_year_range(tmp_path):
    cols = _profile(tmp_path, CSV)

    # Founded is filled for 8 of 9 rows (Avio is blank).
    assert round(cols["Founded"].fill_rate, 3) == 0.889
    assert cols["Founded"].min == 2011.0
    assert cols["Founded"].max == 2019.0


def test_categorical_top_values(tmp_path):
    cols = _profile(tmp_path, CSV)
    countries = {tv["value"] for tv in cols["Country"].top_values}
    assert {"Germany", "Spain", "Italy", "UK"} == countries
