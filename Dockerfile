FROM python:3.8

# it would be nice if the python container came with pipenv by default!
# see issue => https://github.com/docker-library/python/issues/258
RUN pip install pipenv

# all our work happens here
WORKDIR /project

# set the PYTHONPATH to our working directory
# this is necessary primarily for tools like alembic
# which dont adopt the path that they are being invoked inside of
ENV PYTHONPATH="/project"

# copy in requirements files
COPY Pipfile /project/Pipfile
COPY Pipfile.lock /project/Pipfile.lock

# install requirements
# NOTE! in a production environment, we should not be installing `--dev` requirements all the time
# instead we should have one "prod" image, and one "dev" image
RUN pipenv install --system --dev
