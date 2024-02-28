
if __name__ == '__main__':
    import streamlit as st
    from langchain_helper import get_qa_chain, create_vector_db

    st.title("E-Passport BD Q&A 🪪")
    btn = st.button("Create Knowledgebase")
    if btn:
        create_vector_db()

    question = st.text_input("Question: ")

    if question:
        chain = get_qa_chain()
        response = chain(question)

        st.header("Answer")
        st.write(response["result"])
        
        st.write("Note: Sometimes LLM will create answer of its own (hallucination)")
        # also print the result in the console for better debuging purposes
        print(response['result'])