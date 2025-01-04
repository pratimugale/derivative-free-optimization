# derivative-free-optimization
A library that implements derivative free optimization techniques, chiefly for the purpose of understanding them.

### Build from Source

The code is of the form of a library, and currently to run it, you would need to clone this repository and perform the following:

1. Create a new Python virtual environment `python3 -m venv ENV`, and then activate it `source ENV/bin/activate`
2. Install the required dependencies: `make install`

### Usage
1. After installation, you can run any code in the examples folder - any existing one or by creating a new file in the examples directory and calling it by: 
`python examples/{name_of_example_code_file}.py`
2. To view more details for debugging, log level can be set through the environment variable: `OPTIMIZER_LOG_LEVEL` 


### Uninstall
`make uninstall`

### Reference
1. Creating Python Module: https://medium.com/@PythonScriptLab/building-a-python-library-a-step-by-step-guide-with-code-examples-46f960fe966f
