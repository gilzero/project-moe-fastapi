# Multi-Agent AI Analysis Platform

## Overview

This project is a FastAPI-based web application designed to analyze user queries using a multi-agent system of Large Language Models (LLMs). It leverages the power of multiple expert LLMs to provide comprehensive and diverse insights. The application uses Jinja2 templates for dynamic HTML rendering and includes robust error handling and logging. This platform is ideal for complex analysis tasks where different perspectives and expertise are beneficial.

## Key Features

*   **Multi-Agent Architecture:** Employs multiple expert LLMs (OpenAI, Anthropic, xAI) to analyze user queries from different perspectives. Each expert is configured with a specific style (technical, creative, business) to provide diverse insights.
*   **Comprehensive Analysis:** Provides a range of analysis types, including:
    *   **Consensus Analysis:** A summary of the expert responses, highlighting agreements and disagreements.
    *   **Charts and Mindmaps:** Generates descriptions of charts or mindmaps to visualize the analysis.
    *   **Tool-Based Analysis:** Performs sentiment analysis, bias detection, uncertainty highlighting, and jargon explanation.
    *   **Related Questions:** Suggests related questions for deeper learning and exploration.
    *   **Meta-Analysis:** Evaluates the quality of the analysis and identifies patterns.
*   **Asynchronous Operations:** Utilizes `asyncio` for efficient concurrent processing of LLM requests, ensuring the application remains responsive even with multiple API calls.
*   **Dynamic HTML Rendering:** Uses Jinja2 templates to generate dynamic HTML responses, allowing for a flexible and interactive user interface.
*   **Configurable LLMs:** Supports configuration of different LLMs and their parameters (model, temperature, max tokens) via `config.yaml`. This allows for easy customization and experimentation with different models.
*   **API Key Management:** Securely manages API keys using `.env` files and Google Colab userdata, ensuring sensitive information is not exposed in the codebase.
*   **Robust Error Handling:** Includes comprehensive error handling for various scenarios, such as configuration loading, API call failures, and user input validation.
*   **Detailed Logging:** Logs application events for monitoring and debugging, providing insights into the application's behavior and performance.
*   **User-Friendly Interface:** Provides a clean and responsive user interface with example queries and helpful tooltips, making it easy for users to interact with the platform.
*   **Request ID Tracking:** Uses a custom middleware to track requests with unique IDs, aiding in debugging and monitoring.

## File Structure
fastapi-web-app/
├── main.py # Main entry point for the FastAPI application
├── utils.py # Utility functions for API keys, workflow execution, and logging
├── llm_factory.py # Factory class for creating LLM model instances
├── expert.py # Classes for creating and managing expert LLMs
├── models.py # Data models used in the application
├── config_loader.py # Loads and validates configuration from YAML
├── templates/ # Directory containing HTML templates
│ └── index.html # Main page with the query form
│ └── results.html # Page to display analysis results
├── static/ # Directory for static files
│ └── style.css # CSS styles for the application
│ └── script.js # JavaScript for client-side logic
├── tests/ # Directory for tests
│ └── test_expert.py # Tests for expert creation
│ └── test_llm_factory.py # Tests for LLM factory
│ └── test_workflow.py # Tests for the workflow
├── .gitignore # Specifies files to be ignored by Git
├── requirements.txt # Lists project dependencies
├── config.yaml # Configuration file for LLMs and prompts
└── .env # Environment file for API keys


## Installation

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/gilzero/project-moe-fastapi.git
    cd fastapi-web-app
    ```

2.  **Create and activate a virtual environment:**

    It's highly recommended to use a virtual environment to manage dependencies.

    ```sh
    python -m venv venv
    source venv/bin/activate  # On macOS and Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install the dependencies:**

    Install all required Python packages using pip:

    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up API Keys:**

    *   Create a `.env` file in the root directory of the project.
    *   Add your API keys for OpenAI, Anthropic, xAI, and Google in the following format:

        ```env
        OPENAI_API_KEY=your_openai_api_key
        ANTHROPIC_API_KEY=your_anthropic_api_key
        XAI_API_KEY=your_xai_api_key
        GOOGLE_API_KEY=your_google_api_key
        ```
    *   **Note:** Ensure you have the necessary API keys from the respective providers.

5.  **Configure the application:**

    *   Create a `config.yaml` file in the root directory of the project.
    *   Use the following example configuration as a starting point. You can customize the models, temperatures, max tokens, expert styles, and prompts as needed:

        ```yaml
        openai_model: "gpt-4o"
        anthropic_model: "claude-3-5-haiku-20241022"
        xai_model: "grok-beta"
        supervisor_model: "gemini-2.0-flash-exp"
        openai_config:
          model: "gpt-4o"
          temperature: 0.1
          max_tokens: 512
        anthropic_config:
          model: "claude-3-5-haiku-20241022"
          temperature: 0.2
          max_tokens: 512
        xai_config:
          model: "grok-beta"
          temperature: 0.0
          max_tokens: 512
        supervisor_config:
          model: "gemini-2.0-flash-exp"
          temperature: 0.0
          max_tokens: 1024
        expert_styles:
          technical: "Focus on detailed technical explanations."
          creative: "Use imaginative, broad storytelling approaches."
          business: "Emphasize strategic and economic impacts."
        prompts:
          consensus_task: "Analyze the following experts' responses. Provide a consensus analysis and highlight disagreements."
          charts_task: "Generate useful charts or mindmap descriptions in concise text."
          tools_task: "Perform sentiment analysis, bias detection, uncertainty highlighting, and jargon explanation. Separate each analysis by sections."
          questions_task: "Provide related questions for deeper learning."
          meta_task: "Evaluate quality metrics and perform pattern recognition."
        ```

## Usage

1.  **Run the FastAPI application:**

    Start the application using Uvicorn:

    ```sh
    uvicorn main:app --reload
    ```

    The `--reload` flag enables automatic reloading of the server when code changes are detected, which is useful during development.

2.  **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:8000`. You should see the main page with the query form.

3.  **Enter a query:**

    Type your query into the input field and click the "Analyze" button. The application will process your query using the configured LLMs and display the results on a new page.

## Contributing

Contributions are welcome! If you have any ideas for improvements, bug fixes, or new features, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your changes.
3.  Make your changes and commit them with clear and descriptive messages.
4.  Submit a pull request to the main branch.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.