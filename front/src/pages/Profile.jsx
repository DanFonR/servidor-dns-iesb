import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import axios from "axios";

export default function Profile() {
    const navigate = useNavigate();
    const [message, setMessage] = useState("");
    const { logout, token } = useContext(AuthContext);

    useEffect(() => {
        if (!token) {
            console.log("token not found!");
            logout();
            return;
        }

        axios
            .get("http://localhost:5000/profile", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((res) => {
                setMessage(res.data.message);
            })
            .catch((err) => {
                console.error(err);
                logout();
            });
    }, [token]);

    return (
        <div>
            <h1>{message || "Loading..."}</h1>
        </div>
    );
}
