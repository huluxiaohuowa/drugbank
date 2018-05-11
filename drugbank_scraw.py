import json

ID = '{http://www.drugbank.ca}polypeptide'
T = '{http://www.drugbank.ca}target'
with open("drugbank.json","r") as f:
    d = json.load(f)
dd = d['{http://www.drugbank.ca}drugbank']
ddd = dd['{http://www.drugbank.ca}drug']

with open('mat_drugbank_drug_target.txt','w') as f:
    for drug in ddd:
        if (T in drug['{http://www.drugbank.ca}targets']) and (type(drug['{http://www.drugbank.ca}targets']['{http://www.drugbank.ca}target']) is dict) and (ID in drug['{http://www.drugbank.ca}targets']['{http://www.drugbank.ca}target']):
            if type(drug['{http://www.drugbank.ca}targets']['{http://www.drugbank.ca}target']['{http://www.drugbank.ca}polypeptide']) is dict:
                if type(drug['{http://www.drugbank.ca}drugbank-id']) is list:
                    f.write(drug['{http://www.drugbank.ca}drugbank-id'][0]['#text'])
                elif type(drug['{http://www.drugbank.ca}drugbank-id']) is dict:
                    f.write(drug['{http://www.drugbank.ca}drugbank-id']['#text'])
                f.write('\t')
                f.write(drug['{http://www.drugbank.ca}targets']\
                        ['{http://www.drugbank.ca}target']\
                        ['{http://www.drugbank.ca}polypeptide']\
                        ['@id'])
                f.write('\n')
            elif type(drug['{http://www.drugbank.ca}targets']['{http://www.drugbank.ca}target']['{http://www.drugbank.ca}polypeptide']) is list:
                for ttarget in drug['{http://www.drugbank.ca}targets']['{http://www.drugbank.ca}target']['{http://www.drugbank.ca}polypeptide']:
                    if type(drug['{http://www.drugbank.ca}drugbank-id']) is list:
                        f.write(drug['{http://www.drugbank.ca}drugbank-id'][0]['#text'])
                    elif type(drug['{http://www.drugbank.ca}drugbank-id']) is dict:
                        f.write(drug['{http://www.drugbank.ca}drugbank-id']['#text'])
                    f.write('\t')
                    f.write(ttarget['@id'])
                    f.write('\n')
        elif (T in drug['{http://www.drugbank.ca}targets']) and (type(drug['{http://www.drugbank.ca}targets']['{http://www.drugbank.ca}target']) is list):
            for target in drug['{http://www.drugbank.ca}targets']\
                              ['{http://www.drugbank.ca}target']:
                    if ('{http://www.drugbank.ca}polypeptide' in target) and (type(target['{http://www.drugbank.ca}polypeptide']) is dict):
                        if ID in target:
                            if type(drug['{http://www.drugbank.ca}drugbank-id']) is list:
                                f.write(drug['{http://www.drugbank.ca}drugbank-id'][0]['#text'])
                            elif type(drug['{http://www.drugbank.ca}drugbank-id']) is dict:
                                f.write(drug['{http://www.drugbank.ca}drugbank-id']['#text'])
                            f.write('\t')
                            f.write(target['{http://www.drugbank.ca}polypeptide']['@id'])
                            f.write('\n')
                    elif ('{http://www.drugbank.ca}polypeptide' in target) and (type(target['{http://www.drugbank.ca}polypeptide']) is list):
                        if ID in target:
                            for ttarget in target['{http://www.drugbank.ca}polypeptide']:
                                if type(drug['{http://www.drugbank.ca}drugbank-id']) is list:
                                    f.write(drug['{http://www.drugbank.ca}drugbank-id'][0]['#text'])
                                elif type(drug['{http://www.drugbank.ca}drugbank-id']) is dict:
                                    f.write(drug['{http://www.drugbank.ca}drugbank-id']['#text'])
                                f.write('\t')
                                f.write(ttarget['@id'])
                                f.write('\n')