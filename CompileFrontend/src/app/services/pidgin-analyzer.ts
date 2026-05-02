import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// 👇 ADD these interfaces
export interface AnalysisError {
  type: 'SPELLING' | 'SYNTAX' | 'SEMANTIC' | 'UNKNOWN';
  word: string;
  start: number;
  end: number;
  message: string;
  suggestion: string;
  all_suggestions: string[];
}

export interface AnalysisResult {
  sentence: string;
  tokens: any[];
  errors: AnalysisError[];
  summary: {
    total_tokens: number;
    total_errors: number;
    error_types: string[];
    status: string;
  };
}

@Injectable({
  providedIn: 'root',
})
export class PidginAnalyzer {

 
  private readonly apiUrl = 'http://localhost:8000/api/lexer/analyze';

 
  constructor(private http: HttpClient) {}

 
  analyze(sentence: string): Observable<AnalysisResult> {
    return this.http.post<AnalysisResult>(this.apiUrl, { sentence });
  }
}
