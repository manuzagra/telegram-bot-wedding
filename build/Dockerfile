FROM python:3.11

RUN useradd -ms /bin/bash manu
USER manu

WORKDIR /home/manu

COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt