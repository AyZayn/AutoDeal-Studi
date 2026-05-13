import { Link } from "react-router-dom";
import "./Home.css";

function Home() {
    return (
        <div className="home">
            <div className="home-hero">
                <span className="home-badge">Plateforme N°1 en France</span>
                <h1 className="home-title">
                    Achetez ou louez<br />
                    <span>votre véhicule idéal</span>
                </h1>
                <p className="home-subtitle">
                    Des centaines de véhicules disponibles. Processus simple, rapide et securisé.
                </p>
                <div className="home-actions">
                    <Link to="/vehicles" className="home-btn-primary">Voir les véhicules</Link>
                    <Link to="/register" className="home-btn-secondary">Créer un compte</Link>
                </div>
            </div>
            <div className="home-stats">
                <div className="stat-item">
                    <p className="stat-number">500+</p>
                    <p className="stat-label">Véhicules disponibles</p>
                </div>
                <div className="stat-divider"></div>
                <div className="stat-item">
                    <p className="stat-number">1200+</p>
                    <p className="stat-label">Clients satisfaits</p>
                </div>
                <div className="stat-divider"></div>
                <div className="stat-item">
                    <p className="stat-number">10+</p>
                    <p className="stat-label">Années d'expérience</p>
                </div>
            </div>
        </div>
    );
}

export default Home;
