import pytest
import requests
from sqlalchemy.engine import create_engine

localhost='http://127.0.0.1'

DATABASE_URI = 'postgres+psycopg2://cs162_user:cs162_password@localhost:5432/cs162'
engine = create_engine(DATABASE_URI)
conn = engine.connect()

def test_valid_expression():
    rows_before = conn.execute('SELECT COUNT(*) FROM Expression;')

    data = {
        'expression': '2+1'
    }

    r = requests.post(localhost+':5000/add', data=data)
    assert r.status_code==200
    
    rows_after = conn.execute('SELECT COUNT(*) FROM Expression;')

    assert rows_before == rows_after-1


def test_invalid_expression():
    rows_before = conn.execute('SELECT COUNT(*) FROM Expression;')

    data = {
        'expression': 'foo+bar'
    }
    
    r = requests.post(localhost+':5000/add', data=data)
    assert r.status_code==500

    rows_after = conn.execute('SELECT COUNT(*) FROM Expression;')

    assert rows_before == rows_after