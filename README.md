# Rapid7Sub
Subdomain enumeration with Rapid7 FDNS using AWS Athena&S3
# Installation
#### How to install script
    git clone https://github.com/xyele/rapid7sub
    cd rapid7sub
    python3 -m pip install -r requirements.txt
#### How to create Database (Athena)
Go https://console.aws.amazon.com/athena/home <br>
Run that query (https://paste.ubuntu.com/p/hGSGgXb2QP/) <br>
Run `msck repair table rapid7_fdns_any` (as query)

#### The remaining steps is basic. Just create aws api key and configure variables which i specified on python file

# Usage
`python3 rapid7sub.py domain.com`

### Thanks to
Alexey Baikov (sysboss)
