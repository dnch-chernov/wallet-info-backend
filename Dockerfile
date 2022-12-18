FROM python:3.10-slim-bullseye

RUN pip install "fastapi[all]"
RUN pip install web3 pytest pylint black isort

WORKDIR /app

COPY src /app

ENV PROVIDER_URL "http://localhost:8545"
ENV USDC_CONTRACT_ADDRESS "0x07865c6e87b9f70255377e024ace6630c1eaa37f"

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--reload"]