# t=mypch-proxy
# docker build -t "$t" . -f ./Dockerfile
FROM python:3.7
WORKDIR /app/mypch-proxy
RUN mkdir -p /app/mypch-proxy/flask_session
RUN mkdir -p /app/mypch-proxy/app
COPY app/*.py /app/mypch-proxy/app/
COPY app/swagger.yaml /app/mypch-proxy/app/
RUN mkdir -p /app/mypch-proxy/app/templates
COPY app/templates/index.html /app/mypch-proxy/app/templates/
RUN mkdir -p /app/mypch-proxy/app/static/css
COPY app/static/css/w3.css /app/mypch-proxy/app/static/css/
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app/mypch-proxy/"
CMD ["python3", "-u", "/app/mypch-proxy/app/__init__.py"]
EXPOSE 5000/tcp
USER 1000
HEALTHCHECK CMD curl --fail http://localhost:5000/ || exit 1
