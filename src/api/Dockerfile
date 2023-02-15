FROM python:3.9

# set working directory of container
WORKDIR /app

# install dependencies first - leverage cache
# RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

# algorithm likely change less than mode parameters - leverage cache
COPY ./fastapi .

# model parameters last - leverage cache
# COPY ./models .

CMD ["uvicorn", "recommender_api:app", "--host", "0.0.0.0", "--port", "8000"]


# CMD ["uvicorn", "recommender_api:app", "--host", "0.0.0.0", "--port", "8000"]

# # EXPOSE for documentation purposes
# EXPOSE 8000


# RUN UVICORN
# uvicorn recommender_api:app --host 0.0.0.0 --port 8000
# docker build -t recommender_api:v1 .
# docker run -p 8000:8000 recommender_api:v1   

# PUSH TO DOCKERHUB: docker push chingfhen/recommender_api



