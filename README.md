# Revolut Assignment
Revolut Assignment for Data Engineerning

### Problem Statement
Link for problem statement : [here](https://docs.google.com/document/d/11iJO-yoylOamMDneV8WAoo8o6dGpvBghNqhyd5GFWmo/edit)


### SQL
- Solution is in [sql/solution.sql](sql/solution.sql)
- Few assumptions have been taken while solving the question. They are mentioned in [sql/README.md](sql/README.md)



### Programming


#### Requirements
- python 3.6
- sqllite
- flask
- docker


#### Project Structure
```
.
├── Dockerfile
├── Makefile
├── Pipfile
├── Pipfile.lock
├── README.md
├── app
│   ├── __init__.py
│   ├── exceptions.py
│   ├── models.py
│   ├── resources
│   │   ├── __init__.py
│   │   ├── deposit_item.py
│   │   ├── deposit_list.py
│   │   ├── hello.py
│   │   ├── login.py
│   │   ├── nest_api.py
│   │   └── register.py
│   └── utils
│       ├── __init__.py
│       ├── fields.py
│       ├── parser.py
│       └── schema.py
├── config.py
├── entrypoint.sh
├── example_input.json
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── nest.py
├── requirements.txt
├── run.py
├── sql
│   ├── README.md
│   ├── init.sql
│   ├── solution.sql
│   └── test_notebook.md
└── tests
    ├── __init__.py
    ├── base.py
    ├── base_deposit.py
    ├── context.py
    ├── test_auth.py
    ├── test_deposit_item.py
    ├── test_deposit_list.py
    ├── test_model.py
    ├── test_nest.py
    └── test_parser.py

7 directories, 43 files
```


#### Setup

- Pipenv is required to run this project. Installation instruction for pipenv can be found [here](https://github.com/pypa/pipenv)
- Otherwise, virtualenv can be used. **requirements.txt** also is given. Installation instruction for virtualenv can be found [here](https://github.com/pypa/virtualenv)

Initialize with dependenciess
```bash
cd revolut_assignment
pipenv shell
pipenv install
```

Build Docker Image 
```bash
docker build -t revolut_assignment .
```

Run Docker Container
```bash
docker run --name revolut_api -d -p 8000:5000 revolut_assignment:latest
```

The REST API is now running on http://localhost:8000/


#### Testing and Debugging

To run test cases
```bash
make test
```

Login to Docker Container
```bash
docker exec -it revolut_api /bin/bash
```

#### Tasks

- To run parse json cli locally
```bash
docker exec -it revolut_api /bin/bash -c "cat example_input.json | pipenv run python nest.py currency country city"
```
- To use parse json api,
```bash
curl -XPOST -H 'Authorization: Basic YWRtaW46YWRtaW4=' -H "Content-type: application/json" -d '{
    "data": [
  {
    "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100
  }],
    "nesting_levels": ["currency" ,"country", "city"]
}' 'http://localhost:8000/api/v1/deposit/nest'
```
- Other api endpoints

Method | Endpoint     | Description
------------ | ------------ | -------------
GET | /api/v1/auth/register | This endpoint can be used to create user. These user credentails will be used to do Basic Auth with other API Endpoints. 
GET | /api/v1/deposit/ | Fetches all the deposits done by the user.
POST | /api/v1/deposit/ | Insert deposit amount along with its meta information into database.
GET | /api/v1/deposit/[int:deposit_id]| Fetches all information about deposit done by the user using deposit_id
PUT | /api/v1/deposit/[int:deposit_id]|Updates deposit details like amount etc using deposit_id
DELETE | /api/v1/deposit/[int:deposit_id]| Delete deposit using deposit_id
POST | /api/v1/deposit/nest/ | Parse JSON APIs
GET | / | Introduction

#### Sample Requests

- Create User
```bash
curl -XPOST -H "Content-type: application/json" -d '{
    "username": "dummy",
    "password": "dummy"
}' 'http://localhost:8000/api/v1/auth/register'
```

- Check deposits done by the user.
```bash
curl -XGET -H 'Authorization: Basic YWRtaW46YWRtaW4=' -H "Content-type: application/json" 'http://localhost:8000/api/v1/deposit/'
```

- Insert deposit 
```bash
curl -XPOST -H 'Authorization: Basic YWRtaW46YWRtaW4=' -H "Content-type: application/json" -d '{ "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100 }' 'http://localhost:8000/api/v1/deposit/'
```

- Fetches details about deposit with id 1
```bash
curl -XGET -H 'Authorization: Basic YWRtaW46YWRtaW4=' -H "Content-type: application/json" 'http://localhost:8000/api/v1/deposit/1'
```

- Update amount to 1000 for deposit with id 1
```bash
curl -XPUT -H 'Authorization: Basic YWRtaW46YWRtaW4=' -H "Content-type: application/json" -d '{"amount": 1000}' 'http://localhost:8000/api/v1/deposit/1'
```

- Delete deposit with id 1
```bash
curl -XDELETE -H 'Authorization: Basic YWRtaW46YWRtaW4=' -H "Content-type: application/json" 'http://localhost:8000/api/v1/deposit/1'
```