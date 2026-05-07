import { useNavigate } from 'react-router-dom';
import { Shield, LogOut, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useAuthStore } from '@/store/authStore';

export default function Navbar() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="fixed top-0 left-0 right-0 h-16 bg-[#0F2027] text-white z-50 flex items-center justify-between px-6">
      <div className="flex items-center gap-3">
        <Shield className="h-8 w-8 text-emerald-400" />
        <span className="text-xl font-bold">FinGuard AI</span>
      </div>

      <div className="flex items-center gap-4">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="text-white hover:bg-white/10">
              <User className="h-5 w-5 mr-2" />
              {user?.name || 'User'}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={handleLogout}>
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </nav>
  );
}
