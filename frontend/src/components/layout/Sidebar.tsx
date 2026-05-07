import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Receipt,
  PieChart,
  Brain,
} from 'lucide-react';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/expenses', label: 'Expenses', icon: Receipt },
  { path: '/predictions', label: 'Predictions', icon: Brain },
  { path: '/investments', label: 'Investments', icon: PieChart },
];

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-16 w-64 h-[calc(100vh-4rem)] bg-white border-r border-slate-200 z-40">
      <nav className="p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-emerald-50 text-emerald-600 font-medium'
                  : 'text-slate-600 hover:bg-slate-50'
              }`
            }
          >
            <item.icon className="h-5 w-5" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-slate-200">
        <div className="bg-gradient-to-r from-[#0F2027] to-[#203A43] rounded-lg p-4 text-white">
          <p className="text-sm font-medium mb-1">AI-Powered Insights</p>
          <p className="text-xs text-slate-300">
            Get personalized financial recommendations
          </p>
        </div>
      </div>
    </aside>
  );
}
