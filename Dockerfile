FROM python:3
WORKDIR /AI.UpscaleSwan
COPY . /AI.UpscaleSwan
RUN pip install -r AI.UpscaleSwan/requirements.txt
CMD python ./AI.UpscaleSwan/app.py
COPY . .

ENTRYPOINT ["python"]
CMD ["flask_app.py"]