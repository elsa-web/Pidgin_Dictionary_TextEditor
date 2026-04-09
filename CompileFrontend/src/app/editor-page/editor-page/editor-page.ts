import { Component, ElementRef, ViewChild, OnDestroy, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { NeonButtonComponent } from '../../components/neon-button.component/neon-button.component';
import { PidginAnalyzer, AnalysisError } from '../../services/pidgin-analyzer';
// import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-editor-page',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, NeonButtonComponent],
  templateUrl: './editor-page.html',
  styleUrls: ['./editor-page.css']
})
export class EditorPageComponent implements OnDestroy, AfterViewInit{
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;
  @ViewChild('highlightLayer') highlightLayer!: ElementRef<HTMLDivElement>;

  ngAfterViewInit() {
  console.log('highlight layer ready:', this.highlightLayer);
  }

  editorText = '';
  errors: AnalysisError[] = [];

  private debounceTimer: any = null;
  // highlightHtml: SafeHtml = '';

constructor(private analyzer: PidginAnalyzer) {}
  ngOnDestroy() {
    if (this.debounceTimer) clearTimeout(this.debounceTimer);
  }

  get wordCount(): number {
    return this.editorText.trim() ? this.editorText.trim().split(/\s+/).length : 0;
  }

  get charCount(): number {
    return this.editorText.length;
  }

  // 👇 ADD this new method
renderHighlights() {
  if (!this.editorText) {
    if (this.highlightLayer) {
      this.highlightLayer.nativeElement.innerHTML = '';
    }
    return; 
  }


  const text = this.editorText;

  // Sort errors by start position
  const sorted = [...this.errors].sort((a, b) => a.start - b.start);

  let html = '';
  let cursor = 0;

  for (const error of sorted) {
    // Skip if this error overlaps with something already rendered
    if (error.start < cursor) continue;

    // Add plain text before this error
    html += this.escapeHtml(text.slice(cursor, error.start));

    // Add the underlined word
    const colorClass = error.type === 'SPELLING' ? 'underline-red'
                     : error.type === 'SYNTAX'   ? 'underline-blue'
                     : 'underline-green';

    html += `<span class="${colorClass}">${this.escapeHtml(text.slice(error.start, error.end))}</span>`;

    cursor = error.end;
  }

  // Add any remaining plain text
  html += this.escapeHtml(text.slice(cursor));

    console.log('Generated HTML:', html);
  if (this.highlightLayer) {
    this.highlightLayer.nativeElement.innerHTML = html;
}
}


escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>')
    .replace(/ /g, '&nbsp;');
}

  // ── Called on every keystroke ──
  onTextChange() {
    console.log('Text changed, scheduling analysis...');
    if (this.debounceTimer) clearTimeout(this.debounceTimer);

    if (!this.editorText.trim()) {
      this.errors = [];
      return;
    }

    this.debounceTimer = setTimeout(() => {
      this.analyzer.analyze(this.editorText).subscribe({
        next: (result) => {
        this.errors = result.errors;
        this.renderHighlights(); 
        console.log('Errors received:', this.errors);
},
        error: (err) => {
          console.error('Analysis failed:', err);
        }
      });
    }, 400);
  }

  // ── Upload ──
  triggerUpload() {
    this.fileInput.nativeElement.click();
  }

  onFileSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      this.editorText = e.target?.result as string;
      this.onTextChange();
    };
    reader.readAsText(file);
  }

  // ── Download ──
  downloadDocument() {
    if (!this.editorText.trim()) return;
    const blob = new Blob([this.editorText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'pidgincheck-document.txt';
    a.click();
    URL.revokeObjectURL(url);
  }
}