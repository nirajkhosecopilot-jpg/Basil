import React from 'react';

function Header() {
  return (
    <header className="gradient-bg text-white shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">🌿 Basil</h1>
            <p className="text-sm opacity-90 mt-1">
              Multi-Agent Architecture Designer
            </p>
          </div>
          <div className="text-right">
            <div className="inline-block bg-white bg-opacity-20 rounded-lg px-4 py-2">
              <p className="text-xs font-semibold">DESIGN-TIME TOOL</p>
              <p className="text-xs opacity-90">Plan before you build</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
