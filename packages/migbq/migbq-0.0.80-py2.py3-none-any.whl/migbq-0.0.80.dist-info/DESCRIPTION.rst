# migbq 

rdbms-to-bigquery-data-loader

## Requirement

* Python
  - CPython 2.7.x

* RDBMS (below, DB)  
  - Microsoft SQL Server
  - Mysql (development)

* Table Spec
  - All table must have Numeric Primary Key Field

* DB User Grant
  - SELECT, INSERT, UPDATE, CREATE
  - can access DB's metadata ([INFORMATION_SCHEMA] database) 
  - some metadata tables create in source RDBMS
  - (If you don't want create table in source, you can use sqlite. fork this project and edit source)

* Google Cloud SDK 
  - install Google Cloud SDK must be required 
    - https://cloud.google.com/sdk/downloads
    - https://cloud.google.com/sdk/gcloud/reference/auth/login

* Pymssql freetds
  - http://www.pymssql.org/en/stable/

## Install

```
export PYMSSQL_BUILD_WITH_BUNDLED_FREETDS=1
pip install migbq
```

## Usage

### write Configuration File

* like embulk ( http://www.embulk.org ) 

### Example 

#### general congif file
* config.yml 

```yml
in:
  type: mssql
  host: localhost
  user: USER
  password: PASSWORD
  port: 1433
  database: DATABASE
  tables: 
    - tbl
    - tbl2
    - tbl3
  batch_size: 50000
  temp_csv_path: /temp/pymig_csv
  temp_csv_path_complete: /temp/pymig_csv_complete 
out:
  type: bigquery
  project: GCP_PROJECT
  dataset: BQ_DATASET
```

#### jinja2 template 

* config.j2.yml
 - variable is enviromant variable only.
 - file extension is **.j2.yml** 

```yml
in:
  type: mssql
{% include "mssql-connect.yml" %}
  tables: 
    - tbl
    - tbl2
    - tbl3
  batch_size: 50000
  temp_csv_path: /temp/pymig_csv
  temp_csv_path_complete: /temp/pymig_csv_complete 
out:
  type: bigquery
  project: {{ env.GCP_PROJECT }}
  dataset: BQ_DATASET
```


### Run  

#### (1) Execute

```bash
migbq run config.yml
```

#### (2) Check Job Complete

```bash
migbq check config.yml
```


#### (3) Check table count equals  

```bash
migbq sync config.yml
```

* Primary Key base count check. 

### Run Forever 

* you can add crontab 
* migbq have exclusive process lock. so you can add crontab every minute. 
* you must add both **run** and **check**  


## Description

### run command

**[1]** select RDBMS table metadata 
  - get table primary key name in RDBMS metadata table.
  - get column name and type fields in RDBMS metadata table.

**[2]** select RDBMS Primary key value range 
  - get min / max PK of table 

**[3]** select data in primary key range
  - select with pk min and min + batch_size

```sql
	select * from tbl where 0 < idx and idx <= 100;
```

  - create file **pymig-tbl-idx-1-100** 
  - gzip csv  

**[4]** upload csv file to bigquery  
  - direct upload to bigquery table. not upload to GCS (quota exceed can occur)

**[5]** Repeat 1~4 until over the max primary key. 

For example, batch_size : 100, max pk is 321, then rdbms query execute like below.

```sql

select * from tbl where 0 < idx and idx <= 100;
select * from tbl where 100 < idx and idx <= 200;
select * from tbl where 200 < idx and idx <= 300;
select * from tbl where 300 < idx and idx <= 400;

-- end 

```

### check command

* check bigquery jobid end. 
* retry fail job.


### Log file of program

* log file create in config file's sub directory [log]

### Pid file of program

* pid file provide unique process for unique command. created at below directory. exclusive file lock.


```
/tmp
```

### load metadata table

#### META: migrationmetadata

* one row insert when each 'select' runs

| field name | type   | description                            | smaple value  | etc               |
| ----:     |--------|----------------------------------------|-----------------|-------------|
| tableName | STRING  | target [tableName]                         | tbl             | Primary Key |
| firstPk   | INTEGER | [tableName]'s Min Primary Key value       | 1             |           |
| lastPk    | INTEGER | [tableName]'s Max Primary Key value                  | 123             |           |
| currentPk | STRING  | [tableName]'s read complete Primary Key value                  | 20             |           |
| regDate   | DATETIME| this row's insert date   | 2017-11-29 01:02:03             |           |
| modDate   | DATETIME| firstPk, lastPk modify date              | 2017-11-29 01:02:03             |           |
| endDate   | DATETIME| currentPk reach lastPk date | 2017-11-29 11:22:33             |           |
| pkName    | STRING  | [tableNames]'s Primary Key Name          | idx             |           |
| rowCnt    | INTEGER | [tableNames]'s count(*)              | 123             |           |
| pageTokenCurrent | STRING | not use now                                   | tbl             |           |
| pageTokenNext | STRING |  not use now                                     | tbl             |           |

#### LOG:  migrationmetadatalog

* sequance
  - run :  insert a row to this table when 'select [tableName]' executed
  - run :  update a row to this table when bigquery jobId created 
  - check : update a row to this table's jobComplete and checkComplete when bigquery jobId call ends 

| field name | type   | description                            | smaple value  | etc               |
| ----:     |--------|----------------------------------------|-----------------|-------------|
| idx | BigInt |  PK                                  | 1             | Primary Key Auto Increment |
| tableName | STRING | [tableName]                                  | tbl             | Primary Key |
| regDate   | DATETIME | row insert date   | 2017-11-29 01:02:03             |           |
| endDate   | DATETIME | when jobId is 'DONE'  | 2017-11-29 11:22:33             |           |
| pkName    | STRING | [tableNames]'s Primary Key Name          | idx             |           |
| cnt    | INTEGER | bigquery api : statistics.load.outputRows         | 123             |           |
| pkUpper    | INTEGER | each 'select' executed : [PKName] <= [pkUpper] | 100             |           |
| pkLower    | INTEGER | each 'select' executed : [PKName] > [pkLower]    | 0             |           |
| pkCurrent    | INTEGER | same as pkUpper  | 99             |           |
| jobId    | STRING | bigquery upload job jobId        | job-adf132f31rf3f             |           |
| errorMessage    | STRING | when jodId check result is 'ERROR', then write this  | ERROR:bigquery quota exceed             |           |
| checkComplete | INTEGER | check command       | 1             |           |
| jobComplete | INTEGER |  check command jobId check complete. success=1, fail=-1 | 1             |           |
| pageToken | STRING |  use as etc                                       |              |           |


## loadmap

* parallel loading not supported.  


