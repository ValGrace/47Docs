'use server';

import {
  translatePdfContent,
  type TranslatePdfContentInput,
} from '@/ai/flows/translate-pdf-content';

export async function handleTranslation(input: TranslatePdfContentInput) {
  try {
    const result = await translatePdfContent(input);
    return { success: true, data: result };
  } catch (error) {
    console.error('Translation failed:', error);
    const errorMessage =
      error instanceof Error
        ? error.message
        : 'An unknown error occurred during translation.';
    return { success: false, error: errorMessage };
  }
}
