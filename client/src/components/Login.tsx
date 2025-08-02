import React, { useState, type ChangeEvent, type FormEvent } from "react";

interface LoginData {
  username: string;
  password: string;
}

const Login: React.FC = () => {
  const [credentials, setCredentials] = useState<LoginData>({
    username: "",
    password: "",
  });

  const [message, setMessage] = useState<string>("");
  const [resetEmail, setResetEmail] = useState<string>("");
  const [resetMessage, setResetMessage] = useState<string>("");

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setCredentials(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleLoginSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const res = await fetch("http://localhost:8000/api/v1/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // important for session login
      body: JSON.stringify(credentials),
    });

    const data = await res.json();
    if (res.ok) {
      setMessage("Login successful!");
      // Optional: Redirect
    } else {
      setMessage(data.error || "Login failed.");
    }
  };

  const handleResetPassword = async () => {
    setResetMessage("");

    const res = await fetch("http://localhost:8000/api/v1/resetPassword/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: resetEmail }),
    });

    const data = await res.json();
    if (res.ok) {
      setResetMessage("Password reset link sent!");
    } else {
      setResetMessage(data.email?.[0] || "Something went wrong.");
    }
  };

  return (
    <div>
      <form onSubmit={handleLoginSubmit}>
        <h2>Login</h2>
        <input
          name="username"
          value={credentials.username}
          onChange={handleChange}
          placeholder="Username"
          required
        />
        <input
          name="password"
          type="password"
          value={credentials.password}
          onChange={handleChange}
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
        <p>{message}</p>
      </form>

      <hr />

      <div>
        <h3>Forgot your password?</h3>
        <input
          type="email"
          placeholder="Enter your email"
          value={resetEmail}
          onChange={(e) => setResetEmail(e.target.value)}
          required
        />
        <button onClick={handleResetPassword}>Send Reset Link</button>
        <p>{resetMessage}</p>
      </div>
    </div>
  );
};

export default Login;
