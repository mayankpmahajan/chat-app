// pages/ResetPassword.tsx
import { useParams } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import Cookies from 'js-cookie';


const ResetPassword = () => {
  const { uid, token } = useParams();
  const [password, setPassword] = useState("");
  const csrfToken = Cookies.get("csrftoken") || "";  

  const handleSubmit = async () => {
    try {
      await axios.post("http://localhost:8000/api/v1/changePassword/", {
        uid,
        token,
        new_password: password,
      }, {headers:{ "X-CSRFToken": csrfToken}, withCredentials: true });  // withCredentials if using session auth

      alert("Password reset successful!");
    } catch (err) {
      console.error(err);
      alert("Invalid or expired token.");
    }
  };

  return (
    <div>
      <h2>Reset Password</h2>
      <input
        type="password"
        placeholder="Enter new password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleSubmit}>Reset</button>
    </div>
  );
};

export default ResetPassword;
