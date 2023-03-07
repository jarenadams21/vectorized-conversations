import gradio as gr
import openai
import config
import subprocess

openai.api_key = config.OPENAI_API_KEY

messages = [
        {"role": "system", "content": "You are a down-to-earth, considerate, respectful, and realistic entity to talk to for any reason, or for none at all!"},
        #{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        #{"role": "user", "content": "Where was it played?"}
    ]

def transcribe(audio):
    global messages


    print(audio)

    # Process audio input from user
    audio_file= open(audio, "rb")

    # Whisper-1 Model
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)

    messages.append({"role": "user", "content": transcript["text"]})
    #Gpt-3.5 Turbo Model
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
)

    system_message = response['choices'][0]['message']

    messages.append(system_message)

    print(response)

    # Output Formatting
    chat_transcript = ""

    for message in messages:
        if message['role'] != 'system':
            if message['role'] == 'assistant':
               message['role'] = 'entity' 
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    # Return chat log after each transcription
    subprocess.call(["say", system_message['content']])
    return chat_transcript

ul = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()
ul.launch() 