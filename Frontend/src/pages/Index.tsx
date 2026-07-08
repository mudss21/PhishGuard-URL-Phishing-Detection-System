import { Shield, Activity, Menu, X } from "lucide-react";
import { useState } from "react";
import URLChecker from "@/components/URLChecker";
import HistoryTable from "@/components/HistoryTable";
import AnalyticsPanel from "@/components/AnalyticsPanel";

type Tab = "scan" | "history" | "analytics";

const tabs: { id: Tab; label: string }[] = [
  { id: "scan", label: "URL Scanner" },
  { id: "history", label: "History" },
  { id: "analytics", label: "Analytics" },
];

const Index = () => {
  const [activeTab, setActiveTab] = useState<Tab>("scan");
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 glass border-b border-border/50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-primary/15 flex items-center justify-center">
              <Shield className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h1 className="text-base font-bold text-foreground tracking-tight">PhishGuard</h1>
              <p className="text-[10px] text-muted-foreground uppercase tracking-widest">URL Threat Detection</p>
            </div>
          </div>

          {/* Desktop nav */}
          <nav className="hidden sm:flex items-center gap-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                  activeTab === tab.id
                    ? "bg-primary/15 text-primary"
                    : "text-muted-foreground hover:text-foreground hover:bg-secondary/50"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>

          {/* Status indicator */}
          <div className="hidden sm:flex items-center gap-2 text-xs text-muted-foreground">
            <span className="w-2 h-2 rounded-full bg-safe animate-pulse-glow" />
            System Active
          </div>

          {/* Mobile menu button */}
          <button
            className="sm:hidden text-muted-foreground"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

        {/* Mobile nav */}
        {mobileMenuOpen && (
          <nav className="sm:hidden border-t border-border/50 px-4 py-2 flex flex-col gap-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id);
                  setMobileMenuOpen(false);
                }}
                className={`px-4 py-2.5 rounded-md text-sm font-medium text-left transition-all ${
                  activeTab === tab.id
                    ? "bg-primary/15 text-primary"
                    : "text-muted-foreground"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        )}
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        {activeTab === "scan" && <URLChecker />}
        {activeTab === "history" && <HistoryTable />}
        {activeTab === "analytics" && <AnalyticsPanel />}
      </main>
    </div>
  );
};

export default Index;
