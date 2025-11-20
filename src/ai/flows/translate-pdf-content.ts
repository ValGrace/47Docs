'use server';

/**
 * @fileOverview This file defines a Genkit flow for translating the text content of a PDF document into a specified Kenyan language (Luo, Kikuyu, Luhya, or Kisii).
 *
 * - translatePdfContent - The main function to initiate the PDF content translation.
 * - TranslatePdfContentInput - Interface for the input parameters required for translation.
 * - TranslatePdfContentOutput - Interface for the output containing the translated PDF content.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const TranslatePdfContentInputSchema = z.object({
  pdfDataUri: z
    .string()
    .describe(
      'The PDF document as a data URI that must include a MIME type and use Base64 encoding. Expected format: \'data:<mimetype>;base64,<encoded_data>\'.' 
    ),
  targetLanguage: z
    .enum(['Luo', 'Kikuyu', 'Luhya', 'Kisii'])
    .describe('The target Kenyan language for translation (Luo, Kikuyu, Luhya, or Kisii).'),
});

export type TranslatePdfContentInput = z.infer<typeof TranslatePdfContentInputSchema>;

const TranslatePdfContentOutputSchema = z.object({
  translatedPdfDataUri: z
    .string()
    .describe(
      'The translated PDF document as a data URI that must include a MIME type and use Base64 encoding.'
    ),
});

export type TranslatePdfContentOutput = z.infer<typeof TranslatePdfContentOutputSchema>;

/**
 * Initiates the translation of the PDF content into the specified Kenyan language.
 * @param input - The input parameters including the PDF data URI and the target language.
 * @returns A promise resolving to the translated PDF content as a data URI.
 */
export async function translatePdfContent(
  input: TranslatePdfContentInput
): Promise<TranslatePdfContentOutput> {
  return translatePdfContentFlow(input);
}

const translatePdfContentPrompt = ai.definePrompt({
  name: 'translatePdfContentPrompt',
  input: {schema: TranslatePdfContentInputSchema},
  output: {schema: TranslatePdfContentOutputSchema},
  prompt: `You are a proficient translator specializing in Kenyan languages. Translate the text content of the following PDF document into the specified target language, preserving the original document structure and formatting as much as possible.

Target Language: {{{targetLanguage}}}
PDF Content: {{media url=pdfDataUri}}

Ensure that the translated PDF content maintains the layout, fonts, and overall structure of the original document.

Return the translated PDF as a data URI.
`,
});

const translatePdfContentFlow = ai.defineFlow(
  {
    name: 'translatePdfContentFlow',
    inputSchema: TranslatePdfContentInputSchema,
    outputSchema: TranslatePdfContentOutputSchema,
  },
  async input => {
    const {output} = await translatePdfContentPrompt(input);
    return output!;
  }
);
