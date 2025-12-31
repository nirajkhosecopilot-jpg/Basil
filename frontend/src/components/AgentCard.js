import React, { useState } from 'react';

function AgentCard({ agent }) {
  const [expanded, setExpanded] = useState(false);

  const tierColors = {
    flagship: 'bg-purple-100 text-purple-800',
    advanced: 'bg-blue-100 text-blue-800',
    efficient: 'bg-green-100 text-green-800',
    specialized: 'bg-orange-100 text-orange-800'
  };

  const typeIcons = {
    coordinator: '👑',
    specialist: '🎯',
    executor: '⚙️',
    analyzer: '🔍',
    validator: '✅'
  };

  return (
    <div className={`agent-card agent-${agent.type} bg-white border border-gray-200 rounded-lg p-5 hover:shadow-lg transition-all`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <span className="text-2xl">{typeIcons[agent.type] || '🤖'}</span>
            <h4 className="font-bold text-gray-900">{agent.name}</h4>
          </div>
          <p className="text-sm text-gray-600">{agent.description}</p>
        </div>

        <button
          onClick={() => setExpanded(!expanded)}
          className="ml-2 text-gray-400 hover:text-gray-600 transition-colors"
        >
          {expanded ? '▼' : '▶'}
        </button>
      </div>

      {/* LLM Info */}
      <div className="flex items-center justify-between mb-3 pb-3 border-b border-gray-100">
        <div>
          <p className="text-xs text-gray-500 mb-1">LLM Model</p>
          <p className="text-sm font-semibold text-gray-900">{agent.llm_model}</p>
        </div>
        <div>
          <span className={`text-xs px-2 py-1 rounded-full font-medium ${tierColors[agent.llm_tier]}`}>
            {agent.llm_tier}
          </span>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-3 gap-2 mb-3">
        <div className="text-center bg-gray-50 rounded p-2">
          <p className="text-xs text-gray-500">Cost/1K</p>
          <p className="text-sm font-bold text-gray-900">${agent.llm_cost_per_1k}</p>
        </div>
        <div className="text-center bg-gray-50 rounded p-2">
          <p className="text-xs text-gray-500">Reusability</p>
          <p className="text-sm font-bold text-gray-900">
            {(agent.reusability_score * 100).toFixed(0)}%
          </p>
        </div>
        <div className="text-center bg-gray-50 rounded p-2">
          <p className="text-xs text-gray-500">Deps</p>
          <p className="text-sm font-bold text-gray-900">{agent.dependencies.length}</p>
        </div>
      </div>

      {/* Expanded Details */}
      {expanded && (
        <div className="mt-4 pt-4 border-t border-gray-200 space-y-3">
          <div>
            <p className="text-xs font-semibold text-gray-700 mb-2">Capabilities</p>
            <div className="flex flex-wrap gap-1">
              {agent.capabilities.map((cap, i) => (
                <span
                  key={i}
                  className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded"
                >
                  {cap}
                </span>
              ))}
            </div>
          </div>

          {agent.dependencies.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-gray-700 mb-2">Dependencies</p>
              <div className="flex flex-wrap gap-1">
                {agent.dependencies.map((dep, i) => (
                  <span
                    key={i}
                    className="text-xs bg-purple-50 text-purple-700 px-2 py-1 rounded"
                  >
                    {dep}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div>
            <p className="text-xs font-semibold text-gray-700 mb-1">Provider</p>
            <p className="text-sm text-gray-600 capitalize">{agent.llm_provider}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default AgentCard;
