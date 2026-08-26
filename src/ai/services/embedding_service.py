"""
Embedding Service using Gemini
Generates vector embeddings for Arabic/Quranic text
"""

import asyncio
from typing import List, Optional, Union
import logging
from google import genai
from ..config import gemini_config

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating text embeddings using Gemini.
    Supports both single texts and batch processing.
    """

    def __init__(self):
        self.client = genai.Client(api_key=gemini_config.api_key)
        self.model = gemini_config.embedding_model
        self.dimensions = gemini_config.embedding_dimensions

    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text (Arabic or English)

        Returns:
            List of floats representing the embedding vector
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        text = self._prepare_text(text)

        try:
            result = self.client.models.embed_content(
                model=self.model,
                contents=text
            )
            return result.embeddings[0].values
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def get_embeddings_batch(
        self,
        texts: List[str],
        batch_size: int = 100
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batches.

        Args:
            texts: List of input texts
            batch_size: Number of texts to process per API call

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch = [self._prepare_text(t) for t in batch if t and t.strip()]

            if not batch:
                continue

            try:
                # Gemini embedContent processes one content at a time,
                # so we process each text individually within the batch
                batch_embeddings = []
                for text in batch:
                    result = self.client.models.embed_content(
                        model=self.model,
                        contents=text
                    )
                    batch_embeddings.append(result.embeddings[0].values)

                all_embeddings.extend(batch_embeddings)
                logger.info(f"Processed batch {i//batch_size + 1}, total: {len(all_embeddings)}")

            except Exception as e:
                logger.error(f"Error in batch {i//batch_size + 1}: {e}")
                all_embeddings.extend([None] * len(batch))

        return all_embeddings

    def _prepare_text(self, text: str) -> str:
        """
        Prepare text for embedding.
        - Remove excessive whitespace
        - Truncate if too long
        """
        text = ' '.join(text.split())

        # Gemini embedding model supports up to 2048 tokens (~8000 chars)
        max_chars = 8000
        if len(text) > max_chars:
            text = text[:max_chars]

        return text

    def compute_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """
        Compute cosine similarity between two embeddings.

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Similarity score between 0 and 1
        """
        import math

        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        norm1 = math.sqrt(sum(a * a for a in embedding1))
        norm2 = math.sqrt(sum(b * b for b in embedding2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)


# Singleton instance
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """Get or create singleton EmbeddingService instance."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
