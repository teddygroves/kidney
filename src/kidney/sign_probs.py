import numpy as np


def get_sign_prob(t):
    k = np.mean(np.asarray(t) > 0)
    return max(k, 1 - k)


def get_sign_probs(ts):
    return {k: get_sign_prob(v) for k, v in ts.items()}


def get_signif(sp, thresh_prob=0.975):
    "Return '*' if sp > 0.975"
    return "*" if sp > thresh_prob else ""
