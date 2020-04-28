
FROM python:3.8

# it would be nice if the python container came with pipenv by default!
# see issue => https://github.com/docker-library/python/issues/258
RUN pip install pipenv

# set the PYTHONPATH to our working directory
# this is necessary primarily for tools like alembic
# which dont adopt the path that they are being invoked inside of
ENV PYTHONPATH="/project"
