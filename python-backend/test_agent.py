#!/usr/bin/env python3
"""
Test script for the enhanced AI Financial Analyst Agent
Demonstrates the agent's ability to use tools for financial analysis
"""

import asyncio
import json
import sys
import os
from datetime import datetime, timedelta

# Add the current directory to the Python path to enable relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Agents.Analyst.agent import AIAgent

# Sample financial data for testing
sample_transactions = [
    {
        "id": "1",
        "amount": 5000.00,
        "category": "Revenue",
        "description": "Client payment - ABC Corp",
        "date": "2024-01-15T10:00:00Z"
    },
    {
        "id": "2", 
        "amount": -1200.00,
        "category": "Office & Rent",
        "description": "Monthly office rent",
        "date": "2024-01-01T09:00:00Z"
    },
    {
        "id": "3",
        "amount": -800.00,
        "category": "Utilities",
        "description": "Electric and internet bills",
        "date": "2024-01-05T14:30:00Z"
    },
    {
        "id": "4",
        "amount": -350.00,
        "category": "Marketing",
        "description": "Google Ads campaign",
        "date": "2024-01-10T16:00:00Z"
    },
    {
        "id": "5",
        "amount": 2500.00,
        "category": "Revenue", 
        "description": "Product sales - January",
        "date": "2024-01-20T11:15:00Z"
    },
    {
        "id": "6",
        "amount": -2000.00,
        "category": "Payroll",
        "description": "Employee wages",
        "date": "2024-01-30T10:00:00Z"
    }
]

sample_user_data = {
    "transactions": sample_transactions,
    "business_name": "Tech Startup Inc",
    "analysis_period": "January 2024"
}

async def test_agent_response():
    """Test the agent's response to financial analysis queries"""
    
    print("🚀 Initializing AI Financial Analyst Agent...")
    agent = AIAgent()
    
    print("\n📊 Testing Agent with Sample Financial Data")
    print("=" * 60)
    
    # Test queries
    test_queries = [
        "Please analyze my business cash flow and provide insights.",
        "What are my biggest expense categories and how can I optimize them?",
        "How is my business performing financially this month?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Query {i}: {query}")
        print("-" * 40)
        
        try:
            # Get complete response
            response = await agent.get_complete_response(query, sample_user_data)
            print(f"💡 Agent Response:\n{response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*60)

    # Test streaming response
    print("\n🌊 Testing Streaming Response:")
    print("-" * 40)
    
    try:
        print("💬 Agent (streaming): ", end="", flush=True)
        async for chunk in agent.stream_response(
            "Give me a quick summary of my financial health.", 
            sample_user_data
        ):
            print(chunk, end="", flush=True)
        print("\n")
        
    except Exception as e:
        print(f"❌ Streaming Error: {e}")

async def test_individual_tools():
    """Test individual tools directly"""
    
    print("\n🔧 Testing Individual Tools")
    print("=" * 60)
    
    from Agents.Analyst.agent import tool_registry
    
    # Test cash flow analysis
    print("\n📈 Testing Cash Flow Analysis Tool:")
    try:
        result = await tool_registry.execute_tool("analyze_cash_flow", {
            "transactions": sample_transactions
        })
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test expense categorization
    print("\n🏷️ Testing Expense Categorization Tool:")
    try:
        result = await tool_registry.execute_tool("categorize_expense", {
            "description": "Monthly subscription for project management software",
            "amount": 29.99
        })
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test insights generation
    print("\n💡 Testing Financial Insights Tool:")
    try:
        result = await tool_registry.execute_tool("generate_financial_insights", {
            "data": {
                "net_cash_flow": 3150.00,
                "total_income": 7500.00,
                "total_expenses": 4350.00,
                "category_breakdown": {
                    "Revenue": 7500.00,
                    "Office & Rent": -1200.00,
                    "Utilities": -800.00,
                    "Marketing": -350.00,
                    "Payroll": -2000.00
                }
            }
        })
        for insight in result:
            print(f"  • {insight}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🏦 AI Financial Analyst Agent - Test Suite")
    print("=" * 60)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key before running tests.")
        exit(1)
    
    # Run tests
    asyncio.run(test_agent_response())
    asyncio.run(test_individual_tools())
    
    print("\n✅ Test suite completed!") 