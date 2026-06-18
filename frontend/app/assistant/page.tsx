"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { PageHeader } from "@/components/UI";

type Message={role:"user"|"assistant";text:string;data?:Record<string,any>[]};
const prompts=["Which employees were absent more than 5 times this month?","Department-wise list the employees whose salary is second highest.","Who joined this month?","Which department has the highest payroll cost?","Show employees currently on leave.","Give me a summary of HR performance this month."];

export default function AssistantPage(){
  const [messages,setMessages]=useState<Message[]>([{role:"assistant",text:"Hello, Jawad. I’m PeopleOps AI. I can analyze employees, attendance, leave, payroll, and workforce trends using your live HRMS data."}]);
  const [input,setInput]=useState(""); const [busy,setBusy]=useState(false);
  const ask=async(text:string)=>{if(!text.trim()||busy)return;setMessages(m=>[...m,{role:"user",text}]);setInput("");setBusy(true);try{const r=await api<{answer:string;data:Record<string,any>[]}>("/chat/",{method:"POST",body:JSON.stringify({message:text})});setMessages(m=>[...m,{role:"assistant",text:r.answer,data:r.data}])}catch{setMessages(m=>[...m,{role:"assistant",text:"I couldn’t reach the HR analytics service. Please try again."}])}finally{setBusy(false)}};
  return <><PageHeader eyebrow="SECURE HR INTELLIGENCE" title="PeopleOps AI" copy="Ask natural-language questions about your workforce. Answers are grounded in HRMS data." />
    <div className="ai-layout"><section className="chat-card"><div className="chat-head"><div className="ai-orb">✦</div><div><b>PeopleOps AI</b><span><i/> Online · HR data only</span></div><BadgeSecure /></div><div className="messages">{messages.map((m,i)=><div className={`message ${m.role}`} key={i}><div className="bubble">{m.text}{m.data&&m.data.length>0&&<div className="mini-table"><table><thead><tr>{Object.keys(m.data[0]).map(k=><th key={k}>{k.replaceAll("_"," ")}</th>)}</tr></thead><tbody>{m.data.slice(0,8).map((r,j)=><tr key={j}>{Object.keys(m.data![0]).map(k=><td key={k}>{String(r[k]??"")}</td>)}</tr>)}</tbody></table></div>}</div></div>)}{busy&&<div className="message assistant"><div className="typing"><i/><i/><i/></div></div>}</div><div className="chat-input"><textarea value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();ask(input)}}} placeholder="Ask about employees, leave, payroll, or attendance..." /><button onClick={()=>ask(input)}>↑</button><small>PeopleOps AI uses deterministic HR queries; Gemini only polishes the response.</small></div></section>
      <aside className="prompt-panel"><span className="eyebrow">SUGGESTED ANALYSIS</span><h2>Try asking</h2><p>These questions run safely against the sample workforce dataset.</p>{prompts.map((p,i)=><button key={p} onClick={()=>ask(p)}><span>{["⌁","◇","♙","↗","◷","✦"][i]}</span>{p}</button>)}<div className="guardrail"><b>◉ Privacy by design</b><p>The API key stays server-side. The assistant cannot modify or delete employee data.</p></div></aside>
    </div></>;
}

function BadgeSecure(){return <span className="secure-badge">▣ Grounded in HRMS</span>}
