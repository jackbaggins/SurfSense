#!/usr/bin/env python3
"""
Docling Document Processing Service for SurfSense
SSL-related configuration with pre-downloaded models
"""

import logging
import os
import ssl
from typing import Any

logger = logging.getLogger(__name__)


class DoclingService:
    """Docling service for enhanced document processing with SSL and model configuration."""

    def __init__(self):
        """Initialize Docling service with SSL, model fixes, and GPU acceleration."""
        self.converter = None
        self.use_gpu = True
        self._configure_ssl_environment()
        self._check_gpu_support()
        self._initialize_docling()

    def _configure_ssl_environment(self):
        """Configure SSL environment for model downloads."""
        try:
            # WARNING: this disables SSL verification by using an unverified context.
            # Consider removing this if you want strict SSL verification.
            ssl._create_default_https_context = ssl._create_unverified_context

            # Set SSL environment variables if not already set
            if not os.environ.get("SSL_CERT_FILE"):
                try:
                    import certifi

                    os.environ["SSL_CERT_FILE"] = certifi.where()
                    os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
                except ImportError:
                    # certifi not installed; leave environment unchanged
                    pass

            logger.info("SSL environment configured for model downloads")
        except Exception as e:
            logger.warning(f"SSL configuration warning: {e}")

    def _check_gpu_support(self):
        """Check and configure GPU support (currently generic CUDA detection)."""
        try:
            import torch

            if torch.cuda.is_available():
                gpu_count = torch.cuda.device_count()
                gpu_name = torch.cuda.get_device_name(0) if gpu_count > 0 else "Unknown"
                logger.info(f"CUDA detected - Docling: {gpu_name} ({gpu_count} devices)")
                logger.info(f"CUDA version - Docling: {torch.version.cuda}")
                self.use_gpu = True
            else:
                logger.info("CUDA not available, falling back to CPU")
                self.use_gpu = False
        except ImportError:
            logger.info("PyTorch not found for Docling, falling back to CPU")
            self.use_gpu = False
        except Exception as e:
            logger.warning(f"GPU detection failed for Docling: {e}, falling back to CPU")
            self.use_gpu = False

    def _initialize_docling(self):
        """Initialize Docling with OCR, tables, and accelerator configuration."""
        try:
            from docling.datamodel.accelerator_options import (
                AcceleratorDevice,
                AcceleratorOptions,
            )
            from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
            from docling.datamodel.base_models import InputFormat
            from docling.datamodel.pipeline_options import (
                PdfPipelineOptions,
                EasyOcrOptions,
            )
            from docling.document_converter import DocumentConverter, PdfFormatOption

            logger.info("Initializing Docling with OCR and accelerator configuration...")

            # If you prefetch models into a specific path, you can set it via env:
            #   DOCLING_ARTIFACTS_PATH=/opt/docling_models
            artifacts_path = os.environ.get("DOCLING_ARTIFACTS_PATH")



            if artifacts_path:
                pipeline_options = PdfPipelineOptions(artifacts_path=artifacts_path)
                logger.info(f"Using Docling artifacts path: {artifacts_path}")
            else:
                pipeline_options = PdfPipelineOptions()

            # --- OCR configuration (EasyOCR via Docling) ---

            # Enable OCR
            if hasattr(pipeline_options, "do_ocr"):
                pipeline_options.do_ocr = True
                logger.info("Docling OCR enabled")
            else:
                logger.warning("PdfPipelineOptions has no 'do_ocr' attribute; OCR cannot be enabled explicitly")

            # Ensure we have EasyOCR options and configure them minimally
            ocr_opts = getattr(pipeline_options, "ocr_options", None)

            # In recent Docling versions, this is already an EasyOcrOptions instance by default,
            # but we keep this defensive.
            if isinstance(ocr_opts, EasyOcrOptions) or ocr_opts is not None:
                try:
                    # Language(s) you care about
                    if hasattr(ocr_opts, "lang"):
                        ocr_opts.lang = ["en"]

                    logger.info("Docling EasyOCR options configured (lang=['en'])")
                except Exception as e:
                    logger.warning(f"Failed to fine-tune EasyOCR options: {e}")
            else:
                logger.warning("Unexpected OCR configuration options; using Docling defaults")

            # --- Table structure configuration ---

            if hasattr(pipeline_options, "do_table_structure"):
                pipeline_options.do_table_structure = True
                logger.info("Table structure detection enabled")

                tso = getattr(pipeline_options, "table_structure_options", None)
                if tso is not None and hasattr(tso, "do_cell_matching"):
                    # Recommended in current docs for better table reconstruction
                    tso.do_cell_matching = True
                    logger.info("Table cell matching enabled")
            else:
                logger.info("Table structure option not available in this Docling version")

            # --- Accelerator (CPU/GPU) configuration ---

            if hasattr(pipeline_options, "accelerator_options"):
                if self.use_gpu:
                    device = AcceleratorDevice.CUDA
                else:
                    device = AcceleratorDevice.CPU

                pipeline_options.accelerator_options = AcceleratorOptions(
                    num_threads=16,
                    device=device,
                )
                logger.info(f"Docling accelerator configured: {device}")
            else:
                logger.info("Accelerator options not available in this Docling version")

            # Optional: set a document timeout to avoid pathological PDFs hanging forever
            if hasattr(pipeline_options, "document_timeout"):
                pipeline_options.document_timeout = 600.0  # seconds
                logger.info("Docling document timeout set to 600 seconds")

            # --- Create converter ---
            
            
            # Docling enrichment options
            docling_pdf_enrich_code = os.environ.get("DOCLING_PDF_ENRICH_CODE")
            docling_pdf_formulas = os.environ.get("DOCLING_PDF_ENRICH_FORMULAS")
            docling_pdf_pic_class = os.environ.get("DOCLING_PDF_ENRICH_PIC_CLASS")
            docling_pdf_enrich_pic_desc = os.environ.get("DOCLING_PDF_ENRICH_PIC_DESCRIPTION")
            
            if docling_pdf_enrich_code is not None and hasattr(pipeline_options, "enrich_code_blocks"):
                pipeline_options.do_code_enrichment = True
                logger.info(f"Docling PDF code block enrichment set to: {pipeline_options.do_code_enrichment}")
            if docling_pdf_formulas is not None and hasattr(pipeline_options, "enrich_formulas"):
                pipeline_options.do_formula_enrichment = True
                logger.info(f"Docling PDF formula enrichment set to: {pipeline_options.do_formula_enrichment}")
            if docling_pdf_pic_class is not None and hasattr(pipeline_options, "enrich_picture_classification"):
                pipeline_options.do_picture_classification = True
                logger.info(f"Docling PDF picture classification enrichment set to: {pipeline_options.do_picture_classification}")
                # SmolVLM vision model (3GB)
                from docling.datamodel.pipeline_options import smolvlm_picture_description
                pipeline_options.picture_description_options = smolvlm_picture_description
                # Granite vision model granite-vision-3.1-2b-preview (11GB)
                # from docling.datamodel.pipeline_options import granite_picture_description
                # pipeline_options.picture_description_options = granite_picture_description
            if docling_pdf_enrich_pic_desc is not None and hasattr(pipeline_options, "enrich_picture_description"):
                pipeline_options.do_picture_description = True
                logger.info(f"Docling PDF picture description enrichment set to: {pipeline_options.do_picture_description}")
                # SmolVLM vision model (3GB)
                from docling.datamodel.pipeline_options import smolvlm_picture_description
                pipeline_options.picture_description_options = smolvlm_picture_description
                # Granite vision model granite-vision-3.1-2b-preview (11GB)
                # from docling.datamodel.pipeline_options import granite_picture_description
                # pipeline_options.picture_description_options = granite_picture_description


            pdf_format_option = PdfFormatOption(
                pipeline_options=pipeline_options,
                backend=PyPdfiumDocumentBackend,
            )

            self.converter = DocumentConverter(
                format_options={InputFormat.PDF: pdf_format_option}
            )

            acceleration_type = "GPU" if self.use_gpu else "CPU"
            logger.info(
                f"Docling initialized successfully with {acceleration_type} acceleration and OCR enabled"
            )

        except ImportError as e:
            logger.error(f"Docling not installed: {e}")
            raise RuntimeError(f"Docling not available: {e}") from e
        except Exception as e:
            logger.error(f"Docling initialization failed: {e}")
            raise RuntimeError(f"Docling initialization failed: {e}") from e


    def _configure_easyocr_local_models(self):
        """Configure EasyOCR to use pre-downloaded local models."""
        try:
            import os
            import easyocr

            # NOTE: These environment variables disable SSL verification for requests.
            # This may be intentional for your environment, but it weakens security.
            os.environ["CURL_CA_BUNDLE"] = ""
            os.environ["REQUESTS_CA_BUNDLE"] = ""

            # Try to use local models first, fallback to download if needed
            artifacts_path = os.environ.get("DOCLING_ARTIFACTS_PATH")
            try:
                reader = easyocr.Reader(
                    ["en"],
                    download_enabled=False,
                    model_storage_directory=artifacts_path,
                )
                logger.info("EasyOCR configured for local models")
                return reader
            except Exception:
                # If local models fail, allow download
                logger.info(
                    "Local EasyOCR models failed, attempting download using configured SSL behavior"
                )
                reader = easyocr.Reader(
                    ["en"],
                    download_enabled=True,
                    model_storage_directory=artifacts_path,
                )
                logger.info("EasyOCR configured with downloaded models")
                return reader
        except Exception as e:
            logger.warning(f"EasyOCR configuration failed: {e}")
            return None

    async def process_document(
        self, file_path: str, filename: str | None = None
    ) -> dict[str, Any]:
        """Process document with Docling using pre-downloaded models."""

        if self.converter is None:
            raise RuntimeError("Docling converter not initialized")

        try:
            logger.info(
                f"Processing {filename} with Docling (using local models)..."
            )

            # Process document with local models
            result = self.converter.convert(file_path)

            # Extract content using version-safe methods
            content = None
            if hasattr(result, "document") and result.document:
                # Try different export methods (version compatibility)
                if hasattr(result.document, "export_to_markdown"):
                    content = result.document.export_to_markdown()
                    logger.info("Used export_to_markdown method")
                elif hasattr(result.document, "to_markdown"):
                    content = result.document.to_markdown()
                    logger.info("Used to_markdown method")
                elif hasattr(result.document, "text"):
                    content = result.document.text
                    logger.info("Used text property")
                elif hasattr(result.document, "__str__"):
                    content = str(result.document)
                    logger.info("Used string conversion")

                if content:
                    logger.info(
                        f"Docling SUCCESS - {filename}: {len(content)} characters extracted (local models)"
                    )

                    return {
                        "content": content,
                        "full_text": content,
                        "service_used": "docling",
                        "status": "success",
                        "processing_notes": "Processed with Docling using pre-downloaded models",
                    }
                else:
                    raise ValueError("No content could be extracted from document")
            else:
                raise ValueError("No document object returned by Docling")

        except Exception as e:
            logger.error(f"Docling processing failed for {filename}: {e}")
            # Log the full error for debugging
            import traceback

            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise RuntimeError(f"Docling processing failed: {e}") from e

    async def process_large_document_summary(
        self, content: str, llm, document_title: str = "Document"
    ) -> str:
        """
        Process large documents using chunked LLM summarization.

        Args:
            content: The full document content
            llm: The language model to use for summarization
            document_title: Title of the document for context

        Returns:
            Final summary of the document
        """
        # Large document threshold (100K characters ≈ 25K tokens)
        large_document_threshold = 100_000

        if len(content) <= large_document_threshold:
            # For smaller documents, use direct processing
            logger.info(
                f"Document size: {len(content)} characters - using direct processing"
            )
            from app.prompts import SUMMARY_PROMPT_TEMPLATE

            summary_chain = SUMMARY_PROMPT_TEMPLATE | llm
            result = await summary_chain.ainvoke({"document": content})
            return result.content

        logger.info(
            f"Large document detected: {len(content)} characters - using chunked processing"
        )

        # Import chunker from config
        # Create LLM-optimized chunks (8K tokens max for safety)
        from chonkie import OverlapRefinery, RecursiveChunker
        from langchain_core.prompts import PromptTemplate

        llm_chunker = RecursiveChunker(
            chunk_size=8000  # Conservative for most LLMs
        )

        # Apply overlap refinery for context preservation (25% overlap = 2000 tokens)
        overlap_refinery = OverlapRefinery(
            context_size=0.25,  # 25% overlap for context preservation
            method="suffix",  # Add next chunk context to current chunk
        )

        # First chunk the content, then apply overlap refinery
        initial_chunks = llm_chunker.chunk(content)
        chunks = overlap_refinery.refine(initial_chunks)
        total_chunks = len(chunks)

        logger.info(f"Split into {total_chunks} chunks for LLM processing")

        # Template for chunk processing
        chunk_template = PromptTemplate(
            input_variables=["chunk", "chunk_number", "total_chunks"],
            template="""<INSTRUCTIONS>
You are summarizing chunk {chunk_number} of {total_chunks} from a large document.

Create a comprehensive summary of this document chunk. Focus on:
- Key concepts, facts, and information
- Important details and context
- Main topics and themes

Provide a clear, structured summary that captures the essential content.

Chunk {chunk_number}/{total_chunks}:
<document_chunk>
{chunk}
</document_chunk>
</INSTRUCTIONS>""",
        )

        # Process each chunk individually
        chunk_summaries = []
        for i, chunk in enumerate(chunks, 1):
            try:
                logger.info(
                    f"Processing chunk {i}/{total_chunks} ({len(chunk.text)} characters)"
                )

                chunk_chain = chunk_template | llm
                chunk_result = await chunk_chain.ainvoke(
                    {
                        "chunk": chunk.text,
                        "chunk_number": i,
                        "total_chunks": total_chunks,
                    }
                )

                chunk_summary = chunk_result.content
                chunk_summaries.append(f"=== Section {i} ===\n{chunk_summary}")

                logger.info(f"Completed chunk {i}/{total_chunks}")

            except Exception as e:
                logger.error(
                    f"Failed to process chunk {i}/{total_chunks}: {e}"
                )
                chunk_summaries.append(f"=== Section {i} ===\n[Processing failed]")

        # Combine summaries into final document summary
        logger.info(f"Combining {len(chunk_summaries)} chunk summaries")

        try:
            combine_template = PromptTemplate(
                input_variables=["summaries", "document_title"],
                template="""<INSTRUCTIONS>
You are combining multiple section summaries into a final comprehensive document summary.

Create a unified, coherent summary from the following section summaries of "{document_title}".
Ensure:
- Logical flow and organization
- No redundancy or repetition  
- Comprehensive coverage of all key points
- Professional, objective tone

<section_summaries>
{summaries}
</section_summaries>
</INSTRUCTIONS>""",
            )

            combined_summaries = "\n\n".join(chunk_summaries)
            combine_chain = combine_template | llm

            final_result = await combine_chain.ainvoke(
                {"summaries": combined_summaries, "document_title": document_title}
            )

            final_summary = final_result.content
            logger.info(
                f"Large document processing complete: {len(final_summary)} characters in final summary"
            )

            return final_summary

        except Exception as e:
            logger.error(f"Failed to combine summaries: {e}")
            # Fallback: return concatenated chunk summaries
            fallback_summary = "\n\n".join(chunk_summaries)
            logger.warning("Using fallback combined summary")
            return fallback_summary


def create_docling_service() -> DoclingService:
    """Create a Docling service instance."""
    return DoclingService()
