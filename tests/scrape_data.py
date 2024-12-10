import os
import pandas as pd
from openpyxl import load_workbook


def adjust_column_widths(excel_file):
    try:
        # Load the workbook and the first sheet
        wb = load_workbook(excel_file)
        sheet = wb.active
        
        # Iterate through each column and adjust the width based on the max length of the values
        for col in sheet.columns:
            max_length = 0
            column = col[0].column_letter  # Get the column name (e.g., 'A')
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            sheet.column_dimensions[column].width = adjusted_width
        
        # Save the workbook after adjusting the column widths
        wb.save(excel_file)
        
    except Exception as e:
        print(f"Error adjusting column widths: {str(e)}")


def extract_script_data(driver):
    try:
        # Extract ScriptData from JavaScript context
        script_data = driver.execute_script("return window.ScriptData")
        
        # Extract required data
        data = {
            'SiteURL': script_data['config']['SiteUrl'],
            'CampaignID': script_data['pageData']['CampaignId'],
            'SiteName': script_data['config']['SiteName'],
            'Browser': script_data['userInfo']['Browser'],
            'CountryCode': script_data['userInfo']['CountryCode'],
            'IP': script_data['userInfo']['IP'],
        }
        
        # Define the file name
        file_name = 'script_data.xlsx'
        
        # Check if the Excel file already exists
        if os.path.exists(file_name):
            # If it exists, load the existing file
            df = pd.read_excel(file_name)
            # Concatenate the new data with the existing DataFrame
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        else:
            # If it doesn't exist, create a new DataFrame
            df = pd.DataFrame([data])

        # Save the data to the Excel file (overwrites if exists)
        df.to_excel(file_name, index=False)

        # Adjust the column widths after saving the data
        adjust_column_widths(file_name)
        
    except Exception as e:
        print(f"Error extracting script data: {str(e)}")
