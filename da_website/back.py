from flask import Flask
from flask import request,jsonify
app = Flask(__name__,static_folder='da_website/build')
from flask_cors import CORS,cross_origin
import pickle
CORS(app)
model=pickle.load(open('model.pkl','rb'))
univRanking={'Arizona State University': 4,
 'California Institute of Technology': 7,
 'Carnegie Mellon University': 4,
 'Clemson University': 5,
 'Columbia University': 6,
 'Cornell University': 6,
 'George Mason University': 2,
 'Georgia Institute of Technology': 8,
 'Harvard University': 8,
 'Johns Hopkins University': 5,
 'Massachusetts Institute of Technology': 9,
 'New Jersey Institute of Technology': 2,
 'New York University': 4,
 'North Carolina State University': 6,
 'Northeastern University': 4,
 'Northwestern University': 5,
 'Ohio State University Columbus': 6,
 'Princeton University': 10,
 'Purdue University': 8,
 'Rutgers University New Brunswick/Piscataway': 6,
 'SUNY Buffalo': 4,
 'SUNY Stony Brook': 6,
 'Stanford University': 9,
 'Syracuse University': 4,
 'Texas A and M University College Station': 7,
 'University of Arizona': 4,
 'University of California Davis': 8,
 'University of California Irvine': 7,
 'University of California Los Angeles': 8,
 'University of California San Diego': 8,
 'University of California Santa Barbara': 8,
 'University of California Santa Cruz': 7,
 'University of Cincinnati': 3,
 'University of Colorado Boulder': 5,
 'University of Florida': 6,
 'University of Illinois Chicago': 4,
 'University of Illinois Urbana-Champaign': 8,
 'University of Maryland College Park': 6,
 'University of Massachusetts Amherst': 8,
 'University of Michigan Ann Arbor': 6,
 'University of Minnesota Twin Cities': 7,
 'University of North Carolina Chapel Hill': 8,
 'University of North Carolina Charlotte': 3,
 'University of Pennsylvania': 7,
 'University of Southern California': 3,
 'University of Texas Arlington': 3,
 'University of Texas Austin': 9,
 'University of Texas Dallas': 3,
 'University of Utah': 5,
 'University of Washington': 5,
 'University of Wisconsin Madison': 8,
 'Virginia Polytechnic Institute and State University': 7,
 'Wayne State University': 2,
 'Worcester Polytechnic Institute': 4}
acceptanceRate={'Arizona State University': 0.6605960264900662,
 'California Institute of Technology': 0.4,
 'Carnegie Mellon University': 0.613251155624037,
 'Clemson University': 0.5468113975576662,
 'Columbia University': 0.49521531100478466,
 'Cornell University': 0.4194690265486726,
 'George Mason University': 0.8461538461538461,
 'Georgia Institute of Technology': 0.28008519701810436,
 'Harvard University': 0.2916666666666667,
 'Johns Hopkins University': 0.5944444444444444,
 'Massachusetts Institute of Technology': 0.13636363636363635,
 'New Jersey Institute of Technology': 0.9077868852459017,
 'New York University': 0.6374407582938388,
 'North Carolina State University': 0.4394400486914181,
 'Northeastern University': 0.6540880503144654,
 'Northwestern University': 0.5773195876288659,
 'Ohio State University Columbus': 0.43735763097949887,
 'Princeton University': 0.06,
 'Purdue University': 0.2662013958125623,
 'Rutgers University New Brunswick/Piscataway': 0.4418145956607495,
 'SUNY Buffalo': 0.6575963718820862,
 'SUNY Stony Brook': 0.43295530353569045,
 'Stanford University': 0.1347305389221557,
 'Syracuse University': 0.6393700787401575,
 'Texas A and M University College Station': 0.3578026251823043,
 'University of Arizona': 0.6662995594713657,
 'University of California Davis': 0.2894736842105263,
 'University of California Irvine': 0.3457051961823966,
 'University of California Los Angeles': 0.2558139534883721,
 'University of California San Diego': 0.21739130434782608,
 'University of California Santa Barbara': 0.27114967462039047,
 'University of California Santa Cruz': 0.31724137931034485,
 'University of Cincinnati': 0.7102001906577693,
 'University of Colorado Boulder': 0.5034293552812071,
 'University of Florida': 0.47713897691263013,
 'University of Illinois Chicago': 0.6670353982300885,
 'University of Illinois Urbana-Champaign': 0.2684563758389262,
 'University of Maryland College Park': 0.49853658536585366,
 'University of Massachusetts Amherst': 0.29873417721518986,
 'University of Michigan Ann Arbor': 0.413290113452188,
 'University of Minnesota Twin Cities': 0.38823529411764707,
 'University of North Carolina Chapel Hill': 0.2717391304347826,
 'University of North Carolina Charlotte': 0.7122370936902486,
 'University of Pennsylvania': 0.33974358974358976,
 'University of Southern California': 0.7109670448406267,
 'University of Texas Arlington': 0.7574021012416428,
 'University of Texas Austin': 0.14708785784797632,
 'University of Texas Dallas': 0.7417342482844667,
 'University of Utah': 0.504258943781942,
 'University of Washington': 0.5184331797235023,
 'University of Wisconsin Madison': 0.24882629107981222,
 'Virginia Polytechnic Institute and State University': 0.30448717948717946,
 'Wayne State University': 0.8554216867469879,
 'Worcester Polytechnic Institute': 0.6736111111111112}

def getRecommendations(safe_univ_list,acceptanceRate):
    allUsersRecommendations=[]

    for univs in safe_univ_list:
      temp=[]
      for safe_univ in univs:
          temp.append((acceptanceRate[safe_univ],safe_univ))
      temp.sort()
      temp=list(map(lambda x:x[1],temp))
      if len(temp)<4:
          allUsersRecommendations.append(temp)
          continue
      finalSafeRecommendations=[temp[0],temp[1],temp[2],temp[3]]
      scoreOfCurrentHighest=univRanking[finalSafeRecommendations[-1]]
      ambitious=[]

      for univ,ranking in univRanking.items():
          if ranking==scoreOfCurrentHighest+1:
            ambitious.append(univ)
            break
      finalRecommendations=finalSafeRecommendations + ambitious
      allUsersRecommendations.append(finalRecommendations)

    return allUsersRecommendations
def predictUniv(prediction):
  pred=[]
  for i in range(len(prediction)):
      univs=[]
      for key,value in univRanking.items():
          if value<=int(prediction[i]):
              univs.append(key)
      pred.append(univs)
  return pred
@app.route('/submit',methods=["POST"])
@cross_origin()
def handleSubmit():
    finalUnivList=[]
    res=request.get_json()
    columns=['researchExp', 'industryExp', 'toeflScore', 'toeflEssay','internExp','greV', 'greQ', 'journalPubs', 'greA', 'confPubs','Percentile']
    data=[[float(res[x]) for x in columns]]
    prediction=model.predict(data)
    univList=predictUniv(prediction)
    print(prediction)
    finalUnivList=getRecommendations(univList,acceptanceRate)
    return jsonify({"finalUnivList":finalUnivList[0]})


app.run(debug=True)