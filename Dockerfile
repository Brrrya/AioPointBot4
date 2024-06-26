FROM python:3.11
WORKDIR /usr/src/aiopointbot4
COPY . .
RUN unlink /etc/localtime \
&& ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime \
&& apt-get update -y \
&& apt-get upgrade -y \
&& pip install -r ./requirements.txt

CMD ["python", "./main.py"]
