import React from 'react';
import { Package } from 'lucide-react';

export default function Header({ error }) {
  return (
    <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200/50 sticky top-0 z-10 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-xl shadow-lg">
            <Package className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">StockFlow IMS</h1>
            <p className="text-xs text-gray-500">Inventory Management System</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium ${error ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}`}>
            <div className={`w-2 h-2 rounded-full ${error ? 'bg-red-500 animate-pulse' : 'bg-green-500'}`}></div>
            {error ? 'Disconnected' : 'Connected'}
          </div>
        </div>
      </div>
    </header>
  );
}
