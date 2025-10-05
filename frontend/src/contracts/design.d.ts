/**
 * Design System Public API Contract
 * Version: 0.1.0
 *
 * TypeScript type definitions for the frontend.design module.
 * Provides foundational UI components and utilities for consistent UX.
 */

import * as React from 'react';
import { VariantProps } from 'class-variance-authority';

/**
 * Button component variants and sizes
 */
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual variant */
  variant?: 'default' | 'destructive' | 'outline' | 'ghost' | 'link';

  /** Size variant */
  size?: 'default' | 'sm' | 'lg' | 'icon';

  /** Render as child component */
  asChild?: boolean;
}

export const Button: React.FC<ButtonProps>;

/**
 * Dialog (Modal) component
 */
export interface DialogProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  children: React.ReactNode;
}

export interface DialogTriggerProps {
  asChild?: boolean;
  children: React.ReactNode;
}

export interface DialogContentProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export interface DialogHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export interface DialogTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  children: React.ReactNode;
}

export interface DialogDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {
  children: React.ReactNode;
}

export const Dialog: React.FC<DialogProps>;
export const DialogTrigger: React.FC<DialogTriggerProps>;
export const DialogContent: React.FC<DialogContentProps>;
export const DialogHeader: React.FC<DialogHeaderProps>;
export const DialogTitle: React.FC<DialogTitleProps>;
export const DialogDescription: React.FC<DialogDescriptionProps>;

/**
 * Input component
 */
export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** Error state (applies error styling) */
  error?: boolean;
}

export const Input: React.ForwardRefExoticComponent<
  InputProps & React.RefAttributes<HTMLInputElement>
>;

/**
 * Label component
 */
export interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  children: React.ReactNode;
}

export const Label: React.FC<LabelProps>;

/**
 * Card component
 */
export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  children: React.ReactNode;
}

export interface CardDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {
  children: React.ReactNode;
}

export interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export const Card: React.FC<CardProps>;
export const CardHeader: React.FC<CardHeaderProps>;
export const CardTitle: React.FC<CardTitleProps>;
export const CardDescription: React.FC<CardDescriptionProps>;
export const CardContent: React.FC<CardContentProps>;

/**
 * Badge component
 */
export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Visual variant */
  variant?: 'default' | 'secondary' | 'destructive' | 'outline';
  children: React.ReactNode;
}

export const Badge: React.FC<BadgeProps>;

/**
 * Utility: Class name merger
 * Combines clsx and tailwind-merge for optimized class names
 */
export function cn(...inputs: (string | undefined | null | boolean)[]): string;
