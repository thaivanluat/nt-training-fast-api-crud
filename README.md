## CRUD api using FastAPI - Python
library: fastapi, sqlalchemy, pydantic, alembic
- [fastapi] - web framework for building RESTful APIs in Python.
- [sqlalchemy] - Python SQL toolkit and Object Relational Mapper
- [pydantic] - Python library for data modeling/parsing
- [alembic] - database migration tool 
- ...

CRUD api for user, company, task

Install the dependencies
```sh
pip install -r requirements.txt
```
To init sample data, run command
```sh
alembic upgrade head
```
Run the server
```sh
cd app
uvicorn main:app --reload
```
