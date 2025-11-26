from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from .forms import DocumentForm
from .services import PDFService, TranslationService
import os
from django.conf import settings

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()
            # Trigger processing immediately for this MVP
            process_document(doc.id)
            return redirect('result', doc_id=doc.id)
    else:
        form = DocumentForm()
    return render(request, 'translator/upload.html', {'form': form})

def process_document(doc_id):
    doc = Document.objects.get(id=doc_id)
    doc.status = 'processing'
    doc.save()

    try:
        # New workflow: Translate while preserving layout
        output_filename = f"translated_{doc.id}.pdf"
        output_path = PDFService.translate_pdf_preserve_layout(
            doc.file.path, 
            output_filename, 
            doc.target_language
        )
        
        # 4. Save result
        # We need to save the relative path to the FileField
        doc.translated_file.name = os.path.join('translated', output_filename)
        doc.status = 'completed'
        doc.save()
    except Exception as e:
        print(f"Error processing document {doc.id}: {e}")
        doc.status = 'failed'
        doc.save()

def result_view(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    return render(request, 'translator/result.html', {'document': doc})
