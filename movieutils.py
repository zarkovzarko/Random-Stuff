import sys

def mixer(masterjson="dbpedia.json", slavejson="imdb.json"):
    mastername = masterjson[:-5]
    slavename = slavejson[:-5]
    with open(masterjson, "r") as masterf:
        with open(slavejson, "r") as slavef:
            auxm = masterf.read().strip()
            auxs = slavef.read().strip()
            if auxm == "[" and auxs == '[':
                print("ACTOR OR ACTRESS NOT FOUND !")
                sys.exit(1)
            try:
                masterlist = eval(auxm)
            except:
                masterlist = []
            
            try:
                slavelist = eval(auxs)
            except:
                slavelist = []
            
            
    # first let's dedupe lists (based on movie name and year) just in case
    auxdictm = {}
    for it in masterlist:
        if auxdictm.get((it['moviename'], it['movieyear']), 'FIRST92537') == 'FIRST92537':
            auxdictm[(it['moviename'], it['movieyear'])] = it['movieuri']
            
    auxdicts = {}
    for it in slavelist:
        if auxdicts.get((it['moviename'], it['movieyear']), 'FIRST92537') == 'FIRST92537':
            auxdicts[(it['moviename'], it['movieyear'])] = it['movieuri']
    
    # let's "merge" data sets now
    # if names of movies match between the two data sources then take the year from the master
    # if master doesn't have the info about the year then take year from the slave
    auxdictm1 = {}
    for k, v in auxdictm.items():
        auxdictm1[k[0]] = {'movieyear': k[1], 'movieuri': v}
        
    auxdicts1 = {}
    for k, v in auxdicts.items():
        auxdicts1[k[0]] = {'movieyear': k[1], 'movieuri': v}
        
    res = []
    for k, v in auxdictm1.items():
        res.append({'moviename': k, 'movieyear': v['movieyear'], 'movieuri'+mastername:v['movieuri']})
        if res[-1]['movieyear'] == 'NONE':
            if auxdicts1.get(k, 'NONE') != 'NONE':
                res[-1]['movieyear'] =  auxdicts1[k]['movieyear']
                
        if auxdicts1.get(k, 'NONE') != 'NONE':
            res[-1]['movieuri'+slavename] = auxdicts1[k]['movieuri']
        else:
            res[-1]['movieuri'+slavename] = 'NONE'
        
        auxdicts1.pop(k, None)
        
    for k, v in auxdicts1.items():
        res.append({'moviename':k, 'movieyear':v['movieyear'], 
                    'movieuri'+slavename:v['movieuri'], 'movieuri'+mastername:'NONE'})
        
    
    return res

if __name__ == "__main__":
    res = mixer()