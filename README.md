# Revolut Assignment
Revolut Assignment for Data Engineerning

#### Problem Statement
Link for problem statement : [here](https://docs.google.com/document/d/11iJO-yoylOamMDneV8WAoo8o6dGpvBghNqhyd5GFWmo/edit)


#### SQL
- Solution is in [sql/solution.sql](sql/solution.sql)
- Few assumptions have been taken while solving the question. They are mentioned in [sql/README.md](sql/README.md)



#### Programming


##### Requirements
- python 3.6
- sqllite
- flask
- docker


##### Project Structure
```
.
├── Dockerfile
├── Makefile
├── Pipfile
├── Pipfile.lock
├── README.md
├── app
│   ├── __init__.py
│   ├── exceptions.py
│   ├── models.py
│   ├── nest.py
│   ├── resources
│   │   ├── __init__.py
│   │   ├── deposit_item.py
│   │   ├── deposit_list.py
│   │   ├── hello.py
│   │   ├── login.py
│   │   ├── nest_api.py
│   │   └── register.py
│   └── utils
│       ├── __init__.py
│       ├── fields.py
│       ├── parser.py
│       └── schema.py
├── config.py
├── entrypoint.sh
├── example_input.json
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── requirements.txt
├── run.py
├── sql
│   ├── README.md
│   ├── init.sql
│   ├── solution.sql
│   └── test_notebook.md
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


##### Tasks
- [x] Command line utility which takes json as input and convert it into specified nested form. 



Build Docker Image 
```
docker build -t revolut_assignment .
```

Run Docker Container
```
docker run --name revolut_api -d -p 8000:5000 revolut_assignment:latest
```

Login to Docker Container
```
docker exec -it revolut_api /bin/bash
```s