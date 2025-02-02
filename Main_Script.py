import Pi_Bradford as Pi_Brad

Test_file = "../BetaTest_Day_5_Spreadsheet.xlsx"
Main_file = "../Day_5_Spreadsheet.xlsx"

# * 1. Bradford Assay --------------------------------------------------

x, y, file = Pi_Brad.Parse_Std_Curve(Main_file, "Trial")

Pi_Brad.plot(x, y, "Trial")
