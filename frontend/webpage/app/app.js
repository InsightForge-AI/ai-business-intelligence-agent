class ChatApp{

constructor(){

this.messagesContainer=document.getElementById("messagesContainer");
this.messageInput=document.getElementById("messageInput");
this.sendBtn=document.getElementById("sendBtn");
this.newChatBtn=document.querySelector(".new-chat-btn");
this.chatHistory=document.getElementById("chatHistory");
this.sidebar=document.getElementById("sidebar");
this.toggleSidebar=document.getElementById("toggleSidebar");
this.downloadBtn=document.getElementById("downloadChat");
this.printBtn=document.getElementById("printChat");
this.clearBtn=document.getElementById("clearChat");
this.uploadBtn=document.getElementById("uploadBtn");
this.fileInput=document.getElementById("fileInput");
this.pdfBtn=document.getElementById("pdfChat");

this.currentChat=[];
this.allChats=[];
this.currentFile=null;

this.init();

}



init(){

this.sendBtn.onclick=()=>this.sendMessage();

this.messageInput.addEventListener("keypress",(e)=>{

if(e.key==="Enter"){

e.preventDefault();
this.sendMessage();

}

});

this.newChatBtn.onclick=()=>this.newChat();

this.toggleSidebar.onclick=()=>{

this.sidebar.classList.toggle("collapsed");

};

this.downloadBtn.onclick=()=>this.downloadJSON();

this.printBtn.onclick=()=>window.print();

this.clearBtn.onclick=()=>this.clearChat();

this.pdfBtn.onclick=()=>this.exportPDF();

this.uploadBtn.onclick=()=>this.fileInput.click();

this.fileInput.onchange=(e)=>{

const file=e.target.files[0];

if(file){

this.currentFile=file;

this.messageInput.value=file.name+" ";

}

};

}



sendMessage(){

const message=this.messageInput.value.trim();

if(!message) return;


/* remove welcome */

if(this.messagesContainer.querySelector(".welcome")){

this.messagesContainer.innerHTML="";

}


/* show query */

this.addUserMessage(message);


/* backend */

this.callBackend(message,this.currentFile);


this.messageInput.value="";
this.currentFile=null;

}



addUserMessage(text){

const div=document.createElement("div");

div.className="message-group user";


const content=document.createElement("div");

content.className="message-content";

content.textContent=text;


div.appendChild(content);

this.messagesContainer.appendChild(div);

this.scrollBottom();

}



showResult(data){

const div=document.createElement("div");

div.className="message-group assistant";


let formatted="";


if(data.agent){

formatted+="Agent: "+data.agent.join(", ")+"\n\n";

}


for(const module in data.module_results){

formatted+=module.toUpperCase()+" RESULT\n";

formatted+="----------------\n";


const result=data.module_results[module];


for(const k in result){

formatted+=k+" : "+result[k]+"\n";

}


formatted+="\n";

}


const content=document.createElement("div");

content.className="message-content";

/* textContent (not innerHTML) so module output -- which can contain
   user- or module-influenced text -- is always rendered as plain text,
   never parsed as HTML. */
const pre=document.createElement("pre");
pre.textContent=formatted;
content.appendChild(pre);


div.appendChild(content);

this.messagesContainer.appendChild(div);

this.scrollBottom();

}



/* Reads a File as base64 (without the data: URL prefix) so its actual
   bytes can travel inside the JSON body -- fetch() with a JSON body
   cannot carry a File object, only its metadata. */
readFileAsBase64(file){

return new Promise((resolve,reject)=>{

const reader=new FileReader();

reader.onload=()=>{

const result=reader.result;
const base64=result.substring(result.indexOf(",")+1);
resolve(base64);

};

reader.onerror=()=>reject(reader.error);

reader.readAsDataURL(file);

});

}



async callBackend(message,file){

let file_name=null;
let file_data=null;

if(file){

try{

file_name=file.name;
file_data=await this.readFileAsBase64(file);

}catch(err){

this.showResult({

agent:["error"],
module_results:{error:{msg:"failed to read attached file"}}

});

return;

}

}

fetch("http://127.0.0.1:8000/analyze",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

query:message,
file_name:file_name,
file_data:file_data

})

})

.then(r=>r.json())

.then(data=>{

this.currentChat.push({

query:message,
response:data

});

this.showResult(data);

})

.catch(()=>{

this.showResult({

agent:["error"],
module_results:{error:{msg:"backend error"}}

});

});

}



/* save chat session */

saveChatSession(){

if(this.currentChat.length===0) return;


const index=this.allChats.length;


const item=document.createElement("div");

item.className="chat-item";


const text=document.createElement("span");

text.textContent=this.currentChat[0].query.substring(0,30);


/* delete icon */

const del=document.createElement("span");

del.innerHTML="🗑";

del.title="Delete Chat";

del.style.cursor="pointer";


del.onclick=(e)=>{

e.stopPropagation();

this.allChats.splice(index,1);

item.remove();

};


item.appendChild(text);

item.appendChild(del);


/* load chat */

item.onclick=()=>{

this.loadChat(index);
this.highlightActive(item);

};


this.chatHistory.appendChild(item);


this.allChats.push(

JSON.parse(JSON.stringify(this.currentChat))

);

}



loadChat(index){

const chat=this.allChats[index];

if(!chat) return;


this.messagesContainer.innerHTML="";


chat.forEach(c=>{

this.addUserMessage(c.query);
this.showResult(c.response);

});


this.currentChat=JSON.parse(JSON.stringify(chat));

}



highlightActive(element){

document.querySelectorAll(".chat-item")

.forEach(i=>i.classList.remove("active"));

element.classList.add("active");

}



newChat(){

this.saveChatSession();


document.querySelectorAll(".chat-item")

.forEach(i=>i.classList.remove("active"));


this.messagesContainer.innerHTML=`

<div class="message-group welcome">

<div class="message-content">

<h2>Welcome to AI Business Intelligence Agent</h2>

<p>Ask me anything about your business data</p>

</div>

</div>

`;

this.currentChat=[];

}



clearChat(){

this.messagesContainer.innerHTML="";
this.currentChat=[];

}



/* JSON download */

downloadJSON(){

if(this.currentChat.length===0) return;


const json=this.currentChat.map(c=>c.response);


const blob=new Blob(

[JSON.stringify(json,null,2)],

{type:"application/json"}

);


const a=document.createElement("a");

a.href=URL.createObjectURL(blob);

a.download="chat.json";

a.click();

}



/* Escapes text before it is interpolated into an HTML template string.
   exportPDF() below builds real HTML (not just a <pre> block like
   showResult()), so every value that can originate from user input or a
   downstream module's response must be escaped here. */
escapeHtml(value){

return String(value)
.replace(/&/g,"&amp;")
.replace(/</g,"&lt;")
.replace(/>/g,"&gt;")
.replace(/"/g,"&quot;")
.replace(/'/g,"&#39;");

}



/* PDF export */

exportPDF(){

const container=document.createElement("div");


/* header */

const header=document.createElement("div");

header.style.marginBottom="12px";


header.innerHTML=`

<div style="display:flex;align-items:center;gap:10px">

<img src="logo.png" style="height:40px">

<div style="font-size:16px;font-weight:bold">

AI Business Intelligence Report

</div>

</div>

<hr>

`;


/* body */

const content=document.createElement("div");

content.style.fontSize="11px";

content.style.lineHeight="1.5";

content.style.fontFamily="Arial";


let html="";


this.currentChat.forEach((chat,index)=>{


html+=`

<div style="margin-bottom:10px">

<div>

<strong>${index+1}. Query :</strong> ${this.escapeHtml(chat.query)}

</div>


<div style="margin-top:4px">

<strong>Output :</strong>

</div>

`;


/* agent */

if(chat.response.agent){

html+=`

<div>

Agent: ${this.escapeHtml(chat.response.agent.join(", "))}

</div><br>

`;

}


/* module results */

for(const module in chat.response.module_results){

html+=`

<div>

<strong>${this.escapeHtml(module.toUpperCase())} RESULT</strong>

</div>

<div style="margin-left:10px">

`;


const result=chat.response.module_results[module];


for(const k in result){

html+=`${this.escapeHtml(k)} : ${this.escapeHtml(result[k])}<br>`;

}


html+=`

</div><br>

`;

}


html+=`

</div>

`;

});


content.innerHTML=html;


container.appendChild(header);

container.appendChild(content);


html2pdf()

.set({

margin:0.4,

filename:"AI_BI_Report.pdf",

html2canvas:{scale:2},

jsPDF:{unit:"in",format:"a4"}

})

.from(container)

.save();

}



scrollBottom(){

this.messagesContainer.scrollTop=

this.messagesContainer.scrollHeight;

}

}



document.addEventListener(

"DOMContentLoaded",

()=>new ChatApp()

);