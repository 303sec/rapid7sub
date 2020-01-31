# Rapid7Sub
Subdomain enumeration with Rapid7 FDNS using AWS Athena&S3

Note: u should pay $0.40 for each query to aws athena (it depends to size of rapid7 open data)

[![asciicast](https://asciinema.org/a/TXXwJ7G1J2bmD4I3OGY7oGUmn.svg)](https://asciinema.org/a/TXXwJ7G1J2bmD4I3OGY7oGUmn)

# About Rapid7 FDNS and AWS Athena
[How to Conduct DNS Reconnaissance Using Rapid7 Open Data and AWS](https://blog.rapid7.com/2018/10/16/how-to-conduct-dns-reconnaissance-for-02-using-rapid7-open-data-and-aws/)

![rapid7fdns](https://0xpatrik.com/content/images/2018/10/Domain_Infrastructure.jpg)

# Installation
#### How to install script
    git clone https://github.com/xyele/rapid7sub
    cd rapid7sub
    python3 -m pip install -r requirements.txt
#### How to create Database (Athena)
Run that queries at Athena Panel (https://console.aws.amazon.com/athena/home) <br>

Query for getting the database from bucket
```
CREATE EXTERNAL TABLE IF NOT EXISTS rapid7_fdns_any (
  `timestamp` timestamp,
  `name` string,
  `type` string,
  `value` string 
) PARTITIONED BY (
  date string 
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = '1'
) LOCATION 's3://rapid7-opendata/fdns/any/v1/'
TBLPROPERTIES ('has_encrypted_data'='false');
```

Then run `msck repair table rapid7_fdns_any` (ofc as query)

#### The remaining steps are basic. Just create aws api key and configure variables which i specified on python file

# Usage
`python3 rapid7sub.py domain.com`

# Contact
https://twitter.com/mehmetxyele

### Thanks to
Alexey Baikov (sysboss)
