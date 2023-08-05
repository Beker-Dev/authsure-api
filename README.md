# AuthSureApi

### Description:
#### AuthSure is a SSO (Single Sign-On) software application, with identity and access management, that is, where it is possible with just a single login, to enter all the applications used by a given company.

### Migrations:
###### Create Migrations
```bash
alembic revision --autogenerate -m "migration_info"
```
###### Run Migrations
```bash
alembic upgrade head
```

### Application:
###### Install requirements
```bash
pip install -r requirements.txt
```
###### Run Application
```bash
uvicorn app.main:app --reload
```

### Docker:
##### Need to change directory to ./docker before executing commands below
```bash
cd ./docker
```
###### Build Docker Image
```bash
docker build -t authsureapi .
```
###### Run Docker Container
```bash
docker run -d --name authsureapi -p 8000:8000 authsureapi
```
###### Run Docker Compose
```bash
docker-compose up -d
```
