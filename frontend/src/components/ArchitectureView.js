import React, { useState } from 'react';
import AgentCard from './AgentCard';
import CostEstimates from './CostEstimates';
import ArchitectureGraph from './ArchitectureGraph';

function ArchitectureView({ architecture, onReset }) {
  const [activeTab, setActiveTab] = useState('overview');
  const [showExportMenu, setShowExportMenu] = useState(false);

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'agents', label: 'Agents', icon: '🤖' },
    { id: 'graph', label: 'Architecture Graph', icon: '🔀' },
    { id: 'costs', label: 'Cost Analysis', icon: '💰' },
    { id: 'raw', label: 'Raw Data', icon: '📄' }
  ];

  const agentTypeColors = {
    coordinator: 'bg-purple-100 text-purple-800 border-purple-300',
    specialist: 'bg-blue-100 text-blue-800 border-blue-300',
    executor: 'bg-green-100 text-green-800 border-green-300',
    analyzer: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    validator: 'bg-red-100 text-red-800 border-red-300'
  };

  const groupedAgents = architecture.agents.reduce((acc, agent) => {
    if (!acc[agent.type]) acc[agent.type] = [];
    acc[agent.type].push(agent);
    return acc;
  }, {});

  const handleExport = (format) => {
    // In a real app, this would call the export API
    const content = format === 'json'
      ? JSON.stringify(architecture, null, 2)
      : architecture.visualization;

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `basil-architecture.${format}`;
    a.click();
    setShowExportMenu(false);
  };

  return (
    <div className="space-y-6">
      {/* Header with Actions */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-3">
              <h2 className="text-2xl font-bold text-gray-900">
                Architecture Design
              </h2>
              {architecture.validation.is_valid ? (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                  ✓ Valid
                </span>
              ) : (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800">
                  ⚠ Issues Found
                </span>
              )}
            </div>
            <p className="text-gray-600 line-clamp-2">
              {architecture.problem_statement}
            </p>
          </div>

          <div className="flex space-x-3 ml-6">
            <div className="relative">
              <button
                onClick={() => setShowExportMenu(!showExportMenu)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                📥 Export
              </button>

              {showExportMenu && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl border border-gray-200 z-10">
                  <div className="py-1">
                    {['json', 'yaml', 'markdown', 'mermaid'].map(format => (
                      <button
                        key={format}
                        onClick={() => handleExport(format)}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Export as {format.toUpperCase()}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <button
              onClick={onReset}
              className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              🔄 New Design
            </button>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4">
            <p className="text-sm text-purple-600 font-medium">Total Agents</p>
            <p className="text-3xl font-bold text-purple-900">{architecture.agents.length}</p>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4">
            <p className="text-sm text-blue-600 font-medium">Communications</p>
            <p className="text-3xl font-bold text-blue-900">{architecture.communications.length}</p>
          </div>
          <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4">
            <p className="text-sm text-green-600 font-medium">Domains</p>
            <p className="text-3xl font-bold text-green-900">{architecture.metadata.num_domains}</p>
          </div>
          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-lg p-4">
            <p className="text-sm text-yellow-600 font-medium">Est. Cost/mo</p>
            <p className="text-3xl font-bold text-yellow-900">
              ${architecture.cost_estimates['10k_requests'].toFixed(2)}
            </p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  flex-1 py-4 px-6 text-sm font-medium border-b-2 transition-colors
                  ${activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Problem Statement</h3>
                <p className="text-gray-700 bg-gray-50 rounded-lg p-4">
                  {architecture.problem_statement}
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Architecture Summary</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-blue-50 rounded-lg p-4">
                    <h4 className="font-medium text-blue-900 mb-2">Agent Distribution</h4>
                    <div className="space-y-2">
                      {Object.entries(groupedAgents).map(([type, agents]) => (
                        <div key={type} className="flex justify-between items-center">
                          <span className={`text-sm px-2 py-1 rounded ${agentTypeColors[type]}`}>
                            {type}
                          </span>
                          <span className="text-sm font-semibold text-gray-700">{agents.length}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="bg-purple-50 rounded-lg p-4">
                    <h4 className="font-medium text-purple-900 mb-2">LLM Distribution</h4>
                    <div className="space-y-2">
                      {Object.entries(
                        architecture.agents.reduce((acc, agent) => {
                          acc[agent.llm_tier] = (acc[agent.llm_tier] || 0) + 1;
                          return acc;
                        }, {})
                      ).map(([tier, count]) => (
                        <div key={tier} className="flex justify-between items-center">
                          <span className="text-sm text-purple-700 capitalize">{tier}</span>
                          <span className="text-sm font-semibold text-purple-900">{count} agents</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {!architecture.validation.is_valid && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <h4 className="font-semibold text-red-900 mb-2">⚠ Validation Issues</h4>
                  <ul className="list-disc list-inside space-y-1">
                    {architecture.validation.errors.map((error, i) => (
                      <li key={i} className="text-sm text-red-700">{error}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Agents Tab */}
          {activeTab === 'agents' && (
            <div className="space-y-6">
              {Object.entries(groupedAgents).map(([type, agents]) => (
                <div key={type}>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 capitalize">
                    {type} Agents ({agents.length})
                  </h3>
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    {agents.map(agent => (
                      <AgentCard key={agent.id} agent={agent} />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Graph Tab */}
          {activeTab === 'graph' && (
            <ArchitectureGraph
              agents={architecture.agents}
              communications={architecture.communications}
            />
          )}

          {/* Costs Tab */}
          {activeTab === 'costs' && (
            <CostEstimates
              agents={architecture.agents}
              costEstimates={architecture.cost_estimates}
            />
          )}

          {/* Raw Data Tab */}
          {activeTab === 'raw' && (
            <div>
              <pre className="bg-gray-900 text-gray-100 rounded-lg p-6 overflow-auto text-sm">
                {JSON.stringify(architecture, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ArchitectureView;
