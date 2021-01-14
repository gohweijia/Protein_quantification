import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import time
import datetime
import sys
import os

protein_dilution_factor = 75
filename = input("Enter file name (excluding '.xlsx'): ")
filename = filename + '.xlsx'

def load_file(filename):
    """
    Loads excel file output from BSA absorbance assay.
    Returns dataframe containing absorbance values.
    """
    
    df = pd.read_excel(filename, skiprows=28, nrows=8, sheet_name='Sheet2', index_col=None, header=None)#, u#secols='A:H')
    df.dropna(inplace=True, axis=1)
    lane_names = [f'Lane {str(i)}' for i in range(1, len(df.columns) - 2)]
    col_names = ['well', 'standard_1'] + lane_names + ['standard_2']
    df.columns = col_names
    df = df.set_index('well')
    df['standard_absorbance'] = (df.standard_1 + df.standard_2) / 2
    df = df.drop(['standard_1', 'standard_2'], axis=1)
    return df


def get_concentrations(df):
    # Prompt for concentration values
    print("The default concentration values are [0, 20, 40, 60, 80, 100, 150, 200].")
    print("To use a new set of values, enter space-separated concentration values. Otherwise, press enter.")
    conc = np.array([0, 20, 40, 60, 80, 100, 150, 200])
    inp = input()
    while True:
        if inp == "":
            #df['conc'] = [0, 20, 40, 60, 80, 100, 150, 200]
            break
        conc = np.array([int(i) for i in inp.split()])
        if len(conc) == 8:
            break
        print("Your input values are:\n")
        print(conc)
        print("Error: there are {} expected values, please try again. Press enter again to use default values".format(len(df.standard_absorbance)))
        inp = input()
    df = df.reset_index().drop('well', axis=1)
    s_abs = df.pop('standard_absorbance')
    samples = np.concatenate([df[column].values for column in df.columns])
    return samples, s_abs, conc


def calc_protein(samples, factor, m, c):
    #os.system('cls' if os.name == 'nt' else 'clear')
    sample_concentrations = (samples - c) / m * factor
    df = pd.DataFrame()
    df['Sample_index'] = np.arange(1, len(sample_concentrations) + 1)
    df['sample_conc'] = sample_concentrations
    df["10µg (µl)"] = np.round(10 / (sample_concentrations / 1000), 1)# volume in µl containing 10 µg of protein
    df["15µg (µl)"] = np.round(15 / (sample_concentrations / 1000), 1)
    df["20µg (µl)"] = np.round(20 / (sample_concentrations / 1000), 1)
    return df


def plot_standard(x, y, m, c, output_dir):
    plt.figure()
    plt.plot(x, y, 'bo')
    plt.plot(x, m * x + c, 'r-')
    plt.xlabel("Concentration")
    plt.ylabel("Absorbance")
    plt.title("Best fit line with intercept")
    print("Line equation: y = {}x + {}".format(m, c))
    plt.savefig(os.path.join(output_dir, 'plot.png'))
    print(f"Plot saved in {output_dir}")


if __name__ == "__main__":
    df = load_file(filename)
    samples, sample_absorbance, concentration = get_concentrations(df)
    x = concentration
    y = sample_absorbance
    m, c, _, _, _ = stats.linregress(x,y)
    df = calc_protein(samples, protein_dilution_factor, m, c)
    save_name = datetime.datetime.strftime(datetime.datetime.now(), "%d%b%y_BSA.csv")
    output_dir = os.path.join(os.getcwd(), datetime.datetime.strftime(datetime.datetime.now(), "%d%b%y_BSA"))
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, save_name), index=False)
    print('Results saved as in {}.'.format(output_dir))
    plot_standard(x, y, m, c, output_dir)
    
