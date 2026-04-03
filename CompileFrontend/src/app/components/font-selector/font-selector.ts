import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

export interface FontOption {
  label: string;
  value: string;
}

export interface TextFormat {
  fontFamily: string;
  fontSize: string;
  bold: boolean;
  italic: boolean;
  underline: boolean;
  strikethrough: boolean;
  alignment: 'left' | 'center' | 'right' | 'justify';
}

@Component({
  selector: 'app-font-selector',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './font-selector.html',
  styleUrls: ['./font-selector.css']
})
export class FontSelectorComponent {
  @Output() formatChanged = new EventEmitter<TextFormat>();
  // Keep backward compat
  @Output() fontChanged = new EventEmitter<string>();

  isFontOpen = false;
  isSizeOpen = false;

  fonts: FontOption[] = [
    { label: 'Segoe UI',      value: "'Segoe UI', system-ui, sans-serif" },
    { label: 'Georgia',       value: "Georgia, 'Times New Roman', serif" },
    { label: 'Courier New',   value: "'Courier New', Courier, monospace" },
    { label: 'Arial',         value: "Arial, Helvetica, sans-serif" },
    { label: 'Trebuchet MS',  value: "'Trebuchet MS', sans-serif" },
    { label: 'Verdana',       value: "Verdana, Geneva, sans-serif" },
    { label: 'Palatino',      value: "'Palatino Linotype', Palatino, serif" },
    { label: 'Impact',        value: "Impact, Charcoal, sans-serif" },
    { label: 'Tahoma',        value: "Tahoma, Geneva, sans-serif" },
    { label: 'Arial Black',   value: "'Arial Black', Gadget, sans-serif" },
  ];

  fontSizes = ['8', '9', '10', '11', '12', '14', '16', '18', '20', '22', '24', '28', '32', '36', '48', '72'];

  format: TextFormat = {
    fontFamily: "'Segoe UI', system-ui, sans-serif",
    fontSize: '14',
    bold: false,
    italic: false,
    underline: false,
    strikethrough: false,
    alignment: 'left'
  };

  get selectedFont(): FontOption {
    return this.fonts.find(f => f.value === this.format.fontFamily) || this.fonts[0];
  }

  toggleFontDropdown() {
    this.isFontOpen = !this.isFontOpen;
    this.isSizeOpen = false;
  }

  toggleSizeDropdown() {
    this.isSizeOpen = !this.isSizeOpen;
    this.isFontOpen = false;
  }

  selectFont(font: FontOption) {
    this.format.fontFamily = font.value;
    this.isFontOpen = false;
    this.emit();
  }

  selectSize(size: string) {
    this.format.fontSize = size;
    this.isSizeOpen = false;
    this.emit();
  }

  toggleBold()          { this.format.bold          = !this.format.bold;          this.emit(); }
  toggleItalic()        { this.format.italic        = !this.format.italic;        this.emit(); }
  toggleUnderline()     { this.format.underline     = !this.format.underline;     this.emit(); }
  toggleStrikethrough() { this.format.strikethrough = !this.format.strikethrough; this.emit(); }

  setAlignment(align: 'left' | 'center' | 'right' | 'justify') {
    this.format.alignment = align;
    this.emit();
  }

  closeAll() {
    this.isFontOpen = false;
    this.isSizeOpen = false;
  }

  private emit() {
    this.formatChanged.emit({ ...this.format });
    this.fontChanged.emit(this.format.fontFamily);
  }
}