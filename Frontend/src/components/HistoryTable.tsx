import { useState, useEffect } from "react";
import { Clock, Shield, ShieldAlert, ExternalLink } from "lucide-react";
import { getHistory, type HistoryEntry } from "@/services/api";

// Demo data used when backend is unavailable
const DEMO_HISTORY: HistoryEntry[] = [
  { url: "https://google.com", result: "Safe", confidence: 98.2, timestamp: "2026-02-13T10:30:00Z" },
  { url: "http://faceb00k-login.xyz/auth", result: "Phishing", confidence: 95.7, timestamp: "2026-02-13T10:25:00Z" },
  { url: "https://github.com", result: "Safe", confidence: 99.1, timestamp: "2026-02-13T10:20:00Z" },
  { url: "http://paypa1-verify.com/update", result: "Phishing", confidence: 92.3, timestamp: "2026-02-13T10:15:00Z" },
  { url: "https://stackoverflow.com", result: "Safe", confidence: 97.8, timestamp: "2026-02-13T10:10:00Z" },
  { url: "http://amaz0n-deal.net/login", result: "Phishing", confidence: 88.9, timestamp: "2026-02-13T10:05:00Z" },
  { url: "https://react.dev", result: "Safe", confidence: 99.5, timestamp: "2026-02-13T10:00:00Z" },
];

const HistoryTable = () => {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getHistory();
        setHistory(data);
      } catch {
        setHistory(DEMO_HISTORY);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const formatTime = (ts: string) => {
    const d = new Date(ts);
    return d.toLocaleString("en-US", {
      month: "short", day: "numeric", hour: "2-digit", minute: "2-digit",
    });
  };

  return (
    <div className="glass rounded-lg p-6">
      <h2 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
        <Clock className="w-5 h-5 text-primary" />
        Scan History
      </h2>

      {loading ? (
        <div className="flex items-center justify-center py-12 text-muted-foreground">
          Loading...
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border text-left text-muted-foreground text-xs uppercase tracking-wider">
                <th className="pb-3 pr-4">URL</th>
                <th className="pb-3 pr-4">Result</th>
                <th className="pb-3 pr-4">Confidence</th>
                <th className="pb-3">Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {history.map((entry, i) => (
                <tr
                  key={i}
                  className="border-b border-border/50 hover:bg-secondary/30 transition-colors"
                >
                  <td className="py-3 pr-4">
                    <div className="flex items-center gap-2 max-w-xs">
                      <ExternalLink className="w-3 h-3 text-muted-foreground flex-shrink-0" />
                      <span className="font-mono text-xs truncate text-foreground">
                        {entry.url}
                      </span>
                    </div>
                  </td>
                  <td className="py-3 pr-4">
                    <span
                      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${
                        entry.result === "Safe"
                          ? "bg-safe/15 text-safe"
                          : "bg-destructive/15 text-destructive"
                      }`}
                    >
                      {entry.result === "Safe" ? (
                        <Shield className="w-3 h-3" />
                      ) : (
                        <ShieldAlert className="w-3 h-3" />
                      )}
                      {entry.result}
                    </span>
                  </td>
                  <td className="py-3 pr-4 font-mono text-xs text-foreground">
                    {entry.confidence}%
                  </td>
                  <td className="py-3 text-xs text-muted-foreground">
                    {formatTime(entry.timestamp)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default HistoryTable;
