import { useState } from 'react';
import FileUpload from './components/FileUpload';
import ResumeAnalysis from './components/ResumeAnalysis';
import type { ResumeResponse } from './types/resume';

function App() {
  const [resumeData, setResumeData] = useState<ResumeResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (file: File) => {
    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/v1/resume/parse`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server error: ${response.status}`);
      }

      const data: ResumeResponse = await response.json();
      setResumeData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Resume Parser & Analyzer</h1>
        <p>Upload your resume to get instant feedback and suggestions</p>
      </header>

      <main className="app-main">
        {!resumeData && (
          <FileUpload onUpload={handleFileUpload} isLoading={isLoading} />
        )}

        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
          </div>
        )}

        {resumeData && (
          <>
            <ResumeAnalysis data={resumeData} />
            <button 
              className="reset-button" 
              onClick={() => setResumeData(null)}
            >
              Analyze Another Resume
            </button>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
