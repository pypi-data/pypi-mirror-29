# Compare psnu and site jsons

[![Build Status](https://travis-ci.org/davidhuser/data-pack-importer-compare.svg?branch=master)](https://travis-ci.org/davidhuser/data-pack-importer-compare)

### Install

```bash
pip install dpi-compare
```

### Usage

```bash
dpi-compare --help

Compare data JSONs in folders

arguments:
  -h, --help           show this help message and exit
  --folder1 FOLDER1    File path of first folder
  --folder2 FOLDER2    File path of second folder
  --country COUNTRY    Country string, e.g. "nigeria"
  --level              Level, either "psnu" or "site"
  --type               Type, either "normal" or "hts"
```

e.g.

```bash
dpi-compare --folder1 data/v1 --folder2 data/v2 --country swazi --level psnu --type normal
```

Outputs a CSV file showing the difference between each file.
Uses a `pandas` DataFrame and applying a _merge_ and _outer join_.

#### Example folder structure

```
data/
├── v1/
│   ├── swazi_psnu_hts.json
│   ├── swazi_psnu_normal.json
│   ├── swazi_site_hts.json
│   └── swazi_site_normal.json
└── v2/
    ├── swazi_psnu_hts.json
    ├── swazi_psnu_normal.json
    ├── swazi_site_hts.json
    └── swazi_site_normal.json
```

#### Naming convention

Files within a directory must have a matching file in the other directory.

`<country>_{psnu|site}_{hts|normal}.json`


### R script to generate those JSONs

Use [data-pack-importer](https://github.com/jason-p-pickering/data-pack-importer)

```R
# ADJUST THIS --->
type="normal"
country="swazi"
disagg_tool_file="SwazilandCOP18DisaggToolv2018.02.26_HTSSELF fixed.xlsx"
distribution_year=2017

# DO NOT CHANGE
support_files="/vagrant/support_files/"
disagg_tools="/vagrant/disagg_tools/"
library(jsonlite)
library(devtools)
library(datapackimporter)
psnu_json_file=paste0(disagg_tools, country, "_psnu_", type, ".json")
site_json_file=paste0(disagg_tools, country, "_site_", type, ".json")
disagg_tool=paste0(disagg_tools, disagg_tool_file)
wb<-disagg_tool
wb
psnu_data<-ImportSheets(wb, distribution_method = distribution_year, support_files_path = support_files)
cat(toJSON(psnu_data, auto_unbox = TRUE), file = psnu_json_file)
site_data<-distributeSite(psnu_data)
export_site_level_tool(site_data)
psnu_json_file
cat(toJSON(site_data, auto_unbox = TRUE), file = site_json_file)
```

## Develop

```bash
pip install pipenv
git clone <this repo>
cd <this repo>
pipenv install --dev
```

## Tests
```
python setup.py test
```