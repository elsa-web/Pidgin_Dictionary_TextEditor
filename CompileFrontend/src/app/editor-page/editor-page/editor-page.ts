import { Component, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { NeonButtonComponent } from '../../components/neon-button.component/neon-button.component';
import { FontSelectorComponent, TextFormat } from '../../components/font-selector/font-selector';

@Component({
  selector: 'app-editor-page',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, NeonButtonComponent, FontSelectorComponent],
  templateUrl: './editor-page.html',
  styleUrls: ['./editor-page.css']
})
export class EditorPageComponent {
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  editorText = '';

  // Applied formatting state
  editorStyle: { [key: string]: string } = {
    fontFamily: "'Segoe UI', system-ui, sans-serif",
    fontSize: '14px',
    fontWeight: 'normal',
    fontStyle: 'normal',
    textDecoration: 'none',
    textAlign: 'left',
  };

  get wordCount(): number {
    return this.editorText.trim() ? this.editorText.trim().split(/\s+/).length : 0;
  }

  get charCount(): number {
    return this.editorText.length;
  }

  // ── Upload ──
  triggerUpload() {
    this.fileInput.nativeElement.click();
  }

  onFileSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => { this.editorText = e.target?.result as string; };
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

  // ── Format ──
  onFontChanged(format: TextFormat) {
    this.editorStyle = {
      fontFamily: format.fontFamily,
      fontSize: format.fontSize + 'px',
      fontWeight: format.bold ? 'bold' : 'normal',
      fontStyle: format.italic ? 'italic' : 'normal',
      textDecoration: [
        format.underline     ? 'underline'    : '',
        format.strikethrough ? 'line-through' : ''
      ].filter(Boolean).join(' ') || 'none',
      textAlign: format.alignment,
    };
  }
}