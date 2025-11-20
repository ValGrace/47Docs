"use client";

import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { handleTranslation } from './actions';
import { Upload, FileText, Languages, Loader2, Download, CheckCircle2 } from 'lucide-react';
import { Logo } from '@/components/logo';

type Language = 'Luo' | 'Kikuyu' | 'Luhya' | 'Kisii';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [fileDataUri, setFileDataUri] = useState<string | null>(null);
  const [language, setLanguage] = useState<Language | ''>('');
  const [isLoading, setIsLoading] = useState(false);
  const [translatedUri, setTranslatedUri] = useState<string | null>(null);
  const { toast } = useToast();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setTranslatedUri(null);
      const reader = new FileReader();
      reader.onload = (e) => {
        setFileDataUri(e.target?.result as string);
      };
      reader.readAsDataURL(selectedFile);
    } else {
      event.target.value = '';
      toast({
        variant: 'destructive',
        title: 'Invalid File Type',
        description: 'Please upload a PDF file.',
      });
      setFile(null);
      setFileDataUri(null);
    }
  };

  const onTranslate = async () => {
    if (!fileDataUri || !language) {
      toast({
        variant: 'destructive',
        title: 'Missing Information',
        description: 'Please upload a PDF and select a language.',
      });
      return;
    }

    setIsLoading(true);
    setTranslatedUri(null);

    const result = await handleTranslation({
      pdfDataUri: fileDataUri,
      targetLanguage: language,
    });

    setIsLoading(false);

    if (result.success && result.data) {
      setTranslatedUri(result.data.translatedPdfDataUri);
      toast({
        title: 'Translation Successful',
        description: 'Your document has been translated.',
      });
    } else {
      toast({
        variant: 'destructive',
        title: 'Translation Failed',
        description: result.error || 'An unexpected error occurred.',
      });
    }
  };

  const languages: Language[] = ['Luo', 'Kikuyu', 'Luhya', 'Kisii'];

  return (
    <div className="flex min-h-screen w-full flex-col items-center justify-center p-4 sm:p-6 md:p-8">
      <header className="mb-8 flex flex-col items-center text-center">
        <Logo className="h-16 w-16 mb-2 text-primary" />
        <h1 className="text-4xl font-bold font-headline text-foreground">47Docs</h1>
        <p className="mt-2 text-lg text-muted-foreground">Translate English PDFs to Kenyan Languages Instantly</p>
      </header>
      <Card className="w-full max-w-2xl shadow-lg border-border/50 bg-card">
        <CardHeader>
          <CardTitle className="text-2xl font-headline">PDF Translator</CardTitle>
          <CardDescription>Upload your document, choose a language, and get your translation.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-8">
          <div className="space-y-4">
            <Label htmlFor="pdf-upload" className="flex items-center gap-2 text-lg font-semibold">
              <Upload className="h-5 w-5" />
              Step 1: Upload PDF
            </Label>
            <div className="flex items-center gap-4">
              <Label
                htmlFor="pdf-upload"
                className="flex-grow cursor-pointer rounded-md border-2 border-dashed border-input p-6 text-center text-muted-foreground transition-colors hover:border-primary hover:bg-secondary/50"
              >
                <div className="flex flex-col items-center gap-2">
                  <Upload className="h-8 w-8" />
                  <span>Click to browse or drag & drop your PDF here</span>
                </div>
              </Label>
              <Input
                id="pdf-upload"
                type="file"
                accept="application/pdf"
                className="hidden"
                onChange={handleFileChange}
              />
            </div>
            {file && (
              <div className="flex items-center gap-2 rounded-md border border-border bg-secondary/30 p-3 text-sm">
                <FileText className="h-5 w-5 flex-shrink-0 text-primary" />
                <span className="flex-grow truncate font-medium">{file.name}</span>
                <CheckCircle2 className="h-5 w-5 text-green-600" />
              </div>
            )}
          </div>

          <div className="space-y-4">
            <Label htmlFor="language-select" className="flex items-center gap-2 text-lg font-semibold">
              <Languages className="h-5 w-5" />
              Step 2: Select Language
            </Label>
            <Select onValueChange={(value: Language) => setLanguage(value)} value={language} disabled={!file}>
              <SelectTrigger id="language-select" className="w-full" aria-label="Select target language">
                <SelectValue placeholder="Choose a target language..." />
              </SelectTrigger>
              <SelectContent>
                {languages.map((lang) => (
                  <SelectItem key={lang} value={lang}>{lang}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="flex flex-col items-center gap-4 pt-4">
            <Button 
              onClick={onTranslate} 
              disabled={!file || !language || isLoading}
              className="w-full max-w-xs text-lg py-6"
              aria-live="polite"
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Translating...
                </>
              ) : (
                'Translate Document'
              )}
            </Button>
            
            {translatedUri && (
              <a
                href={translatedUri}
                download={`${file?.name.replace('.pdf', '') || 'translated'}_${language}.pdf`}
                className="w-full max-w-xs"
              >
                <Button variant="outline" className="w-full text-lg py-6">
                  <Download className="mr-2 h-5 w-5" />
                  Download Translated PDF
                </Button>
              </a>
            )}
          </div>
        </CardContent>
      </Card>
      <footer className="mt-8 text-center text-sm text-muted-foreground">
        <p>&copy; {new Date().getFullYear()} LughaLink. All rights reserved.</p>
      </footer>
    </div>
  );
}
