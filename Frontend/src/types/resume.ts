export type ResumeMetadata = {
  title: string;
  author: string;
  subject: string;
  creator: string;
}

export type ResumePage = {
  page_number: number;
  text: string;
}

export type ResumeData = {
  total_pages: number;
  metadata: ResumeMetadata;
  pages: ResumePage[];
  full_text: string;
}

export type Suggestion = {
  category: string;
  suggestion: string;
}

export type ATSCompatibility = {
  score: number;
  issues: string[];
}

export type ResumeAnalysis = {
  overall_score: number;
  summary: string;
  strengths: string[];
  weaknesses: string[];
  suggestions: Suggestion[];
  missing_sections: string[];
  ats_compatibility: ATSCompatibility;
  keywords_found: string[];
  keywords_missing: string[];
}

export type ResumeResponse = {
  status: string;
  filename: string;
  file_type: string;
  data: ResumeData;
  analysis: ResumeAnalysis;
}
