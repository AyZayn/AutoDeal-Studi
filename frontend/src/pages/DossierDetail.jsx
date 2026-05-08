import { useState, useEffect, useRef } from "react";
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
