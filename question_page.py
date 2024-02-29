import tempfile
import os
import speech_recognition as sr
from gtts import gTTS
import torch
from transformers import (
    AutomaticSpeechRecognitionPipeline,
    WhisperForConditionalGeneration,
    WhisperTokenizer,
    WhisperProcessor,
)
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline
)
from peft import PeftModel, PeftConfig
from audio_recorder_streamlit import audio_recorder

def question_page(st, i):
    st.markdown("<h1 style='text-align: center; font-size: 1.5em;'>Question 1</h1>", unsafe_allow_html=True)
    st.markdown("<hr></hr>", unsafe_allow_html=True)

        # 이미지 추가
    image_url = "https://raw.githubusercontent.com/ttkdenddl11/Algorithm/main/index_woman.png"  # GitHub Raw URL 사용

    st.markdown(f'<div style="text-align: center;"><img src="{image_url}" style="width:33%;"></div>', unsafe_allow_html=True)
    
    def record_audio():
        r = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            audio_data = r.listen(source)

        return audio_data
    
    def save_audio_file(audio_data, directory="records"):
        filename = os.path.join(directory, f"record{i}.wav")
        with open(filename, "wb") as f:
            f.write(audio_data.get_wav_data())
        return filename    

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
        # whisper 허깅페이스
        result = st.session_state.whisper_pipe(audio_filename, generate_kwargs={"language": "english"})
        st.session_state.transcript_text.append(result["text"])
        st.write("인식된 텍스트:", st.session_state.transcript_text[i - 1]) 

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
    