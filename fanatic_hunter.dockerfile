FROM python:3-alpine

RUN apk update && apk add tzdata &&\
    cp /usr/share/zoneinfo/Europe/London /etc/localtime && \
    echo "Europe/London" > /etc/timezone && \
    apk del tzdata

WORKDIR /usr/src/fanatic-hunter

COPY main.py settingsparser.py siteaccessor.py requirements.txt ./
RUN pip install -r requirements.txt

COPY settings.yml logging_config.yml ./

ENTRYPOINT ["python", "main.py"]
CMD ["settings.yml"]
