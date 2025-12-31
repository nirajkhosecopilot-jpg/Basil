import React from 'react';

function ArchitectureGraph({ agents, communications }) {
  const typeColors = {
    coordinator: '#a855f7',
    specialist: '#3b82f6',
    executor: '#10b981',
    analyzer: '#f59e0b',
    validator: '#ef4444'
  };

  const typeIcons = {
    coordinator: '👑',
    specialist: '🎯',
    executor: '⚙️',
    analyzer: '🔍',
    validator: '✅'
  };

  // Group communications by from_agent
  const commsByAgent = communications.reduce((acc, comm) => {
    if (!acc[comm.from_agent]) acc[comm.from_agent] = [];
    acc[comm.from_agent].push(comm);
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Communication Flows</h3>
        <p className="text-sm text-gray-600 mb-6">
          This diagram shows how agents communicate with each other in the architecture.
        </p>
      </div>

      {/* Mermaid-style visualization */}
      <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg p-8 border border-gray-200">
        <div className="space-y-6">
          {/* Agents */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {agents.map(agent => (
              <div
                key={agent.id}
                className="bg-white rounded-lg p-4 shadow-sm border-l-4"
                style={{ borderLeftColor: typeColors[agent.type] }}
              >
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-xl">{typeIcons[agent.type]}</span>
                  <div>
                    <p className="font-semibold text-sm text-gray-900">{agent.name}</p>
                    <p className="text-xs text-gray-500 capitalize">{agent.type}</p>
                  </div>
                </div>
                <div className="mt-2 pt-2 border-t border-gray-100">
                  <p className="text-xs text-gray-600">
                    <span className="font-medium">Model:</span> {agent.llm_model.split('-')[0]}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* Communication Flows */}
          <div>
            <h4 className="font-semibold text-gray-900 mb-4">Message Flows</h4>
            <div className="space-y-3">
              {communications.slice(0, 12).map((comm, idx) => {
                const fromAgent = agents.find(a => a.id === comm.from_agent);
                const toAgent = agents.find(a => a.id === comm.to_agent);

                return (
                  <div
                    key={idx}
                    className="bg-white rounded-lg p-4 shadow-sm border border-gray-200 hover:border-blue-400 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3 flex-1">
                        <div className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium">
                          {fromAgent?.name || comm.from_agent}
                        </div>
                        <div className="flex-1 flex items-center">
                          <div className="flex-1 border-t-2 border-blue-300 border-dashed"></div>
                          <div className="px-2 text-xs text-blue-600 font-medium">
                            {comm.message_type}
                          </div>
                          <div className="flex-1 border-t-2 border-blue-300 border-dashed"></div>
                          <div className="text-blue-500 text-lg">→</div>
                        </div>
                        <div className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium">
                          {toAgent?.name || comm.to_agent}
                        </div>
                      </div>
                    </div>
                    <p className="text-xs text-gray-600 mt-2 ml-2">{comm.description}</p>
                  </div>
                );
              })}

              {communications.length > 12 && (
                <div className="text-center text-sm text-gray-500 py-2">
                  ... and {communications.length - 12} more communication flows
                </div>
              )}
            </div>
          </div>

          {/* Legend */}
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <p className="text-sm font-semibold text-gray-900 mb-3">Agent Types Legend</p>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              {Object.entries(typeColors).map(([type, color]) => (
                <div key={type} className="flex items-center space-x-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: color }}
                  ></div>
                  <span className="text-xs text-gray-700 capitalize">{type}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Mermaid Diagram Code */}
      <div>
        <h4 className="text-sm font-semibold text-gray-900 mb-3">Mermaid Diagram Code</h4>
        <div className="bg-gray-900 text-gray-100 rounded-lg p-4 overflow-auto">
          <pre className="text-xs">
{`graph TD
${agents.map(a => `    ${a.id}[${a.name}]`).join('\n')}

${communications.map(c => `    ${c.from_agent} -->|${c.message_type}| ${c.to_agent}`).join('\n')}`}
          </pre>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Copy this code to use in Mermaid-compatible tools or documentation
        </p>
      </div>
    </div>
  );
}

export default ArchitectureGraph;
