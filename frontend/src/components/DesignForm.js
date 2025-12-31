import React, { useState, useEffect } from 'react';
import axios from 'axios';

function DesignForm({ onDesign, loading, setLoading }) {
  const [formData, setFormData] = useState({
    problemStatement: '',
    preferProvider: '',
    costOptimize: false,
    maxAgents: '',
    complexityPreference: ''
  });

  const [availableModels, setAvailableModels] = useState([]);
  const [domains, setDomains] = useState([]);
  const [examples, setExamples] = useState([
    {
      name: 'E-commerce Platform',
      description: 'Build an e-commerce platform with user authentication, product catalog, shopping cart, payment processing, inventory management, and ML-based recommendations.'
    },
    {
      name: 'Customer Service System',
      description: 'Create a customer service platform with intent classification, FAQ answering, ticket creation, sentiment analysis, and automated email responses.'
    },
    {
      name: 'Data Processing Pipeline',
      description: 'Design a data processing pipeline with data ingestion from multiple sources, ETL transformations, data validation, machine learning inference, storage, and analytics dashboards.'
    }
  ]);

  useEffect(() => {
    // Fetch available models
    axios.get('/api/models')
      .then(response => {
        setAvailableModels(response.data);
      })
      .catch(error => console.error('Error fetching models:', error));

    // Fetch domains
    axios.get('/api/domains')
      .then(response => {
        setDomains(response.data.domains);
      })
      .catch(error => console.error('Error fetching domains:', error));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post('/api/design', {
        problem_statement: formData.problemStatement,
        prefer_provider: formData.preferProvider || null,
        cost_optimize: formData.costOptimize,
        max_agents: formData.maxAgents ? parseInt(formData.maxAgents) : null,
        complexity_preference: formData.complexityPreference || null
      });

      onDesign(response.data);
    } catch (error) {
      console.error('Error designing architecture:', error);
      alert('Failed to design architecture. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const loadExample = (example) => {
    setFormData({
      ...formData,
      problemStatement: example.description
    });
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Design Your Architecture
          </h2>
          <p className="text-gray-600">
            Describe your problem and let Basil design an optimal multi-agent architecture
          </p>
        </div>

        {/* Example Templates */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Quick Start Examples
          </label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {examples.map((example, index) => (
              <button
                key={index}
                onClick={() => loadExample(example)}
                className="text-left p-4 border border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all"
              >
                <p className="font-semibold text-sm text-gray-900">{example.name}</p>
                <p className="text-xs text-gray-500 mt-1 line-clamp-2">{example.description}</p>
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Problem Statement */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Problem Statement *
            </label>
            <textarea
              value={formData.problemStatement}
              onChange={(e) => setFormData({ ...formData, problemStatement: e.target.value })}
              required
              rows={8}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Describe your application requirements in detail. Include features, integrations, scale requirements, and any specific constraints..."
            />
            <p className="mt-2 text-sm text-gray-500">
              Be specific about features, integrations (e.g., Stripe, AWS), and requirements for best results
            </p>
          </div>

          {/* Optimization Options */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* LLM Provider Preference */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                LLM Provider Preference
              </label>
              <select
                value={formData.preferProvider}
                onChange={(e) => setFormData({ ...formData, preferProvider: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Auto (Basil chooses)</option>
                <option value="openai">OpenAI (GPT models)</option>
                <option value="anthropic">Anthropic (Claude models)</option>
              </select>
            </div>

            {/* Max Agents */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Agents (Optional)
              </label>
              <input
                type="number"
                value={formData.maxAgents}
                onChange={(e) => setFormData({ ...formData, maxAgents: e.target.value })}
                min="1"
                max="20"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                placeholder="Auto"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Complexity Preference */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Complexity Preference
              </label>
              <select
                value={formData.complexityPreference}
                onChange={(e) => setFormData({ ...formData, complexityPreference: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Auto</option>
                <option value="low">Low - Simpler agents</option>
                <option value="medium">Medium - Balanced</option>
                <option value="high">High - Advanced agents</option>
              </select>
            </div>

            {/* Cost Optimization */}
            <div className="flex items-center pt-8">
              <input
                type="checkbox"
                id="costOptimize"
                checked={formData.costOptimize}
                onChange={(e) => setFormData({ ...formData, costOptimize: e.target.checked })}
                className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
              <label htmlFor="costOptimize" className="ml-3 text-sm font-medium text-gray-700">
                Optimize for Cost
                <span className="block text-xs text-gray-500 font-normal">
                  Use cheaper models when possible
                </span>
              </label>
            </div>
          </div>

          {/* Info Box */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="text-sm font-semibold text-blue-900 mb-2">💡 Tips for Better Results</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Include specific features and integrations</li>
              <li>• Mention scale requirements (users, requests)</li>
              <li>• Specify critical requirements (security, compliance)</li>
              <li>• List all main functionalities</li>
            </ul>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading || !formData.problemStatement.trim()}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl"
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Designing Architecture...
              </span>
            ) : (
              '🚀 Design Architecture'
            )}
          </button>
        </form>
      </div>

      {/* Supported Domains */}
      {domains.length > 0 && (
        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Supported Domains</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {domains.map((domain) => (
              <div
                key={domain.id}
                className="text-sm text-gray-700 bg-gray-50 rounded px-3 py-2"
                title={domain.keywords.join(', ')}
              >
                {domain.name}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default DesignForm;
