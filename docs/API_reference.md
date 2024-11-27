# QuantumVerse-Nexus API Reference

## Overview

The QuantumVerse-Nexus API provides a set of endpoints for interacting with the blockchain, smart contracts, and decentralized applications.

## Authentication

All API requests require authentication via API keys. Ensure to include your API key in the headers of your requests.

## Endpoints

### 1. Blockchain

- **GET /blocks**: Retrieve the list of all blocks in the blockchain.
- **POST /transactions**: Create a new transaction.

### 2. Smart Contracts

- **POST /contracts**: Deploy a new smart contract.
- **GET /contracts/{contract_id}**: Retrieve details of a specific smart contract.

### 3. dApps

- **GET /dapps**: List all available decentralized applications.
- **POST /dapps/{dapp_id}/execute**: Execute a function in a specified dApp.

## Error Codes

- **400**: Bad Request
- **401**: Unauthorized
- **404**: Not Found
- **500**: Internal Server Error
