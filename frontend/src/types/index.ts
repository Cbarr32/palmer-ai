export interface AnalysisResult {
  company_name?: string;
  claude_analysis?: string;
  mpb_score?: number;
  journey_stage?: string;
  encouragement?: string;
  mia_blessing?: string;
  business_insights?: {
    industry: string;
    website_quality: string;
    description_quality: string;
  };
  error?: string;
  status?: string;
  version?: string;
  claude_powered?: boolean;
}

export interface CompanyData {
  name: string;
  website?: string;
  industry?: string;
  description?: string;
  size?: string;
}
