import React from "react";
import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import axios from "axios";

export default function Profile() {
    const navigate = useNavigate();
    const [userData, setUserData] = useState({
        username: "",
        hostname: "",
        session_id: "",
        login_time: ""
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const { logout, token } = useContext(AuthContext);

    useEffect(() => {
        if (!token) {
            console.log("token not found!");
            logout();
            return;
        }

        axios
            .get("/api/profile", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((res) => {
                setUserData({
                    username: res.data.username,
                    hostname: res.data.hostname,
                    session_id: res.data.session_id || "",
                    login_time: res.data.login_time || ""
                });
                setLoading(false);
            })
            .catch((err) => {
                console.error(err);
                setError("Erro ao carregar perfil");
                setLoading(false);
                logout();
            });
    }, [token]);

    return (
        <div className="page-container full-height-center">
            {loading ? (
                <h1 className="profile-message">Carregando...</h1>
            ) : error ? (
                <h1 className="profile-message" style={{ color: "red" }}>
                    {error}
                </h1>
            ) : (
                <div style={{ textAlign: "center" }}>
                    <h1 className="profile-message">Bem-vindo, {userData.username}!</h1>
                    <div style={{ marginTop: "2rem", fontSize: "1.1rem", lineHeight: 1.6 }}>
                        <p>
                            <strong>Servidor do Backend:</strong> {userData.hostname}
                        </p>
                        <p>
                            <strong>Sessão:</strong> {userData.session_id || "-"}
                        </p>
                        <p>
                            <strong>Data/Hora do login:</strong>{" "}
                            {userData.login_time ? new Date(userData.login_time).toLocaleString() : "-"}
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
}
