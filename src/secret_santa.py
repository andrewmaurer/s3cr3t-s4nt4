import pandas as pd

# step 1: read in names and addresses
data_path = 'data/input.csv'
data = pd.read_csv( data_path )

# step 2: duplicate names and addresses, change column names to specify it's a partner's info, save the new column names
partners = data.copy()
shuffle_cols = 'partner_' + data.columns
partners.columns = shuffle_cols

# step 3: combine horizontally
partners = pd.concat( [data, partners], axis=1 )

# step 4: define a helper function to check for rule breaking
def unacceptable( df ):
    # can't be your own partner
    if ( df.name == df.partner_name ).sum() > 0:
        return True
    # can't get your spouse
    if ( df.spouse == df.partner_name ).sum() > 0:
        return True
    # can't get a gift for someone you live with
    if ( df.household == df.partner_household ).sum() > 0:
        return True
    return False

# step 5: randomly choose partners. if it breaks the rules, try again.
while unacceptable( partners ):
    partners[ shuffle_cols ] = partners[ shuffle_cols ].sample( frac=1 ).reset_index( drop=True )

# step 6: save the results to a new file
partners.to_csv('data/output.csv', index=False)