# Project info

This project is an example of how to implement test automation for a modern web application using a multi-repository approach. It covers all levels of the QA pyramid model, including static analysis, unit tests, integration testing with mocked data, and end-to-end testing in an ephemeral environment. The goal of the project is to showcase how test automation can be integrated into a modern development environment to provide a scalable and robust solution. 

The system under test for this project is a trivial “Wallet info” web application that shows the cryptocurrency balance for a given wallet address. It supports Ethereum and USDC tokens.

# Backend

This repository contains an API service with a few endpoints developed with Python and FastAPI framework as well as unit tests and GitHub workflow configuration.

`server.py` is an API service with following endpoints:

- `GET /status` returns Web connection status
- `GET /balance/crypto/address` communicates with local or public ETH testnet to return balance for a given address

`test_server.py` — Unit tests. Web3 communication is mocked.

`.github/workflows/build.yml` GitHub workflow:

- setup python and required pip modules from the requirements.txt file
- run static analysis tools: pylint, black and isort
- run unit tests
- build and push backend docker image with the latest code
- triggers deploy-and-test pipeline from the [infra](https://github.com/dnch-chernov/grand-test-automation) repository to run end-to-end tests on the ephemeral environment

# Other parts of the project

[Frontend](https://github.com/dnch-chernov/wallet-info-web) is a React application that has just two pages: the first one with the form for wallet address and token type; the second shows the balance.

[Tests](https://github.com/dnch-chernov/wallet-info-tests) repository contains UI and API tests. UI tests are implemented using Cypress, and API tests are Python and Pytest.

[Local testnet](https://github.com/dnch-chernov/wallet-info-local-testnet) repository is an example of how web3-related testing could be implemented using a fast and predictable local testnet (Ganache) instead of a public one.

[Infra](https://github.com/dnch-chernov/grand-test-automation) repository contains the application Helm chart for Kubernetes deployment as well as GitHub action configuration for deployment and end-to-end testing.
