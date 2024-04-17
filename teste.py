from functions import SystemAccounts, System

accounts = SystemAccounts()
system = System()

new_user_1 = {
    'cpf': '02902685165',
    'nome_completo': 'Érico Marques Cunha',
    'data_nascimento': '03/07/1993',
    'endereco': 'Rua São Manoel, 1757'
}

new_user_2 = {
    'cpf': '02702685165',
    'nome_completo': 'Paola Winter Silveira',
    'data_nascimento': '22/12/1997',
    'endereco': 'Rua São Manoel, 1757'
}

system.create_user(**new_user_1)
system.create_user(**new_user_2)

system.create_account(new_user_1['cpf'])
system.create_account(new_user_1['cpf'], 100)
system.create_account(new_user_1['cpf'], 300)
system.create_account(new_user_2['cpf'])

# print(system.users)
print(system.list_accounts('2542'))
# print(system.login())

# accounts.create_user(**new_user_1)
# accounts.create_user(**new_user_2)



# user2_account = accounts.create_account(new_user_2['cpf'])

# print(accounts.list_accounts())
# print(accounts.list_accounts(new_user_1['cpf']))


