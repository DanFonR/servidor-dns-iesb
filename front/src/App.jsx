import { Navigate, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Profile from "./pages/Profile";

export default function App() {
    return (
        <>
        <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
        <div
                style={{
                    position: "fixed",
                    bottom: 5,
                    right: 5,
                    fontSize: "0.8rem",
                    color: "#888",
                    zIndex: 9999,
                }}
            >
                Servidor de front: {window.FRONTEND_HOSTNAME || "unknown"}
            </div>
        </>
        
    );
}
