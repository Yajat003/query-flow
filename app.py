import streamlit as st
from services.data import DataService
from services.agent import AgentService

def main():
    st.set_page_config(page_title="Data Analyst Agent", layout="wide")
    st.title("Data Analyst Agent")

    # sidebar for   selecting api providr
    with st.sidebar:
        st.header("Model Configuration")
        provider = st.selectbox("Select Free Model Provider:", ["Google Gemini", "Groq"])
        
        if provider == "Google Gemini":
            api_key = st.text_input("Enter your Google AI Studio API key:", type="password")
        else:
            api_key = st.text_input("Enter your Groq API key:", type="password")

        if api_key:
            st.session_state.api_key = api_key
            st.session_state.provider = provider
            st.success("API key is saved.")
        else:
            st.warning(f"Please enter your {provider} API key to proceed.")

    # file uploading part 
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    # the app's core part
    if uploaded_file is not None and "api_key" in st.session_state:
        
        # ingestion or processing using  DataService layer
        temp_path, columns, df = DataService.preprocess_and_save(uploaded_file)
        
        if temp_path and columns and df is not None:
            st.write("### Uploaded Data Preview:")
            st.dataframe(df, width="stretch")
            st.write("**Detected Columns:**", columns)        
            
            # setting up the data store connection tracking pipelines
            duckdb_tools = DataService.initialize_database(temp_path)       
            
            # generate the configured analytics engine agent payload
            data_analyst_agent = AgentService.get_analyst_agent(
                provider=st.session_state.provider,
                api_key=st.session_state.api_key,
                duckdb_tools=duckdb_tools
            )        
            
            if "generated_code" not in st.session_state:
                st.session_state.generated_code = None        
            
            user_query = st.text_area("Ask a query about the data:", placeholder="e.g., What is the average value in column X grouped by column Y?")        
            st.info("Use the termninal for a clear output of the agents response")       
            
            if st.button("Submit Query", type="primary"):
                if user_query.strip() == "":
                    st.warning("Please enter a query.")
                else:
                    try:
                        with st.spinner('Processing your query...'):
                            # Request response execution from agent layer
                            response = data_analyst_agent.run(user_query)
                            
                            # Safely extract structured content fallback block
                            if hasattr(response, 'content'):
                                response_content = response.content
                            else:
                                response_content = str(response)
                                
                        st.markdown("### Analyst Response:")
                        st.markdown(response_content)                       
                                            
                    except Exception as e:
                        st.error(f"Error generating response from the agent: {e}")
                        st.error("Please try rephrasing your query or check if the data format is correct.")

if __name__ == "__main__":
    main()