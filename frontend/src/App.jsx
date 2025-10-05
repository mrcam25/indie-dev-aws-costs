import { useState } from 'react';

// Hardcoded project templates with cost breakdowns
const projectTemplates = [
  {
    id: 1,
    name: "Static Portfolio Website",
    description: "HTML/CSS/JS site with global CDN delivery",
    totalCost: 1.5,
    components: [
      { service: "S3", description: "Storage (5GB)", cost: 0.12 },
      { service: "CloudFront", description: "CDN (100GB transfer)", cost: 0.85 },
      { service: "Route53", description: "DNS hosting", cost: 0.50 }
    ],
    estimatedTraffic: "~50K visitors/month",
    complexity: "Beginner"
  },
  {
    id: 2,
    name: "Serverless REST API",
    description: "API with database for small apps",
    totalCost: 4.5,
    components: [
      { service: "Lambda", description: "100K requests, 128MB, 200ms avg", cost: 2.00 },
      { service: "API Gateway", description: "100K requests", cost: 1.00 },
      { service: "DynamoDB", description: "1GB storage, 100K reads/writes", cost: 1.25 },
      { service: "CloudWatch", description: "Basic logs", cost: 0.25 }
    ],
    estimatedTraffic: "~100K API calls/month",
    complexity: "Intermediate"
  },
  {
    id: 3,
    name: "Scheduled Data Scraper",
    description: "Run tasks on a schedule, store results",
    totalCost: 2.0,
    components: [
      { service: "Lambda", description: "Daily runs, 5 min each", cost: 0.50 },
      { service: "EventBridge", description: "Scheduled triggers", cost: 0.00 },
      { service: "S3", description: "Results storage (10GB)", cost: 0.25 },
      { service: "DynamoDB", description: "Metadata storage", cost: 1.25 }
    ],
    estimatedTraffic: "Daily automated tasks",
    complexity: "Intermediate"
  },
  {
    id: 4,
    name: "Small Full-Stack App",
    description: "Always-on server with database",
    totalCost: 9.5,
    components: [
      { service: "EC2", description: "t4g.nano (ARM, 2 vCPU, 0.5GB RAM)", cost: 3.07 },
      { service: "RDS", description: "t4g.micro MySQL (1 vCPU, 1GB RAM)", cost: 5.84 },
      { service: "EBS", description: "20GB SSD storage", cost: 0.40 },
      { service: "Data Transfer", description: "10GB outbound", cost: 0.19 }
    ],
    estimatedTraffic: "~10K users/month",
    complexity: "Advanced"
  },
  {
    id: 5,
    name: "Image Processing Service",
    description: "Upload images, auto-resize/optimize",
    totalCost: 3.5,
    components: [
      { service: "Lambda", description: "50K invocations, 512MB, 2s avg", cost: 2.00 },
      { service: "S3", description: "Input/output storage (20GB)", cost: 0.50 },
      { service: "S3", description: "100K PUT/GET requests", cost: 0.50 },
      { service: "CloudWatch", description: "Logs", cost: 0.50 }
    ],
    estimatedTraffic: "~50K images/month",
    complexity: "Intermediate"
  },
  {
    id: 6,
    name: "Discord/Slack Bot",
    description: "Serverless bot responding to commands",
    totalCost: 1.0,
    components: [
      { service: "Lambda", description: "20K invocations, 128MB, 100ms", cost: 0.40 },
      { service: "API Gateway", description: "Webhook endpoint", cost: 0.20 },
      { service: "DynamoDB", description: "Bot state/config", cost: 0.40 }
    ],
    estimatedTraffic: "~20K bot commands/month",
    complexity: "Beginner"
  }
];

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
            ${project.totalCost.toFixed(2)}
          </div>
          <div className="text-xs text-gray-500">per month</div>
        </div>
      </div>

      <div className="flex items-center justify-between text-sm text-gray-600 mb-3">
        <span>📊 {project.estimatedTraffic}</span>
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
            <span className="font-mono">${project.totalCost.toFixed(2)}</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default function BudgetCalculator() {
  const [budget, setBudget] = useState(10);
  const affordableProjects = projectTemplates.filter(p => p.totalCost <= budget);
  const tooExpensive = projectTemplates.filter(p => p.totalCost > budget);

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
              ${affordableProjects.length > 0 ? Math.min(...affordableProjects.map(p => p.totalCost)).toFixed(2) : '0.00'}
            </div>
            <div className="text-sm text-gray-600">Cheapest Option</div>
          </div>
          <div className="bg-white rounded-lg shadow p-4 text-center">
            <div className="text-2xl font-bold text-purple-600">
              ${affordableProjects.length > 0 ? (budget - Math.max(...affordableProjects.map(p => p.totalCost))).toFixed(2) : budget.toFixed(2)}
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
        </div>
      </div>
    </div>
  );
}