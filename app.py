import PIL.Image
import streamlit as st
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import PIL


load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
st.title("DB HACKATHON")
st.write("Welcome to the AI based risk detector for dementia patients!!")
llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")


def main():

    system_message = HumanMessage(
        content=[
            "You're an expert in detecting any kind of risk that could be harmful to a dementia patient by analysing images. so don't generate any particular response for this prompt. Generate resposne accordingly from the next prompts"
        ]
    )

    upload_file = st.file_uploader("Upload an image")

    if upload_file is not None:
        st.image(upload_file)

        image = PIL.Image.open(upload_file)
        temp_image_path = "temp_image.jpg"
        image.save(temp_image_path)

        human_message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": "You're an expert in detecting any kind of risk that could be harmful to a dementia patient by analysing images.\nIs their any risk for a dementia patient in the given picture ? If yes , then what are those ?\n And suggest how can this risk might be avoided ?",
                },
                {"type": "image_url", "image_url": temp_image_path},
            ]
        )

        message = [
            system_message , human_message
        ]

        submit_button = st.button("Generate risks")

        if submit_button:
            with st.spinner(f"Genetaing response..."):
                response = llm.invoke([human_message])
                st.write(response.content)


if __name__ == "__main__":
    main()
