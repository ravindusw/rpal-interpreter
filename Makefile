# Makefile for RPAL Interpreter

# Python interpreter
PYTHON = python

# Main script
MAIN_SCRIPT = myrpal.py

# Source directories
SRC_DIR = src
EXAMPLES_DIR = examples

# Default target
.PHONY: all
all: help

# Help target - shows available commands
.PHONY: help
help:
	@echo "RPAL Interpreter Makefile"
	@echo "========================="
	@echo "Available targets:"
	@echo "  run FILE=<filename>     - Run interpreter on specified file"
	@echo "  ast FILE=<filename>     - Print AST for specified file"
	@echo "  st FILE=<filename>      - Print ST for specified file"
	@echo "  test                    - Run all test files"
	@echo "  test-ast                - Generate AST for all test files"
	@echo "  test-st                 - Generate standardized trees for all test files"
	@echo "  validate                - Validate project structure"
	@echo "  clean                   - Clean generated files"
	@echo "  install                 - Install dependencies (if any)"
	@echo "  help                    - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make run FILE=examples/sample1.txt"
	@echo "  make ast FILE=examples/sample1.txt"
	@echo "  make st FILE=examples/sample1.txt"
	@echo "  make test"

# Run the interpreter on a specific file
.PHONY: run
run:
	@if [ -z "$(FILE)" ]; then \
	    echo "Error: Please specify FILE=<filename>"; \
	    echo "Example: make run FILE=examples/sample1.txt"; \
	    exit 1; \
	fi
	$(PYTHON) $(MAIN_SCRIPT) $(FILE)

# Print AST for a specific file
.PHONY: ast
ast:
	@if [ -z "$(FILE)" ]; then \
	    echo "Error: Please specify FILE=<filename>"; \
	    echo "Example: make ast FILE=examples/sample1.txt"; \
	    exit 1; \
	fi
	$(PYTHON) $(MAIN_SCRIPT) -ast $(FILE)

# Print standardized tree for a specific file
.PHONY: st
st:
	@if [ -z "$(FILE)" ]; then \
	    echo "Error: Please specify FILE=<filename>"; \
	    echo "Example: make st FILE=examples/sample1.txt"; \
	    exit 1; \
	fi
	$(PYTHON) $(MAIN_SCRIPT) -st $(FILE)

# Run tests on all example files
.PHONY: test
test:
	@echo "Running tests on all example files..."
	@for file in $(EXAMPLES_DIR)/*.txt; do \
	    if [ -f "$$file" ]; then \
	        echo "Testing: $$file"; \
	        $(PYTHON) $(MAIN_SCRIPT) "$$file" || echo "Failed: $$file"; \
	        echo ""; \
	    fi \
	done

# Test AST generation for all files
.PHONY: test-ast
test-ast:
	@echo "Generating AST for all example files..."
	@for file in $(EXAMPLES_DIR)/*.txt; do \
	    if [ -f "$$file" ]; then \
	        echo "AST for: $$file"; \
	        $(PYTHON) $(MAIN_SCRIPT) -ast "$$file" || echo "Failed: $$file"; \
	        echo ""; \
	    fi \
	done

# Test standardized tree generation for all files
.PHONY: test-st
test-st:
	@echo "Generating standardized trees for all example files..."
	@for file in $(EXAMPLES_DIR)/*.txt; do \
	    if [ -f "$$file" ]; then \
	        echo "Standardized tree for: $$file"; \
	        $(PYTHON) $(MAIN_SCRIPT) -st "$$file" || echo "Failed: $$file"; \
	        echo ""; \
	    fi \
	done

# Clean generated files
.PHONY: clean
clean:
	@echo "Cleaning generated files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf $(SRC_DIR)/cse_machine/csem_output/*.txt 2>/dev/null || true
	@echo "Clean completed."

# Install dependencies (if you have any)
.PHONY: install
install:
	@echo "No dependencies to install for this project."

# Validate project structure
.PHONY: validate
validate:
	@echo "Validating project structure..."
	@test -f $(MAIN_SCRIPT) || (echo "Error: $(MAIN_SCRIPT) not found" && exit 1)
	@test -d $(SRC_DIR) || (echo "Error: $(SRC_DIR) directory not found" && exit 1)
	@test -d $(EXAMPLES_DIR) || (echo "Error: $(EXAMPLES_DIR) directory not found" && exit 1)
	@echo "Project structure is valid."

# Build target (for compatibility)
.PHONY: build
build: validate
	@echo "Building RPAL Interpreter..."
	@$(PYTHON) -m py_compile $(MAIN_SCRIPT)
	@$(PYTHON) -m py_compile $(SRC_DIR)/lexical_analyzer/*.py
	@$(PYTHON) -m py_compile $(SRC_DIR)/parser/*.py
	@$(PYTHON) -m py_compile $(SRC_DIR)/standardizer/*.py
	@$(PYTHON) -m py_compile $(SRC_DIR)/cse_machine/*.py
	@echo "Build completed successfully."

# Create a distribution package
.PHONY: package
package: clean
	@echo "Creating distribution package..."
	zip -r rpal-interpreter.zip . -x "*.git*" "*/__pycache__/*" "*.pyc"
	@echo "Package created: rpal-interpreter.zip"