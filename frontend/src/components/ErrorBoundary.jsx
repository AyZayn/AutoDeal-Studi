import { Component } from "react";
import logger from "../services/logger";

class ErrorBoundary extends Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        logger.error("Erreur React non geree", {
            error: error.message,
            stack: errorInfo.componentStack,
        });
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style={{
                    minHeight: "100vh",
                    backgroundColor: "#0a0a0f",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexDirection: "column",
                    gap: "16px",
                    padding: "24px",
                }}>
                    <div style={{
                        background: "rgba(230,57,70,0.1)",
                        border: "1px solid rgba(230,57,70,0.2)",
                        borderRadius: "16px",
                        padding: "40px",
                        textAlign: "center",
                        maxWidth: "500px",
                    }}>
                        <p style={{ fontSize: "48px", marginBottom: "16px" }}>⚠️</p>
                        <h1 style={{ color: "white", fontSize: "22px", marginBottom: "12px" }}>
                            Une erreur est survenue
                        </h1>
                        <p style={{ color: "#9ca3af", fontSize: "14px", marginBottom: "24px" }}>
                            Notre equipe a ete notifiee. Veuillez rafraichir la page.
                        </p>
                        <button
                            onClick={() => window.location.reload()}
                            style={{
                                background: "#e63946",
                                color: "white",
                                border: "none",
                                padding: "12px 28px",
                                borderRadius: "10px",
                                fontSize: "15px",
                                fontWeight: "600",
                                cursor: "pointer",
                            }}
                        >
                            Rafraichir la page
                        </button>
                    </div>
                </div>
            );
        }
        return this.props.children;
    }
}

export default ErrorBoundary;