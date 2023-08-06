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
        with open('.env', 'w') as f:
            for k, v in environments.items():
                f.write(f'{k}={v}\n')
