def page4(st):
    st.markdown("<h6 font-size: 1.0em;'>질문을 읽고 정확히 답변해 주시기 바랍니다. 설문에 대한 응답을 기초로 개인별 문항이 출제됩니다.</h6>", unsafe_allow_html=True)
    st.markdown("<h3 font-size: 1.0em;'>Part 3 of 3</h3>", unsafe_allow_html=True)

    # 여가 및 취미 질문
    leisure_hobbies_options = ["운동", "게임", "SNS", "문화생활", "여행", "자기관리", "예술활동", "자기개발"]
    selected_leisure_hobbies = st.multiselect("귀하는 여가 및 취미활동으로 주로 무엇을 하십니까? (두 개 이상 선택)", leisure_hobbies_options, key="leisure_hobbies")

    # 선택된 옵션을 딕셔너리에 저장
    st.session_state.selected_options['여가 및 취미'] = selected_leisure_hobbies

    # 가운데 정렬하기 위한 HTML/CSS
    centered_style = """
        <style>
            div.stButton > button {
                display: block;
                
            }
        </style>
    """

    # Streamlit 앱에 적용
    st.markdown(centered_style, unsafe_allow_html=True)
    col1_btn, col2_btn = st.columns(2)
    if col1_btn.button("< Back", type="primary", ):
        return 'page3'
        
    elif col2_btn.button("Next >", type="primary", ):
        if len(selected_leisure_hobbies) < 2:
            st.warning("최소 두 개의 활동을 선택해야 합니다.")
            return None  # 다음 페이지로 넘어가지 않음
        return 'page5'