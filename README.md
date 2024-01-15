# rillavoice_assessment
This project is my submission to RillaVoice's take-home coding assessment.

## Requirements
You will need to update the .env file with your own hidden variable values. This includes an `OPENAI_API_KEY`, `NEO4J_BOLT_URL`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD`. The code will otherwise not work. 

Unless you have already have these dependencies installed, you will need to install the following:

- openai
- Neo4j
- python-dotenv

## Setting up the Environment
Update the `.env` file in the root directory of the project. Add the necessary environment variables as follows:
```
OPENAI_API_KEY="<your-openai-api-key-here>"
NEO4J_BOLT_URL="<your-bolt-url-here>"
NEO4J_USERNAME="<your-neo4j-username-here>"
NEO4J_PASSWORD="<your-neo4j-password-here>"
```

Once completed, run the following command to download the required dependencies:
`pip install -r requirements.txt`.

## Run the script
To run the script, all you need to do is open your terminal, navigate to the repository directory, and run `python3 chatbot.py`.

## Testing the chatbot
The chatbot is capable of answering direct questions regarding the Neo4j and capable of referring to previous questions or answers within the conversation. Some example questions include:

`How many movies has Tom Hanks acted in?`<br>
`What are the names of those movies?`<br>
`Who directed Cloud Atlas?`<br>
`What movie did Tom Hanks direct?`<br>
`Find me the shortest path etween Kevin Bacon and Meg Ryan`<br>
`Did Meg Ryan direct any films?`.<br>

The chatbot is also capable of noticing whether a question is off-topic from movies, and thus will refuse to answer. An example question to ask is:

`What is your favorite color?`.

## Stop the program
To stop the chatbot, simply type `stop` when it is your turn to interact. Otherwise, use `control + c` (for MAC).

## Contact
If you run into issues running this code, please feel free to email me at `tobymsavage@gmail.com`.
