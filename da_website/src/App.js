import './App.css';
import {useState} from "react";
//import { Button } from "@material-ui/core";
import axios from 'axios';


function App()
 {
  const [researchExp,setresearchExp]=useState(0);
  const [industryExp,setIndustryExp]=useState(0);
  const [toeflScore,settoeflScore]=useState(0);
  const [toeflEssay,settoeflEssay]=useState(0);
  const [internExp,setinternExp]=useState(0);
  const [greV,setgreV]=useState(0);
  const [greQ,setgreQ]=useState(0);
  const [journalPubs,setjournalPubs]=useState(0);
  const [greA,setgreA]=useState(0);
  const [confPubs,setconfPubs]=useState(0);
  const [Percentile,setPercentile]=useState(0);
  const [univs,setUnivs]=useState([])
  const sendData=(e)=>{
    const data={
      researchExp:researchExp,
      internExp:internExp,
      Percentile:Percentile,
      confPubs:confPubs,
      greV:greV,
      greQ:greQ,
      greA:greA,
      journalPubs:journalPubs,
      industryExp:industryExp,
      toeflScore:toeflScore,
      toeflEssay:toeflEssay
    }
    e.preventDefault()
    axios.post('https://university-recommendation.herokuapp.com/submit',data)
    .then((res)=>{
      console.log(res.data.finalUnivList)
       setUnivs(res.data.finalUnivList)
       console.log("Success")
    })
    .catch((e)=>{
      console.log(e)
    })
  }

  return (
    <div className="App">
      <h1>University Recommendation</h1>
    <form method="POST">
      <label htmlFor="research exp">Research Exp</label><br/>
    <input
      value={researchExp}
      onChange={e => setresearchExp(e.target.value)}
      placeholder="Research Exp"
      type="number"
      name="research exp"
      required
    /><br/>
     <label htmlFor="industryExp">industryExp</label><br/>
    <input
      value={industryExp}
      onChange={e => setIndustryExp(e.target.value)}
      placeholder="Industry Exp"
      type="number"
      name="industryExp"
      required
    /><br/>
     <label htmlFor="toefl score">Toefl Score</label><br/>
    <input
      value={toeflScore}
      onChange={e => settoeflScore(e.target.value)}
      placeholder="Toefl score"
      type="number"
      name="toefl score"
      required
    /><br/>
     <label htmlFor="toefl essay">Toefl Essay</label><br/>
    <input
      value={toeflEssay}
      onChange={e => settoeflEssay(e.target.value)}
      placeholder="Toefl Essay"
      type="number"
      name="toefl essay"
      required
    /><br/>
     <label htmlFor="intern exp">Intern Exp</label><br/>
    <input
      value={internExp}
      onChange={e => setinternExp(e.target.value)}
      placeholder="intern exp"
      type="number"
      name="intern exp"
      required
    /><br/>
     <label htmlFor="GRE V">GRE V</label><br/>
    <input
      value={greV}
      onChange={e => setgreV(e.target.value)}
      placeholder="GRE V"
      type="number"
      name="GRE V"
      required
    /><br/>
     <label htmlFor="GRE Q">GRE Q</label><br/>
    <input
      value={greQ}
      onChange={e => setgreQ(e.target.value)}
      placeholder="GRE Q"
      type="number"
      name="GRE Q"
      required
    /><br/>
     <label htmlFor="journal pubs">Journal Publications</label><br/>
    <input
      value={journalPubs}
      onChange={e => setjournalPubs(e.target.value)}
      placeholder="journal pubs"
      type="number"
      name="journal pubs"
      required
    /><br/>
     <label htmlFor="greA">AWA</label><br/>
    <input
      value={greA}
      onChange={e => setgreA(e.target.value)}
      placeholder="greA"
      type="number"
      name="greA"
      required
    /><br/>
     <label htmlFor="confPubs">Conference Publications</label><br/>
    <input
      value={confPubs}
      onChange={e => setconfPubs(e.target.value)}
      placeholder="confPubs"
      type="number"
      name="confPubs"
      required
    /><br/>
     <label htmlFor="Percentile">Percentile</label><br/>
    <input
      value={Percentile}
      onChange={e => setPercentile(e.target.value)}
      placeholder="Percentile"
      type="number"
      name="Percentile"
      required
    /><br/>
    
    <button type="submit" onClick={sendData}>Submit</button>
    {
      univs.map(univ=><li>{univ}</li>)
    }
  </form>
  </div>
  );
 }
export default App;