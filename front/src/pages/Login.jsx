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
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            // Conecta ao backend através do proxy Nginx
            const res = await axios.post("/login", {
                username,
                password,
            });
            // Se der certo, salva o token
            login(res.data.token);
        } catch (err) {
            console.error("Erro no login:", err);
            // Tenta pegar a mensagem exata do backend ou usa uma genérica
            const msg = err.response?.data?.error || "Falha ao conectar com o servidor.";
            setError(msg);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (token) navigate("/profile");
    }, [token, navigate]);

    return (
        <div className="page-container">
            <div className="card">
                <h2>Acesso ao Sistema</h2>
                
                {error && <div className="alert alert-error">{error}</div>}
                
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="username">Usuário</label>
                        <input
                            id="username"
                            type="text"
                            placeholder="Ex: admin"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    
                    <div className="form-group">
                        <label htmlFor="password">Senha</label>
                        <input
                            id="password"
                            type="password"
                            placeholder="Sua senha"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    
                    <button type="submit" disabled={loading}>
                        {loading ? "Entrando..." : "Entrar"}
                    </button>
                </form>
            </div>
        </div>
    );
}