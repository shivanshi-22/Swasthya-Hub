import pandas as pd
import numpy as np
import pickle

class Symptom_Checker:
    def conditional_probability(self,data,col,val,dec):
        n=0
        m=len(data['Disease'])
        for i in range(m):
            if data['Disease'][i]==dec and data[col][i]==val:
                n+=1    
        return n

    def probability(self,data,col,val):
        adict={}        
        for i in range(len(data['Disease'])):
            if (self.conditional_probability(data,col,val,data['Disease'][i]))!=0:
                adict[data['Disease'][i]]=(self.conditional_probability(data,col,val,data['Disease'][i]))

        keys=list(adict.keys())
        values=list(adict.values())    
        adict = {keys[i]: values[i] for i in np.argsort(values)}        
        return ''.join(i+"," for i in list(adict.keys())).rstrip(",") if len(adict)>0 else ""

    def result(self,data,val):        
        lst=list(data.columns)
        lst.pop()
        val=val.lower().split(",")
        l1=[]
        for i in range(len(lst)):        
            y=""
            for j in val:
                x=self.probability(data,lst[i],j)            
                if len(x)>0:                
                    for k in x.split(","):
                        l1.append(k)                    
                y+=x+","
        adict={}
        for i in l1:
            if i not in adict:
                adict[i]=1
            else:
                adict[i]+=1
        for i in adict:
            adict[i]/=len(lst)        
        l=[i for i in adict if adict[i]==max(adict.values())]
        s=''.join(i+", " for i in l).rstrip(", ")
        return s

    def precaution(self,data,val):
        s=self.result(data,val)       
        s1=""
        if len(s)<=0:
            return "\nNo diseases detected for the given symptoms. Please select the symptoms from the given list."
        else:
            s1+=("\nThe most probable diseases for the given symptoms - "+s+":")
            prec=pd.read_csv(r"C:/Users/Sankrishna Goyal/PycharmProjects/symptoms_checker/symptom_precaution.csv")
            prec=prec.apply(lambda x:x.fillna(x.value_counts().index[0]))        
            lst=list(prec.columns)                
            s1+=("\nThe possible precautions for the diseases are:")
            for i in s.split(","):
                i=i.strip()
                m=list(np.where(prec["Disease"]==i))[0]            
                if len(m)>0:
                    s1+=("\nPrecautions for "+i+"&")                                    
                    for j in range(1,5):                
                        s1+=("\nPrecuation "+str(j)+" - "+list(prec[lst[j]][m])[0]+"&")
                    s1+=":\n"
            return s1

    def preprocessing(self,data):
        adict={}
        for i in range(len(data)):    
            lst=sorted([j.strip().replace('_',' ') for j in data.iloc[i,1:] if pd.isna(j)==False])
            if data.iloc[i,0].strip() not in adict:
                adict[data.iloc[i,0].strip()]=lst
            else:
                for j in lst:
                    if j not in adict[data.iloc[i,0].strip()]:
                        adict[data.iloc[i,0].strip()].append(j)        

        n=max([len(adict[i]) for i in adict])
        for i in adict:
            if len(adict[i])<n:
                for j in range((n-len(adict[i]))):
                    adict[i].append(float('NaN'))

        l2=[]
        for i in range(n):
            l2.append('Symptom_'+str(i+1))
        l2.append('Disease')
        data=pd.DataFrame.from_dict(adict)    
        l3=list(data.columns)
        data=data.transpose()
        data.index=[i for i in range(len(data))]
        data.insert(n,'Disease',l3,True)
        data.columns=l2
        data=data.apply(lambda x:x.fillna(x.value_counts().index[0]))
        return data

    def diagnose(self,val):        
        data=pd.read_csv(r"C:/Users/Sankrishna Goyal/PycharmProjects/symptoms_checker/dataset.csv")
        data=self.preprocessing(data)         
        s=str(self.precaution(data,val))          
        return(s)

sc=Symptom_Checker()
with open("C:/Users/Sankrishna Goyal/PycharmProjects/symptoms_checker/model_symptom_checker.pkl",'wb') as file:
    pickle.dump(sc,file)