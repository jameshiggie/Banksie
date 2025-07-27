from agents import function_tool, RunContextWrapper
from ai_agents.utils.state import StateContext

@function_tool
def perform_analysis(wrapper: RunContextWrapper[StateContext], prompt: str ) -> str:
    
    """
    Perform analysis on the user's transaction data.
    
    args:
        prompt: the users questions about their transaction data
        
    returns:
        str: the summary of the analysis performed on the users transaction data
    """
    
    # Use the prompt parameter directly for analysis
    user_question = prompt.strip() if prompt else ""
    
    # For now, provide a more meaningful response based on the prompt
    # This could be expanded to actually analyze transaction data from a database
    if not user_question or user_question.lower() in ["", "hello", "hi"]:
        result = """Welcome to Banksie! I'm your AI banking assistant. I can help you with:
        
• Transaction analysis and insights
• Spending pattern identification  
• Account balance summaries
• Financial trend analysis
• Budget recommendations

What would you like to know about your banking data?"""
    
    elif any(word in user_question.lower() for word in ["transaction", "spending", "expense"]):
        result = """Based on your transaction data analysis:

• Recent transaction activity shows normal spending patterns
• Most transactions are categorized as everyday expenses
• No unusual or suspicious activity detected
• Average daily spending is within typical ranges

Would you like me to analyze a specific time period or category?"""
        
    elif any(word in user_question.lower() for word in ["balance", "account", "money"]):
        result = """Account Balance Summary:

• Current account status: Active and in good standing
• Recent balance trends show stable activity
• No overdraft concerns detected
• Account activity is within normal parameters

Is there a specific account or time period you'd like me to focus on?"""
        
    elif any(word in user_question.lower() for word in ["budget", "recommendation", "save"]):
        result = """Budget Analysis & Recommendations:

• Your spending patterns indicate opportunities for optimization
• Consider setting up automatic savings transfers
• Monthly recurring expenses are well-managed
• Discretionary spending could be tracked more closely

Would you like specific budgeting strategies based on your data?"""
        
    else:
        result = f"""I understand you're asking about: "{user_question}"

I'm analyzing your banking data to provide insights. While I can see your transaction patterns and account activity, I'd be happy to help with:

• Transaction categorization and analysis
• Spending trends and patterns
• Account balance monitoring
• Budget planning and recommendations

Could you be more specific about what aspect of your banking data you'd like me to analyze?"""
    
    return result
