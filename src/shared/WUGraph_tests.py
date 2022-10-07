import unittest
from WUGraph import WUGraph

class TestWUGraph(unittest.TestCase):
    def test_get_set(self):
        wu = WUGraph(10)

        # set edge
        wu.set_edge(2, 5, 3.5)
        self.assertEqual(wu.get_edge(2, 5), 3.5)
        self.assertEqual(wu.get_edge(5, 2), 3.5)
        self.assertEqual(wu.get_degree(2), 1)
        self.assertEqual(wu.get_degree(5), 1)
        self.assertEqual(wu.get_neighbors(2), [5])
        self.assertEqual(wu.get_neighbors(5), [2])

        # idempotency
        wu.set_edge(5, 2, 3.5)
        self.assertEqual(wu.get_edge(2, 5), 3.5)
        self.assertEqual(wu.get_edge(5, 2), 3.5)
        self.assertEqual(wu.get_degree(2), 1)
        self.assertEqual(wu.get_degree(5), 1)
        self.assertEqual(wu.get_neighbors(2), [5])
        self.assertEqual(wu.get_neighbors(5), [2])

        # modification
        wu.set_edge(2, 5, 10)
        self.assertEqual(wu.get_edge(2, 5), 10)
        self.assertEqual(wu.get_edge(5, 2), 10)
        self.assertEqual(wu.get_degree(2), 1)
        self.assertEqual(wu.get_degree(5), 1)
        self.assertEqual(wu.get_neighbors(2), [5])
        self.assertEqual(wu.get_neighbors(5), [2])

    def test_degree_neighbors(self):
        wu = WUGraph(4)

        wu.set_edge(1, 3, 2.2)
        wu.set_edge(2, 0, 3.3)
        wu.set_edge(1, 0, 1.6)
        wu.set_edge(3, 2, 0.5)
        wu.set_edge(0, 3, 5)

        self.assertEqual(wu.get_degree(0), 3)
        self.assertEqual(wu.get_degree(1), 2)
        self.assertEqual(wu.get_degree(2), 2)
        self.assertEqual(wu.get_degree(3), 3)

        self.assertEqual(wu.get_neighbors(0), [1, 2, 3])
        self.assertEqual(wu.get_neighbors(1), [0, 3])
        self.assertEqual(wu.get_neighbors(2), [0, 3])
        self.assertEqual(wu.get_neighbors(3), [0, 1, 2])

        # remove edges
        wu.set_edge(0, 1, -1)
        wu.set_edge(1, 3, -1)

        self.assertEqual(wu.get_degree(0), 2)
        self.assertEqual(wu.get_degree(1), 0)
        self.assertEqual(wu.get_degree(2), 2)
        self.assertEqual(wu.get_degree(3), 2)

        self.assertEqual(wu.get_neighbors(0), [2, 3])
        self.assertEqual(wu.get_neighbors(1), [])
        self.assertEqual(wu.get_neighbors(2), [0, 3])
        self.assertEqual(wu.get_neighbors(3), [0, 2])

    def test_mst(self):
        wu = WUGraph(10)

        wu.set_edge(0, 1, 3)
        wu.set_edge(0, 3, 6)
        wu.set_edge(0, 4, 9)
        wu.set_edge(1, 2, 2)
        wu.set_edge(1, 3, 4)
        wu.set_edge(1, 4, 9)
        wu.set_edge(1, 5, 9)
        wu.set_edge(2, 3, 2)
        wu.set_edge(2, 5, 8)
        wu.set_edge(2, 6, 9)
        wu.set_edge(3, 6, 9)
        wu.set_edge(4, 5, 8)
        wu.set_edge(4, 9, 18)
        wu.set_edge(5, 6, 7)
        wu.set_edge(5, 8, 9)
        wu.set_edge(5, 9, 10)
        wu.set_edge(6, 7, 4)
        wu.set_edge(6, 8, 5)
        wu.set_edge(7, 8, 1)
        wu.set_edge(7, 9, 4)
        wu.set_edge(8, 9, 3)

        mst = wu.get_mst()

        edges = [(0, 1, 3), (1, 2, 2), (2, 3, 2),
                 (2, 5, 8), (4, 5, 8), (5, 6, 7),
                 (6, 7, 4), (7, 8, 1), (8, 9, 3)]
        
        for edge in edges:
            u, v, w = edge
            self.assertEqual(mst.get_edge(u, v,), w)
            self.assertTrue(mst.get_edge_exists(u, v))

        present_edges = [(0, 1), (1, 2), (2, 3),
                         (2, 5), (4, 5), (5, 6),
                         (6, 7), (7, 8), (8, 9)]

        for edge in mst.all_edges():
            self.assertTrue(edge in present_edges)

        self.assertEqual(len(list(mst.all_edges())), len(present_edges))

if __name__ == '__main__':
    unittest.main()