from database_conections import DataBaseOperations

class ManageLimits(DataBaseOperations):
    def __init__(self):
        super().__init__()
        self.limit_draft = super().get_data('draft_limit')
        self.used_draft = 0
        self.max_per_withdrawal = super().get_data('limit_per_withdrawal')
        self.balance = super().get_data('balance')
    
    def useDraf(self):
        self.used_draft += 1
        return self.used_draft
    
    def checkWithdrawal(self, value):
        if self.used_draft <= self.limit_draft:
            if value <= self.max_per_withdrawal:
                return True
            elif value > self.max_per_withdrawal:
                return f'O limite de saque por vez é de {self.max_per_withdrawal} e {value} excede esse limite.'
            elif self.balance < value:
                return f'Saldo insuficiente. seu saldo atual é {self.balance}'
        else:
            return f'Limite de saques diários execido. O limite é {self.used_draft}'
        
    def validValue(self, value):
        if value  > 0 and isinstance(value, (int,float)):
            return True
        else:
            return f'Valor inválido, favor tentar novamente'

class MenuOperations(DataBaseOperations):
    def __init__(self):
        super().__init__()
        self.manage_limits = ManageLimits()

    def choice_manager(self, choice):
        if choice == 'd':
            value = float(input("Por favor informe o valor do depósito: \nR$ "))
            return self.deposit(value)
        elif choice == 's':
            value = float(input("Por favor informe o valor do saque: \nR$ "))
            return  self.withdrawal(value)
        elif choice == 'e':
            return self.show_balance()
        elif choice == 'q':
            return 'quit'
        else:
            return  "Opção Inválida! Por favor tente novamente."
        
    def withdrawal(self, value):
        valid_value = self.manage_limits.validValue(value)
        possible_withdrawal = self.manage_limits.checkWithdrawal(value)
        if valid_value:
            if possible_withdrawal:
                new_balance = self.manage_limits.balance - value
                response = super().update_data({'balance': new_balance})
                if response != 'Erro na transação':
                    response.replace('balance', 'Saldo')
                    self.manage_limits.used_draft()
            else:
                response = possible_withdrawal
        else:
            response = valid_value
        return response
    
    def deposit(self, value):
        if value > 0:
            balance = super().get_data('balance')
            new_balance = float(balance) + value
            response = super().update_data({'balance': new_balance})
            if 'balance' in response:
                response.replace('balance', 'Saldo')
            return response
        return "Erro na transação, por favor  tente novamente!"
    
    def show_balance(self):
        balance = super().get_data('balance')
        return f"Seu saldo é de R$ {balance}"
            
class System:
    def __init__(self):
        self.manager_menu = MenuOperations()
        self.menu = """
            [D] - Depositar
            [S] - Sacar
            [E] - Extrato
            [Q] - Sair
            ==>"""

        self.extrato = ''
        self.DRAFT_LIMIT = 3

    def start(self):
        print("""
            Olá obrigado por escolher o banco X
            Por favor escolha uma das opções abaixo:""")
        while True:
            choice = input(self.menu)
            result = self.manager_menu.choice_manager(choice.lower())
            if result ==  'quit':
                print("""
            Obrigado por usar nosso sistema""")
                break
            else:
                print(result)