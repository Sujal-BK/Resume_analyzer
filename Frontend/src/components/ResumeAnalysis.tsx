import type { ResumeResponse } from '../types/resume';

interface ResumeAnalysisProps {
  data: ResumeResponse;
}

export default function ResumeAnalysis({ data }: ResumeAnalysisProps) {
  const { analysis, filename, file_type } = data;

  return (
    <div className="analysis-container">
      <div className="analysis-header">
        <h2>Resume Analysis</h2>
        <div className="file-info">
          <span className="filename">{filename}</span>
          <span className="file-type">{file_type.toUpperCase()}</span>
        </div>
      </div>

      <div className="score-card">
        <div className="overall-score">
          <h3>Overall Score</h3>
          <div className="score-circle">
            <span className="score-value">{analysis.overall_score}</span>
            <span className="score-max">/10</span>
          </div>
        </div>
        <div className="ats-score">
          <h3>ATS Compatibility</h3>
          <div className="score-circle">
            <span className="score-value">{analysis.ats_compatibility.score}</span>
            <span className="score-max">/10</span>
          </div>
        </div>
      </div>

      <div className="summary-section">
        <h3>Summary</h3>
        <p>{analysis.summary}</p>
      </div>

      <div className="two-column">
        <div className="section strengths">
          <h3>Strengths</h3>
          <ul>
            {analysis.strengths.map((strength, index) => (
              <li key={index}>{strength}</li>
            ))}
          </ul>
        </div>

        <div className="section weaknesses">
          <h3>Weaknesses</h3>
          <ul>
            {analysis.weaknesses.map((weakness, index) => (
              <li key={index}>{weakness}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="section suggestions">
        <h3>Suggestions for Improvement</h3>
        {analysis.suggestions.map((suggestion, index) => (
          <div key={index} className="suggestion-item">
            <span className="suggestion-category">{suggestion.category}</span>
            <p>{suggestion.suggestion}</p>
          </div>
        ))}
      </div>

      {analysis.ats_compatibility.issues.length > 0 && (
        <div className="section ats-issues">
          <h3>ATS Compatibility Issues</h3>
          <ul>
            {analysis.ats_compatibility.issues.map((issue, index) => (
              <li key={index}>{issue}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="section keywords">
        <h3>Keywords Found</h3>
        <div className="keyword-tags">
          {analysis.keywords_found.map((keyword, index) => (
            <span key={index} className="keyword-tag found">{keyword}</span>
          ))}
        </div>
      </div>

      {analysis.missing_sections.length > 0 && (
        <div className="section missing-sections">
          <h3>Missing Sections</h3>
          <div className="keyword-tags">
            {analysis.missing_sections.map((section, index) => (
              <span key={index} className="keyword-tag missing">{section}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
