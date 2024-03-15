import tempfile
import os
import threading
import time
import speech_recognition as sr
from gtts import gTTS
import torch
from transformers import (
    AutomaticSpeechRecognitionPipeline,
    WhisperForConditionalGeneration,
    WhisperTokenizer,
    WhisperProcessor,
    AutoModelForSpeechSeq2Seq,
    pipeline
)
from streamlit_TTS import auto_play, text_to_audio

import base64
from audiorecorder import audiorecorder

def question_page(st, i):
    if f'question{i}_clicks' not in st.session_state:
        st.session_state[f'question{i}_clicks'] = 2

    # 가운데 정렬하기 위한 HTML/CSS
    centered_style = """
        <style>
            div.stButton > button {
                display: block;
                margin: 0 auto;
            }
        </style>
    """

    # Streamlit 앱에 적용
    st.markdown(centered_style, unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 1.5em;'>Question {i}</h1>", unsafe_allow_html=True)
    st.markdown("<hr></hr>", unsafe_allow_html=True)

    # 이미지 추가
    image_url = "https://raw.githubusercontent.com/ttkdenddl11/Algorithm/main/index_woman.png"  # GitHub Raw URL 사용

    st.markdown(f'<div style="text-align: center;"><img src="{image_url}" style="width:33%;"></div>', unsafe_allow_html=True)
    
    def record_audio():
        r = sr.Recognizer()
        r.pause_threshold = 5.0
        # r.dynamic_energy_threshold = True
        r.energy_threshold = 3500

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=2)
            audio_data = r.listen(source)

        return audio_data
    
    def save_audio_file(audio_data, save_directory = "records"):
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        filename = os.path.join(save_directory, f"record{i}.wav")
        with open(filename, "wb") as f:
            f.write(audio_data.get_wav_data())
        return filename    
    
    def save_transcription_to_file(transcript, audio_filename, save_directory):
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        
        base_filename = os.path.basename(audio_filename)
        base_filename_without_ext = os.path.splitext(base_filename)[0]
        
        transcript_filename = f"{base_filename_without_ext}_transcript.txt"
        transcript_filepath = os.path.join(save_directory, transcript_filename)
        
        with open(transcript_filepath, "w", encoding="utf-8") as file:
            file.write(transcript)
        print(f"Transcript saved to {transcript_filepath}")


    def transcribe_audio_in_background(audio_filename, whisper_pipe):
        # Function to be run in a separate thread for transcribing audio
        # result = st.session_state.whisper_pipe(audio_filename, generate_kwargs={"language": "english"})
        result = whisper_pipe(audio_filename, generate_kwargs={"language": "english"})
        transcript = result["text"]
        save_transcription_to_file(transcript, audio_filename, save_directory='transcription')


    def start_transcription_thread(audio_filename, whisper_pipe):
        thread = threading.Thread(target=transcribe_audio_in_background, args=(audio_filename, whisper_pipe))
        thread.start()

    def autoplay_audio(file_path: str):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls autoplay="true" style="display: none;">
                <source src="data:audio/wav;base64,{b64}" type="audio/wav">
                </audio>
                """
        st.markdown(md, unsafe_allow_html=True,)

    def text_to_speech(text, lang='en'):
        # audio_filename = f"question_audio{i}.wav"
        # 파일 생성
        # tts = gTTS(text=text, lang=lang, slow=False)
        audio = text_to_audio(text, language='en')
        auto_play(audio, key=st.session_state[f'question{i}_clicks'])
        # tts.save(audio_filename)
        # # 오디오 출력
        # autoplay_audio(audio_filename)
        # # 파일 삭제
        # os.remove(audio_filename)
    

    # TTS 버튼
    if st.button(f"question {i}"):
        question = st.session_state.question_list[i - 1]
        if st.session_state[f'question{i}_clicks'] != 0:
            st.session_state[f'question{i}_clicks'] -= 1
            #audio = text_to_audio(question, language='en')
            #auto_play(audio)
            text_to_speech(question)
        else:
            st.error(f"You have already played Question {i}.")

    if st.button("녹음 시작"):
        with st.spinner("녹음 중... 5초 동안 말하지 않으면 종료됩니다."):
            audio_data = record_audio()
            st.success("녹음 완료!")

        audio_filename = save_audio_file(audio_data)
        whisper_pipe = st.session_state.whisper_pipe
        start_transcription_thread(audio_filename, whisper_pipe)
        st.session_state.question_next_btn = True

        # whisper 허깅페이스
        # result = st.session_state.whisper_pipe(audio_filename, generate_kwargs={"language": "english"})
        # st.session_state.transcript_text.append(result["text"])
        # st.write("인식된 텍스트:", st.session_state.transcript_text[i - 1]) 

    if st.session_state.question_next_btn:
        if st.button("Next >", type="primary", ):
            st.session_state.question_page_number += 1
            st.session_state.question_next_btn = False
            
            if st.session_state.question_page_number == 16:
                return 'show_score_page'
            
            return 'question_page'
        