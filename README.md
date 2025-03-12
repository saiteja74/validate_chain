# Solidity Contract Generator and Validator API

Develop an AI model that generates Solidity contracts from text descriptions. 

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
    git clone [https://github.com/saiteja74/validate_chain.git](https://github.com/saiteja74/validate_chain.git)
    cd validate_chain
    ```

2.  Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  Install the Solidity compiler (`solc`) if you want to use the full validation functionality.



## Running the Application

1.  Run the Python script:

    ```bash
    python app.py
    ```

2.  The API server will start at `http://127.0.0.1:5000/`.

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
    127.0.0.1:5000/generate-contract?prompt=Create a simple voting contract
    ```

2.  **Validate a contract:**

    ```bash
    127.0.0.1:5000/validate-contract?solidity_code=pragma%20solidity%20%5E0.80%3B%20contract%20Test%20%7B%20%7D
    ```

3.  **List templates:**

    ```bash
    127.0.0.1:5000/list-templates
    ```

4.  **Get a template:**

    ```bash
    127.0.0.1:5000/get-template?id=0
    ```

## Testing

The application includes a `test_generated_contracts` function that tests the syntax correctness of all contracts in the dataset. The `main` function executes this test upon running the script.

