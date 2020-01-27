"""Pagination settings."""
from base64 import b64encode
from urllib import parse as urlparse
from rest_framework.pagination import PageNumberPagination, CursorPagination


class ProjectPageNumberPagination(PageNumberPagination):
    """Customized pagination class."""

    page_size_query_param = 'page_size'


class ProjectCursorPagination(CursorPagination):
    """Customized cursor pagination class."""

    def encode_cursor(self, cursor):
        """
        Given a Cursor instance, return an url with encoded cursor.
        """
        tokens = {}
        if cursor.offset != 0:
            tokens['o'] = str(cursor.offset)
        if cursor.reverse:
            tokens['r'] = '1'
        if cursor.position is not None:
            tokens['p'] = cursor.position

        querystring = urlparse.urlencode(tokens, doseq=True)
        encoded = b64encode(querystring.encode('ascii')).decode('ascii')
        return encoded


class ProjectMobilePagination(PageNumberPagination):
    """Pagination settings for mobile API."""

    def get_next_link(self):
        """Get next link method."""
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_link(self):
        """Get previous link method."""
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()
