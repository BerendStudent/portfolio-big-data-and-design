import pandas as pd

df = pd.read_csv('dotcom-wrapped/data/wrapped_bank_account_1.csv', on_bad_lines="skip")

print(df.loc[0])

exemptions_list = ['spaarrekening']

def checkExemptCategories(string : str):
    '''
    Checks if the transaction description should exempt the transaction from net income and expenses.

    Returns TRUE if the transaction is valid, FALSE if it is exempt
    '''
    string = string.lower()
    wordlist = string.split()
    for word in wordlist:
        if word in exemptions_list:
            return False
    return True

def checkBank(string : str):
    string = string.lower()
    wordlist = string.split()
    for word in wordlist:
        if word == 'spaarrekening':
            print()
            return True
    return False

total_in = df.loc[
    (df['flow'] == 'inflow') & (df['description'].apply(checkExemptCategories)),
    'amount'
].sum()


total_out = df.loc[
    (df['flow'] == 'outflow') & (df['description'].apply(checkExemptCategories)),
    'amount'
].sum()

total_bank = 10000

total_bank_out = df.loc[
    (df['flow'] == 'inflow') & (df['description'].apply(checkBank)),
    'amount'
].sum()

total_bank_in = df.loc[
    (df['flow'] == 'outflow') & (df['description'].apply(checkBank)),
    'amount'
].sum()


print(f"Incomes: {total_in}, outflow: {total_out}")

total_sum = total_in - total_out

print(f"Net change: {total_sum}")

total_bank += (total_bank_in - total_bank_out)

print(f"Money in your account: ${total_bank}")

