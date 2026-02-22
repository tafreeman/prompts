import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Workflow,
  Radio,
  Zap,
  Database,
  Trophy,
} from "lucide-react";

const links = [
  { to: "/", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/workflows", icon: Workflow, label: "Workflows" },
  { to: "/datasets", icon: Database, label: "Datasets" },
  { to: "/evaluations", icon: Trophy, label: "Evaluations" },
  { to: "/live/latest", icon: Radio, label: "Live" },
];

export default function Sidebar() {
  return (
    <aside className="flex h-full w-56 flex-col border-r border-white/5 bg-surface-1">
      {/* Logo */}
      <div className="flex items-center gap-2 px-4 py-5">
        <Zap className="h-5 w-5 text-accent-blue" />
        <span className="text-sm font-semibold tracking-wide">
          Agentic Workflows
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-2">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors ${
                isActive
                  ? "bg-accent-blue/10 text-accent-blue"
                  : "text-gray-400 hover:bg-white/5 hover:text-gray-200"
              }`
            }
          >
            <link.icon className="h-4 w-4" />
            {link.label}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="border-t border-white/5 px-4 py-3">
        <p className="text-xs text-gray-600">v0.1.0</p>
      </div>
    </aside>
  );
}
