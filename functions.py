import textwrap
from abc import ABC, ABCMeta, abstractclassmethod, abstractproperty
import datetime

class Client:
    def __init__(self, address:str):
        self.address = address
        self.accounts = []

    def realize_transaction(self, account, transaction):
        transaction.register(account)
    
    def add_account(self, account):
        self.accounts.append(account)

class PessoaFisica(Client):
    def __init__(self, name, born_date, cpf, address):
        super().__init__(address)
        self.name = name
        self.born_date = born_date
        self.cpf = cpf
    
class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._number = number
        self._agency = '0001'
        self._client = client
        self._history = History()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)
    
    @property
    def number(self):
        return self._number
    
    @property
    def agency(self):
        return self._agency
    
    @property
    def client(self):
        return self._client
    
    @property
    def history(self):
        return self._history
    
    def withdrawal(self, value):
        balance = self._balance
        exceeded_balance = value > balance

        if exceeded_balance:
            print('\n--- Operação negada! Saldo insuficiente  ---')

        elif value > 0:
            self._balance -= value
            print('\n *** Saque realizado com sucesso! ***')
            return True
        
        else:
            print('\n--- Operação falhou. O valor informado é inválido! ---')

        return False
    
    def deposit(self, value):
        if value>0:
            self._balance += value
            print('\n*** Depósito realizado com sucesso! ***')
        else:
            print('\n --- Operação falhou. O valor informado é inválido! --- ')
            return False

        return True

class ContaCorrente(Account):
    def __init__(self, number, client, limit = 500, withdrawal_limit = 3):
        super().__init__(number, client)
        self.limit = limit
        self.withdrawal_limit = withdrawal_limit

    def withdrawal(self, value):
        withdrawal_number = len(
            [transaction for transaction in self.history.transactions if transaction['type'] == Witdrawal.__name__]
        )

        exceeded_limit = value > self.limit
        exceeded_withdrawal = withdrawal_number >= self.withdrawal_limit

        if exceeded_limit:
            print('\n--- Operação negada. O valor solicitado excede o limite por transação ---')
        elif exceeded_withdrawal:
            print('\n--- Operação negada. O número de saques diários excedido. Tente amanhã novamente! ---')
        else:
            return super().withdrawal(value)
        
        return False

    def __str__(self):
        return f'''
            Agência:\t{self.agency}
            C/C:\t\t{self.number}
            Titular:\t{self.client.name}
        '''

class History:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions
    
    def add_transaction(self, transaction):
        self._transactions.append(
            {
                'type': transaction.__class__.__name__,
                'value': transaction.value,
                'date': datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

class Transaction(ABC):
    @property
    @abstractproperty
    def value(self):
        pass

    @abstractclassmethod
    def register(self, account):
        pass

class Withdrawal(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
    
    def register(self, account):
        transaction_succeed = account.withdraw(self.value)

        if transaction_succeed:
            account.history.add_transaction(self)

class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
    
    def register(self, account):
        transaction_succeed = account.deposit(self.value)

        if  transaction_succeed:
            account.history.add_transaction(self)

class ClientManager:
    @staticmethod
    def filter_client(cpf, clients):
        filtered_clients = [client for client in clients if client.cpf == cpf]
        return filtered_clients[0] if filtered_clients else None

    @staticmethod
    def get_client_account(client):
        if not client.account:
            print('\n --- Cliente não foi encontrado ---')
            return
        return client.account[0]
    
    def return_filtered_client(self, clients):
        cpf = input('Por favor informe o cpf do cliente:\n>')
        return self.filter_client(cpf, clients)
    
    def create_client(self, clients):
        cpf = input('Por favor informe o cpf do cliente:\n>')
        client = self.filter_client(cpf, clients)
        if client:
            print('\n--- CPF já cadastrado! ---')
            return
        
        name = input('Favor informar o nome completo: ')
        born_date = input("Por favor informe a data de nascimento (dd-mm-aaaa): ")
        address = input("Também informe o endereço (logradouro, nro - bairro - cidade/sigla estado):\n>")

        client = PessoaFisica(name = name, born_date = born_date, address = address, cpf= cpf)

        clients.append(client)
        print('\n--- Cliente criado com sucessso! ---')


class MenuManager(ClientManager):
    def __init__(self):
        super().__init__()

    def deposit(self, clients):
        client = super().return_filtered_client(clients)
        if not client:
            print('\n--- Cliente não encontrado ---')
            return
        value = float(input('Por favor informe o valor do depósito: R$ '))
        transaction = Deposit(value)

        account = super().get_client_account(client)
        if not account:
            return
        
        client.realize_transaction(account, transaction)

    def withdrawal(self, clients):
        client = self.return_filtered_client(clients)
        if not client:
            print('\n--- Cliente não encontrado ---')
            return
        
        account = self.get_client_account(client)
        if not account:
            print('\n--- Conta não encontrada para o cliente ---')
            return
        
        try:
            value = float(input('Por favor informe o valor do saque: R$ '))
            if value <= 0:
                raise ValueError("O valor deve ser positivo.")
        except ValueError as e:
            print(f"\n--- Entrada inválida: {e} ---")
            return

        transaction = Withdrawal(value)
        client.realize_transaction(account, transaction)

        if account.balance >= value:
            print('\n*** Saque realizado com sucesso! ***')
        else:
            print('\n--- Saque não realizado. Verifique o saldo e tente novamente. ---')

    def show_extrato(self, clients):
        client = super().return_filtered_client(clients)
        if not client:
            print('\n--- Cliente não encontrado ---')
            return
        
        account = super().get_client_account(client)
        if not account:
            return

        print("\n================ EXTRATO ================")
        transactions = account.history.transactions

        extrato = ""
        if not transactions:
            extrato = "Não foram realizadas movimentações."
        else:
            for transaction in transactions:
                extrato += f"\n{transaction['type']}:\n\tR$ {transaction['value']:.2f}"

        print(extrato)
        print(f"\nSaldo:\n\tR$ {account.balance:.2f}")
        print("==========================================")

    def account_create(account_number, clients, accounts):
        client = super().return_filtered_client(clients)
        if not client:
            print('\n--- Cliente não encontrado, operação encerrada! ---')
            return
        
        account = ContaCorrente.new_account(client= client, number=account_number)
        accounts.append(account)
        client.accounts.append(account)

        print('\n*** Conta criada com sucesso! ***')  
        return accounts  
    
    @staticmethod
    def account_list(accounts):
        for account in accounts:
            print('=' * 100)
            print(textwrap.dedent(str(account)))

class System(MenuManager):
    def __init__(self):
        super().__init__()
        self._clients = []
        self._accounts = []
        self._menu = textwrap.dedent("""
            [D]\tDepositar
            [S]\tSacar
            [E]\tExtrato
            [CC]\tCriar Conta
            [LC]\tListar Contas
            [CU]\tCriar usuário 
            [Q]\tSair
            ==>""")
        
    def menu(self):
        return input(self._menu)

    def start(self):

        while True:
            choice = self.menu().lower()

            if choice == 'd':
                self.deposit(self._clients)

            elif choice == 's':
                self.withdrawal(self._clients)
            
            elif choice == 'e':
                self.show_extrato(self._clients)
            
            elif choice == "cc":
                account_number = len(self._accounts)+1
                client = super().return_filtered_client(self._clients)
                if not client:
                    print('\n--- Cliente não encontrado, operação encerrada! ---')
                    return
            
                account = ContaCorrente.new_account(client= client, number=account_number)
                self._accounts.append(account)
                client.accounts.append(account)
                print('\n*** Conta criada com sucesso! ***') 

            elif choice == "lc":
                self.account_list(self._accounts)
            
            elif choice ==  "cu":
                cpf = input('Por favor informe o cpf do cliente:\n>')
                client = self.filter_client(cpf, self._clients)
                if client:
                    print('\n--- CPF já cadastrado! ---')
                    return
        
                name = input('Favor informar o nome completo: ')
                born_date = input("Por favor informe a data de nascimento (dd-mm-aaaa): ")
                address = input("Também informe o endereço (logradouro, nro - bairro - cidade/sigla estado):\n>")

                client = PessoaFisica(name = name, born_date = born_date, address = address, cpf= cpf)

                self._clients.append(client)
                print('\n*** Cliente criado com sucessso! ***')

            elif choice == 'q':
                print('\nMuito obrigado por usar nosso sistema!')
                break

            else:
                print('\nOperação inválida. Por favor selecione novamente uma opção válida.')