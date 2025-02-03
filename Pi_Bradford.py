# Bradford Assay Functions

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from scipy import linalg
from scipy import stats

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
        x, y, image, unknown
    """

    # Converts it to iterable dataframe objects.
    df_conditions_raw = pd.read_excel(FilePath, sheet_name="Standard Curve", 
                   usecols='A:G', engine='openpyxl', header=3, nrows=4)

    df_Obtained_raw   = pd.read_excel(FilePath, sheet_name="Standard Curve", 
                   usecols='A:B', engine='openpyxl', header=9, nrows=7)
    
    unknown_conc_raw  = pd.read_excel(FilePath, sheet_name="Standard Curve", 
                   usecols='B', engine='openpyxl', header=27)
    
    unknown_conc      = unknown_conc_raw.to_numpy()
                                      
    df_conditions = df_conditions_raw.transpose()

    df_Obtained   = df_Obtained_raw

    # Converts data to array required for plotting
    initial_prot_conc = df_Obtained.iloc[:, 0].to_numpy()

    # Normalised concentration (μg/ml)s

    prot_conc_norm = (initial_prot_conc/1000) * 2                 # x     #! Might need to be multiplied by 2
    absorbance = df_Obtained.iloc[:,1].to_numpy()                   # y

    # generate an image file of the tabulated format of the df
    table_path = "./Data_Storage/"
    table_name = table_name

    table_dict = ({"protein intial": initial_prot_conc, "protein normalised": prot_conc_norm, "absorbance":absorbance})
    df_for_table = pd.DataFrame(table_dict)

    f = open(f"{table_path+table_name}.txt", "w")
    f.write(tabulate(df_for_table, headers='keys', tablefmt="fancy_outline"))
    f.close()

    table_file_df = df_for_table

    return prot_conc_norm, absorbance, table_file_df, unknown_conc

def Graph_Styling(axis):

    # UNIFORM STYLING FOR ALL GRAPHS
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.get_xaxis().tick_bottom()
    axis.get_yaxis().tick_left()
    axis.plot(0, 1, "^k", transform=axis.transAxes, clip_on=False)
    axis.plot(1, 0, ">k", transform=axis.transAxes, clip_on=False)

    return

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

    if __name__ == "__main__":
        print("")
        print("Slope of the line is",        trend.slope)
        print("Intercept of the line is",    trend.intercept)
        print("Correlation of the line is",  trend.rvalue)
        print("pvalue of the line is",       trend.pvalue)
        print("Standard dev of the line is", trend.stderr)
        print("")

    fit_line = trend.slope * x + trend.intercept

    # Plot Data + linreg

    fig1, ax1 = plt.subplots()

    # title
    # ax1.set_title("Bradford Assay (OD at 595nm)", fontsize=20)
    # axis Labels
    ax1.set_xlabel("Protein Concentration (μg/ml)", fontsize=12)
    ax1.set_ylabel("Absorbance (abs. unit)", fontsize=12)
    # Graph equations
    x_loc_of_graph_eq = (x[1] + x[1]/3)
    y_loc_of_graph_eq = (y[-1] - y[-1]/20)
        # Sign Correction
    if '-' in f"{trend.intercept}":
        ax1.text(x_loc_of_graph_eq, y_loc_of_graph_eq, f"y = {trend.slope.round(3)}x - {abs(trend.intercept.round(3))} \n    R² = {trend.rvalue.round(4)}")
    else: 
        ax1.text(x_loc_of_graph_eq, y_loc_of_graph_eq, f"y = {trend.slope.round(3)}x + {trend.intercept.round(3)} \n    R² = {trend.rvalue.round(4)}")
    # plots
    ax1.plot(x, fit_line, label="Linear Fit", color="red", linestyle='--', alpha=0.85)
    ax1.scatter(x, y, color="k", label="Data Points")
    # legend
    ax1.legend()

    # Styling
    Graph_Styling(ax1)
    
    plot_name_unk = plot_name + " w.o. Unknown"
    fig1.savefig(f"./Data_Storage/{plot_name_unk}.png", dpi=600)

    if show_flag == 0:
        pass
    elif show_flag == 1:
        plt.show()

    # return equation

    #  returns Graph descriptors:
        # slope,
        # intercept,
        # rvalue,
        # pvalue,
        # stderr,
        # intercept_stderr. (Specifically in tht order)
    
    return trend

def Equation_solver(unknown, trend):
    """
    Solves simple Bradford Eqaution

    Takes trend,
    Takes unknown,
    returns Normalised values and Denormalised values as array
    """

    # y = mx+c
    # x = (y-c)/m

    list_of_calculations_norm = []
    list_of_calculations_denorm = []

    if len(unknown) != 0:
        for unk in unknown:
            Normalised_ans   = (unk - trend.intercept) / trend.slope
            Denormalised_ans = (Normalised_ans * 1000)/2
            list_of_calculations_norm.append(Normalised_ans)
            list_of_calculations_denorm.append(Denormalised_ans)
    else:
        print("No unknown values were found, defaulted to 0.5")
        unknown = [0.5]
        for unk in unknown:
            Normalised_ans   = (unk - trend.intercept) / trend.slope
            Denormalised_ans = (Normalised_ans * 1000)/2
            list_of_calculations_norm.append(Normalised_ans)
            list_of_calculations_denorm.append(Denormalised_ans)

    # convert list to arrays
    calculations_norm   = np.array(list_of_calculations_norm)
    calculations_denorm = np.array(list_of_calculations_denorm)

    return calculations_norm, calculations_denorm

def unknown_calculator_and_plotter(x, y, unknown, trend, plot_name="Bradford", show_flag=0):
    """
    Takes unknown(s), 
    plots unknown on bradford assay,
    return calculated unknown.
    """

    calculations_norm, calculations_denorm = Equation_solver(unknown, trend)

    x_unk = calculations_norm
    y_unk = unknown
    values_unk = calculations_denorm

    fit_line = trend.slope * x + trend.intercept

    fig2, ax2 = plt.subplots()
    
    # title
    # ax2.set_title("Bradford Assay (OD at 595nm)", fontsize=20)
    # axis Labels
    ax2.set_xlabel("Protein Concentration (μg/ml)", fontsize=12)
    ax2.set_ylabel("Absorbance (abs. unit)", fontsize=12)
    # Graph equations
    x_loc_of_graph_eq = (x[1] + x[1]/3)
    y_loc_of_graph_eq = (y[-1] - y[-1]/20)
    # Sign Correction
    if '-' in f"{trend.intercept}":
        ax2.text(x_loc_of_graph_eq, y_loc_of_graph_eq, f"y = {trend.slope.round(3)}x - {abs(trend.intercept.round(3))} \n    R² = {trend.rvalue.round(4)}")
    else: 
        ax2.text(x_loc_of_graph_eq, y_loc_of_graph_eq, f"y = {trend.slope.round(3)}x + {trend.intercept.round(3)} \n    R² = {trend.rvalue.round(4)}")
    # plots
    ax2.plot(x, fit_line, label="Linear Fit", color="red", linestyle='--', alpha=0.85)
    ax2.scatter(x, y, color="k", label="BSA Points")
    ax2.scatter(x_unk[:-1], y_unk[:-1], color="blue", marker="^", label="1 - 8", alpha=0.15)
    ax2.scatter(x_unk[-1], y_unk[-1], color="green", marker="^", label="Conc. ADH")
    # legend
    ax2.legend()

    # Styling
    Graph_Styling(ax2)

    plot_name_kn = plot_name+" w Unknown"
    fig2.savefig(f"./Data_Storage/{plot_name_kn}.png", dpi=600)

    if show_flag == 0:
        pass
    elif show_flag == 1:
        plt.show()

    return calculations_denorm

if __name__ == "__main__":
    x, y, file, unk = Parse_Std_Curve(Test_file)
    trend = plot(x, y, show_flag=0)
    unknown_calculator_and_plotter(x, y, unk, trend)