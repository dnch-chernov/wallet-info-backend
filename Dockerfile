FROM python:3.10-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip -r requirements.txt

ENV PROVIDER_URL "http://localhost:8545"
ENV USDC_CONTRACT_ADDRESS "0x07865c6e87b9f70255377e024ace6630c1eaa37f"

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--reload"]