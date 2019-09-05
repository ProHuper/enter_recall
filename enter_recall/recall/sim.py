import math
import numpy as np


def o_sim(vector1, vector2):
    npvec1, npvec2 = np.array(vector1), np.array(vector2)
    similirity = math.sqrt(((npvec1 - npvec2) ** 2).sum())
    return similirity


def cos_sim(vector1, vector2):
    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a
    :param vector_b: 向量 b
    :return: sim
    """
    vector_a = np.mat(vector1)
    vector_b = np.mat(vector2)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim
