import textwrap

class SystemData:
    def __init__(self):
        self._withdrawal_limit = 3
        self._limit_per_withdrawal = 500

    @property
    def withdrawal_limit(self):
        return self._withdrawal_limit
    
    def decrease_withdrawal_limit(self):
        self._withdrawal_limit -= 1
    
    def reset_withdrawal_limit(self, new_limit):
        self._withdrawal_limit = new_limit

    @property
    def limit_per_withdrawal(self):
        return self._limit_per_withdrawal
    
    @limit_per_withdrawal.setter
    def limit_per_withdrawal(self, value):
        self._limit_per_withdrawal = value
    
class SystemUsers:
    def __init__(self):
        self._users = {}

    @property
    def users(self):
        return self._users
    
    def add_user(self):
        nome_completo = input('Por favor digite  o seu nome completo:\n>')
        data_nascimento = input('Por favor digite a data do seu nascimento no formato  DD/MM/AAAA:\n>')
        endereco = input('Por favor digite o seu endereço no formato Logadouro, número, bairro, cidade, uf:\n>')
        cpf = str(input('Por favor digite seu CPF (somente os números):\n>'))

        return self.save_user(**{
            'nome_completo': nome_completo,
            'cpf': cpf,
            'data_nascimento': data_nascimento,
            'endereco': endereco
        })
        

    def save_user(self, **new_user):
        required_key = {'nome_completo', 'cpf', 'data_nascimento', 'endereco'}
        if not required_key <= new_user.keys():
            missing_keys = required_key - new_user.keys()
            return {'error': f'Faltam os seguintes dados:\n'+'\n'.join(f'- {key}' for key in missing_keys)}
        
        cpf = new_user['cpf']
        if cpf in self._users:
            return {'error': f'CPF {cpf} já cadastrado.'}
        
        self._users[cpf] = {
            'nome_completo': new_user['nome_completo'],
            'data_nascimento': new_user['data_nascimento'],
            'endereco': new_user['endereco']
        }
    
        return {'message':f'Usuário {new_user["nome_completo"]} cadastrado com sucesso.'}

class SystemAccounts(SystemUsers):
    def __init__(self):
        super().__init__()
        self._accounts = {}
        self._next_account_number = 1

    def create_account(self, cpf, balance = 0):
        if cpf not in self._users:
            return {'error': 'CPF não cadastrado. Favor considere  o cadastro do usuário.'}

        nome_usuario = self._users[cpf]['nome_completo']
        account_number = f'{self._next_account_number:04}'

        if cpf not in self._accounts:
            self._accounts[cpf] = []
        self._accounts[cpf].append({
            'agencia': '0001',
            'conta_corrente': account_number,
            'balance': balance,
            'extrato': ''
        })
        self._next_account_number += 1

        return {'message': f'Conta {account_number} criada com o usuário {nome_usuario}.'}

    def list_accounts(self, cpf=None):
        if cpf is None:
            return self._accounts
        else:
            try:
                return self._accounts[cpf]
            except KeyError:
                return {'error':'CPF não encontrado'}
        
class MenuOperations():
    def extrato(self, acc_list:list, account):
        for acc in acc_list:
            if acc['conta_corrente'] == account:
                top_extrato = 'Extrato conta corrente relacionado à conta {account}'
                middle_extrato = acc['extrato']
                botton_extrato = self.balance(acc_list, account)
                return {'message': f'{top_extrato}\n\n{middle_extrato}\n\n{botton_extrato}'}    
        return {'error': 'Conta corrente não encontrada, por favor tente novamente'}

    def deposit(self, acc_list:list, account, value:float):
        for acc in acc_list:
            if acc['conta_corrente'] == account:
                acc['balance'] += value
                acc['extrato'] += f'\n'+ '+ \tR$\t{value:.2f}'
                return {'message': f'Depósito de R$ {value:.2f} efetuado com sucesso'}    
        return {'error': 'Conta corrente não encontrada, por favor tente novamente'}

    def withdrawal(self, acc_list:list, account, value:float):
        for acc in acc_list:
            if acc['conta_corrente'] == account:
                if  acc['balance'] >= value:
                    acc['balance'] -= value
                    acc['extrato'] += f'\n'+ '- \tR$\t{value:.2f}'
                    return {'message': f'Saque de R$ {value:.2f} efetuado com sucesso'}
                else:
                    return {'error': f'Saldo insuficiente:\t R${acc["balance"]:.2f}'}
        return {'error': 'Conta corrente não encontrada, por favor tente novamente'}
    
    def balance(self, acc_list:list, account):
        for acc in acc_list:
            if acc['conta_corrente'] == account:
                return {'message': f'Seu saldo é de R$ {acc["balance"]:.2f}'}
        return {'error': 'Conta corrente não encontrada, por favor tente novamente'}
            
class System(SystemData, SystemAccounts):
    def __init__(self):
        SystemData.__init__(self)
        SystemAccounts.__init__(self)
        self.manager_options = MenuOperations()
        self._menu = textwrap.dedent("""
            [D]\tDepositar
            [S]\tSacar
            [E]\tExtrato
            [CC]\tCriar Conta
            [LC]\tListar Contas
            [CU]\tCriar usuário 
            [Q]\tSair
            ==>""")

    def validate_withdrawal(self, value):
        message = ''
        valid = True
        withdrawal_value_limit = self.limit_per_withdrawal>= value
        withdrawal_credit = self.withdrawal_limit > 0

        if not withdrawal_value_limit:
            message += f'\nValor acima do limite permitido por saque. O limite é de R$ {self.limit_per_withdrawal:.2f}'
            valid = False
        if not withdrawal_credit:
            message += f'\nQuantidade de saque diário excedido. Tente a operação novamente amanhã'
            valid = False
        
        return {'valid': valid, 'message': message}
    
    def login(self):
        print(textwrap.dedent("""
            Olá obrigado por escolher o banco X""")
        )
        cpf = input('Por favor digite seu CPF ou digite [Q] para sair:\n>')

        if cpf not in self.users or cpf == None:
            print('CPF não cadastrado ainda, favor realizar o cadastro')
        elif cpf.lower() == 'q':
            return False

        cadastro = input('Deseja fazer o cadastro? \n\n[S]\tSIM\n[N]\tNÃO\n[Q]\tSAIR\n>').lower()
        if cadastro == 's':
            new_user = self.add_user
            try:
                print(new_user['message'])
                return True
            except:
                print(new_user['error'])
        return False


    def manage_choices(self, choice, cpf):
        accounts = self.list_accounts(cpf)

        def choice_account(cpf, accounts):
            if not accounts['error']:
                message = 'Contas do usuário:\n\n'
                for acc in accounts:
                    message += f'- {acc["conta_corrente"]}\t\t Saldo: R$ {acc["balance"]:.2f}\n'
                print(message)
                account = input('Por favor digite o número da conta que quer operar:\n\n>')    
                return account
            else:
                return accounts

        if choice == 'd':
            try:
                acc = choice_account(cpf, accounts)
                value = float(input("Por favor informe o valor do depósito: \nR$ "))
                return self.manager_options.deposit(accounts,acc, value)
            except ValueError as e:
                return {'error':'Valor inválido.\nTente novamente.\n{e}'}
            
        elif choice == 's':
            try:
                acc = choice_account(cpf, accounts)
                value = float(input("Por favor informe o valor do saque: \nR$ "))
                validation = self.validate_withdrawal(value)

                if validation['valid']:
                    return self.manager_options.withdrawal(accounts, acc, value)
                return  validation['message']
            except ValueError as e:
                return {'error':'Valor inválido.\nTente novamente.\n{e}'}
            
        elif choice == 'e':
            acc = choice_account(cpf, accounts)
            return self.manager_options.extrato(accounts, acc)
        
        elif choice == 'cc':
            return self.create_account(cpf)
        
        elif choice == 'lc':
            if not accounts['error']:
                message = 'Contas do usuário:\n\n'
                for acc in accounts:
                    message += f'- {acc["conta_corrente"]}\t\t Saldo: R$ {acc["balance"]:.2f}\n'  
                return message
            else:
                return accounts
    
        elif choice == 'cu':
            new_user = self.add_user()
            return new_user
        
        elif choice == 'q':
            return 'quit'
        
        else:
            return  "Opção Inválida! Por favor tente novamente."

    def start(self):
        print(textwrap.dedent("""
            Olá obrigado por escolher o banco X\n""")
        )
        
        cpf = input('Por favor digite seu CPF: ')
        
        while True:
            print('Por favor escolha uma das opções abaixo')
            choice = input(self._menu)
            result = self.manage_choices(choice.lower(), cpf)
            if result ==  'quit':
                print(textwrap.dedent("""
                    Obrigado por usar nosso sistema""")
                )
                break
            else:
                print(result['message'] or  result['error'])