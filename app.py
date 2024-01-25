import io
import requests
import streamlit as st
from PIL import Image


def query_stable_diffusion_model(payload, headers):
    API_URL = 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0'
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


st.title('💬 Chatbot - Text2Image')
st.caption('🚀 A Streamlit chatbot powered by Stable Diffusion XL Base 1.0')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {'role': 'assistant', 'content': 'What kind of image that I need to draw? (example: cat wearing goggles)'}
    ]
    
for message in st.session_state.messages:
    st.chat_message(message['role']).write(message['content'])
    if 'image' in message:
        st.chat_message('assistant').image(message['image'], caption=message['prompt'], use_column_width=True)

if prompt := st.chat_input():
    if not st.secrets.hugging_face_token.api_key:
        st.info('Please add your Hugging Face Token to continue.')
        st.stop()
    
    # Input prompt
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    st.chat_message('user').write(prompt)
    
    # Query Stable Diffusion
    headers = {'Authorization': f'Bearer {st.secrets.hugging_face_token.api_key}'}
    
    image_bytes = query_stable_diffusion_model({
        'inputs': prompt,
    }, headers)
    print(image_bytes)
    # Return Image
    image = image = Image.open(io.BytesIO(image_bytes))
    msg = f'here is your image related to "{prompt}"'

    # Show Result
    st.session_state.messages.append({'role': 'assistant', 'content': msg, 'prompt': prompt, 'image': image})
    st.chat_message('assistant').write(msg)
    st.chat_message('assistant').image(image, caption=prompt, use_column_width=True)