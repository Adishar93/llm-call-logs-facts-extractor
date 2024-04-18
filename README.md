# Call Logs Fact Extractor

This project is a combination of a Python Flask server and a React frontend designed to extract facts from call logs provided via text file links. The server implements prompt engineering using the GPT-4 model, while the frontend allows users to input questions and text file URLs for processing.

## High-Level Approach

The project follows an engineering approach utilizing the GPT-4 model for prompt engineering. It consists of two main parts deployed seperately on Google AppEngine:

1. **Python Flask Server**: Implements the required API endpoints for processing questions and documents.
2. **React Frontend**: Provides a user interface for submitting questions and document URLs. Communicates with the Flask server to process the data and display the results.

## Design Considerations

- **Prompt Engineering**: Utilizes the GPT-4 model with prompt engineering to generate responses based on the provided questions and call logs.
- **Separation of Concerns**: The project separates frontend and backend logic for better organization and scalability. Also, the code is grouped into different files based on their utility for better readability.
- **Deployment**: The frontend and backend are deployed on separate instances of Google App Engine.
- **Error Handling**: Includes basic error handling for input validation to ensure a smooth user experience. In case of invalid urls, it ignores those text files.
- **Responsive Design**: The frontend is tested to run on both mobile and desktop.

## Usage

To run the project, follow these steps:

1. Start the Flask server by running `python main.py` in the root directory.
2. Start the React frontend by running `npm start` inside the `react-frontend` folder.
3. If testing with a local Flask server, uncomment the `SERVER_URL` constant inside `Constants.js` to point to the localhost address.

