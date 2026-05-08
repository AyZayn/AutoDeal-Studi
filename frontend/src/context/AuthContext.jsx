import { createContext, useState, useContext } from "react";
import API from "../services/api";

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem("access_token"));

    const login = async (username, password) => {
        const res = await API.post("/auth/login/", { username, password });
        const accessToken = res.data.access;
        localStorage.setItem("access_token", accessToken);
        localStorage.setItem("refresh_token", res.data.refresh);
        setToken(accessToken);
        const profile = await API.get("/profile/");
        setUser(profile.data);
        return true;
    };

    const logout = () => {
        setUser(null);
        setToken(null);
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}
