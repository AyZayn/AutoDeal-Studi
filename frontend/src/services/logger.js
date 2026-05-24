const logger = {
    info: (message, data) => {
        console.log("[INFO]", message, data || "");
    },
    warning: (message, data) => {
        console.warn("[WARNING]", message, data || "");
    },
    error: (message, error) => {
        console.error("[ERROR]", message, error || "");
    },
};

export default logger;