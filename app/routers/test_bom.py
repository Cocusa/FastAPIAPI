import unittest

from ..test_main import client


class TestGetBomInfoAPI(unittest.TestCase):
    def test_get_bom_info(self):

        response = client.get("/api/bom/19818/info")
        self.assertEqual(response.status_code, 200)

        response = client.get("/api/bom/1/info")
        self.assertEqual(response.status_code, 404)

        response = client.get("/api/bom/-1/info")
        self.assertEqual(response.status_code, 422)

        response = client.get("/api/bom/INVALID~ID/info")
        self.assertEqual(response.status_code, 422)
   
        response = client.get("/api/bom/{bom_id}/info")        
        self.assertEqual(response.status_code, 404)

        response = client.get("/api/bom/𡨸漢/info")
        self.assertEqual(response.status_code, 422)
