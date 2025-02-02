# Bradford Assay Functions

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from scipy import stats
# import pylustrator as pl

# pl.start()

Test_file = "../BetaTest_Day_5_Spreadsheet.xlsx"

def Parse_Std_Curve(FilePath, table_name="Bradford"):

    """Extracts Data
    converts it to iterable dataframe objects.
    converts it to data required for plotting.
    also returns an image file of the tabulated format of the df

    Args:
        FilePath (str): _description_

    Returns:
        Pandas.Dataframe object

    Returns:
        x, y, image
    """

    # Converts it to iterable dataframe objects.
    df_conditions_raw = pd.read_excel(FilePath, sheet_name="Standard Curve", 
                   usecols='A:G', engine='openpyxl', header=3, nrows=4)

    df_Obtained_raw   = pd.read_excel(FilePath, sheet_name="Standard Curve", 
                   usecols='A:B', engine='openpyxl', header=9, nrows=7)
    
    df_conditions = df_conditions_raw.transpose()

    df_Obtained   = df_Obtained_raw

    # Converts data to array required for plotting
    initial_prot_conc = df_Obtained.iloc[:, 0].to_numpy()

    # Normalised concentrations
    Total_volume = df_conditions.iloc[1:, -1].to_numpy()

    prot_conc_norm = (initial_prot_conc/Total_volume)*2                 # x     #! Might need to be multiplied by 2
    absorbance = df_Obtained.iloc[:,1].to_numpy()                   # y

    # generate an image file of the tabulated format of the df
    table_path = "./Data_Storage/"
    table_name = table_name

    table_dict = ({"protein intial": initial_prot_conc, "protein normalised": prot_conc_norm, "absorbance":absorbance})
    df_for_table = pd.DataFrame(table_dict)

    f = open(f"{table_path+table_name}.txt", "w")
    f.write(tabulate(df_for_table, headers='keys', tablefmt="fancy_outline"))
    f.close()

    table_file_path = table_path+table_name

    return prot_conc_norm, absorbance, table_file_path

def plot(x, y, plot_name="Bradford", show_flag=0):

    """
    Plots Data,
    plots linreg,
    returns Graph descriptors:
        slope,
        intercept,
        rvalue,
        pvalue,
        stderr,
        intercept_stderr. (Specifically in tht order)

    Args:
        FilePath (str): _description_
        Plot_name (str): _description_

    Returns:
        Pandas.Dataframe object

    Returns:
        image_path, equation
    """

    # Find linreg

    trend = stats.linregress(x.astype(float), y.astype(float))

    print("")
    print("Slope of the line is",        trend.slope)
    print("Intercept of the line is",    trend.intercept)
    print("Correlation of the line is",  trend.rvalue)
    print("pvalue of the line is",       trend.pvalue)
    print("Standard dev of the line is", trend.stderr)
    print("")

    fit_line = trend.slope * x + trend.intercept

    # Plot Data + linreg
    # title
    plt.title("Bradford Assay (OD at 595nm)", fontsize=20)
    # axis Labels
    plt.xlabel("Protein Concentration", fontsize=16)
    plt.ylabel("Absorbance", fontsize=16)
    # Graph equations
    x_loc_of_graph_eq = (x[1] - x[1]/20)
    y_loc_of_graph_eq = (y[-1] - y[-1]/20)
    plt.text(x_loc_of_graph_eq, y_loc_of_graph_eq, f"y = {trend.slope.round(3)}x + {trend.intercept.round(3)} \n R² = {trend.rvalue.round(4)}")
    # plots
    plt.plot(x, fit_line, label="best", color="red", linestyle='--', alpha=0.85)
    plt.scatter(x, y)
    # legend
    plt.legend()
    # store current figure
    fig1 = plt.gcf()
    
    if show_flag == 0:
        pass
    elif show_flag == 1:
        plt.show()
    
    fig1.savefig(f"./Data_Storage/{plot_name}.png", dpi=600)

    # return equation

    # 
    
    return trend






if __name__ == "__main__":
    x, y, file = Parse_Std_Curve(Test_file)
    plot(x, y, show_flag=1)