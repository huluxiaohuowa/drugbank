import numpy as np
def presim(datas,row1,row2):
    sum = 0
    for i in datas[row1,]+datas[row2,]:
        if i!=0:
            sum += 1
    if sum != 0:
        return np.dot(np.transpose(datas[row1,]),datas[row2,])/sum
    else:
        return 0

def penalty(dataset,row1,row2):
    icol = []
    for i in range(len(dataset[row1,])):
        if (dataset[row1,]+dataset[row2,])[i] > 1:
            icol.append(i)

    penalty_score = 0
    penalty_array=[]
    
    
    for irow in range(dataset.shape[0]):
        score = 0
        if irow != row1 and irow != row2:
            for item in icol:
                if dataset[irow,item] != 0:
                    score +=1
        if score != 0:
            penalty_array.append(np.abs(np.tanh(float(presim(dataset,irow,row1))-float(presim(dataset,irow,row2)))))

            
    for i in penalty_array:
        penalty_score += np.power(i,2)
    if len(penalty_array) != 0:
        penalty_score /= len(penalty_array)

    return np.sqrt(penalty_score)

def simp(datass,row1,row2):
    simp_score=np.power(presim(datass,row1,row2),penalty(datass,row1,row2)+1)
    return simp_score


def corrmat(resmat):
    z=[]
    for i in range(resmat.shape[0]):
        z.append([])
        for j in range(resmat.shape[0]):
            if i == j:
                z[i].append(1)
            else:
                z[i].append(simp(resmat,i,j))
    return z

