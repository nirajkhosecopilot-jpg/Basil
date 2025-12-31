import React, { useState } from 'react';
import DesignForm from './components/DesignForm';
import ArchitectureView from './components/ArchitectureView';
import Header from './components/Header';

function App() {
  const [architecture, setArchitecture] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleDesign = (newArchitecture) => {
    setArchitecture(newArchitecture);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-7xl mx-auto">
          {!architecture ? (
            <DesignForm
              onDesign={handleDesign}
              loading={loading}
              setLoading={setLoading}
            />
          ) : (
            <ArchitectureView
              architecture={architecture}
              onReset={() => setArchitecture(null)}
            />
          )}
        </div>
      </main>

      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="container mx-auto px-4 py-6 text-center text-gray-600">
          <p>Basil - Multi-Agent Architecture Designer v1.0.0</p>
          <p className="text-sm mt-2">Design-time architecture planner for multi-agent AI systems</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
