import pandas as pd

df = pd.read_csv('dotcom-wrapped/data/wrapped_bank_account_1.csv', on_bad_lines="skip")

class MoneyChecker:
    '''
    Wrapper class for calculations

    data argument accepts pandas dataframe
    '''

    exemptionslist = ['spaarrekening']

    def __init__(self, data):
        self.data = data
    
    def checkBank(self, string : str):
        string = string.lower()
        wordlist = string.split()
        for word in wordlist:
            if word == 'spaarrekening':
                print()
                return True
        return False

    def checkExemptions(self, string : str):
        '''
        Checks if the transaction description should exempt the transaction from net income and expenses.

        Returns TRUE if the transaction is valid, FALSE if it is exempt
        '''
        string = string.lower()
        wordlist = string.split()
        for word in wordlist:
            if word in self.exemptionslist:
                return False
        return True
    
    def getProfits(self):
        df = self.data
        total_in = df.loc[
            (df['flow'] == 'inflow') & (df['description'].apply(self.checkExemptions)),
            'amount'
        ].sum()


        total_out = df.loc[
            (df['flow'] == 'outflow') & (df['description'].apply(self.checkExemptions)),
            'amount'
        ].sum()
        return total_in - total_out
    
    def getCashOnHand(self):
        return
    
    def getNetBank(self, accountID : str):
        total_bank_out = df.loc[
            (df['flow'] == 'inflow') & (df['description'].apply(self.checkBank)),
            'amount'
        ].sum()

        total_bank_in = df.loc[
            (df['flow'] == 'outflow') & (df['description'].apply(self.checkBank)),
            'amount'
        ].sum()
        return total_bank_in - total_bank_out

    def getTransactionsByDescription(self, description : str):
        
        return 0
    
    def checkColumnByString(self, category : str, string : str, strict = False):
        if strict:
            for index, row in df.iterrows():
                if row[category] == string:
                    return True
            return False
        else:
            string = string.lower()
            wordlist = string.split()
            for index, row in df.iterrows():
                for word in wordlist:
                    if word in row[category]:
                        return True
            return False
    

Account = MoneyChecker(df)

print(Account.getProfits())