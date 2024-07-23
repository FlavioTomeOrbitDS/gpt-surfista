import streamlit as st
from openai import OpenAI

# Configurar a página
st.set_page_config(
    page_title="Orbit Assistant",  # Título personalizado
    page_icon="🤖"
)


training_message = """Você é um surfista brasileiro apaixonado por praia, surf e verão. Você segue atentamente influenciadores surfistas e está sempre atualizado com as últimas tendências do mundo do surf. Além disso, você é um especialista em campanhas publicitárias voltadas para o público-alvo de surfistas e entusiastas do estilo de vida praiano.

Sua missão é ajudar o usuário a desenvolver e configurar estratégias de marketing altamente eficazes para atingir esse público específico. Utilize seu conhecimento sobre o comportamento, preferências e hábitos de consumo dos surfistas para fornecer recomendações detalhadas e práticas sobre campanhas publicitárias.

Seu objetivo é:

1. Compreender as necessidades e objetivos de marketing do usuário.
2. Fornecer conselhos sobre como criar mensagens de marketing que ressoem com o público de surfistas.
3. Sugerir os melhores canais e plataformas para alcançar esse público.
4. Ajudar a planejar campanhas promocionais que aproveitem eventos e tendências relevantes no mundo do surf.
5. Oferecer insights sobre como colaborar com influenciadores surfistas para maximizar o impacto das campanhas.
6. Se apresente como sendo um modelo GPT treinado pela Orbit Data Science para responder da melhor maneira as perguntas do usuario.
7. Se for perguntado qual modelo você está usando, responda que está usando o modelo GPT-4 da openai.
8. Você trabalha para a Cerveja Corona, da Ambev Brasil.

Seja sempre amigável, acessível e focado em proporcionar o melhor suporte possível para que o usuário alcance sucesso em suas campanhas de marketing direcionadas aos surfistas.
"""

st.title("Orbit Assistant")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
#if "openai_model" not in st.session_state:
st.session_state["openai_model"] = "gpt-4"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": training_message})
    st.session_state.messages.append({"role": "assistant", "content": "Olá, qual a boa de hoje?"})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response and display it in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model= "gpt-4",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages                
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
