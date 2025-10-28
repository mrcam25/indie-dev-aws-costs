import { useState, useEffect } from 'react';

// API configuration
const API_BASE_URL = 'http://127.0.0.1:8000';

function ProjectCard({ project, isAffordable }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={`border rounded-lg p-5 transition-all ${
      isAffordable 
        ? 'border-green-300 bg-green-50' 
        : 'border-gray-200 bg-gray-50 opacity-60'
    }`}>
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <h3 className="text-lg font-semibold text-gray-800">{project.name}</h3>
            <span className={`text-xs px-2 py-1 rounded ${
              project.complexity === 'Beginner' ? 'bg-green-100 text-green-700' :
              project.complexity === 'Intermediate' ? 'bg-yellow-100 text-yellow-700' :
              'bg-red-100 text-red-700'
            }`}>
              {project.complexity}
            </span>
          </div>
          <p className="text-sm text-gray-600">{project.description}</p>
        </div>
        <div className="text-right ml-4">
          <div className="text-2xl font-bold text-gray-800">
            ${project.total_cost.toFixed(2)}
          </div>
          <div className="text-xs text-gray-500">per month</div>
        </div>
      </div>

      <div className="flex items-center justify-between text-sm text-gray-600 mb-3">
        <span>📊 {project.estimated_traffic}</span>
        {isAffordable && <span className="text-green-600 font-medium">✓ Within Budget</span>}
        {!isAffordable && <span className="text-red-600 font-medium">✗ Over Budget</span>}
      </div>

      <button 
        onClick={() => setExpanded(!expanded)}
        className="text-sm text-blue-600 hover:text-blue-800 font-medium"
      >
        {expanded ? '▼ Hide' : '▶ Show'} cost breakdown
      </button>

      {expanded && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <div className="space-y-2">
            {project.components.map((component, idx) => (
              <div key={idx} className="flex justify-between text-sm">
                <div>
                  <span className="font-medium text-gray-700">{component.service}</span>
                  <span className="text-gray-500 ml-2">{component.description}</span>
                </div>
                <span className="text-gray-700 font-mono">${component.cost.toFixed(2)}</span>
              </div>
            ))}
          </div>
          <div className="mt-2 pt-2 border-t border-gray-300 flex justify-between font-semibold">
            <span>Total</span>
            <span className="font-mono">${project.total_cost.toFixed(2)}</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default function BudgetCalculator() {
  const [budget, setBudget] = useState(10);
  const [projectData, setProjectData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch projects from API whenever budget changes
  useEffect(() => {
    const fetchProjects = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await fetch(`${API_BASE_URL}/api/projects?budget=${budget}`);
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        setProjectData(data);
      } catch (err) {
        setError(err.message);
        console.error('Failed to fetch projects:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, [budget]); // Re-run when budget changes

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading projects...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="bg-white rounded-xl shadow-lg p-8 max-w-md">
          <div className="text-red-600 text-5xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Connection Error</h2>
          <p className="text-gray-600 mb-4">
            Could not connect to the backend API. Make sure your Python server is running:
          </p>
          <code className="block bg-gray-100 p-3 rounded text-sm mb-4">
            cd backend && uvicorn app.main:app --reload
          </code>
          <p className="text-sm text-gray-500">Error: {error}</p>
        </div>
      </div>
    );
  }

  const affordableProjects = projectData?.affordable_projects || [];
  const tooExpensive = projectData?.expensive_projects || [];
  const stats = projectData?.stats || {};

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            ☁️ AWS Budget Planner
          </h1>
          <p className="text-gray-600">
            Discover what you can build and deploy on AWS within your budget
          </p>
          <div className="mt-2 inline-flex items-center gap-2 bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            Connected to API
          </div>
        </div>

        {/* Budget Input */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Your Monthly Budget (USD)
          </label>
          <div className="flex items-center gap-4">
            <input
              type="range"
              min="1"
              max="50"
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
            />
            <div className="flex items-center gap-2">
              <span className="text-3xl font-bold text-blue-600">${budget}</span>
              <input
                type="number"
                min="1"
                max="1000"
                value={budget}
                onChange={(e) => setBudget(Number(e.target.value) || 1)}
                className="w-20 px-3 py-2 border border-gray-300 rounded-lg text-center"
              />
            </div>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-4 text-center">
            <div className="text-2xl font-bold text-green-600">{affordableProjects.length}</div>
            <div className="text-sm text-gray-600">Projects You Can Build</div>
          </div>
          <div className="bg-white rounded-lg shadow p-4 text-center">
            <div className="text-2xl font-bold text-blue-600">
              ${stats.cheapest?.toFixed(2) || '0.00'}
            </div>
            <div className="text-sm text-gray-600">Cheapest Option</div>
          </div>
          <div className="bg-white rounded-lg shadow p-4 text-center">
            <div className="text-2xl font-bold text-purple-600">
              ${stats.remaining_budget?.toFixed(2) || budget.toFixed(2)}
            </div>
            <div className="text-sm text-gray-600">Budget Remaining</div>
          </div>
        </div>

        {/* Affordable Projects */}
        {affordableProjects.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              ✅ Projects Within Your Budget
            </h2>
            <div className="space-y-4">
              {affordableProjects.map(project => (
                <ProjectCard key={project.id} project={project} isAffordable={true} />
              ))}
            </div>
          </div>
        )}

        {/* Too Expensive Projects */}
        {tooExpensive.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              💰 Increase Budget For These
            </h2>
            <div className="space-y-4">
              {tooExpensive.map(project => (
                <ProjectCard key={project.id} project={project} isAffordable={false} />
              ))}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-600">
          <p>💡 Costs are estimates based on typical usage patterns. Actual costs may vary.</p>
          <p className="mt-1">Prices based on US East (N. Virginia) region.</p>
          <p className="mt-2 text-xs text-gray-500">Data fetched from backend API in real-time</p>
        </div>
      </div>
    </div>
  );
}