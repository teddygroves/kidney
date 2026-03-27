def get_sign_probs(ts):
    return {k: (v>0).mean().item() for k, v in ts.items()}

def get_signif(sp, thresh_prob=0.025):
    if sp == 0.5:
        return ''
    if sp > 0.5:
        if 1-sp < thresh_prob:
            return '*'
        else:
            return ''
    if sp < 0.5:
        if sp < thresh_prob:
            return '*'
        else:
            return ''