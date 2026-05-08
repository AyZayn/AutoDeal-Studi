import os

base = os.path.join("..", "frontend", "src")

files = {}

files[os.path.join(base, "pages", "DossierDetail.jsx")] = """import { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../services/api";
import "./DossierDetail.css";

function DossierDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [dossier, setDossier] = useState(null);
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(null);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const fileRefs = {
        cni: useRef(),
        justificatif_domicile: useRef(),
        fiche_de_paie: useRef(),
    };

    useEffect(() => {
        fetchDossier();
    }, [id]);

    const fetchDossier = () => {
        API.get("/contracts/" + id + "/")
            .then((res) => { setDossier(res.data); setLoading(false); })
            .catch(() => setLoading(false));
    };

    const handleUpload = async (documentType, file) => {
        if (!file) return;
        setUploading(documentType);
        setError("");
        const formData = new FormData();
        formData.append("document_type", documentType);
        formData.append("file", file);
        try {
            await API.post("/contracts/" + id + "/upload_document/", formData, {
                headers: { "Content-Type": "multipart/form-data" }
            });
            setSuccess("Document uploade avec succes !");
            setTimeout(() => setSuccess(""), 3000);
            fetchDossier();
        } catch {
            setError("Erreur lors de l upload");
        }
        setUploading(null);
    };

    const downloadTemplate = (type) => {
        const content = type === "formulaire"
            ? generateFormulaire()
            : generateListeDocuments();
        const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = type === "formulaire" ? "formulaire_dossier.txt" : "liste_documents_requis.txt";
        a.click();
        URL.revokeObjectURL(url);
    };

    const generateFormulaire = () => {
        return `FORMULAIRE DE DOSSIER - AUTODEAL
================================

Type de demande : ${dossier?.contract_type === "sale" ? "ACHAT" : "LOCATION"}
Vehicule : ${dossier?.vehicle_detail?.brand} ${dossier?.vehicle_detail?.model} (${dossier?.vehicle_detail?.year})
Montant total : ${dossier?.total_price} EUR

INFORMATIONS PERSONNELLES
-------------------------
Nom : ___________________________
Prenom : ________________________
Date de naissance : ______________
Adresse : _______________________
Ville : _________________________
Code postal : ___________________
Telephone : _____________________
Email : _________________________

SITUATION PROFESSIONNELLE
-------------------------
Employeur : _____________________
Poste occupe : __________________
Salaire mensuel net : ____________
Anciennete : ____________________

INFORMATIONS BANCAIRES
----------------------
Banque : ________________________
IBAN : __________________________

Fait a ________________, le ________________

Signature : _____________________
`;
    };

    const generateListeDocuments = () => {
        return `LISTE DES DOCUMENTS REQUIS - AUTODEAL
======================================

Pour constituer votre dossier, merci de fournir les documents suivants :

1. CARTE NATIONALE D IDENTITE (CNI)
   - Recto et verso
   - En cours de validite
   - Format accepte : PDF, JPG, PNG

2. JUSTIFICATIF DE DOMICILE
   - De moins de 3 mois
   - Facture EDF, eau, internet ou quittance de loyer
   - Format accepte : PDF, JPG, PNG

3. FICHE DE PAIE
   - Les 3 derniers mois
   - Ou dernier avis d imposition
   - Format accepte : PDF, JPG, PNG

IMPORTANT
---------
- Tous les documents doivent etre lisibles
- Les fichiers ne doivent pas depasser 5 MB
- En cas de doute, contactez-nous

Contact : contact@autodeal.fr
Telephone : 01 23 45 67 89
`;
    };

    const statusSteps = [
        { key: "pending", label: "Dossier depose" },
        { key: "documents_received", label: "Documents recus" },
        { key: "under_review", label: "En verification" },
        { key: "approved", label: "Approuve" },
    ];

    const getStepIndex = (status) => {
        const index = statusSteps.findIndex(s => s.key === status);
        return index === -1 ? 0 : index;
    };

    const documentsRequired = [
        { type: "cni", label: "Carte Nationale d Identite", icon: "🪪" },
        { type: "justificatif_domicile", label: "Justificatif de domicile", icon: "🏠" },
        { type: "fiche_de_paie", label: "Fiche de paie", icon: "💼" },
    ];

    if (loading) return <div className="page-loading">Chargement...</div>;
    if (!dossier) return <div className="page-loading">Dossier introuvable</div>;

    const currentStep = getStepIndex(dossier.status);
    const isRejected = dossier.status === "rejected";
    const isCompleted = dossier.status === "completed";

    return (
        <div className="dossier-detail-page">
            <div className="dossier-detail-container">
                <button onClick={() => navigate("/dossiers")} className="back-btn-d">← Retour</button>

                <div className="dossier-detail-header">
                    <div>
                        <h1>Dossier de {dossier.contract_type === "sale" ? "demande d achat" : "demande de location"}</h1>
                        <p className="dossier-detail-vehicle">
                            {dossier.vehicle_detail?.brand} {dossier.vehicle_detail?.model} ({dossier.vehicle_detail?.year})
                        </p>
                    </div>
                    <span className={"dossier-detail-status " + dossier.status}>
                        {dossier.status === "pending" && "En attente"}
                        {dossier.status === "documents_received" && "Documents recus"}
                        {dossier.status === "under_review" && "En verification"}
                        {dossier.status === "approved" && "Approuve"}
                        {dossier.status === "rejected" && "Refuse"}
                        {dossier.status === "completed" && "Termine"}
                        {dossier.status === "cancelled" && "Annule"}
                    </span>
                </div>

                {!isRejected && !isCompleted && (
                    <div className="dossier-timeline">
                        {statusSteps.map((step, index) => (
                            <div key={step.key} className="timeline-item">
                                <div className={"timeline-dot " + (index <= currentStep ? "active" : "") + (index === currentStep ? " current" : "")}>
                                    {index < currentStep ? "✓" : index + 1}
                                </div>
                                <p className={"timeline-label " + (index <= currentStep ? "active" : "")}>{step.label}</p>
                                {index < statusSteps.length - 1 && (
                                    <div className={"timeline-line " + (index < currentStep ? "active" : "")}></div>
                                )}
                            </div>
                        ))}
                    </div>
                )}

                {isRejected && (
                    <div className="dossier-rejected-banner">
                        ❌ Votre dossier a ete refuse. Veuillez nous contacter pour plus d informations.
                    </div>
                )}

                <div className="dossier-detail-grid">
                    <div className="dossier-detail-left">
                        <div className="dossier-section">
                            <h2>Telecharger les documents</h2>
                            <p className="dossier-section-sub">Telechargez et remplissez ces documents avant de les uploader</p>
                            <div className="download-buttons">
                                <button onClick={() => downloadTemplate("formulaire")} className="download-btn">
                                    <span className="download-icon">📄</span>
                                    <div>
                                        <p className="download-btn-title">Formulaire de dossier</p>
                                        <p className="download-btn-sub">A remplir et signer</p>
                                    </div>
                                </button>
                                <button onClick={() => downloadTemplate("liste")} className="download-btn">
                                    <span className="download-icon">📋</span>
                                    <div>
                                        <p className="download-btn-title">Liste des documents requis</p>
                                        <p className="download-btn-sub">Guide complet</p>
                                    </div>
                                </button>
                            </div>
                        </div>

                        <div className="dossier-section">
                            <h2>Uploader vos documents</h2>
                            <p className="dossier-section-sub">Formats acceptes : PDF, JPG, PNG (max 5MB)</p>
                            {success && <div className="dossier-success-msg">{success}</div>}
                            {error && <div className="dossier-error-msg">{error}</div>}
                            <div className="upload-list">
                                {documentsRequired.map((doc) => {
                                    const uploaded = dossier.documents?.find(d => d.document_type === doc.type);
                                    return (
                                        <div key={doc.type} className={"upload-item " + (uploaded ? "uploaded" : "")}>
                                            <div className="upload-item-left">
                                                <span className="upload-icon">{doc.icon}</span>
                                                <div>
                                                    <p className="upload-item-label">{doc.label}</p>
                                                    <p className="upload-item-status">
                                                        {uploaded
                                                            ? uploaded.verified ? "✅ Verifie" : "⏳ En attente de verification"
                                                            : "⚠️ Non uploade"}
                                                    </p>
                                                </div>
                                            </div>
                                            <div className="upload-item-right">
                                                <input
                                                    type="file"
                                                    ref={fileRefs[doc.type]}
                                                    onChange={(e) => handleUpload(doc.type, e.target.files[0])}
                                                    accept=".pdf,.jpg,.jpeg,.png"
                                                    style={{ display: "none" }}
                                                />
                                                <button
                                                    onClick={() => fileRefs[doc.type].current.click()}
                                                    disabled={uploading === doc.type}
                                                    className={"upload-btn " + (uploaded ? "re-upload" : "")}
                                                >
                                                    {uploading === doc.type ? "Upload..." : uploaded ? "Remplacer" : "Uploader"}
                                                </button>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    </div>

                    <div className="dossier-detail-right">
                        <div className="dossier-section">
                            <h2>Recapitulatif</h2>
                            {dossier.vehicle_detail?.image && (
                                <img src={dossier.vehicle_detail.image} alt={dossier.vehicle_detail.brand} className="dossier-vehicle-img" />
                            )}
                            <div className="dossier-recap-list">
                                <div className="dossier-recap-item">
                                    <span>Type</span>
                                    <span>{dossier.contract_type === "sale" ? "Achat" : "Location"}</span>
                                </div>
                                <div className="dossier-recap-item">
                                    <span>Date de debut</span>
                                    <span>{dossier.start_date}</span>
                                </div>
                                {dossier.end_date && (
                                    <div className="dossier-recap-item">
                                        <span>Date de fin</span>
                                        <span>{dossier.end_date}</span>
                                    </div>
                                )}
                                <div className="dossier-recap-item total">
                                    <span>Montant total</span>
                                    <span>{Number(dossier.total_price).toLocaleString("fr-FR")} EUR</span>
                                </div>
                            </div>
                        </div>

                        {dossier.notes && (
                            <div className="dossier-section">
                                <h2>Votre message</h2>
                                <p className="dossier-notes-text">"{dossier.notes}"</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default DossierDetail;
"""

files[os.path.join(base, "pages", "DossierDetail.css")] = """.dossier-detail-page {
    min-height: calc(100vh - 68px);
    padding: 48px;
    background: #0a0a0f;
}

.dossier-detail-container {
    max-width: 1100px;
    margin: 0 auto;
}

.dossier-detail-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 40px;
}

.dossier-detail-header h1 {
    font-size: 26px;
    font-weight: 800;
    color: white;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
    text-transform: capitalize;
}

.dossier-detail-vehicle {
    color: #6b7280;
    font-size: 15px;
}

.dossier-detail-status {
    padding: 6px 16px;
    border-radius: 99px;
    font-size: 13px;
    font-weight: 600;
    white-space: nowrap;
}

.dossier-detail-status.pending           { background: rgba(234,179,8,0.15);   color: #eab308; }
.dossier-detail-status.documents_received { background: rgba(59,130,246,0.15);  color: #3b82f6; }
.dossier-detail-status.under_review      { background: rgba(139,92,246,0.15);  color: #8b5cf6; }
.dossier-detail-status.approved          { background: rgba(34,197,94,0.15);   color: #22c55e; }
.dossier-detail-status.rejected          { background: rgba(230,57,70,0.15);   color: #e63946; }
.dossier-detail-status.completed         { background: rgba(156,163,175,0.15); color: #9ca3af; }
.dossier-detail-status.cancelled         { background: rgba(156,163,175,0.15); color: #9ca3af; }

.dossier-timeline {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    gap: 0;
    margin-bottom: 40px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 28px 40px;
}

.timeline-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    flex: 1;
}

.timeline-dot {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
    border: 2px solid rgba(255,255,255,0.1);
    color: #6b7280;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 10px;
    transition: all 0.3s;
    position: relative;
    z-index: 1;
}

.timeline-dot.active {
    background: rgba(34,197,94,0.15);
    border-color: #22c55e;
    color: #22c55e;
}

.timeline-dot.current {
    background: #e63946;
    border-color: #e63946;
    color: white;
    box-shadow: 0 0 16px rgba(230,57,70,0.4);
}

.timeline-label {
    font-size: 12px;
    color: #6b7280;
    text-align: center;
    font-weight: 500;
}

.timeline-label.active { color: white; }

.timeline-line {
    position: absolute;
    top: 18px;
    left: 50%;
    width: 100%;
    height: 2px;
    background: rgba(255,255,255,0.08);
    z-index: 0;
}

.timeline-line.active { background: #22c55e; }

.dossier-rejected-banner {
    background: rgba(230,57,70,0.1);
    border: 1px solid rgba(230,57,70,0.2);
    color: #e63946;
    padding: 16px 20px;
    border-radius: 12px;
    margin-bottom: 32px;
    font-size: 15px;
}

.dossier-detail-grid {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 24px;
    align-items: start;
}

.dossier-section {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 20px;
}

.dossier-section h2 {
    font-size: 17px;
    font-weight: 700;
    color: white;
    margin-bottom: 6px;
}

.dossier-section-sub {
    color: #6b7280;
    font-size: 13px;
    margin-bottom: 20px;
}

.download-buttons {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.download-btn {
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px 20px;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    width: 100%;
}

.download-btn:hover {
    background: rgba(255,255,255,0.06);
    border-color: rgba(255,255,255,0.15);
    transform: translateY(-1px);
}

.download-icon { font-size: 28px; }

.download-btn-title {
    color: white;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 2px;
}

.download-btn-sub {
    color: #6b7280;
    font-size: 12px;
}

.dossier-success-msg {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.2);
    color: #22c55e;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 13px;
    margin-bottom: 16px;
}

.dossier-error-msg {
    background: rgba(230,57,70,0.1);
    border: 1px solid rgba(230,57,70,0.2);
    color: #e63946;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 13px;
    margin-bottom: 16px;
}

.upload-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.upload-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px 18px;
    transition: border-color 0.2s;
}

.upload-item.uploaded {
    border-color: rgba(34,197,94,0.2);
    background: rgba(34,197,94,0.03);
}

.upload-item-left {
    display: flex;
    align-items: center;
    gap: 14px;
}

.upload-icon { font-size: 22px; }

.upload-item-label {
    color: white;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 3px;
}

.upload-item-status {
    color: #6b7280;
    font-size: 12px;
}

.upload-btn {
    background: #e63946;
    color: white;
    border: none;
    padding: 8px 18px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
    white-space: nowrap;
}

.upload-btn:hover { background: #c1121f; }

.upload-btn.re-upload {
    background: transparent;
    border: 1px solid rgba(255,255,255,0.15);
    color: #9ca3af;
}

.upload-btn.re-upload:hover {
    color: white;
    border-color: rgba(255,255,255,0.3);
}

.upload-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.dossier-vehicle-img {
    width: 100%;
    height: 160px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 20px;
}

.dossier-recap-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.dossier-recap-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.dossier-recap-item span:first-child {
    color: #6b7280;
    font-size: 13px;
}

.dossier-recap-item span:last-child {
    color: white;
    font-size: 14px;
    font-weight: 500;
}

.dossier-recap-item.total span:last-child {
    color: #e63946;
    font-weight: 700;
    font-size: 16px;
}

.dossier-notes-text {
    color: #9ca3af;
    font-style: italic;
    font-size: 14px;
    line-height: 1.6;
}
"""

files[os.path.join(base, "pages", "Dossiers.jsx")] = """import { useState, useEffect } from "react";
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

    useEffect(() => {
        if (!token) { navigate("/login"); return; }
        fetchDossiers();
    }, [token]);

    const fetchDossiers = () => {
        API.get("/contracts/")
            .then((res) => { setDossiers(res.data); setLoading(false); })
            .catch(() => setLoading(false));
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Voulez-vous vraiment annuler ce dossier ?")) return;
        setDeleting(id);
        try {
            await API.delete("/contracts/" + id + "/");
            setDossiers(dossiers.filter(c => c.id !== id));
        } catch {
            alert("Erreur lors de l annulation");
        }
        setDeleting(null);
    };

    const statusConfig = {
        pending:              { label: "En attente",          color: "pending" },
        documents_received:   { label: "Documents recus",     color: "documents_received" },
        under_review:         { label: "En verification",     color: "under_review" },
        approved:             { label: "Approuve",            color: "approved" },
        rejected:             { label: "Refuse",              color: "rejected" },
        completed:            { label: "Termine",             color: "completed" },
        cancelled:            { label: "Annule",              color: "cancelled" },
    };

    if (loading) return <div className="page-loading">Chargement...</div>;

    return (
        <div className="dossiers-page">
            <div className="dossiers-header">
                <h1>Mes <span>Dossiers</span></h1>
                <p>Suivez vos demandes d achat et de location</p>
            </div>
            {dossiers.length === 0 ? (
                <div className="dossiers-empty">
                    <p>Vous n avez pas encore de dossiers</p>
                    <button onClick={() => navigate("/vehicles")} className="dossiers-browse-btn">
                        Voir les vehicules
                    </button>
                </div>
            ) : (
                <div className="dossiers-list">
                    {dossiers.map((dossier) => {
                        const status = statusConfig[dossier.status] || { label: dossier.status, color: "pending" };
                        const canDelete = dossier.status === "pending";
                        return (
                            <div key={dossier.id} className="dossier-card" onClick={() => navigate("/dossiers/" + dossier.id)} style={{ cursor: "pointer" }}>
                                <div className="dossier-card-header">
                                    <div className="dossier-card-header-left">
                                        <span className="dossier-type">
                                            {dossier.contract_type === "sale" ? "Demande d achat" : "Demande de location"}
                                        </span>
                                        <span className={"dossier-status " + status.color}>
                                            {status.label}
                                        </span>
                                    </div>
                                    {canDelete && (
                                        <button
                                            onClick={(e) => { e.stopPropagation(); handleDelete(dossier.id); }}
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
                                                <p>{dossier.vehicle_detail.mileage} km</p>
                                            </div>
                                        </div>
                                    )}
                                    <div className="dossier-card-details">
                                        <div className="dossier-detail-item">
                                            <span>Date de debut</span>
                                            <span>{dossier.start_date}</span>
                                        </div>
                                        {dossier.end_date && (
                                            <div className="dossier-detail-item">
                                                <span>Date de fin</span>
                                                <span>{dossier.end_date}</span>
                                            </div>
                                        )}
                                        <div className="dossier-detail-item">
                                            <span>Montant total</span>
                                            <span className="dossier-card-price">{Number(dossier.total_price).toLocaleString("fr-FR")} EUR</span>
                                        </div>
                                    </div>
                                    <p className="dossier-card-cta">Cliquer pour voir le detail et uploader vos documents →</p>
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
"""

files[os.path.join(base, "App.jsx")] = """import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import VehicleList from "./pages/VehicleList";
import VehicleDetail from "./pages/VehicleDetail";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dossiers from "./pages/Dossiers";
import DossierDetail from "./pages/DossierDetail";
import NewDossier from "./pages/NewDossier";
import Profile from "./pages/Profile";

function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/vehicles" element={<VehicleList />} />
                    <Route path="/vehicles/:id" element={<VehicleDetail />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/dossiers" element={<Dossiers />} />
                    <Route path="/dossiers/:id" element={<DossierDetail />} />
                    <Route path="/dossier/new" element={<NewDossier />} />
                    <Route path="/profile" element={<Profile />} />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;
"""

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK " + filepath)

print("")
print("Page DossierDetail creee avec succes !")