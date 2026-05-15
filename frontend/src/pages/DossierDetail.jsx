import { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../services/api";
import "./DossierDetail.css";
import { jsPDF } from "jspdf";
import autoTable from "jspdf-autotable";

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
            setError("Erreur lors de l'upload");
        }
        setUploading(null);
    };


const downloadTemplate = (type) => {
    if (type === "liste") {
const a = document.createElement("a");
a.href = "/Documents/Liste_Documents_Requis_AutoDeal.pdf";
a.download = "Liste_Documents_Requis_AutoDeal.pdf";
a.click();
        return;
    }
    generateFormulairePDF();
};

const generateFormulairePDF = () => {
    const doc = new jsPDF();
    const rouge = [230, 57, 70];
    const noir = [10, 10, 15];
    const gris = [107, 114, 128];

    // En-tête
    doc.setFillColor(...rouge);
    doc.rect(0, 0, 210, 35, "F");

    doc.setTextColor(255, 255, 255);
    doc.setFontSize(22);
    doc.setFont("helvetica", "bold");
    doc.text("AutoDeal", 15, 18);

    doc.setFontSize(11);
    doc.setFont("helvetica", "normal");
    doc.text("Formulaire de dossier de " + (dossier?.contract_type === "sale" ? "demande d achat" : "demande de location"), 15, 28);

    // Informations vehicule
    doc.setTextColor(...noir);
    doc.setFontSize(13);
    doc.setFont("helvetica", "bold");
    doc.text("Vehicule concerne", 15, 50);

    autoTable(doc, {
        startY: 55,
        head: [],
        body: [
            ["Marque / Modele", `${dossier?.vehicle_detail?.brand} ${dossier?.vehicle_detail?.model}`],
            ["Annee", `${dossier?.vehicle_detail?.year}`],
            ["Type de demande", dossier?.contract_type === "sale" ? "Achat" : "Location"],
            ["Montant total", `${Number(dossier?.total_price).toLocaleString("fr-FR")} EUR`],
            ["Date de debut", dossier?.start_date || ""],
            ["Date de fin", dossier?.end_date || "Non applicable"],
        ],
        theme: "grid",
        styles: { fontSize: 10, cellPadding: 4 },
        columnStyles: {
            0: { fillColor: [245, 245, 245], fontStyle: "bold", cellWidth: 60 },
            1: { cellWidth: 120 },
        },
        margin: { left: 15, right: 15 },
    });

    // Informations personnelles
    const y1 = doc.lastAutoTable.finalY + 15;
    doc.setFontSize(13);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(...noir);
    doc.text("Informations personnelles", 15, y1);

    autoTable(doc, {
        startY: y1 + 5,
        head: [],
        body: [
            ["Nom", ""],
            ["Prenom", ""],
            ["Date de naissance", ""],
            ["Adresse", ""],
            ["Ville", ""],
            ["Code postal", ""],
            ["Telephone", ""],
            ["Email", ""],
        ],
        theme: "grid",
        styles: { fontSize: 10, cellPadding: 6 },
        columnStyles: {
            0: { fillColor: [245, 245, 245], fontStyle: "bold", cellWidth: 60 },
            1: { cellWidth: 120 },
        },
        margin: { left: 15, right: 15 },
    });

    // Situation professionnelle
    const y2 = doc.lastAutoTable.finalY + 15;
    doc.setFontSize(13);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(...noir);
    doc.text("Situation professionnelle", 15, y2);

    autoTable(doc, {
        startY: y2 + 5,
        head: [],
        body: [
            ["Employeur", ""],
            ["Poste occupe", ""],
            ["Salaire mensuel net", ""],
            ["Anciennete", ""],
        ],
        theme: "grid",
        styles: { fontSize: 10, cellPadding: 6 },
        columnStyles: {
            0: { fillColor: [245, 245, 245], fontStyle: "bold", cellWidth: 60 },
            1: { cellWidth: 120 },
        },
        margin: { left: 15, right: 15 },
    });

    // Informations bancaires
    const y3 = doc.lastAutoTable.finalY + 15;
    doc.setFontSize(13);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(...noir);
    doc.text("Informations bancaires", 15, y3);

    autoTable(doc, {
        startY: y3 + 5,
        head: [],
        body: [
            ["Banque", ""],
            ["IBAN", ""],
        ],
        theme: "grid",
        styles: { fontSize: 10, cellPadding: 6 },
        columnStyles: {
            0: { fillColor: [245, 245, 245], fontStyle: "bold", cellWidth: 60 },
            1: { cellWidth: 120 },
        },
        margin: { left: 15, right: 15 },
    });

    // Signature
    const y4 = doc.lastAutoTable.finalY + 15;
    doc.setFontSize(10);
    doc.setFont("helvetica", "normal");
    doc.setTextColor(...gris);
    doc.text("Fait a _________________________, le _________________________", 15, y4);
    doc.text("Signature :", 15, y4 + 15);
    doc.line(40, y4 + 15, 120, y4 + 15);

    // Pied de page
    doc.setFillColor(...rouge);
    doc.rect(0, 280, 210, 17, "F");
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(9);
    doc.text("AutoDeal — contact@autodeal.fr — 01 23 45 67 89", 15, 290);
    doc.text("www.autodeal.fr", 160, 290);

    doc.save("formulaire_dossier_autodeal.pdf");
};

    const statusSteps = [
        { key: "pending", label: "Dossier déposé" },
        { key: "documents_received", label: "Documents reçus" },
        { key: "under_review", label: "En verification" },
        { key: "approved", label: "Approuvé" },
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
                        ❌ Votre dossier a été refusé. Veuillez nous contacter pour plus d informations.
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
