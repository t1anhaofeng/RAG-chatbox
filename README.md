It is a chatbox using OpenAi model for the three txt files in the Data Directory.

For this project, I used Langchain as a library to create the Chroma database to install the vector data and then used OpenAi model to generate a response for the question the user could add.

To be more specific, during the creating Database part, I used the document loader from langchain to chunk the info read from the txt file into smaller pieces. After that, I used the OpenAiEmbedding and chroma database to store the vector data.
After creating the database, I used the OpenAIEmbeddings to create the vector data for the query text and then compare it with all chunks to get the closest three results. Based on the results, I used the OpenAi model to get the final response.

To set up the project, first include a python file called Key and add an attribute called "API_KEY" for openAI. After that, first run the creat_database.py to create the vector database and then run python query_data.py "Your question".

Time for the project:

Watching tutorials and development: 3h
Setup: 0.5h
