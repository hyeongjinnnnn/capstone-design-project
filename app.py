import mysql.connector
import streamlit as st
import pandas as pd
from page1 import page1
from page2 import page2
from page3 import page3
from page4 import page4
from page5 import page5
from question_page import question_page
import torch
from transformers import (
    AutomaticSpeechRecognitionPipeline,
    WhisperForConditionalGeneration,
    WhisperTokenizer,
    WhisperProcessor,
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline
)

# st.session_state 초기화
# mysql 연결
if 'connection' not in st.session_state:
    st.session_state.connection = mysql.connector.connect(
        host='db4free.net',
        user='hyeongjin',
        password='abcd1234',
        database='opic_automatic'
    )

# whisper 허깅페이스 파이프 구축
if 'whisper_pipe' not in st.session_state:
    device = "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = "openai/whisper-large-v3"
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device).float()
    print(device)
    processor = AutoProcessor.from_pretrained(model_id)

    st.session_state.whisper_pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=256,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'page1'

if 'selected_options' not in st.session_state:
    st.session_state.selected_options = {}

if "question_list" not in st.session_state:
    st.session_state.question_list = []
    
if "transcript_text" not in st.session_state:
    st.session_state.transcript_text = []

if "question_page_number" not in st.session_state:
    st.session_state.question_page_number = 0

# 다음 페이지 문자열 변수
next_page = None

# 현재 페이지에 따라서 함수 호출
if st.session_state.current_page == 'page1':
    next_page = page1(st)
elif st.session_state.current_page == 'page2':
    next_page = page2(st)
elif st.session_state.current_page == 'page3':
    next_page = page3(st)
elif st.session_state.current_page == 'page4':
    next_page = page4(st)
elif st.session_state.current_page == 'page5':
    next_page = page5(st)
elif st.session_state.current_page == 'question_page':
    next_page = question_page(st, st.session_state.question_page_number)

# next_page에 따라서 current_page 업데이트
if next_page:
    st.session_state.current_page = next_page
    next_page = None  # next_page 초기화
    st.rerun()  # Rerun the app to update the layout