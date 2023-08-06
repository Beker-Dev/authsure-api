import os
import sys


def set_test_environments():
    if 'pytest' in sys.argv[0]:
        environments = {
            'PROJECT_NAME': 'AuthSureApi',
            'BACKEND_CORS_ORIGINS': '[]',
            'POSTGRES_USER': 'postgres',
            'POSTGRES_PASSWORD': 'postgres',
            'POSTGRES_SERVER': 'database',
            'POSTGRES_PORT': '5434',
            'POSTGRES_DB': 'postgres'
        }

        {os.environ.setdefault(k, v) for k, v in environments.items()}
