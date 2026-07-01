import React, { useState } from 'react';

export default function CandidateDashboard() {
  const [loading, setLoading] = useState(false);
  const [candidates, setCandidates] = useState([]);
  const [stats, setStats] = useState({ total: 0, message: "" });
  const [error, setError] = useState(null);

  // Trigger the Semantic AI Engine Execution
  const handleEvaluate = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('https://candidate-discovery-engine.onrender.com/evaluate-static', {
        method: 'POST',
        headers: { 'Accept': 'application/json' }
      });
      
      if (!response.ok) throw new Error('Failed to run ranking pipeline.');
      
      const data = await response.json();
      setCandidates(data.top_10_preview || []);
      setStats({
        total: data.total_candidates_evaluated,
        message: data.message
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Direct Deliverable Download Trigger
  const handleDownload = () => {
    window.open('https://candidate-discovery-engine.onrender.com/download-deliverable', '_blank');
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans">
      {/* Navbar Banner Layout */}
      <nav className="bg-indigo-600 text-white p-4 shadow-md flex justify-between items-center">
        <h1 className="text-xl font-bold tracking-tight">👥 AI Candidate Discovery Portal</h1>
        <div className="space-x-3">
          <button 
  onClick={handleEvaluate} 
  className="bg-blue-600 text-white px-4 py-2 rounded mr-4" // ◄ Added mr-4 here
>
  Run Discovery Engine
</button>

<button 
  onClick={handleDownload} 
  className="bg-green-600 text-white px-4 py-2 rounded"
>
  📥 Download Excel Deliverable
</button>
          )}
        </div>
      </nav>

      {/* Main Screen Layout Container */}
      <main className="max-w-7xl mx-auto p-6">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
            <strong>Execution Error:</strong> {error}
          </div>
        )}

        {candidates.length === 0 && !loading ? (
          <div className="text-center py-20 bg-white border-2 border-dashed border-gray-300 rounded-2xl">
            <h3 className="text-lg font-medium text-gray-600">No Evaluations Executed Yet</h3>
            <p className="text-gray-400 mt-1 text-sm">Click the execution trigger at the top right to parse files.</p>
          </div>
        ) : loading ? (
          <div className="text-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
            <p className="text-gray-500 mt-4 font-medium animate-pulse">Computing dense contextual vectors & sorting database...</p>
          </div>
        ) : (
          <div>
            {/* Real-time HR Statistics Metrics */}
            <div className="mb-4 text-sm text-gray-500 bg-indigo-50 p-3 rounded-lg border border-indigo-100">
              📊 <strong>System Status:</strong> {stats.message} Evaluated <strong>{stats.total}</strong> active target schema records.
            </div>

            {/* Structured Leaderboard Data Table */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-gray-100 text-gray-600 text-xs font-semibold uppercase tracking-wider border-b border-gray-200">
                    <th className="px-6 py-4">Rank</th>
                    <th className="px-6 py-4">Candidate ID</th>
                    <th className="px-6 py-4">Anonymized Name</th>
                    <th className="px-6 py-4">AI Semantic Match</th>
                    <th className="px-6 py-4">Extracted Experience</th>
                    <th className="px-6 py-4">Composite Score</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 text-sm">
                  {candidates.map((c) => (
                    <tr key={c.rank} className="hover:bg-gray-50 transition duration-150">
                      <td className="px-6 py-4 font-bold text-indigo-600">#{c.rank}</td>
                      <td className="px-6 py-4 font-mono text-xs text-gray-500">{c.candidate_id}</td>
                      <td className="px-6 py-4 font-semibold text-gray-900">{c.name}</td>
                      <td className="px-6 py-4">{(c.semantic_score * 100).toFixed(1)}%</td>
                      <td className="px-6 py-4 text-gray-600">{c.extracted_exp_years} Years</td>
                      <td className="px-6 py-4">
                        <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-800">
                          {c.composite_match_score.toFixed(4)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}