/**
 * Palmer AI Design System - Color Tokens
 * Inspired by Steve Jobs' philosophy: "Simplicity is the ultimate sophistication"
 * Following Linear's sophisticated dark theme approach
 */

export const colors = {
  // Base surfaces (Progressive lightening for elevation)
  base: '#0a0a0a',
  surface: '#121212', 
  elevated: '#1a1a1a',
  panel: '#1f1f1f',
  overlay: '#252525',
  
  // Borders and dividers
  border: '#2a2a2a',
  borderMuted: '#1f1f1f',
  borderSubtle: '#171717',
  
  // Text hierarchy (WCAG compliant opacity layers)
  textPrimary: '#ffffff',
  textSecondary: 'rgba(255, 255, 255, 0.87)',
  textMuted: 'rgba(255, 255, 255, 0.60)',
  textDisabled: 'rgba(255, 255, 255, 0.38)',
  textInverse: '#000000',
  
  // Palmer brand colors (Carefully chosen for dark themes)
  primary: {
    50: '#ecfdf5',
    100: '#d1fae5',
    200: '#a7f3d0',
    300: '#6ee7b7',
    400: '#34d399',
    500: '#10b981', // Main brand color
    600: '#059669',
    700: '#047857',
    800: '#065f46',
    900: '#064e3b',
  },
  
  secondary: {
    50: '#eef2ff',
    100: '#e0e7ff',
    200: '#c7d2fe',
    300: '#a5b4fc',
    400: '#818cf8',
    500: '#6366f1', // Secondary brand
    600: '#4f46e5',
    700: '#4338ca',
    800: '#3730a3',
    900: '#312e81',
  },
  
  accent: {
    50: '#fffbeb',
    100: '#fef3c7',
    200: '#fde68a',
    300: '#fcd34d',
    400: '#fbbf24',
    500: '#f59e0b', // Accent color
    600: '#d97706',
    700: '#b45309',
    800: '#92400e',
    900: '#78350f',
  },
  
  // Semantic colors (Optimized for dark backgrounds)
  success: '#22c55e',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',
  
  // Component-specific colors
  input: {
    background: '#171717',
    border: '#2a2a2a',
    focus: '#10b981',
    placeholder: 'rgba(255, 255, 255, 0.38)',
  },
  
  button: {
    primary: '#10b981',
    primaryHover: '#059669',
    secondary: '#1a1a1a',
    secondaryHover: '#252525',
  }
} as const;

export type ColorToken = keyof typeof colors;
