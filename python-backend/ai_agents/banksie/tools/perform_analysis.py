import io
import re
from contextlib import redirect_stderr, redirect_stdout
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
from agents import RunContextWrapper, function_tool
from ai_agents.utils.state import StateContext


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
    
    python_code = extract_python_code_block(code)
    
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
            'pd': pd,
            'np': np,
            'pandas': pd,
            'numpy': np,
        },
        'data': data,
        'transaction_data': data,  # Provide both names for convenience
        'datetime': datetime,
        'date': date,
        'timedelta': timedelta,
    }
    
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
    
    return result


def extract_python_code_block(code: str) -> str:
    # Extract the python code block from the code
    code = code.replace("```python\n", "").replace("```", "").strip()

    return code

