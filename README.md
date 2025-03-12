# Solidity Contract Generator and Validator API

This repository contains a Python-based application that leverages Groq's Mistral model to generate Solidity smart contracts from text prompts. It also includes functionalities to validate the generated contracts and manage a dataset of contract templates. The application is implemented using Flask, making it accessible through a RESTful API.

## Features

* **Smart Contract Generation:** Generates Solidity smart contracts from natural language prompts using Groq's Mistral AI model.
* **Syntax Validation:** Validates Solidity contract syntax using both basic checks and the `solc` compiler (if available).
* **Template Management:** Manages a dataset of contract templates, allowing users to list and retrieve templates.
* **RESTful API:** Provides a simple and accessible API for contract generation and validation.
* **Basic Syntax Validation:** Performs basic syntax validation without requiring external tools.
* **Solc Validation:** Uses the `solc` compiler for thorough validation.
* **API Documentation:** Includes a basic homepage with API documentation.

## Dependencies

* Python 3.6+
* Flask
* Groq Python SDK
* Solc (Solidity compiler, optional for full validation)
* Requests (for API testing)

## Installation

1.  Clone the repository:

    ```bash
    git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
    cd your-repo-name
    ```

2.  Install Python dependencies:

    ```bash
    pip install Flask groq requests
    ```

3.  (Optional) Install the Solidity compiler (`solc`) if you want to use the full validation functionality.

4.  Set your Groq API key:

    * Replace `"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"` with your actual Groq API key in the Python code.

## Running the Application

1.  Run the Python script:

    ```bash
    python your_script_name.py
    ```

2.  The API server will start at `http://0.0.0.0:5000`.

## API Endpoints

* **`/generate-contract` (GET/POST):**
    * Generates a Solidity contract from a text prompt.
    * Parameters: `prompt` (string).
    * Returns: JSON with `solidity_code`, `is_valid`, and `validation_message`.
* **`/validate-contract` (GET/POST):**
    * Validates a Solidity contract.
    * Parameters: `solidity_code` (string).
    * Returns: JSON with `is_valid` and `validation_message`.
* **`/list-templates` (GET):**
    * Lists available contract templates.
    * Returns: JSON with a list of templates.
* **`/get-template` (GET):**
    * Gets a specific contract template by ID.
    * Parameters: `id` (integer).
    * Returns: JSON with the contract template.
* **`/` (GET):**
    * Homepage with API documentation.

## Example Usage

1.  **Generate a contract:**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"prompt": "Generate an ERC-20 token contract"}' [http://0.0.0.0:5000/generate-contract](http://0.0.0.0:5000/generate-contract)
    ```

2.  **Validate a contract:**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"solidity_code": "pragma solidity ^0.8.0; contract MyContract {}"}' [http://0.0.0.0:5000/validate-contract](http://0.0.0.0:5000/validate-contract)
    ```

3.  **List templates:**

    ```bash
    curl [http://0.0.0.0:5000/list-templates](http://0.0.0.0:5000/list-templates)
    ```

4.  **Get a template:**

    ```bash
    curl [http://0.0.0.0:5000/get-template?id=0](http://0.0.0.0:5000/get-template?id=0)
    ```

## Testing

The application includes a `test_generated_contracts` function that tests the syntax correctness of all contracts in the dataset. The `main` function executes this test upon running the script.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Your Name / Your GitHub Profile

## Contact

Your Email / Your preferred contact method.