import argparse

from langchain_openai import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from openai import embeddings, api_key

from Key import CHROMA_PATH, API_KEY

PROMPT_TEMPLATE = """
Answer the question based on the following content:

{context}

---

Answer the question based on the above context: {question}

"""

def main():
    parser = argparse.ArgumentParser(description="hi")
    parser.add_argument("query_text", type = str, help = "The query text")
    args = parser.parse_args()
    query_text = args.query_text

    embedding_function = OpenAIEmbeddings(api_key = API_KEY)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0:
        print(f"Unable to find matching results")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE, api_key =API_KEY)
    prompt = prompt_template.format(context=context_text, question = query_text)
    print(prompt)

    model = ChatOpenAI(api_key=API_KEY)
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text.content}\nSources:{sources}"
    print(formatted_response)

if __name__ == "__main__":
    main()