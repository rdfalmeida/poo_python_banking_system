from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict


class Historico:
    """
    Class to store the transaction history of an account.
    """
    def __init__(self):
        self._transacoes: List[Dict] = []

    @property
    def transacoes(self) -> List[Dict]:
        """Returns the list of transactions."""
        return self._transacoes

    def adicionar_transacao(self, transacao: 'Transacao') -> None:
        """Adds a transaction to the history."""
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })


class Transacao(ABC):
    """
    Abstract base class for transactions.
    """
    @property
    @abstractmethod
    def valor(self) -> float:
        """Abstract property to get the transaction value."""
        pass

    @abstractmethod
    def registrar(self, conta: 'Conta') -> None:
        """Abstract method to register the transaction in an account."""
        pass


class Saque(Transacao):
    """
    Class for withdrawals.
    """
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        """Returns the value of the withdrawal."""
        return self._valor

    def registrar(self, conta: 'Conta') -> None:
        """Register a withdrawal transaction on the given account."""
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """
    Class for deposits.
    """
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        """Returns the value of the deposit."""
        return self._valor

    def registrar(self, conta: 'Conta') -> None:
        """Register a deposit transaction on the given account."""
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Cliente:
    """
    Class representing a customer with one or more bank accounts.
    """
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas: List[Conta] = []

    def realizar_transacao(self, conta: 'Conta', transacao: Transacao) -> None:
        """Perform a transaction on the given account."""
        transacao.registrar(conta)

    def adicionar_conta(self, conta: 'Conta') -> None:
        """Add a new account to the client."""
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """
    Class representing an individual customer.
    """
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    """
    Base class representing a generic bank account.
    """
    def __init__(self, numero: int, cliente: Cliente):
        self._saldo: float = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> 'Conta':
        """Factory method to create a new account."""
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        """Returns the account balance."""
        return self._saldo

    @property
    def numero(self) -> int:
        """Returns the account number."""
        return self._numero

    @property
    def agencia(self) -> str:
        """Returns the account agency."""
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        """Returns the account holder."""
        return self._cliente

    @property
    def historico(self) -> Historico:
        """Returns the transaction history."""
        return self._historico

    def sacar(self, valor: float) -> bool:
        """Withdraw money if sufficient balance is available."""
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        if valor > self.saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            return False

        self._saldo -= valor
        print("Saque realizado com sucesso!")
        return True

    def depositar(self, valor: float) -> bool:
        """Deposit money into the account."""
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False

        self._saldo += valor
        print("Depósito realizado com sucesso!")
        return True


class ContaCorrente(Conta):
    """
    Class representing a checking account with withdrawal limits.
    """
    def __init__(self, numero: int, cliente: Cliente, limite: float = 500.0, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        """Withdraw money, ensuring limits are respected."""
        numero_saques = len([t for t in self.historico.transacoes if t["tipo"] == Saque.__name__])

        if valor > self.limite:
            print("Operação falhou! O valor do saque excede o limite.")
            return False
        if numero_saques >= self.limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False

        return super().sacar(valor)

    def __str__(self) -> str:
        """Returns a string representation of the account details."""
        return f"Agência: {self.agencia}\nC/C: {self.numero}\nTitular: {self.cliente.nome}"
