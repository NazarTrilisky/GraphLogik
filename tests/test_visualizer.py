
import sys
sys.path.insert(0, '.')

from src.visualizer import DisplayGraph


def test_show_simple_graph():
    dg = DisplayGraph()
    dg.addNode('solo')
    dg.addNode('a')
    dg.addNode('b')
    dg.addNode('c', label='C-label')
    dg.addNode('d')
    dg.addNode('e', label='E label')
    dg.addNode('f')
    dg.addNode('g')
    dg.addEdge('a', 'b', weight=2)
    dg.addEdge('a', 'd')
    dg.addEdge('a', 'e')
    dg.addEdge('a', 'f')
    dg.addEdge('g', 'f')
    dg.addEdge('c', 'g')
    #dg.show()
    #dg.save_image()


if __name__ == '__main__':
    test_show_simple_graph()

