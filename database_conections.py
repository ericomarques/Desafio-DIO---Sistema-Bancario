import pandas as pd

class DataBaseConnect:
    def __init__(self):
        self.csv_path = 'simple_data.csv'

    def connet(self):
        try:
            return pd.read_csv(self.csv_path)
        except FileNotFoundError:
            return 'Erro ao conectar com o banco de dados'
        
class DataBaseOperations(DataBaseConnect):
    def __init__(self):
        super().__init__()
        self.database = super().connet()
    
    def get_data_list(self):
        return self.database
    
    def get_data_dict(self):
        return self.self.database.to_dict(orient='records')
    
    def get_data(self, name_variable:str = None):
        if not name_variable:
            return self.get_data_list()
        else:
            try:
                # return  self.database[self.database['variable']== name_variable]
                return  self.database.loc[self.database['variable'] == name_variable]['value'].iloc[0]
            except KeyError as e:
                return  f"Erro: {e}.\nNão foi encontrada a variável {name_variable} no banco de dados!"
            
    def update_data(self, value:dict):
        for key, new_value in value.items():
            if key in self.database['variable'].values:
                self.database.loc[self.database['variable'] == key, 'value'] = new_value
                self.database.to_csv(self.csv_path, index=False)
                return f"{key} atualizado para {new_value}"
            else:
                return "Erro na transação"
            
class BankSystem:
    def __init__(self):
        self._users = {}
        self._accounts = {}
        self._next_account_number = 1

    def create_user(self, nome_completo, cpf, data_nascimento, endereco):
        if cpf in self._users:
            return f"Erro: CPF {cpf} já cadastrado."
        self._users[cpf] = {
            "nome_completo": nome_completo,
            "data_nascimento": data_nascimento,
            "endereco": endereco
        }
        return f"Usuário {nome_completo} cadastrado com sucesso."

    def create_account(self, cpf):
        if cpf not in self._users:
            return "Erro: Usuário não encontrado."
        account_number = f"{self._next_account_number:04}"
        self._next_account_number += 1
        if cpf not in self._accounts:
            self._accounts[cpf] = []
        self._accounts[cpf].append({
            "agencia": "0001",
            "conta_corrente": account_number
        })
        return f"Conta {account_number} criada para CPF {cpf}."

    def list_accounts_by_cpf(self, cpf):
        if cpf not in self._accounts:
            return "Nenhuma conta encontrada para este CPF."
        return self._accounts[cpf]