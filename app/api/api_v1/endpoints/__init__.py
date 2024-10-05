import pymysql

# Database connection details
db_config = {
    'host': 'the-boys-rds.cxcoo02qemtr.ap-southeast-2.rds.amazonaws.com',
    'user': 'admin',
    'password': 'nZXne~-.3[X6>hgMt4%SDBB|tJaB',
    'database': 'TheBoys',
    'port': 3306
}

connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        port=db_config['port']
    )