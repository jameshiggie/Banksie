from agents import function_tool, RunContextWrapper
from ai_agents.utils.state import StateContext
import io
import sys
import re
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, date, timedelta

# Optional imports for data analysis
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    pd = None
    PANDAS_AVAILABLE = False

try:
    import numpy as np  # type: ignore
    NUMPY_AVAILABLE = True
except ImportError:
    np = None
    NUMPY_AVAILABLE = False

@function_tool
def perform_analysis(wrapper: RunContextWrapper[StateContext], code: str) -> str:
    
    """
    Perform analysis on the user's transaction data using python code. 
    Guidelines:
    - Its run in a restricted environment
    - You can only use the libraries and variables that are already imported.
        - The code must use the variable `transaction_data` as tis source of transaction data.
        - Pandas and Numpy are already imported so you can use them.
    - The code must print out the final conclusion of the analysis and any data the user needs to see using f-string.
    - DO NOT include import statements in your code - pandas is available as 'pd' and numpy as 'np'

    args:
        code: python code to be executed to perform the analysis and achieve the user's goal.
        
    returns:
        str: final conclusion of the analysis and any data the user needs to see.
    """
    
    # Access transaction data from the context
    data = wrapper.context.transaction_data
    
    # Parse the code from ```python\n...\n``` format
    if code.startswith("```python\n") and code.endswith("\n```"):
        # Extract the code between the markdown code blocks
        python_code = code[10:-4]  # Remove ```python\n at start and \n``` at end
    elif code.startswith("```python"):
        # Handle case where there might be no newline after python
        match = re.match(r'```python\n?(.*?)\n?```', code, re.DOTALL)
        if match:
            python_code = match.group(1)
        else:
            python_code = code
    else:
        # If no code block format, use the code as-is
        python_code = code
    
    # Remove common import statements that won't work in restricted environment
    python_code = re.sub(r'^import pandas as pd\s*\n?', '', python_code, flags=re.MULTILINE)
    python_code = re.sub(r'^import numpy as np\s*\n?', '', python_code, flags=re.MULTILINE)
    python_code = re.sub(r'^from pandas import .*\n?', '', python_code, flags=re.MULTILINE)
    python_code = re.sub(r'^from numpy import .*\n?', '', python_code, flags=re.MULTILINE)
    
    # Create a restricted namespace for code execution
    # Include common libraries and the transaction data
    restricted_globals = {
        '__builtins__': {
            'print': print,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
            'sum': sum,
            'max': max,
            'min': min,
            'round': round,
            'sorted': sorted,
            'enumerate': enumerate,
            'range': range,
            'zip': zip,
            'map': map,
            'filter': filter,
            'any': any,
            'all': all,
        },
        'data': data,
        'transaction_data': data,  # Provide both names for convenience
        'datetime': datetime,
        'date': date,
        'timedelta': timedelta,
    }
    
    # Add optional libraries if available
    if PANDAS_AVAILABLE and pd is not None:
        restricted_globals['pd'] = pd
        restricted_globals['pandas'] = pd
    
    if NUMPY_AVAILABLE and np is not None:
        restricted_globals['np'] = np
        restricted_globals['numpy'] = np
    
    # Add library availability info for debugging
    restricted_globals['PANDAS_AVAILABLE'] = PANDAS_AVAILABLE
    restricted_globals['NUMPY_AVAILABLE'] = NUMPY_AVAILABLE
    
    # Capture stdout and stderr
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    try:
        # Execute the code in the restricted environment
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(python_code, restricted_globals, {})
        
        # Get the captured output
        output = stdout_capture.getvalue()
        error_output = stderr_capture.getvalue()
        
        if error_output:
            result = f"Errors occurred:\n{error_output}\n\nOutput:\n{output}"
        else:
            result = output if output else "Code executed successfully but produced no output."
            
    except Exception as e:
        # Handle any execution errors
        error_output = stderr_capture.getvalue()
        result = f"Error executing code: {str(e)}\n"
        if error_output:
            result += f"Additional errors: {error_output}\n"
            
        # Add helpful debugging info
        result += f"\nDebugging info:\n"
        result += f"- Pandas available: {PANDAS_AVAILABLE}\n"
        result += f"- Numpy available: {NUMPY_AVAILABLE}\n"
        result += f"- Transaction data type: {type(data)}\n"
        result += f"- Transaction data length: {len(data) if hasattr(data, '__len__') else 'N/A'}\n"
        result += f"- Available variables: {[k for k in restricted_globals.keys() if not k.startswith('__')]}\n"
    
    return result
