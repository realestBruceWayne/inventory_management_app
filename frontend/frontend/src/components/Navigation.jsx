import React from 'react';
import { Activity, Box, UserCheck, ShoppingCart } from 'lucide-react';

export default function Navigation({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'products', label: 'Products', icon: Box },
    { id: 'customers', label: 'Customers', icon: UserCheck },
    { id: 'orders', label: 'Orders', icon: ShoppingCart },
  ];

  return (
    <div className="bg-white/80 backdrop-blur-lg border-b border-gray-200/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav className="flex space-x-1">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-3 rounded-lg font-medium text-sm transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-md'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Icon className="h-4 w-4 inline mr-2" />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </div>
    </div>
  );
}
