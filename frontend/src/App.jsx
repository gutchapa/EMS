
import React from "react";
import ImportPage from "./pages/ImportPage";
import Dashboard from "./pages/Dashboard";

export default function App(){
  return (
    <div style={{padding:20}}>
      <h1>EMS - Minimal Demo</h1>
      <ImportPage />
      <hr />
      <Dashboard />
    </div>
  );
}
