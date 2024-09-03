import pymysql

# Database connection details
db_config = {
    'host': 'the-boys-rds.cxcoo02qemtr.ap-southeast-2.rds.amazonaws.com',
    'user': 'admin',
    'password': '0Lnxl5Y7kKX3at)sqH(0dQ9S|f3|',
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