import pandas as pd


def import_data(path):
    py_data = pd.read_csv(path + 'pY.csv')
    pst_data = pd.read_csv(path + 'pST.csv')
    global_data = pd.read_csv(path + 'global.csv')

    sup_data = pd.read_csv(path + 'G_F1.csv')

    py_pep_data = pd.read_csv(path + 'pY_pepgroup.csv')
    pst_pep_data = pd.read_csv(path + 'pST_pepgroup.csv')

    return py_data, pst_data, global_data, sup_data, py_pep_data, pst_pep_data
