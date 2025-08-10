
import React, {useEffect, useState} from "react";
import Plot from "react-plotly.js";
import axios from "axios";

export default function MissingHeatmap(){
  const [data, setData] = useState(null);
  useEffect(()=>{
    async function load(){
      try{
        const res = await axios.get(`${process.env.REACT_APP_API || "http://localhost:8000"}/analytics/missing`);
        setData(res.data);
      }catch(e){
        setData(null);
      }
    }
    load();
  },[]);
  if(!data) return <div>No missing data yet</div>;
  return <Plot
    data={[{ z: data.rows, x: data.columns, y: data.index, type: "heatmap", colorscale: "Viridis" }]}
    layout={{title:"Missing Values"}}
    style={{width:"100%", height:400}}
  />;
}
