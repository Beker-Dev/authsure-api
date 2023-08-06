import os
import dotenv


dotenv.load_dotenv()

environments = {
    'PROJECT_NAME': 'AuthSureApi',
    'BACKEND_CORS_ORIGINS': '[]',
    'POSTGRES_USER': 'postgres',
    'POSTGRES_PASSWORD': 'postgres',
    'POSTGRES_SERVER': 'database',
    'POSTGRES_PORT': 5434,
    'POSTGRES_DB': 'postgres'
}

{os.environ.setdefault(k, v) for k, v in environments.items()}

print('Set test environment variables')
