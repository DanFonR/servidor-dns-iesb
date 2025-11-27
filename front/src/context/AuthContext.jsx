import React from "react";
import { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const navigate = useNavigate();

    const [token, setToken] = useState(() => localStorage.getItem("token"));
    const [checked, setChecked] = useState(false); // whether token validity was checked

    // Persist token to localStorage
    useEffect(() => {
        if (token) localStorage.setItem("token", token);
        else localStorage.removeItem("token");
    }, [token]);

    // On mount, validate token (if any) before allowing redirects
    useEffect(() => {
        let mounted = true;

        const validate = async () => {
            if (!token) {
                if (mounted) setChecked(true);
                return;
            }

            try {
                await axios.get("/api/profile", {
                    headers: { Authorization: `Bearer ${token}` },
                });
                // token valid
            } catch (err) {
                // invalid token -> clear it
                if (mounted) setToken(null);
            } finally {
                if (mounted) setChecked(true);
            }
        };

        validate();

        return () => {
            mounted = false;
        };
    }, []);

    const login = (tokenValue) => {
        setToken(tokenValue);
        navigate("/profile");
    };

    const logout = () => {
        setToken(null);
        navigate("/login");
    };

    return (
        <AuthContext.Provider value={{ token, login, logout, checked }}>
            {children}
        </AuthContext.Provider>
    );
};
