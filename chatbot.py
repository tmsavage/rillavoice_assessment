import os
import openai
import sys
from neo4j import GraphDatabase, basic_auth
sys.path.append('../..')
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key = os.environ['OPENAI_API_KEY']

def produce_cypher_query(user_prompt, context_array):
    context = context_array.copy()
    start_delim = "---START_CODE---"
    end_delim = "---END_CODE---"

    conversation_summary = ""
    for message in context:
        if message['role'] == 'system':
            conversation_summary += message['content'] + " "
        elif message['role'] == 'assistant':
            conversation_summary += "In response to the user, the chatbot said: " + message['content'] + " "

    enhanced_context = f"Based on the conversation so far, which includes: {conversation_summary}, the user is now asking: {user_prompt}"

    system_prompt = """
        You will be provided a conversation between a chatbot and a user prompt, where you must produce a Cypher query based on Neo4J's Sandbox Movie database
        that answers the preceding question. Use your intuition and info from the conversation to figure out what the user is asking to produce an appropriate query. 
        The known labels are 'Person' and 'Movie'. 
        The possible relationship types are 'ACTED_IN', 'DIRECTED', 'FOLLOWS', 'PRODUCED', 'REVIEWED', and 'WROTE'. Your response should be between 
        the delimiters ---START_CODE--- and ---END_CODE---.

        ONLY output the Cypher query.
    """
    
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': enhanced_context}
    ]

    response = get_completion_from_messages(messages, model="gpt-4")
    start_index = response.find(start_delim) + len(start_delim)
    end_index = response.find(end_delim)
    cypher_query = response[start_index:end_index].strip()

    return cypher_query


def get_data_from_neo4j(cypher_query):
    try:
        driver = GraphDatabase.driver(
            os.environ['NEO4J_BOLT_URL'],
            auth=basic_auth(os.environ['NEO4J_USERNAME'], os.environ['NEO4J_PASSWORD']))

        with driver.session(database="neo4j") as session:
            results = session.execute_read(lambda tx: tx.run(cypher_query).data())
        
        driver.close()
        return results
    except Exception as e:
        print("Failed to retrieve data:", e)
        return None


def get_completion_from_messages(messages, model="gpt-3.5-turbo-16k", temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]


def question_checker(user_input):
    system_prompt = """
        Based on the following user prompt, you are to decide the category of the user's question. Here are the categories:
   
        Respond with 1 or 0:
        1 - This category relates to anything to the Neo4J Sandbox Movie dataset.
        0 - Category for queries NOT related to the Neo4J Sandbox Movie dataset. Typically a general question.
        
        ONLY Output a single character.
    """

    neo4j_user_prompt = f"""
        What movies did Tom Hanks act in?
    """
    other_user_prompt = f"""
        Can you sing me a song?
    """
    messages = [
        {'role':'system', 'content': system_prompt},
        {'role':'user', 'content': f"{neo4j_user_prompt}"},
        {'role':'assistant', 'content': '1'},
        {'role': 'user', 'content': f"{other_user_prompt}"},
        {'role':'assistant', 'content': '0'},
        {'role':'user', 'content': f"{user_input}"},
    ]
    
    return get_completion_from_messages(messages, model="gpt-4", max_tokens=1)

def check_if_question_asked(user_input, context_array):
    context = context_array.copy()
    delimiter = "!!!!"

    system_prompt = f"""
        Check if the following user question delimited by {delimiter} or similar one has been asked before in this conversation. Do NOT answer the question.

        Respond only with 1 or 0:
        1 - if the question has been asked before.
        0 - if the question has NOT been asked yet.
    """

    messages = [
        {'role':'system', 'content': f"{system_prompt}"},
        {'role':'user', 'content': f"{delimiter}{user_input}{delimiter}"}
    ]

    context.extend(messages)

    return get_completion_from_messages(context, model="gpt-4", max_tokens=50)


def main():
    delimiter = "~~~~"

    start_convo_flag = True
    context = [{'role':'system', 'content':f"""
        You are a chatbot called 'Movie Genius' that will answer questions based on movies. For each quesiton, you will be provided the 
        answer through the 'system' roles, which will contain information from the Neo4J sandbox database on Movies. You will reply to 
        the user using the provided answer. At the end of your answer, ask the user if they want to ask another question. 
    """}]

    context.append({'role':'user', 'content':f"{delimiter}Hi!{delimiter}"})
    init_response = get_completion_from_messages(context)

    print("-- Movie Genius: ", init_response)
    while start_convo_flag:
        user_input = input("-- User: ")
        if user_input == "stop":
            break

        result = ""
        question_category = question_checker(user_input)

        if int(question_category) == 1: # if user's question is related to movies
            asked_previously = check_if_question_asked(user_input, context)
            if int(asked_previously) == 0: # if user's question was previously asked
                cypher_query = produce_cypher_query(user_input, context)
                results = get_data_from_neo4j(cypher_query)

                if results == None:
                    context.append({'role':'system', 'content':f"""
                        ERROR: issue pulling data from database. Apologize to the user and suggest to try again.
                    """})
                else:
                    context.append({'role':'system', 'content':f"{results}"})
        else:
            context.append({'role':'system', 'content':f"""
                ERROR: user tried asking a question off-topic. Apologize to the user and suggest to try another question.
            """})

        context.append({'role':'user', 'content':f"{delimiter}{user_input}{delimiter}"})
        response = get_completion_from_messages(context)
        print("-- Movie Genius: ", response)
        context.append({'role': 'assistant', 'content':f"{response}"})

if __name__ == "__main__":
    main()