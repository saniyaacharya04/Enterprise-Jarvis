import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app
from app.services.embedder import embed
from app.services.retriever import retrieve
from app.services.rag_pipeline import run_rag

class TestEnterpriseJarvis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")

    def test_identity_intent(self):
        response = self.client.post("/api/chat", json={"query": "Who are you?"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Enterprise Jarvis", data["response"])

    def test_embedder_dimension(self):
        vector = embed("Enterprise knowledge assistant")
        self.assertEqual(len(vector), 384)

    def test_retriever_offline_fallback(self):
        docs = retrieve("What are the data privacy principles?", k=2)
        self.assertEqual(len(docs), 2)
        self.assertTrue(any("privacy" in doc.lower() or "security" in doc.lower() for doc in docs))

    def test_rag_query_execution(self):
        ans = run_rag("What is Jarvis?")
        self.assertTrue("internal knowledge" in ans.lower() or "enterprise ai assistant" in ans.lower())

if __name__ == '__main__':
    unittest.main()
