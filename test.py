import pandas as pd


def delete_d(del_d):
    df = pd.read_csv('directories.csv', index_col=0)
    try:
        # Prompt user if they want to delete directory
        prompt_msg = df.loc[del_d].values.tolist()
        prompt_msg.insert(0, del_d)
        while True:
            print(prompt_msg)
            check = input('Do you wish to remove? (Y/N): ')
            check = check.upper()
            if check == 'Y':
                df = df.drop(del_d)
                df.to_csv(r'directories.csv')
                print('\'{name}\' successfully removed'.format(name=del_d))
                break
            if check == 'N':
                print('Operation canceled')
                break
    except KeyError:
        print('\'{name}\' not found'.format(name=del_d))
        exit()

delete_d('yo')