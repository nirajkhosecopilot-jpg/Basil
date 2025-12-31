import React from 'react';

function CostEstimates({ agents, costEstimates }) {
  const scales = [
    { key: '10k_requests', label: '10K requests/month', requests: 10000 },
    { key: '100k_requests', label: '100K requests/month', requests: 100000 },
    { key: '1m_requests', label: '1M requests/month', requests: 1000000 }
  ];

  const agentsByTier = agents.reduce((acc, agent) => {
    if (!acc[agent.llm_tier]) acc[agent.llm_tier] = [];
    acc[agent.llm_tier].push(agent);
    return acc;
  }, {});

  const tierCosts = {};
  Object.entries(agentsByTier).forEach(([tier, tierAgents]) => {
    tierCosts[tier] = tierAgents.reduce((sum, agent) => sum + agent.llm_cost_per_1k, 0);
  });

  return (
    <div className="space-y-6">
      {/* Cost Estimates by Scale */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Cost Estimates</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {scales.map(scale => (
            <div
              key={scale.key}
              className="bg-gradient-to-br from-green-50 to-emerald-100 rounded-lg p-6 border border-green-200"
            >
              <p className="text-sm text-green-700 font-medium mb-2">{scale.label}</p>
              <p className="text-4xl font-bold text-green-900 mb-2">
                ${costEstimates[scale.key].toFixed(2)}
              </p>
              <p className="text-xs text-green-600">
                ~{scale.requests.toLocaleString()} API calls
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Cost Breakdown by Agent */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Cost Breakdown by Agent</h3>
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Agent
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Model
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tier
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Cost/1K Tokens
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Est. Monthly (10K req)
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {agents.map(agent => (
                <tr key={agent.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{agent.name}</div>
                    <div className="text-xs text-gray-500">{agent.type}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    {agent.llm_model}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full
                      ${agent.llm_tier === 'flagship' ? 'bg-purple-100 text-purple-800' : ''}
                      ${agent.llm_tier === 'advanced' ? 'bg-blue-100 text-blue-800' : ''}
                      ${agent.llm_tier === 'efficient' ? 'bg-green-100 text-green-800' : ''}
                    `}>
                      {agent.llm_tier}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 font-mono">
                    ${agent.llm_cost_per_1k.toFixed(4)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 font-bold">
                    ${(10000 * 1000 * agent.llm_cost_per_1k / 1000).toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
            <tfoot className="bg-gray-100">
              <tr>
                <td colSpan="4" className="px-6 py-3 text-sm font-semibold text-gray-900 text-right">
                  Total Estimated Cost (10K req/month):
                </td>
                <td className="px-6 py-3 text-sm font-bold text-gray-900 text-right">
                  ${costEstimates['10k_requests'].toFixed(2)}
                </td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

      {/* Cost Breakdown by Tier */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Cost Distribution by LLM Tier</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(agentsByTier).map(([tier, tierAgents]) => (
            <div
              key={tier}
              className="bg-white border border-gray-200 rounded-lg p-4"
            >
              <p className="text-sm font-semibold text-gray-700 capitalize mb-2">{tier}</p>
              <p className="text-2xl font-bold text-gray-900 mb-1">
                {tierAgents.length} agents
              </p>
              <p className="text-xs text-gray-500">
                Avg cost: ${(tierCosts[tier] / tierAgents.length).toFixed(4)}/1K
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Cost Optimization Tips */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <h4 className="text-sm font-semibold text-yellow-900 mb-3">💡 Cost Optimization Tips</h4>
        <ul className="space-y-2 text-sm text-yellow-800">
          <li>• Consider using cost optimization mode to reduce flagship model usage</li>
          <li>• Efficient models (GPT-3.5, Claude Haiku) are 10-30x cheaper than flagship models</li>
          <li>• Use caching and batching to reduce total API calls</li>
          <li>• Monitor actual usage to refine estimates</li>
        </ul>
      </div>
    </div>
  );
}

export default CostEstimates;
