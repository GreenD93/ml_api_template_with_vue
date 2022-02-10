import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import joblib
import re
import numpy as np

from ml.procs.txt.sif_generator import SIFGenerator
from konlpy.tag import Mecab, Kkma

from utils.settings import *
from utils.utils import *

class LevelModelHandeler():

    #-----------------------------
    # constructor
    def __init__(self):

        # -----------------------------
        # define model
        self.model = None
        self.scaler = None
        self.sif_generator = SIFGenerator()
        self.tagger = Kkma()

        # -----------------------------
        # model & meta path 설정
        self.model_path = BOOK_LEVEL_MODEL_PATH
        self.scaler_path = SCLAER_PATH
        self.top_word_dict_path = TOP_WORD_PATH

        self.sif_w2v_model_path = SIF_W2V_MODEL_PATH
        self.sif_word_freq_dict = SIF_WORD_FREQ_DICT

        # -----------------------------
        # 단어 리스트
        self.pos_tag_list = ['NNG', 'VV', 'MAG', 'VA', 'XR', 'MAJ', 'NNBC']
        self.top_word_set_by_level = None

        # -----------------------------
        # init
        self._prepare()

        pass

    #-----------------------------
    # _prepare
    def _prepare(self):
        self._load_model()
        self._load_scaler()
        self._load_top_word_dict()
        self._load_sif_generator()
        pass

    #-----------------------------
    # _load_model
    def _load_model(self):
        self.model = joblib.load(self.model_path)
        pass

    #-----------------------------
    # _load_scaler
    def _load_scaler(self):
        self.scaler = joblib.load(self.scaler_path)
        pass

    #-----------------------------
    # _load_top_word_dict
    def _load_top_word_dict(self):
        top_word_dict = file_to_json(self.top_word_dict_path)
        self.top_word_set_by_level = [set(top_word_dict['level_{0}'.format(i)]) for i in range(1,10)]
        pass

    #-----------------------------
    # _load_model
    def _load_sif_generator(self):
        self.sif_generator.load_w2v_model(self.sif_w2v_model_path)
        self.sif_generator.load_word_freq_dict(self.sif_word_freq_dict)
        pass

    #-----------------------------
    # predict
    def predict(self, sentence):

        """
        :param text: 형태소 처리가 끝난 결과 (morpheme)
        :return: predicted level
        """
        sentence = self._preprocess_sentence(sentence)
        morpheme = self._get_morpheme(sentence)


        if not morpheme:
            return print('분석에 필요한 형태소가 부족합니다.')

        else:

            # make features
            embedding_vector = self.sif_generator.make_sif_wvs_vector(morpheme)
            meta_features = self._get_book_meta_features(sentence, morpheme).reshape(1, -1)
            count_vector = self._count_word_by_grade(morpheme).reshape(1, -1)

            # concat all features
            x = np.hstack((embedding_vector, meta_features, count_vector))

            scaled_x = self.scaler.transform(x)
            pred = self.model.predict(scaled_x)

            return pred

    #-----------------------------
    # _preprocess_sentence
    def _preprocess_sentence(self, sentence):

        def clean_sentence(sentence):
            sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', sentence)
            return sentence

        splited_sentence = sentence.split('@##@')
        sentence = "@##@".join([clean_sentence(sent) for sent in splited_sentence])

        return sentence

    #-----------------------------
    # _get_morpheme
    def _get_morpheme(self, sentence):

        sentence = sentence.replace('@##@', '')
        tag_list = self.tagger.pos(sentence)
        morpheme = " ".join([tag[0] + '/' + tag[1] for tag in tag_list if tag[1] in self.pos_tag_list])

        return morpheme

    #-----------------------------
    # _get_book_meta_features
    def _get_book_meta_features(self, sentence, morpheme):

        splited_sentence = sentence.split('@##@')
        sen_cnt = len(splited_sentence)

        def get_avg_char_cnt():
            total_char = sum([len(line.replace(' ', '')) for line in splited_sentence])
            avg_char_cnt = total_char / sen_cnt
            return avg_char_cnt

        def get_avg_sentence_len():
            total_sentence_len = sum([len(line) for line in splited_sentence])
            avg_sentence_len = total_sentence_len / sen_cnt
            return avg_sentence_len

        def get_mor_cnt():
            mor_cnt = len(morpheme.split(' '))
            return mor_cnt

        def get_sen_cnt():
            return sen_cnt

        avg_char_cnt = get_avg_char_cnt()
        sentence_len = get_avg_sentence_len()
        sen_cnt = get_sen_cnt()
        mor_cnt = get_mor_cnt()

        meta_features = np.array([avg_char_cnt, sentence_len, mor_cnt, sen_cnt])

        return meta_features

    def _count_word_by_grade(self, text, norm=True):

        cnt_list = []

        splited_text = set(text.split(' '))
        total_word_cnt = len(splited_text)

        for top_word_set in self.top_word_set_by_level:
            inter_words = top_word_set.intersection(splited_text & top_word_set)
            cnt_list.append(len(inter_words))

        if total_word_cnt != 0 and norm:
            normalzed_cnt_list = [round((cnt / total_word_cnt), 4) if cnt != 0 else 0 for cnt in cnt_list]

        else:
            normalzed_cnt_list = [0 for _ in range(0,9)]

        return np.array(normalzed_cnt_list)