import Pi_Bradford as Pi_Brad

Test_file = "../BetaTest_Day_5_Spreadsheet.xlsx"
Main_file = "../Day_5_Spreadsheet.xlsx"

# * 1. Bradford Assay --------------------------------------------------

print("1. Bradford Assay \n")

x, y, df, unk = Pi_Brad.Parse_Std_Curve(Test_file, "Trial")

trend = Pi_Brad.plot(x, y, "Trial")

Obtained_concentration = Pi_Brad.unknown_calculator_and_plotter(x, y, unk, trend, "Trial")

Fixed_concentration = Obtained_concentration / 20                 # Obtained Concentration / Volume (μl)

print(f"Graph Equation: \n\n\t y={trend.slope:.4f}x + ({trend.intercept:.4f}) with an R² of {trend.rvalue:.4f} \n\n")

print("Concentration of protein = ", Fixed_concentration, " μg/μl. \n")
print()

# * 2. Enzymatic Assay --------------------------------------------------