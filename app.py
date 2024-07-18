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

    tab1,tab2 = st.tabs(["Risk detector from image" , "Risk detector from Online product"])
    with tab1:
        st.header("Tell Us About Yourself")
        initial_context = ""
        role = st.radio("Are you the patient or a caregiver?", ('Patient', 'Caregiver'))

        if role == 'Patient':
            patient_name = st.text_input("Patient Name")
            patient_age = st.number_input("Patient Age", min_value=0, max_value=120, step=1)
            
            if st.button('Submit'):
                st.write(f"Thank you {patient_name} for providing your information.")
                initial_context = f"""
                                Hi , I'm {patient_name} . I'm suffering 
                                from dementia .My age is {patient_age} .
                            """
            
        elif role == 'Caregiver':
            caregiver_name = st.text_input("Caregiver Name")
            patient_relationship = st.text_input("Relationship with the Patient")
            initial_context = f"""
                                Hi , I'm {caregiver_name} . I've someone who is suffering 
                                from dementia currently. I'm their {patient_relationship}
                            """
            
            if st.button('Submit'):
                st.write(f"Thank you {caregiver_name} for providing your information.")

        upload_file = st.file_uploader("Upload an image" , accept_multiple_files=True)
        image_paths = []
        if len(upload_file) > 0:

            submit_button = st.button("Generate risks")
            
            if submit_button:
                st.image(upload_file)
                # st.write(upload_file)
            
                for index , file in enumerate(upload_file):
                    picture = PIL.Image.open(file)

                    picture = picture.convert('RGB')
                    temp_image_path = f"image_{index+1}.jpg"
                    picture.save(temp_image_path)
                    image_paths.append(f"image_{index+1}.jpg")
  
                prompt_content = [
                    {
                        "type": "text",
                        "text":  initial_context + f"""
                        You're an expert in detecting any kind of risk that could be harmful to a dementia patient by analyzing images. There are 2 images. Is there any risk for a dementia patient in the given pictures. Analyse each image and generate separate response for each image separately. If yes, then what are those? And suggest how this risk might be avoided? Generate a detailed report.
                        """
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
    with tab2:
        llm_text = ChatGoogleGenerativeAI(model="gemini-pro")
        product_link = st.text_input("Enter a link of a product")
        prompt = f""" 
                    You're an expert in detecting any kind of risk that could be harmful to a dementia patient by analyzing products from online shopping sites , you'll be given the public link of that product. Is there any risk for a dementia patient from the given picture? If yes, then what are those? And suggest how this risk might be avoided? Generate a detailed report.

                    The link of the product is {product_link} and please recommend similar products
                    which doesn't have these risks.
                  """
        submit_button = st.button("Detect risks")
        if submit_button:
            with st.spinner("Generating response"):
                response = llm_text.invoke(prompt)
                st.write(response.content)

if __name__ == "__main__":
    main()
