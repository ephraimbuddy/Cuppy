from pyramid import testing

from . import BaseTest
from . import dummy_request


class TestDocumentViewSuccess(BaseTest):

    def _callFUT(self, request):
        from ..views.document.views import DocumentView
        return DocumentView.doc_view(request)
    
    def test_view(self):
        "Test the document view"
        from ..views.document import DocumentResource

        user = self.makeUser("myusername","email@example.com","John")
        doc = self.createDoc(
            meta_title = "My Document meta title",
            title = "My Document title",
            body = "This is the body",
            user = user
        )
        self.session.add_all([user,doc])
        request = dummy_request(self.session)
        request.context = DocumentResource(doc)
        result = self._callFUT(request)
        self.assertEqual(result['document'],doc)
