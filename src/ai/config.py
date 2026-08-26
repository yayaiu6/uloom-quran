"""
AI Configuration for علوم القرآن Platform
Gemini and Qdrant settings
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class GeminiConfig:
    """Gemini Configuration"""
    api_key: str = os.getenv("GEMINI_API_KEY", "")

    # Models
    chat_model: str = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash")
    embedding_model: str = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")

    # Settings
    chat_temperature: float = 0.7
    chat_max_tokens: int = 4096
    embedding_dimensions: int = 3072  # gemini-embedding-001 default dimensions


@dataclass
class QdrantConfig:
    """Qdrant Vector Database Configuration - Supports remote URL for GKE deployment"""
    # Support both URL-based and host/port-based configuration
    url: str = os.getenv("QDRANT_URL", "")
    api_key: str = os.getenv("QDRANT_API_KEY", "")
    host: str = os.getenv("QDRANT_HOST", "localhost")
    port: int = int(os.getenv("QDRANT_PORT", "6333"))
    grpc_port: int = int(os.getenv("QDRANT_GRPC_PORT", "6334"))

    # Collections
    verses_collection: str = "quran_verses"
    tafsir_collection: str = "tafsir_texts"
    qiraat_collection: str = "qiraat_differences"
    asbab_collection: str = "asbab_nuzul"

    # Search settings
    default_limit: int = 10
    score_threshold: float = 0.7


@dataclass
class RAGConfig:
    """RAG Pipeline Configuration"""
    # Retrieval settings
    top_k_verses: int = 5
    top_k_tafsir: int = 3
    top_k_qiraat: int = 5

    # Context window
    max_context_length: int = 8000

    # Response settings
    include_citations: bool = True
    include_arabic: bool = True
    language: str = "ar"  # ar, en, or both


# Global config instances
gemini_config = GeminiConfig()
qdrant_config = QdrantConfig()
rag_config = RAGConfig()


# System prompts for different AI features
SYSTEM_PROMPTS = {
    "general_qa": """أنت مساعد ذكي متخصص في علوم القرآن الكريم.

مهمتك:
- الإجابة على الأسئلة المتعلقة بالقرآن الكريم بدقة علمية
- الاستشهاد بالآيات والتفاسير والمصادر الموثوقة
- التمييز بين المسائل المتفق عليها والمسائل الخلافية
- استخدام لغة محترمة ومناسبة للموضوعات الدينية

قواعد مهمة:
1. لا تختلق آيات أو أحاديث غير موجودة
2. اذكر المصادر والمراجع عند الاستشهاد
3. إذا لم تكن متأكداً، اعترف بذلك بدلاً من الاختراع
4. احترم اختلاف العلماء في المسائل الفقهية

السياق المسترجع من قاعدة البيانات:
{context}

السؤال: {question}

الإجابة:""",

    "verse_explanation": """أنت مفسر متخصص في شرح آيات القرآن الكريم.

مهمتك شرح الآية التالية بشكل شامل يتضمن:
1. المعنى الإجمالي للآية
2. معاني المفردات الغريبة
3. سبب النزول (إن وجد)
4. الأحكام المستنبطة (إن وجدت)
5. الفوائد والعبر

السياق من التفاسير:
{context}

الآية: {verse}
السورة: {surah} - الآية رقم: {ayah}

 الشرح:""",

    "qiraat_analysis": """أنت متخصص في علم القراءات القرآنية.

مهمتك تحليل الفروق بين القراءات المختلفة للآية وتوضيح:
1. الفرق في اللفظ بين القراءات
2. الأثر في المعنى (إن وجد)
3. التوجيه النحوي لكل قراءة
4. أقوال العلماء في ذلك

القراءات المختلفة:
{context}

الآية: {verse}

التحليل:""",

    "tafsir_comparison": """أنت باحث متخصص في مقارنة التفاسير القرآنية.

مهمتك مقارنة أقوال المفسرين في الآية التالية وتوضيح:
1. نقاط الاتفاق بين المفسرين
2. نقاط الاختلاف ومنشأها
3. الراجح من الأقوال مع التعليل
4. المنهج التفسيري لكل مفسر

التفاسير المختلفة:
{context}

الآية: {verse}

المقارنة:""",

    "semantic_search": """Based on the user's search query, identify the most relevant Quranic verses and explain why they match.

Query: {query}

Retrieved verses:
{context}

Provide a summary of the most relevant verses and their connection to the query."""
}
