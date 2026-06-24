import React from 'react';

export default function Loading() {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="relative">
        <div className="w-12 h-12 border-4 border-blue-200 rounded-full"></div>
        <div className="w-12 h-12 border-4 border-blue-600 rounded-full absolute top-0 left-0 animate-spin border-t-transparent"></div>
      </div>
      <p className="mt-4 text-gray-600 font-medium">Loading your data...</p>
    </div>
  );
}
