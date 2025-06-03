# rpal-interpreter
A Python based interpreter for the Right-reference Pedagogic Algorithmic Language (RPAL) consisting of Lexical Analyzer, Parser, Standardizer, and Control Stack Environment (CSE) Machine.

**Important**

- Don't use `'` for strings and chars in the input, always use `"` instead.
- For function definitions, always keep a space between the function name and the opening parenthesis or function parameters, e.g., `f (x) = x + 1` or `f x = x + 1` instead of `f(x) = x + 1` or `fx = x + 1`.
- During function definition and function call, if there is a single parameter with negative sign, use parentheses around the parameter, e.g., `f (-x) = x + 1` or `Print (f (-2))` instead of `f -x = x + 1` or `Print (f -2)`. Reason is, for example, `f -2` is interpreted as `f` minus `2` instead of function call with parameter `-2`.
