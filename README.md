# Banking System

## Overview

This banking system is implemented in Python and utilizes object-oriented programming principles to manage bank accounts, transactions, and customer information. It supports various transaction types, including deposits and withdrawals, while maintaining a transaction history for each account.

## Features

- **Transaction Management**: Supports deposits and withdrawals, ensuring sufficient balance and transaction limits.
- **Account Management**: Allows customers to create and manage multiple bank accounts.
- **Transaction History**: Tracks all transactions with timestamps.
- **Customer Profiles**: Represents individual customers with their personal information.

## Classes

- **Historico**: Manages the transaction history of an account.
- **Transacao**: An abstract class for defining transaction types.
- **Saque**: Represents withdrawal transactions.
- **Deposito**: Represents deposit transactions.
- **Cliente**: Represents a bank customer who can hold multiple accounts.
- **Conta**: A base class for bank accounts, supporting deposit and withdrawal operations.
- **ContaCorrente**: A derived class for checking accounts with withdrawal limits.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/username/repository.git
   ```
2. Navigate to the project directory:
   ```bash
   cd repository
   ```

## Usage

To use the banking system, instantiate the classes and perform transactions. Here’s a basic example:

```python
# Create a client
cliente = PessoaFisica(nome="John Doe", data_nascimento="01-01-1990", cpf="12345678901", endereco="123 Main St")

# Create a new account
conta = Conta.nova_conta(cliente, numero=12345)

# Perform a deposit
deposito = Deposito(valor=1000.0)
cliente.realizar_transacao(conta, deposito)

# Perform a withdrawal
saque = Saque(valor=500.0)
cliente.realizar_transacao(conta, saque)

# View transaction history
print(conta.historico.transacoes)
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss improvements or bugs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
