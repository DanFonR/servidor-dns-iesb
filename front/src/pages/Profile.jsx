import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import axios from "axios";

export default function Profile() {
    const navigate = useNavigate();
    const [userData, setUserData] = useState({
        username: "",
        hostname: ""
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
            .get("/profile", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((res) => {
                setUserData({
                    username: res.data.username,
                    hostname: res.data.hostname
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
                    <div style={{ marginTop: "2rem", fontSize: "1.2rem" }}>
                        <p>
                            <strong>Servidor:</strong> {userData.hostname}
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
}
