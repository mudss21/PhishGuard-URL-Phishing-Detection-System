import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";
import { BarChart3, Activity, ShieldCheck, ShieldAlert } from "lucide-react";

const STATS = {
  total: 1247,
  safe: 982,
  phishing: 265,
};

const pieData = [
  { name: "Safe", value: STATS.safe },
  { name: "Phishing", value: STATS.phishing },
];

const weeklyData = [
  { day: "Mon", safe: 42, phishing: 8 },
  { day: "Tue", safe: 55, phishing: 12 },
  { day: "Wed", safe: 38, phishing: 15 },
  { day: "Thu", safe: 60, phishing: 9 },
  { day: "Fri", safe: 48, phishing: 11 },
  { day: "Sat", safe: 30, phishing: 6 },
  { day: "Sun", safe: 25, phishing: 4 },
];

const PIE_COLORS = ["hsl(145, 70%, 45%)", "hsl(0, 75%, 55%)"];

const StatCard = ({
  icon: Icon,
  label,
  value,
  color,
}: {
  icon: typeof Activity;
  label: string;
  value: number;
  color: string;
}) => (
  <div className="glass rounded-lg p-5 flex items-center gap-4">
    <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${color}`}>
      <Icon className="w-6 h-6" />
    </div>
    <div>
      <p className="text-xs text-muted-foreground uppercase tracking-wider">{label}</p>
      <p className="text-2xl font-bold text-foreground font-mono">{value.toLocaleString()}</p>
    </div>
  </div>
);

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload) return null;
  return (
    <div className="glass rounded-md p-3 text-xs">
      <p className="text-foreground font-semibold mb-1">{label}</p>
      {payload.map((p: any) => (
        <p key={p.name} style={{ color: p.fill }} className="font-mono">
          {p.name}: {p.value}
        </p>
      ))}
    </div>
  );
};

const AnalyticsPanel = () => {
  return (
    <div className="space-y-6">
      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard icon={Activity} label="Total Scanned" value={STATS.total} color="bg-primary/15 text-primary" />
        <StatCard icon={ShieldCheck} label="Safe URLs" value={STATS.safe} color="bg-safe/15 text-safe" />
        <StatCard icon={ShieldAlert} label="Phishing Detected" value={STATS.phishing} color="bg-destructive/15 text-destructive" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <div className="glass rounded-lg p-6">
          <h3 className="text-sm font-semibold text-foreground mb-4 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-primary" />
            Detection Distribution
          </h3>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={4}
                  dataKey="value"
                  stroke="none"
                >
                  {pieData.map((_, i) => (
                    <Cell key={i} fill={PIE_COLORS[i]} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center gap-6 mt-2">
            {pieData.map((d, i) => (
              <div key={d.name} className="flex items-center gap-2 text-xs">
                <span className="w-3 h-3 rounded-full" style={{ background: PIE_COLORS[i] }} />
                <span className="text-muted-foreground">{d.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Bar Chart */}
        <div className="glass rounded-lg p-6">
          <h3 className="text-sm font-semibold text-foreground mb-4 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-primary" />
            Weekly Activity
          </h3>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={weeklyData} barGap={2}>
                <XAxis dataKey="day" axisLine={false} tickLine={false} tick={{ fill: "hsl(215,15%,50%)", fontSize: 12 }} />
                <YAxis axisLine={false} tickLine={false} tick={{ fill: "hsl(215,15%,50%)", fontSize: 12 }} width={30} />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: "hsl(220,15%,15%)" }} />
                <Bar dataKey="safe" fill="hsl(145,70%,45%)" radius={[4, 4, 0, 0]} />
                <Bar dataKey="phishing" fill="hsl(0,75%,55%)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPanel;
