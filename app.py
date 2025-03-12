import os
import json
import groq
import time
import re

from flask import Flask, request, jsonify
import subprocess
import tempfile



# Initialize Groq client with API key
client = groq.Client(api_key="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")

def generate_contract(prompt):
    """Generate a Solidity contract based on the text prompt using Groq's Mistral model."""
    
    # Enhance the prompt with specific instructions
    enhanced_prompt = f"""
    You are an expert Solidity developer. Generate a complete, syntactically correct Solidity contract based on the following description:
    
    {prompt}
    
    Requirements:
    - Use Solidity version 0.8.0 or higher
    - Include necessary imports
    - Implement all standard functions based on the contract type
    - Add clear comments
    - Ensure contract is secure and follows best practices
    - Only return the complete Solidity code without explanations
    """
    
    try:
        # implementing groq api with mistral model
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768", 
            messages=[
                {"role": "system", "content": "You are a Solidity expert that generates clean, secure, and complete smart contract code."},
                {"role": "user", "content": enhanced_prompt}
            ],
            temperature=0.2, 
            max_tokens=4000,
            top_p=0.9
        )
        
        # generated code should be returned
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error generating contract: {e}")
        return None

def create_dataset(num_examples=10):
    """Create a dataset of example prompt-output pairs."""
    
    # sample prompts
    example_prompts = [
        "Generate an ERC-20 token contract with burn functionality",
        "Generate an ERC-721 NFT contract with metadata storage",
        "Create a simple crowdfunding contract with a time limit and minimum contribution",
        "Develop a staking contract that rewards users with tokens over time",
        "Create a multi-signature wallet contract that requires 2 of 3 signatures",
        "Design a DAO governance contract with proposal and voting mechanisms",
        "Create a decentralized exchange contract for swapping ERC-20 tokens",
        "Develop a time-locked vault contract that releases funds on a schedule",
        "Create an auction contract for NFTs with bidding functionality",
        "Design a yield farming contract that rewards liquidity providers",
        "Create a lending protocol with collateral and interest calculation",
        "Develop a prediction market contract with outcome resolution",
        "Create a supply chain tracking contract with product verification",
        "Design a token vesting contract with cliff and linear release",
        "Create a lottery contract with random winner selection"
    ]
    
    # iterating different prompts at a time
    dataset = []
    for prompt in example_prompts[:num_examples]:
        print(f"Generating contract for: {prompt}")
        output = generate_contract(prompt)
        
        if output:
            dataset.append({
                "prompt": prompt,
                "output": output
            })
            
            # Add delay to respect API rate limits
            time.sleep(2)
        else:
            print(f"Failed to generate output for: {prompt}")
    
    return dataset

def validate_solidity_syntax(solidity_code):
    """
    Validate Solidity code syntax using a temporary file and solc compiler.
    Returns (is_valid, error_message)
    """
    try:
        # temporary file for solidatory code
        with tempfile.NamedTemporaryFile(suffix='.sol', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(solidity_code.encode('utf-8'))
        
        # solc compiler
        result = subprocess.run(
            ['solc', '--ast', temp_file_path],
            capture_output=True,
            text=True
        )
        
        
        os.unlink(temp_file_path)
        
        
        if result.returncode == 0:
            return True, "Syntax is valid"
        else:
            return False, result.stderr
    
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def basic_syntax_validation(solidity_code):
    """Basic syntax validation for Solidity code without requiring external tools."""
    # Check for common syntax issues
    required_elements = [
        "pragma solidity",
        "contract",
        "{"
    ]
    
    for element in required_elements:
        if element not in solidity_code:
            return False, f"Missing required element: {element}"
    
    # Check for balanced braces
    if solidity_code.count("{") != solidity_code.count("}"):
        return False, "Unbalanced braces"
    
    # Check for balanced parentheses
    if solidity_code.count("(") != solidity_code.count(")"):
        return False, "Unbalanced parentheses"
    
    # Check for function declarations
    if not re.search(r'function\s+\w+\s*\(', solidity_code):
        return False, "No function declarations found"
    
    return True, "Basic syntax validation passed"

def validate_contract(solidity_code):
    """
    Validate a Solidity contract using both basic syntax checks and the solc compiler if available.
    Falls back to basic validation if solc is not installed.
    """
    # First, run basic syntax validation
    basic_valid, basic_msg = basic_syntax_validation(solidity_code)
    
    if not basic_valid:
        return False, basic_msg
    
    # Try using solc if available
    try:
        # Check if solc is installed
        subprocess.run(['solc', '--version'], capture_output=True, check=True)
        
        # If solc is available, use it for validation
        return validate_solidity_syntax(solidity_code)
    
    except (subprocess.SubprocessError, FileNotFoundError):
        # If solc is not available, just return basic validation results
        return basic_valid, "Basic validation passed (solc compiler not available for thorough validation)"

def save_dataset(dataset, filename="contract_prompts.json"):
    """Save the dataset to a JSON file."""
    with open(filename, "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"Dataset saved to {filename}")

# Flask API server implementation
app = Flask(__name__)

@app.route('/generate-contract', methods=['POST', 'GET'])
def api_generate_contract():
    """API endpoint to generate a Solidity contract from a text description."""
    if request.method == 'POST':
        data = request.json
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400
        
        prompt = data['prompt']
    elif request.method == 'GET':
        prompt = request.args.get('prompt')
        
        if not prompt:
            return jsonify({"error": "Missing 'prompt' parameter"}), 400
    
    contract = generate_contract(prompt)
    
    if not contract:
        return jsonify({"error": "Failed to generate contract"}), 500
    
    # Validate the generated contract
    is_valid, validation_msg = validate_contract(contract)
    
    return jsonify({
        "prompt": prompt,
        "solidity_code": contract,
        "is_valid": is_valid,
        "validation_message": validation_msg
    })

@app.route('/validate-contract', methods=['POST', 'GET'])
def api_validate_contract():
    """API endpoint to validate a Solidity contract."""
    if request.method == 'POST':
        data = request.json
        
        if not data or 'solidity_code' not in data:
            return jsonify({"error": "Missing 'solidity_code' in request"}), 400
        
        solidity_code = data['solidity_code']
    elif request.method == 'GET':
        solidity_code = request.args.get('solidity_code')
        
        if not solidity_code:
            return jsonify({"error": "Missing 'solidity_code' parameter"}), 400
    
    is_valid, validation_msg = validate_contract(solidity_code)
    
    return jsonify({
        "is_valid": is_valid,
        "validation_message": validation_msg
    })

@app.route('/list-templates', methods=['GET'])
def api_list_templates():
    """API endpoint to list available contract templates from the dataset."""
    try:
        with open("contract_prompts.json", "r") as f:
            dataset = json.load(f)
        
        templates = [{"id": i, "prompt": item["prompt"]} for i, item in enumerate(dataset)]
        return jsonify({"templates": templates})
    
    except Exception as e:
        return jsonify({"error": f"Failed to list templates: {str(e)}"}), 500

@app.route('/get-template', methods=['GET'])
def api_get_template():
    """API endpoint to get a specific contract template by ID."""
    template_id = request.args.get('id')
    
    if not template_id:
        return jsonify({"error": "Missing template ID"}), 400
    
    try:
        template_id = int(template_id)
        with open("contract_prompts.json", "r") as f:
            dataset = json.load(f)
        
        if template_id < 0 or template_id >= len(dataset):
            return jsonify({"error": f"Template ID {template_id} out of range"}), 404
        
        return jsonify(dataset[template_id])
    
    except Exception as e:
        return jsonify({"error": f"Failed to get template: {str(e)}"}), 500

# Add a basic homepage/documentation route
@app.route('/', methods=['GET'])
def homepage():
    """Homepage with API documentation."""
    return jsonify({
        "service": "Solidity Contract Generator API",
        "endpoints": [
            {
                "path": "/generate-contract",
                "methods": ["GET", "POST"],
                "description": "Generate a Solidity contract from text description",
                "parameters": ["prompt"]
            },
            {
                "path": "/validate-contract",
                "methods": ["GET", "POST"],
                "description": "Validate Solidity contract syntax",
                "parameters": ["solidity_code"]
            },
            {
                "path": "/list-templates",
                "methods": ["GET"],
                "description": "List available contract templates"
            },
            {
                "path": "/get-template",
                "methods": ["GET"],
                "description": "Get a specific contract template",
                "parameters": ["id"]
            }
        ]
    })

def test_generated_contracts(dataset):
    """Test the syntax correctness of all contracts in the dataset."""
    print("\nTesting generated contracts:")
    results = []
    
    for i, item in enumerate(dataset):
        prompt = item["prompt"]
        solidity_code = item["output"]
        
        is_valid, validation_msg = validate_contract(solidity_code)
        
        result = {
            "id": i,
            "prompt": prompt,
            "is_valid": is_valid,
            "validation_message": validation_msg
        }
        
        results.append(result)
        print(f"Contract {i+1}: {'✓ Valid' if is_valid else '✗ Invalid'} - {prompt[:40]}...")
    
    # Count valid and invalid contracts
    valid_count = sum(1 for r in results if r["is_valid"])
    print(f"\nValidation summary: {valid_count}/{len(results)} contracts are valid")
    
    return results

def main():
    """Main function to run the application."""
    # Check if dataset exists, otherwise create it
    if not os.path.exists("contract_prompts.json"):
        print("Generating dataset...")
        dataset = create_dataset(num_examples=10)
        save_dataset(dataset)
    else:
        print("Dataset already exists")
        
        # Load existing dataset
        with open("contract_prompts.json", "r") as f:
            dataset = json.load(f)
        
        print(f"Loaded {len(dataset)} examples from existing dataset")
    
    # Test all contracts in the dataset
    test_results = test_generated_contracts(dataset)
    
    # Example of generating a new contract
    print("\nExample contract generation:")
    new_prompt = "Create a simple voting contract where users can vote on proposals"
    contract = generate_contract(new_prompt)
    
    if contract:
        print("\nGenerated contract preview:")
        print(contract[:200] + "..." if len(contract) > 200 else contract)
        
        # Validate the contract
        is_valid, validation_msg = validate_contract(contract)
        print(f"Contract validation: {'Valid' if is_valid else 'Invalid'}")
        print(f"Validation message: {validation_msg}")
    
    # Instructions for running the API server
    print("\nTo start the API server, run:")
    print("flask run --host=0.0.0.0 --port=5000")
    print("\nAvailable endpoints:")
    print("- GET/POST /generate-contract: Generate a contract from a prompt")
    print("- GET/POST /validate-contract: Validate a Solidity contract")
    print("- GET /list-templates: List available contract templates")
    print("- GET /get-template?id=X: Get a specific contract template")
    print("- GET /: Homepage with API documentation")

if __name__ == "__main__":
    main()
    
    app.run(host='0.0.0.0', port=5000, debug=True)