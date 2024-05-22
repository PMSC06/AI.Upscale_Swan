FROM python:3
WORKDIR /AIUpscaleSwan
COPY . /AIUpscaleSwan
RUN pip install -r AIUpscaleSwan/requirements.txt
CMD python ./AIUpscaleSwan/app.py
COPY . .

ENTRYPOINT ["py"]
CMD ["AIUpscaleSwna/app.py"]