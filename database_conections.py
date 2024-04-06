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