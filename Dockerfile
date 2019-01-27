FROM python:3.6

RUN mkdir -p /opt/services/polestar/src
WORKDIR /opt/services/polestar/src


COPY . /opt/services/polestar/src

RUN pip3 install -r requirements.txt
RUN cd polestar  && python3 manage.py collectstatic --no-input 

EXPOSE 8000
CMD ["gunicorn", "--chdir", "polestar", "--bind", ":8000", "polestar.wsgi:application"]

