import httplib2 
from lxml import etree  
import numpy as np


def getInfo(id):
    url = "https://www.drugbank.ca/drugs/"+str(id)
    print(id)
    mol = {}
    mol['drugbank_id'] = str(id)
    try:#请求网页内容
        http = httplib2.Http()
        response, content = http.request(url,'GET')
        tree = etree.HTML(content)
        #soup = BeautifulSoup(content, 'html.parser')
        
        #identification
        elen = len(tree.xpath("/html/body/main/div/div[4]/dl[1]/dt"))
        for i in range(1,elen+1):
            try:
                if tree.xpath("/html/body/main/div/div[4]/dl[1]/dt["+str(i)+"]/text()")[0]== 'Name':
                    mol['name'] = tree.xpath("/html/body/main/div/div[4]/dl[1]/dd["+str(i)+"]/text()")[0]
                if tree.xpath("/html/body/main/div/div[4]/dl[1]/dt["+str(i)+"]/text()")[0]== 'CAS number':
                    mol['cas_no'] = tree.xpath("/html/body/main/div/div[4]/dl[1]/dd["+str(i)+"]/text()")[0]
                if tree.xpath("/html/body/main/div/div[4]/dl[1]/dt["+str(i)+"]/text()")[0]== 'SMILES':
                    mol['smiles'] = tree.xpath("/html/body/main/div/div[4]/dl[1]/dd["+str(i)+"]/div/text()")[0]
            except:
                print("check identification")
        
        #Pharmacology
        elen = len(tree.xpath("/html/body/main/div/div[4]/dl[2]/dt"))
        for i in range(1,elen+1):
            try:
                if tree.xpath("/html/body/main/div/div[4]/dl[2]/dt["+str(i)+"]/text()")[0]== 'Structured Indications ':
                    if tree.xpath("/html/body/main/div/div[4]/dl[2]/dd["+str(i)+"]/span/text()") == []:
                        mol['structured_indications'] = tree.xpath("/html/body/main/div/div[4]/dl[2]/dd["+str(i)+"]/ul/li/a/text()")
                    else:
                        mol['structured_indications'] = ['Not Available']
                if tree.xpath("/html/body/main/div/div[4]/dl[2]/dt["+str(i)+"]/text()")[0]== 'Indication':
                    try:
                        mol['indication'] = tree.xpath("/html/body/main/div/div[4]/dl[2]/dd["+str(i)+"]/p/text()")[0]
                    except:
                        mol['indication'] = "Not Available"
            except:
                print("check pharmacology")
        
        #references
        #chembl_id
        elen = len(tree.xpath("/html/body/main/div/div[4]/dl/dd/dl/dt"))
        for i in range(1,elen+1):
            try:
                if tree.xpath("/html/body/main/div/div[4]/dl/dd/dl/dt["+str(i)+"]/text()")[0] == 'ChEMBL':
                    mol['chembl_id'] = tree.xpath('/html/body/main/div/div[4]/dl/dd/dl/dd['+str(i)+']/a/text()')[0]
                
            except:
                print("check chembl id")
         #atc_codes
        elen = len(tree.xpath("/html/body/main/div/div/dl[4]/dt"))
        for i in range(1,elen+1):
            try:
                if tree.xpath("/html/body/main/div/div/dl[4]/dt["+str(i)+"]/text()")[0] == 'ATC Codes':
                    mol['atc_codes'] = tree.xpath('/html/body/main/div/div[4]/dl[4]/dd['+str(i)+']/a/text()')
                    for ia in range(len(mol['atc_codes'])):
                        mol['atc_codes'][ia] = mol['atc_codes'][ia][0:7]
            except:
                mol['atc_codes'] = ['Not Available']
        
        #Targets
        #target name
        mol['targets'] = {}
        ts = tree.xpath('/html/body/main/div/div[4]/div[1]/div/div/div/strong/a/text()')
        for i in range(len(ts)):
            mol['targets'][ts[i]] = {}
            
            #left
            for flen in range(len(tree.xpath(("/html/body/main/div/div[4]/div[1]/div[1]/div["+str(i+1)+"]/div/div/div/dl/dt/text()")))):
                # targets_Pharmacological action
                if tree.xpath("/html/body/main/div/div[4]/div[1]/div[1]/div["+str(i+1)+"]/div/div/div/dl/dt/text()")[flen] ==  \
                'Pharmacological action':
                    mol['targets'][ts[i]]['pharmacological_action'] = \
                    tree.xpath("/html/body/main/div/div[4]/div[1]/div/div["+str(i+1)+"]/div/div[1]/div[1]/dl/dd["+str(flen+1)+"]/div/text()")[0]
                # targets_Actions
                if tree.xpath("/html/body/main/div/div[4]/div[1]/div[1]/div["+str(i+1)+"]/div/div/div/dl/dt/text()")[flen] ==  \
                'Actions':
                    mol['targets'][ts[i]]['actions'] = \
                    tree.xpath("/html/body/main/div/div[4]/div[1]/div[1]/div["+str(i+1)+"]/div/div/div/dl/dd["+str(flen+1)+"]/div/text()")[0]
            # right        
            for flen in range(len(tree.xpath("/html/body/main/div/div[4]/div[1]/div[1]/div["+str(i+1)+"]/div/div/div[2]/dl/dt/text()"))):
                if tree.xpath("/html/body/main/div/div[4]/div[1]/div[1]/div["+str(i+1)+"]/div/div/div[2]/dl/dt/text()")[flen] == \
                'Gene Name':
                    mol['targets'][ts[i]]['gene_name'] = \
                    tree.xpath("/html/body/main/div/div[4]/div[1]/div[1]/div["+str(i+1)+"]/div/div/div[2]/dl/dd["+str(flen+1)+"]/text()")[0]
                if tree.xpath("/html/body/main/div/div[4]/div[1]/div[1]/div["+str(i+1)+"]/div/div/div[2]/dl/dt/text()")[flen] == \
                'Uniprot ID':
                    mol['targets'][ts[i]]['uniprot_id'] = \
                    tree.xpath("/html/body/main/div/div[4]/div[1]/div[1]/div["+str(i+1)+"]/div/div/div[2]/dl/dd["+str(flen+1)+"]/a/text()")[0]
                if tree.xpath("/html/body/main/div/div[4]/div[1]/div[1]/div["+str(i+1)+"]/div/div/div[2]/dl/dt/text()")[flen] == \
                'Uniprot Name':
                    mol['targets'][ts[i]]['uniprot_name'] = \
                    tree.xpath("/html/body/main/div/div[4]/div[1]/div[1]/div["+str(i+1)+"]/div/div/div[2]/dl/dd["+str(flen+1)+"]/text()")[0]
                       
    
    except:
        print("data not found")
    
    return mol

def getDic(data):
    drpr = {}
    drin = {}
    for v in data.values():
        drpr[v['name']]=[]
        drin[v['name']]=[]
        for i in v['targets']:
            drpr[v['name']].append(i)
        for i in v['structured_indications']:
            drin[v['name']].append(i)
    return drpr,drin 

def getDrugs(dic):
    dr = []
    for i in dic.keys():
        dr.append(i)
    return dr

def getTargets(dic):
    ta = []
    for i in dic.values():
        for _ in i:
            if _ not in ta:
                ta.append(_)
    return ta

def getIndications(dic):
    ic = []
    for i in dic.values():
        for _ in i:
            if _ not in ic:
                ic.append(_)
    if 'Not Available' in ic:
        ic.remove('Not Available')
    return ic

def toResmat(dic,drugs,prs):
    mat = np.zeros([len(prs),len(drugs)])
    for i in range(len(prs)):
        for j in range(len(drugs)):
            if prs[i] in dic[drugs[j]]:
                mat[i,j] = 1
    return mat

def ResToFreq(item,resmat):
    freqdic = {}
    if len(item) == len(resmat):
        for i in range(len(item)):
            freqdic[item[i]] = np.sum(resmat[i,])
    else:
        print('length not match!')
    return freqdic

def CorrToWei(item,corrmat):
    wei = {}
    if len(item) == len(corrmat):
        for i in range(len(item)-1):
            wei[item[i]] = {}
            for j in range(i+1,len(item)):
                wei[item[i]][item[j]] = corrmat[i,j]
    else:
        print('length not match!')
    return wei