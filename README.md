# AI Fact Extractor

### Website: http://factai-alb1-1373833785.us-east-2.elb.amazonaws.com/

## Overview
This web application is designed to extract relevant facts from a series of call logs in response to a user-provided question. Utilizing GPT-4, the application processes textual call log data fetched from specified URLs and distills this information into concise, actionable facts.

## High-Level Approach
- **Frontend**: Two main screens are implemented using React. The **Input Screen** allows users to submit a question along with URLs to call logs. The **Output Screen** displays the extracted facts once processed.
- **Backend**: Implemented in Python, the backend fetches call logs from provided URLs, processes them using GPT-4 to extract relevant facts based on the user's question, and handles API requests to submit data and retrieve facts.
- **Integration with GPT-4**: The application sends combined textual data from call logs to GPT-4 with a prompt that instructs the model to extract facts relevant to the posed question. This integration is key to leveraging AI for automated text analysis.

## Design Considerations
- **User Experience**: Ensuring a simple and intuitive user interface that allows easy submission of questions and URLs, and clear presentation of bulleted facts.
- **API Design**: RESTful API design to handle data submissions and fact retrieval with robust error handling to manage potential failures in data fetching or processing.
- **Fact Consistency**: Implementing a logical context prompt to update the list of facts as new call logs are processed, ensuring that the most recent documents can modify earlier extracted facts to maintain relevance and accuracy.
- **Error Handling**: Comprehensive error handling across both frontend and backend to gracefully manage and report issues encountered during the fetching and processing of documents.
