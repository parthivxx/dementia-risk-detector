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

    upload_file = st.file_uploader("Upload an image" , accept_multiple_files=True)
    image_paths = []

    if upload_file is not None:

        submit_button = st.button("Generate risks")

        if submit_button:
            st.image(upload_file)

            # image = PIL.Image.open(upload_file[0])
            # temp_image_path = "temp_image.jpg"
            # image.save(temp_image_path)

            for index , file in enumerate(upload_file):
                picture = PIL.Image.open(file)
                temp_image_path = f"image_{index+1}.jpg"
                picture.save(temp_image_path)
                image_paths.append(f"image_{index+1}.jpg")
                
            prompt_content = [
                {
                    "type": "text",
                        "text": "You're an expert in detecting any kind of risk that could be harmful to a dementia patient by analysing images.\nIs their any risk for a dementia patient in the given picture ? If yes , then what are those ?\n And suggest how can this risk might be avoided ?"
                }
            ]

            for image_path in image_paths:
                prompt_content.append({
                     "type": "image_url", "image_url": image_path
                })

            human_message = HumanMessage(
                content=prompt_content
            )

            with st.spinner(f"Genetaing response..."):
                response = llm.invoke([human_message])
                st.write(response.content)


if __name__ == "__main__":
    main()
