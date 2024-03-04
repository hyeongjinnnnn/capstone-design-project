import tempfile
import os
import threading
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

# from peft import PeftModel, PeftConfig
from audio_recorder_streamlit import audio_recorder

def question_page(st, i):
    st.markdown(f"<h1 style='text-align: center; font-size: 1.5em;'>Question {i}</h1>", unsafe_allow_html=True)
    st.markdown("<hr></hr>", unsafe_allow_html=True)

        # 이미지 추가
    image_url = "https://raw.githubusercontent.com/ttkdenddl11/Algorithm/main/index_woman.png"  # GitHub Raw URL 사용

    st.markdown(f'<div style="text-align: center;"><img src="{image_url}" style="width:33%;"></div>', unsafe_allow_html=True)
    
    def record_audio():
        r = sr.Recognizer()
        r.pause_threshold = 10.0
        mic = sr.Microphone()

        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio_data = r.listen(source)

        return audio_data
    
    def save_audio_file(audio_data, directory = "records"):
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = os.path.join(directory, f"record{i}.wav")
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
        save_transcription_to_file(transcript, audio_filename, save_directory='D:/capstone_project/opic/transcription')
        st.session_state.transcript_text.append(transcript)
        # transcript_filename = audio_filename.replace(".wav", "_transcript.txt")

    def start_transcription_thread(audio_filename, whisper_pipe):
        thread = threading.Thread(target=transcribe_audio_in_background, args=(audio_filename, whisper_pipe))
        thread.start()

    def text_to_speech(text, lang='en'):
        # 임시 파일 생성
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_filename = temp_file.name

        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(temp_filename)
        return temp_filename

    # TTS 버튼
    if st.button(f"question {i}"):
        question = st.session_state.question_list[i - 1]
        output_file = text_to_speech(question, lang="en")
        st.audio(output_file, format='audio/wav')

    
    # audio_bytes = audio_recorder(
    #     energy_threshold=(-1.0, 1.0),
    #     pause_threshold=60.0,
    # )

    # if audio_bytes:
    #     st.audio(audio_bytes, format="audio/wav")
        
    if st.button("녹음 시작"):
        with st.spinner("녹음 중..."):
            audio_data = record_audio()
            st.success("녹음 완료!")

        audio_filename = save_audio_file(audio_data)
        whisper_pipe = st.session_state.whisper_pipe
        start_transcription_thread(audio_filename, whisper_pipe)
        # whisper 허깅페이스
        # result = st.session_state.whisper_pipe(audio_filename, generate_kwargs={"language": "english"})
        # st.session_state.transcript_text.append(result["text"])
        # st.write("인식된 텍스트:", st.session_state.transcript_text[i - 1]) 

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

    if st.button("Next >", type="primary", ):
        st.session_state.question_page_number += 1
        return 'question_page'