import { useState } from "react";
import {
  Shield,
  ShieldAlert,
  Search,
  Loader2,
  Link as LinkIcon,
} from "lucide-react";
import { predictURL } from "@/services/api";

interface DisplayResult {
  result: string;
  confidence: number;
}

const URLChecker = () => {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DisplayResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [checkedUrl, setCheckedUrl] = useState("");

  const handleCheck = async () => {
    if (!url.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await predictURL(url);

      setResult({
        result:
          data.prediction === "Legitimate"
            ? "Safe"
            : "Phishing",
        confidence: Number(
          (data.probability * 100).toFixed(2)
        ),
      });

      setCheckedUrl(url);
    } catch (err) {
      console.error(err);
      setError("Failed to connect to backend server.");
    } finally {
      setLoading(false);
    }
  };

  const isSafe = result?.result === "Safe";

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="glass rounded-lg p-6">
        <h2 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
          <Search className="w-5 h-5 text-primary" />
          Scan URL
        </h2>

        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <LinkIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />

            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              onKeyDown={(e) =>
                e.key === "Enter" && handleCheck()
              }
              placeholder="Enter URL to analyze..."
              className="w-full bg-input border border-border rounded-md pl-10 pr-4 py-3 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all font-mono text-sm"
            />
          </div>

          <button
            onClick={handleCheck}
            disabled={loading || !url.trim()}
            className="flex items-center justify-center gap-2 bg-primary text-primary-foreground px-6 py-3 rounded-md font-semibold hover:opacity-90 transition-all disabled:opacity-40 disabled:cursor-not-allowed glow-primary"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Shield className="w-4 h-4" />
            )}

            {loading ? "Scanning..." : "Check URL"}
          </button>
        </div>
      </div>

      {/* Result */}
      {result && (
        <div
          className={`rounded-lg p-6 border animate-fade-in-up ${
            isSafe
              ? "glass border-safe/30 glow-safe"
              : "glass border-destructive/30 glow-danger"
          }`}
        >
          <div className="flex items-center gap-4">
            <div
              className={`w-16 h-16 rounded-full flex items-center justify-center ${
                isSafe
                  ? "bg-safe/15"
                  : "bg-destructive/15"
              }`}
            >
              {isSafe ? (
                <Shield className="w-8 h-8 text-safe" />
              ) : (
                <ShieldAlert className="w-8 h-8 text-destructive" />
              )}
            </div>

            <div className="flex-1 min-w-0">
              <p className="text-sm text-muted-foreground font-mono truncate mb-1">
                {checkedUrl}
              </p>

              <p
                className={`text-2xl font-bold ${
                  isSafe
                    ? "text-safe"
                    : "text-destructive"
                }`}
              >
                {result.result}
              </p>
            </div>

            <div className="text-right">
              <p className="text-xs text-muted-foreground uppercase tracking-wider">
                Probability
              </p>

              <p
                className={`text-3xl font-bold font-mono ${
                  isSafe
                    ? "text-safe"
                    : "text-destructive"
                }`}
              >
                {result.confidence}%
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="glass border-destructive/30 rounded-lg p-4 text-destructive text-sm">
          {error}
        </div>
      )}
    </div>
  );
};

export default URLChecker;