import React, { useState, type ChangeEvent, type FormEvent } from "react";
import Cookies from 'js-cookie';

interface SignupData {
    username: string;
    email: string;
    password: string;
}

const Signup: React.FC = () => {
    const [formData, setFormData] = useState<SignupData>({
        username: "",
        email: "",
        password: "",
    });

    const csrfToken = Cookies.get("csrftoken") || "";



    const [message, setMessage] = useState<string>("");

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

  

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        const res = await fetch("http://localhost:8000/api/v1/signup/", {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken, },
            credentials: "include",
            body: JSON.stringify(formData),
        });

        const data = await res.json();
        if (res.ok) {
            setMessage("Signup successful! You can now log in.");
        } else {
            setMessage(data.error || "Signup failed.");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Signup</h2>
            <input name="username" value={formData.username} onChange={handleChange} placeholder="Username" required />
            <input name="email" value={formData.email} onChange={handleChange} placeholder="Email" required />
            <input name="password" type="password" value={formData.password} onChange={handleChange} placeholder="Password" required />
            <button type="submit">Sign Up</button>
            <p>{message}</p>
        </form>
    );
};

export default Signup;
