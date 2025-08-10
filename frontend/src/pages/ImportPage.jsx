
import React, {useState} from "react";
import axios from "axios";
import RecaptchaV3 from "../components/RecaptchaV3";

export default function ImportPage(){
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const api = process.env.REACT_APP_API || "http://localhost:8000";

  const onSubmit = async () => {
    if (!file) return alert("select a file");
    const form = new FormData();
    form.append("file", file);
    try{
      const res = await axios.post(`${api}/import/upload`, form, { headers: {"Content-Type": "multipart/form-data"} });
      setMessage(JSON.stringify(res.data));
    }catch(e){
      setMessage("Upload error: " + (e.response?.data || e.message));
    }
  };

  return (
    <div>
      <h2>Upload Excel / CSV</h2>
      <input type="file" accept=".xlsx,.csv" onChange={e => setFile(e.target.files[0])} />
      <button onClick={onSubmit}>Upload</button>
      <div style={{marginTop:10}}>{message}</div>
      <RecaptchaV3 siteKey={process.env.RECAPTCHA_SITE_KEY || "test-site-key"} action={"upload"} onToken={(t)=>console.log("recap token",t)} />
    </div>
  );
}
