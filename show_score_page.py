from transformers import RobertaForSequenceClassification, RobertaTokenizer
import torch
import time
import os

def show_score_page(st):
    transcription_dir = "transcription"
    transcript_complete = False
    transcript_list = []

    with st.spinner("전사중입니다..."):  
        while not transcript_complete:
            for filename in os.listdir(transcription_dir):
                if "record15_transcript.txt" in filename:
                    for i in range(1, 16):
                        record_filename = f"record{i}_transcript.txt"
                        if os.path.exists(os.path.join(transcription_dir, record_filename)):
                            with open(os.path.join(transcription_dir, record_filename), "r", encoding="utf-8") as file:
                                text = file.read()
                                transcript_list.append(text)
                                print(f"Added text from {record_filename}")
                    transcript_complete = True
            time.sleep(1)


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

    st.markdown("<h1 style='text-align: center; color: blue; font-size: 2em;'>Oral Proficiency Interview - computer (OPIc)</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 1.5em;'>점수</h1>", unsafe_allow_html=True)

    def load_model_and_tokenizer(model_path):
        model = RobertaForSequenceClassification.from_pretrained(model_path)
        tokenizer = RobertaTokenizer.from_pretrained(model_path)
        return model, tokenizer

    models_paths = {
        "Task_Completion": "model/Task_Completion",
        "Delivery": "model/Delivery",
        "Accuracy": "model/Accuracy",
        "Appropriateness": "model/Appropriateness"
    }

    models_and_tokenizers = {criteria: load_model_and_tokenizer(path) for criteria, path in models_paths.items()}

    def predict(criteria, text, models_and_tokenizers):
        model, tokenizer = models_and_tokenizers[criteria]
    
        # 텍스트를 토크나이징하여 모델 입력 형식으로 변환
        inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    
        # GPU 사용 가능 여부 확인
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        inputs = {k: v.to(device) for k, v in inputs.items()}
    
        # 예측 수행
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            # probabilities = torch.softmax(logits, dim=1)
    
        # return probabilities
        return logits
    
    # 각 평가 항목별로 예측 수행
    for question, transcript in zip(st.session_state.question_list, transcript_list):
        a = f"question : {question}  \n\n answer : {transcript}"

        # 각 평가 항목에 대해 점수 예측
        for criteria in models_paths.keys():
            score = predict(criteria, a, models_and_tokenizers)
            print(f"{criteria}: {score}")

    
    st.markdown("<h3 style='text-align: center; font-size: 1.5em;'>수고하셨습니다.</h3>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)