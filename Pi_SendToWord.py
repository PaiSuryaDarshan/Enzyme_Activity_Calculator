# Bradford Assay Functions

from docx import Document
import Pi_Bradford as PB
from datetime import datetime

def MakeTable(doc, df):
    
    # add a table to the end and create a reference variable
    # extra row is so we can add the header row
    t = doc.add_table(df.shape[0]+1, df.shape[1])

    # add the header rows.
    for j in range(df.shape[-1]):
        t.cell(0,j).text = df.columns[j]

    # add the rest of the data frame
    for i in range(df.shape[0]):
        for j in range(df.shape[-1]):
            t.cell(i+1,j).text = str(df.values[i,j])

class Brad:

    def Edit_Brad_temp(df_norm, df_calc, trend, ImageName, savename = f"Brad_{datetime.now().date()}.docx"):

        doc = Document("./Templates/Bradfor_Temp.docx")

        dict_to_replace = {
            '{Date}': f'Date: {datetime.now().date()}',
            '{Time}': f'Time: {datetime.now().time()}',
            '{Table_norm}': MakeTable(doc, df_norm),
            '{Table_calc}': MakeTable(doc, df_calc),
            '{Image_1}': "PLACEHOLDER",
            '{Image_2}': "PLACEHOLDER",
            '{Graph_Eq}': f"y = {trend.slope.round(4)}x + {trend.intercept.round(4)} \n R2 = {trend.rvalue.round(4)}",
            }            
        
        counter = 0
        for paragraph in doc.paragraphs:
            for key in dict_to_replace.keys():
                if f"{key}" in paragraph.text and dict_to_replace[key] != "PLACEHOLDER":
                    print(paragraph.text)
                    paragraph.text = dict_to_replace[key]
                    break

                elif f"{key}" == "{Image_1}" and counter == 0:
                    print(counter)
                    counter += 1
                    paragraph.text = " "
                    p = doc.add_paragraph()
                    r = p.add_run()
                    imagePath = "./Data_Storage/"
                    r.add_picture(imagePath+ImageName+' w.o. Unknown.png')
                    break

                elif f"{key}" == "{Image_2}" and counter == 1:
                    print(counter)
                    counter += 1
                    paragraph.text = " "
                    p = doc.add_paragraph()
                    r = p.add_run()
                    imagePath = "./Data_Storage/"
                    r.add_picture(imagePath+ImageName+' w Unknown.png')
                    break

        doc.save(f"./Output/{savename}")
        
        return
    
if __name__ == "__main__":
    Test_file = "../BetaTest_Day_5_Spreadsheet.xlsx"
    x, y, df, path = PB.Parse_Std_Curve(Test_file)
    # Brad.Edit_Brad_temp(df, "Trial")