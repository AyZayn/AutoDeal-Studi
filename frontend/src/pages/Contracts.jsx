import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import { useAuth } from "../context/AuthContext";

function Contracts() {
    const [contracts, setContracts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [deleting, setDeleting] = useState(null);
    const { token } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (!token) { navigate("/login"); return; }
        fetchContracts();
    }, [token]);

    const fetchContracts = () => {
        API.get("/contracts/")
            .then((res) => { setContracts(res.data); setLoading(false); })
            .catch(() => setLoading(false));
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Voulez-vous vraiment annuler ce contrat ?")) return;
        setDeleting(id);
        try {
            await API.delete("/contracts/" + id + "/");
            setContracts(contracts.filter(c => c.id !== id));
        } catch {
            alert("Erreur lors de la suppression");
        }
        setDeleting(null);
    };

    const statusConfig = {
        pending:   { label: "En attente", color: "bg-yellow" },
        confirmed: { label: "Confirme",   color: "bg-blue" },
        active:    { label: "En cours",   color: "bg-green" },
        completed: { label: "Termine",    color: "bg-gray" },
        cancelled: { label: "Annule",     color: "bg-red" },
    };

    if (loading) return (
        <div className="page-loading">Chargement...</div>
    );

    return (
        <div className="contracts-page">
            <div className="contracts-header">
                <h1>Mes <span>Contrats</span></h1>
                <p>Historique de vos achats et locations</p>
            </div>
            {contracts.length === 0 ? (
                <div className="contracts-empty">
                    <p>Vous n avez pas encore de contrats</p>
                    <button onClick={() => navigate("/vehicles")} className="contracts-browse-btn">
                        Voir les vehicules
                    </button>
                </div>
            ) : (
                <div className="contracts-list">
                    {contracts.map((contract) => {
                        const status = statusConfig[contract.status] || { label: contract.status, color: "bg-gray" };
                        const canDelete = contract.status === "pending";
                        return (
                            <div key={contract.id} className="contract-card">
                                <div className="contract-card-header">
                                    <div className="contract-card-header-left">
                                        <span className="contract-type">
                                            {contract.contract_type === "sale" ? "Achat" : "Location"}
                                        </span>
                                        <span className={"contract-status " + contract.status}>
                                            {status.label}
                                        </span>
                                    </div>
                                    {canDelete && (
                                        <button
                                            onClick={() => handleDelete(contract.id)}
                                            disabled={deleting === contract.id}
                                            className="contract-delete-btn"
                                        >
                                            {deleting === contract.id ? "Suppression..." : "Annuler"}
                                        </button>
                                    )}
                                </div>
                                <div className="contract-card-body">
                                    {contract.vehicle_detail && (
                                        <h2>{contract.vehicle_detail.brand} {contract.vehicle_detail.model} ({contract.vehicle_detail.year})</h2>
                                    )}
                                    <p>Date de debut : {contract.start_date}</p>
                                    {contract.end_date && <p>Date de fin : {contract.end_date}</p>}
                                    <p className="contract-price">Total : {contract.total_price} EUR</p>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}

export default Contracts;
