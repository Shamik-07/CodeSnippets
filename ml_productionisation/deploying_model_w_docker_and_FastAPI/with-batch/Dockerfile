FROM frolvlad/alpine-miniconda3:python3.7

COPY requirements.txt .

ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt && \
        rm requirements.txt
RUN pip install -U pip

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
