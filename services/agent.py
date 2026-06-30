from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.tools.pandas import PandasTools

class AgentService:
    @staticmethod
    def create_model(provider, api_key):
        """
        Instantiates the respective free tier model provider endpoint.
        """
        if provider == "Google Gemini":
            return Gemini(id="gemini-2.0-flash", api_key=api_key)
        elif provider == "Groq":
            return Groq(id="llama-3.3-70b-versatile", api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider configuration: {provider}")

    @classmethod
    def get_analyst_agent(cls, provider, api_key, duckdb_tools):
        """
        Assembles the complete analytical Agno Agent instance package.
        """
        model_instance = cls.create_model(provider, api_key)
        
        tools = [duckdb_tools] if provider == "Groq" else [duckdb_tools, PandasTools()]

        return Agent(
            model=model_instance,
            tools=tools,            

            system_message=("You are an expert data analyst. Use the 'uploaded_data' table to answer user queries. "
                           "Generate SQL queries using DuckDB tools to solve the user's query. "
                           "Provide clear and concise answers with the results.",
                           "CRITICAL ENFORCEMENT RULES:\n"
                            "1. NEVER wrap function executions in string text tags like '<function=describe_table>'.\n"
                            "2. You must invoke functions exclusively using your native backend JSON tool-calling capabilities.\n"
                            "3. Do not print out the code or brackets of your tool choice to the user."
            ),                           
            markdown=True,
        )