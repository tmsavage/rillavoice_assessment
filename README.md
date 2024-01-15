# rillavoice_assessment
This project is my submission to RillaVoice's take-home coding assessment.

## Requirements
You will need to update the .env file with your own hidden variable values. This includes an `OPENAI_API_KEY`, `NEO4J_BOLT_URL`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD`. The code will otherwise not work. 

Unless you have already have these dependencies installed, you will need to install the following:

- openai
- Neo4j
- python-dotenv

## Setting pu the Environment
Update the `.env` file in the root directory of the project. Add the necessary environment variables as follows:
```
OPENAI_API_KEY=your_openai_api_key_here
NEO4J_BOLT_URL=bolt://your_neo4j_url_here
NEO4J_USERNAME=your_neo4j_username_here
NEO4J_PASSWORD=your_neo4j_password_here
```

Once completed, run the following command to download the required dependencies:
`pip install -r requirements.txt`.

## Run the script
To run the script, all you need to do is open your terminal, navigate to the repository directory, and run `python3 chatbot.py`.

## Testing the Chatbot
The chatbot is capable of answering direct questions regarding the Neo4j and capable of referring to previous questions or answers within the conversation. Some example questions include:

`How many movies has Tom Hanks acted in?`
`What are the names of those movies?`
`Who directed Cloud Atlas?`
`What movie did Tom Hanks direct?`
`Find me the shortest path etween Kevin Bacon and Meg Ryan`
`Did Meg Ryan direct any films?`.

The chatbot is also capable of noticing whether a question is off-topic from movies, and thus will refuse to answer. An example question to ask is:

`What is your favorite color?`.

# Contact
If you run into issues running this code, please feel free to email me at `tobymsavage@gmail.com`.
