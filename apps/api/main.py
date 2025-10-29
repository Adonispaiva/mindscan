from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class MindScanInput(BaseModel):
    performance: list[int]
    matcher: list[int]

@app.post("/mindscan/submit")
def submit(data: MindScanInput):
    p = round(sum(data.performance)/max(len(data.performance),1),2)
    m = round(sum(data.matcher)/max(len(data.matcher),1),2)
    cutoff=80
    if p>=cutoff and m>=cutoff: t="inspiradores"
    elif p>=cutoff and m<cutoff: t="especialistas"
    elif p<cutoff and m>=cutoff: t="promissores"
    else: t="buscadores"
    return {"performance":p,"matcher":m,"territory":t,"insights":[]}
