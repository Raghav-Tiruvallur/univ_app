import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.linear_model import LinearRegression
import sys
import pickle
from impyute.imputation.cs import mice
def cleaning_phase(df):
  research_exp=df.researchExp
  industry_exp=df.industryExp
  intern_exp=df.internExp

  #filling 0 in place of null values if present in experience features
  df[['researchExp','industryExp','internExp']].fillna(value=0,inplace=True)
  
  #rescaling the experience features to a scale of 0-5
  def convert_range(old_min,old_max,new_min,new_max,data):
    for i in range(len(data)):
      new_value = (((data[i] - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
      data[i]=new_value

  convert_range(research_exp.min(),research_exp.max(),0,5,research_exp)
  convert_range(intern_exp.min(),intern_exp.max(),0,5,intern_exp)
  convert_range(industry_exp.min(),industry_exp.max(),0,5,industry_exp)

  #check for null values in publications
  print(sum(df.journalPubs.isnull()),sum(df.confPubs.isnull()))
  
  #links present in journalPubs and datapoints in confPubs arent of right type and converting some rows which have digits stored as strings
  for index in range(len(df.journalPubs)):
    if type(df.journalPubs[index])==str and df.journalPubs[index].isdigit():
      df.journalPubs[index]=int(df.journalPubs[index])

  for index in range(len(df.confPubs)):
      if type(df.confPubs[index])==str and df.confPubs[index].isdigit():
        df.confPubs[index]=int(df.confPubs[index])
  
  df[df['journalPubs']=='http://www.edulix.com/unisearch/user.php?uid=225747']=np.nan
  
  df[df['confPubs']=='Fall - 2015']=np.nan
  df[df['confPubs']=='Fall - 2012']=np.nan
  df[df['confPubs']=='Fall - 2014']=np.nan

  #filling 0 in place of null values if present in publications features
  df[['journalPubs','confPubs']].fillna(value=0,inplace=True)

  #cleaning and transforming scores
  sys.setrecursionlimit(100000)
  df.drop(["gmatA","gmatQ","gmatV"],axis=1,inplace=True)
  imputed_training=mice(df[["greQ","greV","greA"]].values)
  imputedDf=pd.DataFrame()
  imputedDf[["greQ","greV","greA"]]=pd.DataFrame(imputed_training)
  imputedDf=imputedDf[["greQ","greV","greA"]]
  imputedDf.loc[:,"greQ"]=(imputedDf.loc[:,"greQ"]//10)*10
  imputedDf.loc[:,"greV"]=(imputedDf.loc[:,"greV"]//10)*10
  conversion=pd.read_csv("score.csv")
  conversion=pd.DataFrame(conversion)
  dQscores=dict()
  dVscores=dict()
  oldgreScores=conversion.iloc[:,0]
  newgreQScores=conversion.iloc[:,1]
  newgreVScores=conversion.iloc[:,2]
  def getDict(d,x,y):
      d[x]=y
      return d
  dQscores=list(map(lambda x,y:getDict(dQscores,x,y),oldgreScores,newgreQScores))[0]

  dVscores=list(map(lambda x,y:getDict(dVscores,x,y),oldgreScores,newgreVScores))[0]
  dScores=dict()
  for key in dQscores.keys():
      dScores[key]=(dQscores[key],dVscores[key])
  newQScores=[]
  newVScores=[]
  for i in range(len(imputedDf["greQ"])):
      if imputedDf["greQ"][i] > 800:
          newQScores.append(dScores[800][0])
      elif 170<imputedDf["greQ"][i]<200:
            newQScores.append(dScores[200][0])
      elif dScores.get(imputedDf["greQ"][i])==None:
          newQScores.append(int(imputedDf["greQ"][i]))
      else:
          newQScores.append(dScores.get(imputedDf["greQ"][i])[0])
  for i in range(len(imputedDf["greV"])):
      if imputedDf["greV"][i] > 800:
          newVScores.append(dScores[800][0])
      elif 170<imputedDf["greV"][i]<200:
            newVScores.append(dScores[200][0])
      elif dScores.get(imputedDf["greV"][i])==None:
          newVScores.append(int(imputedDf["greV"][i]))
      else:
          newVScores.append(dScores.get(imputedDf["greV"][i])[0])
  
  df["greQ"]=newQScores
  df["greV"]=newVScores
  cgpadf=df[["topperCgpa","cgpaScale"]].replace({0:np.nan})
  percentile=df["cgpa"]/df["topperCgpa"]
  df["Percentile"]=percentile*10
  df["Percentile"].fillna(0,inplace = True)

  df.loc[df["greA"] > 6,"greA"]=df['greA'].mean()
  df.loc[df["greV"] > 170,"greV"]=df['greV'].mean()
  df.loc[df["greQ"] > 170,"greQ"]=df['greQ'].mean()
  df.loc[df["Percentile"] > 10,"Percentile"]=10

  #Casting "toeflEssay" values to type Float
  df["toeflEssay"] = pd.to_numeric(df["toeflEssay"])
  df["toeflEssay"].fillna(df["toeflEssay"].mean(),inplace=True)

  df["toeflScore"].fillna(df["toeflScore"].median(),inplace=True)

  #Cleaning the department feature
  df.drop(df.loc[df['department']=='0'].index, inplace = True)

  #Cleaning the termAndYear feature
  df.drop(df.loc[df['termAndYear']==np.nan].index, inplace = True)
    
  #Cleaning the ugCollege feature
  df.drop(df.loc[df['ugCollege'].isnull()].index, inplace = True)

  dfAdmits=df[df["admit"]==1]
  dfAdmitsIndex=dfAdmits["univName"].value_counts().index.tolist()
  dfAdmitCounts=list()
  for i in dfAdmits["univName"].value_counts():
    dfAdmitCounts.append(i)

  return df

df=pd.read_csv('original_data.csv')
df = cleaning_phase(df)


df=df.reset_index()
df2=df.drop(["index","userProfileLink","department","userName","specialization","major","topperCgpa",'termAndYear','cgpa','cgpaScale','ugCollege','program'],axis=1)

#assigning scores to universities using their acceptance rate as the measure 
#higher the acceptance rate lower the score and vice versa
def assignUnivScores(df,listOfUnivs):
    admitCount=dict()
    for univ in listOfUnivs:
        df2=df[df["univName"]==univ]
        applicationCount=len(df2)
        df2=df2[df2["admit"]==1]
        admitCount[univ]=len(df2)/applicationCount
    return admitCount

listOfUnivs=list(set(df["univName"]))
admitCount=assignUnivScores(df,listOfUnivs)
admitCount=sorted(admitCount.items(),key=lambda key_value_pair:(key_value_pair[1],key_value_pair[0]))
univRanking=dict()

for (univ,rating) in admitCount:
    if 0 <= rating <=0.1:
        univRanking[univ]=10
    if 0.1<rating<=0.2:
        univRanking[univ]=9
    if 0.2<rating<=0.3:
        univRanking[univ]=8
    if 0.3<rating<=0.4:
        univRanking[univ]=7
    if 0.4<rating<=0.5:
        univRanking[univ]=6
    if 0.5<rating<=0.6:
        univRanking[univ]=5
    if 0.6<rating<=0.7:
        univRanking[univ]=4
    if 0.7<rating<=0.8:
        univRanking[univ]=3
    if 0.8<rating<=1:
        univRanking[univ]=2
df2["toeflEssay"].fillna(df2["toeflEssay"].astype(float).mean(),inplace=True)
df2["greA"].fillna(df2["greA"].astype(float).mean(),inplace=True)
x_data=df2.iloc[:,df2.columns!="admit"]
x_data=x_data.iloc[:,x_data.columns!="univName"]
y_data=[]

for i in range(len(x_data)):
    y_data.append(univRanking[df2.iloc[i,10]])
x_train,x_test,y_train,y_test=train_test_split(x_data,y_data,test_size=0.2,random_state=1024)
LR=LinearRegression(normalize=True)
LR.fit(x_train,y_train)
def predictUniv(prediction):
  pred=[]
  for i in range(len(prediction)):
      univs=[]
      for key,value in univRanking.items():
          if value<=int(prediction[i]):
              univs.append(key)
      pred.append(univs)
  return pred

pickle.dump(LR,open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))