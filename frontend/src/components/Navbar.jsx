import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Navbar.css";

function Navbar() {
    const { token, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate("/");
    };

    return (
        <nav className="navbar">
            <Link to="/" className="navbar-brand">
                Auto<span>Deal</span>
            </Link>
            <div className="navbar-links">
                <Link to="/vehicles" className="nav-link">Vehicules</Link>
                {token ? (
                    <>
                        <Link to="/dossiers" className="nav-link">Mes Dossiers</Link>
                        <Link to="/profile" className="nav-link">Mon Profil</Link>
                        <button onClick={handleLogout} className="btn-danger">Deconnexion</button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="nav-link">Connexion</Link>
                        <Link to="/register" className="btn-primary">Inscription</Link>
                    </>
                )}
            </div>
        </nav>
    );
}

export default Navbar;
