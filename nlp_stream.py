#스트림릿 사용
import streamlit as st

#텍스트 전처리 패키지
import neattext as nt 

# 정규표현식 가-힣
import re

#텍스트 처리, 감정분석 패키지
from textblob import TextBlob

#시각화 패키치
import matplotlib.pyplot as plt
import matplotlib 
matplotlib.use("Agg")

# 자연어 처리와 관련된 패키치
from wordcloud import WordCloud
from deep_translator import GoogleTranslator
import spacy 

#카운팅용 함수
from collections import Counter


def text_anlysis(text):
    #자연어처리 spacy -> en_core_web_sm(영어 처리) 모델 로드
    nlp = spacy.load("en_core_web_sm")

    #입력한 text를, nlp 전처리기를 활용해서 doc 변수에 저장
    doc = nlp(text)

    #doc에 저장된 토큰화된 데이터를
    #Token, Lemma 라는 라벨을 붙여 all_data에 저장
    #이 함수가 실행된 후 최종적으로 결과를 전달
    all_Data = [('"Token" : {}, \n "Lemma : {} '.format(token.text, token.lemma_)) for token in doc]
    return all_Data

#입력한 텍스트를 저장하는 함수
def summarize_text(text, num_sentence=3):

    #입력한 텍스트를 정리
    #re -> 정규표현식
    #r'[^a-zA-Z]' -> 알파벳이 아닌 것들을 찾아서 ' '로 대체
    cleaned_text = re.sub(r'[^a-zA-Z]', ' ', text).lower()

    #cleaned_text를 공백 기준으로 분할하여, words에 저장
    words = cleaned_text.split()

    #Counter를 활용하여, words의 각 단어의 빈도수를 계산
    words_freq = Counter(words)

    #얼마나 빈번하게 나타났는가를 기준으로 정렬
    sorted_words_freq = sorted(words_freq, key=words_freq.get, reverse=True)

    #top 3개의 빈번하게 나타난 단어 추출
    top_words = sorted_words_freq[:num_sentence]

    #top_words를 공백을 기준으로 합치기
    summary = ' '.join(top_words)

    return summary




#스트림릿 페이지에서 사용할 모든 함수, 레이아웃 등을 정의
def main():
    subheader = """
    <div style="background-color:rgba(125, 200, 125, 0.8); padding:8px;">
    <h3 style="color:white">텍스트 분석 및 감성분석</h1>
    </div>
    """

    title = "자연어처리프로젝트"
    st.title(title)
    st.markdown(subheader, unsafe_allow_html=True)

    #사이드바를 만들어서/ 사이드바 제목 및 메뉴 선택 적용
    st.sidebar.title("NLP 프로젝트")

    #셀렉트박스의 다양한 결과물을 menu 변수에 저장하여 
    #선택에 따라 sidebar에 text 출력
    menu = st.sidebar.selectbox("메뉴", ["텍스트 분석", "감성 분석", "번역", "이 프로젝트에 대하여"])

    if menu == "텍스트 분석":
        raw_text = st.text_area("TEXT INPUT",
                             "여기에 영어 텍스트를 입력하세요", height=300)
    
        #버튼을 누르면 분석을 실행하도록 함
        if st.button("Start"): 
            if len(raw_text) == 0:
                st.warning("텍스트가 입력되지 않았습니다.")
            else: 
                col1, col2 = st.columns(2)
                with col1:
                    #내가 입력한 자연어 대한 기본적인 분석 정보
                    with st.expander("Basic Info for NLP"):
                        word_desc = nt.TextFrame(raw_text).word_stats()
                        result_desc = {"Len of Text:", word_desc['Length of Text'],
                                    "Num of Vowels:", word_desc['Num of Vowels'],
                                    "Num of Stopwords: ", word_desc['Num of Stopwords']}
                    st.write(result_desc)

                with col2:
                    with st.expander("Pre-processed-Text"):
                        processed_text = str(nt.TextFrame(raw_text).remove_stopwords())
                        st.write(processed_text)


    elif menu == "감성 분석":
        raw_text = st.text_area("TEXT INPUT", "여기에 텍스트를 입력하세요", height = 300)

        #버튼을 누르면 분석을 실행하도록 함
        if st.button("분석 시작"):
            if len(raw_text) == 0:
                st.warning("텍스트가 입력되지 않았습니다.")
            else:
                blob = TextBlob(raw_text)
                result = blob.sentiment
                st.success(result)

    elif menu == "번역":
        raw_text = st.text_area("TEXT INPUT", "여기에 텍스트를 입력하세요", height = 300)

        if len(raw_text) < 3:
            st.warning("텍스트가 너무 짧습니다.")
        else:
            target_language = st.selectbox("번역할 언어를 선택하세요", ["German", "Spanish", "French", "Italian"])
            if target_language == 'German':
                target_language = 'de'
            elif target_language == 'Spanish':
                target_language = 'es'
            elif target_language == 'French':
                target_language = 'fr'
            else:
                target_language = 'it'

            if st.button("번역 시작"):
                translator = GoogleTranslator(source='auto', target_language)
                translated_text = translator.translate(raw_text)
                st.write(translated_text)
                
#파이썬 파일이 처음 시행될 때,
#여기부터 순서대로 실행됩니다.
if __name__ == "__main__":
    main()