import Pi_Bradford as Pi_Brad
import Pi_SendToWord as Pi_S2W

Test_file = "../BetaTest_Day_5_Spreadsheet.xlsx"
Main_file = "../Day_5_Spreadsheet.xlsx"

# * 1. Bradford Assay --------------------------------------------------

print("1. Bradford Assay \n")

x, y, df_norm, unk = Pi_Brad.Parse_Std_Curve(Test_file, "Trial")

trend = Pi_Brad.plot(x, y, "Trial")

Obtained_concentration, df_calc = Pi_Brad.unknown_calculator_and_plotter(x, y, unk, trend, "Trial")

print(f"Graph Equation: \n\n\t y={trend.slope:.4f}x + ({trend.intercept:.4f}) with an R² of {trend.rvalue:.4f} \n\n")

print("Concentration of protein = ", Obtained_concentration, " μg/μl. \n")
print()

# Pi_S2W.Brad.Edit_Brad_temp(df_norm, df_calc, trend, "Trial") # TODO: <--- Uncheck to save to doc

# * 2. Enzymatic Assay --------------------------------------------------