import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import { useAuth } from "../context/AuthContext";
import "./Dossiers.css";

function Dossiers() {
    const [dossiers, setDossiers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [deleting, setDeleting] = useState(null);
    const { token } = useAuth();
    const navigate = useNavigate();


    // Récupération des dossiers via l'API
    const fetchDossiers = () => {
        API.get("/contracts/")
            .then((res) => { 
                setDossiers(res.data); 
                setLoading(false); 
            })
            .catch((err) => {
                console.error("Erreur fetch:", err);
                setLoading(false);
            });
    };

    // Redirection si non connecté + chargement des données
    useEffect(() => {
        if (!token) { 
            navigate("/login"); 
            return; 
        }
        fetchDossiers();
    }, [token, navigate]);

    // Suppression (Annulation) d'un dossier
    const handleDelete = async (id) => {
        if (!window.confirm("Voulez-vous vraiment annuler ce dossier ?")) return;
        
        setDeleting(id);
        try {
            await API.delete("/contracts/" + id + "/");
            setDossiers(dossiers.filter(c => c.id !== id));
        } catch (err) {
            console.error("Erreur delete:", err);
            alert("Erreur lors de l'annulation");
        } finally {
            setDeleting(null);
        }
    };

    // Configuration des libellés et couleurs selon le statut
    const statusConfig = {
        pending:            { label: "En attente",        color: "pending" },
        documents_received: { label: "Documents reçus",   color: "documents_received" },
        under_review:       { label: "En vérification",   color: "under_review" },
        approved:           { label: "Approuvé",          color: "approved" },
        rejected:           { label: "Refusé",            color: "rejected" },
        completed:          { label: "Terminé",           color: "completed" },
        cancelled:          { label: "Annulé",            color: "cancelled" },
    };

    if (loading) return <div className="page-loading">Chargement...</div>;

    const formatDate = (dateString) => {
        if (!dateString) return "-";
        const [year, month, day] = dateString.split("-");
        return `${day}/${month}/${year}`;
    };


    return (
        <div className="dossiers-page">
            <div className="dossiers-header">
                <h1>Mes <span>Dossiers</span></h1>
                <p>Suivez vos demandes d'achat et de location</p>
            </div>

            {dossiers.length === 0 ? (
                <div className="dossiers-empty">
                    <p>Vous n'avez pas encore de dossiers</p>
                    <button onClick={() => navigate("/vehicles")} className="dossiers-browse-btn">
                        Voir les véhicules
                    </button>
                </div>
            ) : (
                <div className="dossiers-list">
                    {dossiers.map((dossier) => {
                        const status = statusConfig[dossier.status] || { label: dossier.status, color: "pending" };
                        const canDelete = dossier.status === "pending";

                        return (
                            <div 
                                key={dossier.id} 
                                className="dossier-card" 
                                onClick={() => navigate("/dossiers/" + dossier.id)} 
                                style={{ cursor: "pointer" }}
                            >
                                <div className="dossier-card-header">
                                    <div className="dossier-card-header-left">
                                        <span className="dossier-type">
                                            {dossier.contract_type === "sale" ? "Demande d'achat" : "Demande de location"}
                                        </span>
                                        <span className={"dossier-status " + status.color}>
                                            {status.label}
                                        </span>
                                    </div>

                                    {canDelete && (
                                        <button
                                            onClick={(e) => { 
                                                e.stopPropagation(); // Empêche de déclencher le clic sur la carte
                                                handleDelete(dossier.id); 
                                            }}
                                            disabled={deleting === dossier.id}
                                            className="dossier-delete-btn"
                                        >
                                            {deleting === dossier.id ? "Annulation..." : "Annuler"}
                                        </button>
                                    )}
                                </div>

                                <div className="dossier-card-body">
                                    {dossier.vehicle_detail && (
                                        <div className="dossier-card-vehicle">
                                            {dossier.vehicle_detail.image && (
                                                <img src={dossier.vehicle_detail.image} alt={dossier.vehicle_detail.brand} />
                                            )}
                                            <div>
                                                <h2>{dossier.vehicle_detail.brand} {dossier.vehicle_detail.model} ({dossier.vehicle_detail.year})</h2>
                                                <p>{dossier.vehicle_detail.mileage.toLocaleString()} km</p>
                                            </div>
                                        </div>
                                    )}

                                    <div className="dossier-card-details">
                                        <div className="dossier-detail-item">
                                            <span>Date de début</span>
                                            <span>{formatDate(dossier.start_date)}</span>
                                        </div>
                                        {dossier.end_date && (
                                            <div className="dossier-detail-item">
                                                <span>Date de fin</span>
                                                <span>{formatDate(dossier.end_date)}</span>
                                            </div>
                                        )}
                                        <div className="dossier-detail-item">
                                            <span>Montant total</span>
                                            <span className="dossier-card-price">
                                                {Number(dossier.total_price).toLocaleString("fr-FR")} EUR
                                            </span>
                                        </div>
                                    </div>
                                    <p className="dossier-card-cta">Cliquer pour voir le détail et uploader vos documents →</p>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}

export default Dossiers;