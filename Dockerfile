FROM 370531249777.dkr.ecr.ap-south-1.amazonaws.com/ubuntu-nginx-sql:2.0.0

#set timezone
RUN rm /etc/localtime
RUN ln -s /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
RUN export TZ=Asia/Kolkata

#codebase
RUN mkdir -p /ecs-sot/

#setup env
COPY requirements.txt /ecs-sot/

COPY __init__.py /ecs-sot/
COPY dumper.py /ecs-sot/
COPY config.py /ecs-sot/

# set app name
RUN export APP_NAME=sot
RUN export PATH=$PATH:/root/.local/bin/

#set work dir
WORKDIR /ecs-sot

#install dependencies
RUN pip install -q -r requirements.txt

#container port expose
EXPOSE 80

CMD ["python", "/ecs-sot/dumper.py"]

