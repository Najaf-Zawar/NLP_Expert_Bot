# NLP Expert Chatbot

This is an AI-powered chatbot built using Chainlit, OpenAI and Tavily Search API. It's designed to assist users with natural language processing (NLP) related queries and tasks. The chatbot, named "Lexi", is an expert in providing information, explanations, and advice about various NLP concepts, algorithms, and research.

## Features

- **NLP-Focused Expertise**: Lexi is exclusively focused on NLP-related topics and can help with a variety of tasks, including:
  - Explaining NLP algorithms and techniques
  - Providing guidance on NLP-related coding problems
  - Discussing the latest NLP research and developments
  - Answering general NLP-related questions

- **Integrated Search Capabilities**: Lexi can leverage the Tavily search API to find the latest information and updates related to NLP, ensuring that the responses are up-to-date and relevant. Lexi will search Google using the Tavily API and provide the relevant search results as part of the answer.

- **Conversational Interface**: Lexi is designed to engage in natural, human-like conversations, making it easy for users to interact with and get the information they need.

## Getting Started

### Prerequisites

- Python 3.10 or later
- OpenAI API key
- Tavily API key

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/Najaf-Zawar/NLP_Expert_Bot.git
   ```

2. Install the required dependencies:

   ```
   cd nlp-expert-chatbot
   pip install -r requirements.txt
   ```

3. Set up the environment variables:

   - Create a `.env` file in the project directory.
   - Add your OpenAI API key and Tavily API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key
     TAVILY_API_KEY=your_tavily_api_key
     ```

### Running the App

To start the chatbot, run the following command:

```
chainlit run src/app.py
```

This will start the Chainlit server and make the chatbot available at `http://localhost:8000`.

## Usage

Once the app is running, you can interact with Lexi, the NLP expert chatbot, by sending messages through the Chainlit web interface. Lexi will respond with relevant information, explanations, and advice related to your NLP-related queries. If Lexi needs additional information, it will search Google using the Tavily API and include the relevant search results in its response.

## License

This project is licensed under the [Apache 2.0 License](LICENSE).