import { useNavigate } from "react-router-dom";
import { useContext, useState, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import axios from "axios";

export default function Login() {
    const navigate = useNavigate();
    const { login, token } = useContext(AuthContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const res = await axios.post("http://localhost:5000/login", {
                username,
                password,
            });
            login(res.data.token);
        } catch (err) {
            console.log(err || "Login failed");
            setError(err);
        }
    };

    useEffect(() => {
        if (token) navigate("/profile");
    }, []);

            // {error && (<h3 className="error-msg">{JSON.stringify(error.message).slice(1,-1)}</h3>)}
    return (
        <div className="page-container full-height-center">
            <h2>Login</h2>
            {error && error.response === "Invalid credentials" && <h3>Invalid Credentials</h3>}
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Sign In</button>
            </form>
        </div>
    );
}
