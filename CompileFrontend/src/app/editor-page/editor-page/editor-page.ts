import { Component, ElementRef, ViewChild, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { NeonButtonComponent } from '../../components/neon-button.component/neon-button.component';
import { PidginAnalyzer, AnalysisError } from '../../services/pidgin-analyzer';

@Component({
  selector: 'app-editor-page',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, NeonButtonComponent],
  templateUrl: './editor-page.html',
  styleUrls: ['./editor-page.css']
})
export class EditorPageComponent implements OnDestroy {
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;
  @ViewChild('highlightLayer') highlightLayer!: ElementRef<HTMLDivElement>;

  editorText = '';
  errors: AnalysisError[] = [];

  private debounceTimer: any = null;

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
          console.log('Errors received:', this.errors); // so you can see it working
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