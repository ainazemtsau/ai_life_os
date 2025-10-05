import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge Tailwind CSS classes with proper precedence.
 *
 * Combines clsx for conditional class names with tailwind-merge
 * to handle Tailwind class conflicts correctly.
 *
 * @param inputs - Class names, conditionals, arrays, or objects
 * @returns Merged class string
 *
 * @example
 * cn('text-sm', 'text-lg') // => 'text-lg' (later wins)
 * cn('p-4', isActive && 'bg-blue-500') // conditional
 * cn(['text-sm', 'font-bold'], { 'text-red-500': hasError })
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
