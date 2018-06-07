import numpy as np
from scipy.special import polygamma, gamma, digamma

init_alpha = 1
init_beta = 1

def gen_samples(alpha, beta, num=100):
    data = np.random.gamma(shape=alpha, scale=1/beta, size=num)
    global s_x, s_logx
    s_x = np.sum(data) / num
    s_logx = np.sum(np.log(data)) / num
    return data

def nll(alpha, beta):
    return -3 * alpha * np.log(beta) + np.log(gamma(alpha)) - (alpha - 1) * s_logx + beta ** 3 * s_x

def metric(alpha, beta):
    return np.array([
        [polygamma(1, alpha), -3/beta],
        [-3/beta, 9 * alpha / beta**2]
    ])

def inverse_metric(alpha, beta):
    return np.linalg.pinv(metric(alpha, beta))

def dL(alpha, beta):
    return np.array(
        [-3 * np.log(beta) + digamma(alpha) - s_logx,
         -3 * alpha / beta + s_x * beta ** 2 * 3]
    )

def Cxx(alpha, beta, params):
    E = polygamma(1, alpha)
    F = -3 / beta
    G =  9 * alpha / beta ** 2
    E1 = polygamma(2, alpha)
    E2 = 0
    F1 = 0
    F2 = 3 / beta ** 2
    G1 = 9 / beta ** 2
    G2 = - 18 * alpha / beta ** 3
    C111 = G * E1 - 2 * F * F1 + F * E2
    C112 = G * E2 - F * G1
    C122 = 2 * G * F2 - G * G1 - F * G2
    C211 = 2 * E * F1 - E * E2 - F * E1
    C212 = E * G1 - F * E2
    C222 = E * G2 - 2 * F * F2 + F * G1

    dim1 = C111 * params[0] ** 2 + C112 * params[0] * params[1] * 2 + C122 * params[1] ** 2
    dim2 = C211 * params[0] ** 2 + C212 * params[0] * params[1] * 2 + C222 * params[1] ** 2
    return np.array([dim1, dim2]) / (2 * (E * G - F ** 2))
