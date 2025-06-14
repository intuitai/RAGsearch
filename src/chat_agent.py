import streamlit as st
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from pprint import pprint

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

load_dotenv()
storage_path = "./vector_store"
document_path = "./documents"

Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
Settings.num_output = 512
Settings.context_window = 3900

@st.cache_resource(show_spinner=False)
def initialize():
    if not os.path.exists(storage_path):
        documents = SimpleDirectoryReader(document_path).load_data()
        local_index = VectorStoreIndex.from_documents(documents)
        local_index.storage_context.persist(persist_dir=storage_path)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=storage_path)
        local_index = load_index_from_storage(storage_context)
    return local_index

index = initialize()
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

st.title("Chat bot")
if 'messages' not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("Ask a question about the documents:"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            pprint(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)




