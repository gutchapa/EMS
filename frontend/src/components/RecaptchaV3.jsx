
import React, {useEffect} from "react";

export default function RecaptchaV3({siteKey, action="submit", onToken}){
  useEffect(()=>{
    // Minimal placeholder: in test mode we don't call Google
    // In production you must load grecaptcha and execute
    onToken && onToken("test-token");
  },[siteKey,action,onToken]);

  return null;
}
