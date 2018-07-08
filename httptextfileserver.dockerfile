FROM python:3-alpine

WORKDIR /usr/src

COPY httptextfileserver ./httptextfileserver

ENTRYPOINT ["python", "httptextfileserver/httptextfileserver.py"]
CMD ["0.0.0.0", "5678", "log/output.log"]
