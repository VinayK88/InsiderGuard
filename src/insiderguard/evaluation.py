def metrics(scored, threshold=0.55):
    tp=fp=tn=fn=0
    for r in scored:
        pred=r['score']>=threshold; truth=r['label']=='risky'
        if pred and truth: tp+=1
        elif pred and not truth: fp+=1
        elif not pred and truth: fn+=1
        else: tn+=1
    precision=tp/(tp+fp) if tp+fp else 1.0; recall=tp/(tp+fn) if tp+fn else 1.0; fpr=fp/(fp+tn) if fp+tn else 0.0
    return {"threshold":threshold,"tp":tp,"fp":fp,"tn":tn,"fn":fn,"precision":round(precision,3),"recall":round(recall,3),"fpr":round(fpr,3)}
