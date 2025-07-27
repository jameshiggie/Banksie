# AI Financial Analyst Agent - OpenAI Agents SDK Architecture

## Overview

This project has been enhanced to use an **agent-like architecture** inspired by the OpenAI Agents SDK, providing more powerful and structured financial analysis capabilities for business banking applications.

## Key Improvements

### 🔧 **Agent-Based Architecture**
- **Tool Registry System**: Centralized management of agent tools with automatic function calling
- **Modular Design**: Separated tools from the main agent logic for better maintainability
- **Enhanced Error Handling**: Robust error handling for tool execution and API calls

### 🛠️  **Advanced Financial Analysis Tools**

#### 1. **Cash Flow Analysis Tool** (`analyze_cash_flow`)
- Calculates total income, expenses, and net cash flow
- Provides category-wise transaction breakdown
- Generates monthly trend analysis from transaction dates
- Returns comprehensive financial metrics with analysis summaries

#### 2. **Expense Categorization Tool** (`categorize_expense`) 
- Intelligent expense categorization using keyword matching
- Supports 9+ business expense categories:
  - Office & Rent, Payroll, Inventory & Supplies
  - Marketing, Utilities, Professional Services
  - Insurance, Travel & Entertainment, Technology
- Amount-based categorization for edge cases
- Provides reasoning for each categorization decision

#### 3. **Financial Insights Generator** (`generate_financial_insights`)
- Generates actionable business insights with specific metrics
- Provides cash flow health indicators with emoji visual cues
- Identifies top expense categories with percentage analysis
- Month-over-month trend analysis
- Actionable recommendations for business improvement

### 💬 **Enhanced Communication**
- **Professional tone** with accessible language
- **Visual emphasis** using emojis for key insights
- **Specific metrics** and percentages in recommendations
- **Data-driven insights** using actual calculations rather than assumptions

### 🔄 **Advanced Streaming & Tool Integration**
- **Two-phase processing**: Initial tool calls followed by streaming response
- **Automatic tool execution** based on available user data
- **Context-aware responses** that adapt to the provided financial data
- **Streaming support** with proper error handling

## Architecture Benefits

### **Compared to Original Implementation:**

| Feature | Original | Enhanced |
|---------|----------|----------|
| Tool Integration | None | 3 specialized financial tools |
| Data Analysis | Generic responses | Calculated metrics & insights |
| Architecture | Simple chat completion | Agent-based with tool registry |
| Error Handling | Basic | Comprehensive with tool-level handling |
| Insights Quality | General advice | Specific, data-driven recommendations |
| Scalability | Limited | Easily extensible with new tools |

### **OpenAI Agents SDK Compatibility:**
While we couldn't install the full OpenAI Agents SDK due to dependency conflicts, this implementation provides:
- ✅ **Tool Registration System** similar to `@function_tool` decorator
- ✅ **Agent Instructions** with clear capability definitions  
- ✅ **Tool Integration** with automatic function calling
- ✅ **Error Handling** and validation
- ✅ **Modular Architecture** for easy extension

## Usage Examples

### Basic Usage
```python
from Agents.Analyst.agent import AIAgent

# Initialize the agent
agent = AIAgent()

# Analyze financial data
user_data = {
    "transactions": [
        {"amount": 5000, "category": "Revenue", "date": "2024-01-15T10:00:00Z"},
        {"amount": -1200, "category": "Rent", "date": "2024-01-01T09:00:00Z"}
    ]
}

# Get streaming response
async for chunk in agent.stream_response("Analyze my cash flow", user_data):
    print(chunk, end="")
```

### Tool Testing
```python
from Agents.Analyst.agent import tool_registry

# Test individual tools
result = await tool_registry.execute_tool("analyze_cash_flow", {
    "transactions": transaction_data
})
```

## Testing

Run the test suite to see the agent in action:

```bash
cd python-backend
python test_agent.py
```

**Requirements:**
- Set `OPENAI_API_KEY` environment variable
- Python 3.8+ with `openai`, `fastapi`, `asyncio` libraries

## Future Enhancements

### Potential OpenAI Agents SDK Integration
When dependency conflicts are resolved, the architecture can be upgraded to use:
- `agents.Agent` for agent management
- `agents.Runner` for execution
- `@function_tool` decorators
- Built-in handoffs and session management
- Advanced tracing and debugging

### Additional Tools
- **Budget Planning Tool**: Create and track budgets
- **Forecasting Tool**: Predict future cash flows
- **Risk Assessment Tool**: Identify financial risks
- **Comparative Analysis Tool**: Compare periods/benchmarks
- **Tax Optimization Tool**: Identify tax-saving opportunities

## Architecture Diagram

```
┌─────────────────────┐
│   AIAgent Class     │
├─────────────────────┤
│ - client: OpenAI    │
│ - system_prompt     │
│ - _process_tools()  │
│ - stream_response() │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│   ToolRegistry      │
├─────────────────────┤
│ - tools: Dict       │
│ - function_defs     │
│ - register_tool()   │
│ - execute_tool()    │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Financial Tools    │
├─────────────────────┤
│ • analyze_cash_flow │
│ • categorize_expense│ 
│ • generate_insights │
└─────────────────────┘
```

This enhanced architecture provides a solid foundation for building sophisticated AI-powered financial analysis tools while maintaining compatibility with existing systems and providing clear upgrade paths to full agent frameworks. 