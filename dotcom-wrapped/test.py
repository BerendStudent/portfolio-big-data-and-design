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
    
    def getProfits(self, df=None):
        if df is None:
            df = self.data
        
        total_in = self.getRevenue(df)
        total_out = self.getExpenses(df)

        return total_in - total_out
    
    def getCashOnHand(self, date='2100-01-01'):
        '''
        Returns the cash on hand at a specified date. No date specified returns at present moment.

        Arguments:
        date: Date where the cash on hand is requested. Defaults to 2100-01-01 (all transactions on record)
        '''
        df = self.getTransactionsByDateRange('2000-01-01', date)
        total_in = df.loc[df['flow'] == 'inflow','amount'].sum()

        total_out = df.loc[df['flow'] == 'outflow','amount'].sum()

        cash_on_hand = (total_in - total_out) + self.getNetBank()
        return cash_on_hand
    
    def getNetBank(self, accountID=None, df=None):
        if df is None:
            df = self.data
        total_bank_out = df.loc[
            (df['flow'] == 'inflow') & (df['description'].apply(self.checkBank)),
            'amount'
        ].sum()

        total_bank_in = df.loc[
            (df['flow'] == 'outflow') & (df['description'].apply(self.checkBank)),
            'amount'
        ].sum()
        return total_bank_in - total_bank_out

    def getTransactionsByDescription(self, description: str, df=None):
        if df is None:
            df = self.data
        description = description.lower()
        words = description.split()

        mask = df["description"].astype(str).str.lower().apply(
            lambda text: all(word in text for word in words)
        )

        return df[mask]

    def checkColumnByString(self, category: str, string: str, strict=False, df=None):
        if df is None:
            df = self.data
        string = string.lower()

        if strict:
            return any(str(row[category]).lower() == string for _, row in df.iterrows())
        else:
            words = string.split()
            return any(all(word in str(row[category]).lower() for word in words)
                    for _, row in df.iterrows())

    def getTransactionsByDateRange(self, start: str, end: str, df=None):
        if df is None:
            df = self.data
        df['booking_date'] = pd.to_datetime(df['booking_date'])
        begin_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)

        if begin_date > end_date:
            raise ValueError("Start date must be before end date")
        
        return df[(df['booking_date'] >= start) & (df['booking_date'] <= end)]

    def getTransactionsByBankAccount(self, relation_iban : str, df=None):
        if df is None:
            df=self.data
        return df[df["relation_iban"] == relation_iban]
    
    def getRevenue(self, df=None):
        revenue = 0

        if df is None:
            df = self.data

        revenue = df.loc[
            (df['flow'] == 'inflow') & (df['description'].apply(self.checkExemptions)),
            'amount'
        ].sum()

        return revenue
    
    def getExpenses(self, df=None):
        expenses = 0
        if df is None:
            df = self.data
        
        expenses = df.loc[
            (df['flow'] == 'outflow') & (df['description'].apply(self.checkExemptions)),
            'amount'
        ].sum()

        return expenses

    def getRevenueChange(self):

        return
    
    def topCustomersByMoneyFlow(self, df=None, num = 3, dir = 'in'):
        '''
        Function for getting the total amount of money going in or out. 

        Arguments:
        df: Dataframe of relevant transactions. Defaults to all.
        num: Number of customers to return. Defaults to 3.
        dir: Direction of money flow. Accepts 'in' or 'out'. Defaults to 'in'
        '''
        customers = {}
        
        if df is None:
            df = self.data

        for _, row in df.iterrows():
            if row['relation_iban'] not in customers:
                customers[row['relation_iban']] = 0
        
        for id in customers:
            transactions = self.getTransactionsByBankAccount(id, df)
            if dir == 'in':
                flow = self.getRevenue(transactions)
            elif dir == 'out':
                flow = self.getExpenses(transactions)
            else:
                raise Exception("Invalid direction in topCustomersByMoneyFlow. Accepted directions: 'in', 'out'.")
            
            customers[id] = int(flow)
        
        sorted_customers = sorted(customers.items(), key=lambda item: item[1], reverse=True)

        return dict(sorted_customers[:num])
    

    def getTransactionsByCategory(self, category : str, df=None):
        if df is None:
            df = self.data

        df = df.loc[df['category'] == category]

        return df
    
    def getExpensesByCategory(self, df=None):
        if df is None:
            df = self.data

        expenses = {}

        for _, row in df.iterrows():
            if row['category'] not in expenses:
                expenses[row['category']] = 0

        for id in expenses:
            transactions = self.getTransactionsByCategory(id, df)
            flow = self.getExpenses(transactions)
            expenses[id] = int(flow)
        
        sorted_expenses = sorted(expenses.items(), key=lambda item: item[1], reverse=True)

        return dict(sorted_expenses)

    def getAverageExpenses(self, start: str = '2000-01-01', end: str = '2100-01-01', df=None):
        if df is None:
            df = self.data

        begin_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)

        subset = self.getTransactionsByDateRange(start, end, df)

        expenses = self.getExpenses(subset)

        months = (end_date.year - begin_date.year) * 12 + (end_date.month - begin_date.month) + 1

        return expenses / months if months > 0 else 0

    def getAverageMonthlyExpenses(self, start: str = '2000-01-01', end: str = '2100-01-01', df=None):
        if df is None:
            df = self.data

        subset = self.getTransactionsByDateRange(start, end, df).copy()

        subset["booking_date"] = pd.to_datetime(subset["booking_date"])

        subset["year_month"] = subset["booking_date"].dt.to_period("M").astype(str)

        monthly_expenses = {}

        for year_month in subset["year_month"].unique():
            month_df = subset[subset["year_month"] == year_month]

            expense_value = self.getExpenses(month_df)
            monthly_expenses[year_month] = int(expense_value)

        total_value = 0
        months = 0

        for month in monthly_expenses:
            total_value += monthly_expenses[month]
            months += 1
        
        average = total_value / months

        return average




Account = MoneyChecker(df)

#print(Account.getProfits())

#print(Account.getTransactionsByDescription('Badkamer'))

#print(Account.getTransactionsByDateRange('2024-01-01', '2024-12-31'))

#transactions_2024 = Account.getTransactionsByDateRange('2024-01-01', '2024-12-31')

#print(Account.getProfits(transactions_2024))

#print(Account.getCashOnHand('2025-01-01'))

#print(Account.getTransactionsByBankAccount('xxxxxx'))

#print(Account.getRevenue(Account.getTransactionsByDateRange('2024-01-01', '2024-02-01')))

#print(Account.topCustomersByMoneyFlow())

#print(Account.getExpenses((Account.getTransactionsByDateRange('2024-01-01', '2024-02-01'))))

#print(Account.getExpensesByCategory())

#print(Account.getExpenses(Account.getTransactionsByDescription('Drankenspeciali')))

print(Account.getAverageMonthlyExpenses())