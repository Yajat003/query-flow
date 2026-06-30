import csv
import tempfile
import pandas as pd
import streamlit as st
from agno.tools.duckdb import DuckDbTools

class DataService:
    @staticmethod
    def preprocess_and_save(file):
        """
        Reads, cleans, & prepares uploaded data into a temporary CSV file.
        """
        try:
            # reading the uploaded file into a DataFrame
            if file.name.endswith('.csv'):
                df = pd.read_csv(file, encoding='utf-8', na_values=['NA', 'N/A', 'missing'])
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file, na_values=['NA', 'N/A', 'missing'])
            else:
                st.error("Unsupported file format. Please upload a CSV or Excel file.")
                return None, None, None     
            
            # making sure the columns are properly quoted
            for col in df.select_dtypes(include=['object']):
                df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)    
            
            # parsing dates and numeric columns
            for col in df.columns:
                if 'date' in col.lower():
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                elif df[col].dtype == 'object':
                    try:
                        df[col] = pd.to_numeric(df[col])
                    except (ValueError, TypeError):
                        pass        
            
            # creating temporary file to save the preprocessed data
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
                temp_path = temp_file.name
                df.to_csv(temp_path, index=False, quoting=csv.QUOTE_ALL)        
                
            return temp_path, df.columns.tolist(), df
        except Exception as e:
            st.error(f"Error processing file: {e}")
            return None, None, None

    @staticmethod
    def initialize_database(temp_path):
        """
        Loads the local file's data securely into DuckDB.
        """
        duckdb_tools = DuckDbTools()
        duckdb_tools.load_local_csv_to_table(
            path=temp_path,
            table="uploaded_data",
        )
        return duckdb_tools