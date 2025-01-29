#include "algorithms.h"
#include <cassert>
#include <vector>
#include <tuple>

using namespace GraphAlgorithms;

void TestBFS() {
    // Test 1: Linear graph 0-1-2
    std::vector<int> adj1[3];
    adj1[0].push_back(1);
    adj1[1].push_back(0);
    adj1[1].push_back(2);
    adj1[2].push_back(1);
    
    std::vector<int> dist1 = BFS(adj1, 3, 0);
    assert(dist1[0] == 0 && dist1[1] == 1 && dist1[2] == 2);
    
    // Test 2: Disconnected graph
    std::vector<int> adj2[4];
    adj2[0].push_back(1);
    adj2[1].push_back(0);
    adj2[2].push_back(3);
    adj2[3].push_back(2);
    
    std::vector<int> dist2 = BFS(adj2, 4, 0);
    assert(dist2[0] == 0 && dist2[1] == 1 && dist2[2] == -1 && dist2[3] == -1);
}

void TestDFS() {
    // Test: Traversal order from 0 in a triangle graph
    std::vector<int> adj[3];
    adj[0].push_back(1);
    adj[1].push_back(2);
    adj[2].push_back(0);
    
    std::vector<int> traversal = DFS(adj, 3, 0);
    assert(traversal.size() == 3);
    // Exact order depends on DFS implementation, but all nodes should be visited
    std::vector<bool> visited(3, false);
    for (int node : traversal) visited[node] = true;
    assert(visited[0] && visited[1] && visited[2]);
}

void TestKruskal() {
    // Test: Simple connected graph
    std::vector<std::pair<int, int>> adj[3];
    adj[0].emplace_back(1, 1);
    adj[0].emplace_back(2, 2);
    adj[1].emplace_back(2, 3);
    
    auto [weight, edges] = Kruskal(adj, 3);
    assert(weight == 3); // MST includes 0-1 (1) and 0-2 (2)
}

void TestBellmanFord() {
    // Test: No negative cycle
    std::vector<std::pair<int, int>> adj[3];
    adj[0].emplace_back(1, 1);
    adj[1].emplace_back(2, 2);
    auto [success, dist] = BellmanFord(adj, 3, 0);
    assert(success && dist[2] == 3);
    
    // Test with negative weight but no cycle
    adj[0].emplace_back(2, -1);
    auto [s2, d2] = BellmanFord(adj, 3, 0);
    assert(s2 && d2[2] == -1);
    
    // Test with negative cycle
    std::vector<std::pair<int, int>> adj_neg[2];
    adj_neg[0].emplace_back(1, -1);
    adj_neg[1].emplace_back(0, -1);
    auto [s3, d3] = BellmanFord(adj_neg, 2, 0);
    assert(!s3);
}

void TestDijkstra() {
    std::vector<std::pair<int, int>> adj[3];
    adj[0].emplace_back(1, 1);
    adj[1].emplace_back(2, 2);
    adj[0].emplace_back(2, 4);
    std::vector<int> dist = Dijkstra(adj, 3, 0);
    assert(dist[2] == 3); // Path through 1 is shorter
}

void TestNumberOfConnectedComponents() {
    std::vector<int> adj[4];
    adj[0].push_back(1);
    adj[1].push_back(0);
    adj[2].push_back(3);
    adj[3].push_back(2);
    assert(NumberOfConnectedComponents(adj, 4) == 2);
}

void TestTopologicalSort() {
    // Valid DAG
    std::vector<int> adj[3];
    adj[0].push_back(1);
    adj[0].push_back(2);
    adj[1].push_back(2);
    std::vector<int> order = TopologicalSort(adj, 3);
    assert(order.size() == 3 && order[0] == 0 && order[2] == 2);
    
    // Cyclic graph
    adj[2].push_back(0);
    order = TopologicalSort(adj, 3);
    assert(order.empty());
}

void TestCountStronglyConnectedComponents() {
    std::vector<int> adj[3];
    adj[0].push_back(1);
    adj[1].push_back(2);
    adj[2].push_back(0);
    assert(CountStronglyConnectedComponents(adj, 3) == 1);
}

void TestLevenshteinDistance() {
    assert(LevenshteinDistance("kitten", "sitting") == 3);
    assert(LevenshteinDistance("", "abc") == 3);
    assert(LevenshteinDistance("abc", "abc") == 0);
}

void TestHamiltonianCycle() {
    std::vector<int> adj[3];
    adj[0].push_back(1);
    adj[1].push_back(2);
    adj[2].push_back(0);
    adj[2].push_back(1);
    adj[1].push_back(0);
    adj[0].push_back(2);
    auto [exists, path] = HamiltonianCycle(adj, 3);
    assert(exists && path.size() == 3);
}

void TestHasEulerianCycle() {
    std::vector<int> adj[2];
    adj[0].push_back(1);
    adj[1].push_back(0);
    assert(HasEulerianCycle(adj, 2)); // In-degree equals out-degree and strongly connected
}

void TestFordFulkerson() {
    std::vector<std::pair<int, int>> adj[4];
    adj[0].emplace_back(1, 3);
    adj[0].emplace_back(2, 2);
    adj[1].emplace_back(2, 5);
    adj[1].emplace_back(3, 2);
    adj[2].emplace_back(3, 3);
    auto [flow, edges] = FordFulkerson(adj, 4, 0, 3);
    assert(flow == 5);
}

void TestEdmondKarp() {
    // Same graph as FordFulkerson test
    std::vector<std::pair<int, int>> adj[4];
    adj[0].emplace_back(1, 3);
    adj[0].emplace_back(2, 2);
    adj[1].emplace_back(2, 5);
    adj[1].emplace_back(3, 2);
    adj[2].emplace_back(3, 3);
    assert(EdmondKarp(adj, 4, 0, 3) == 5);
}

void TestIsBipartite() {
    std::vector<int> adj[3];
    adj[0].push_back(1);
    adj[1].push_back(0);
    adj[1].push_back(2);
    adj[2].push_back(1);
    assert(IsBipartite(adj, 3)); // It's a bipartite graph (chain)
    
    adj[0].push_back(2);
    adj[2].push_back(0);
    assert(!IsBipartite(adj, 3)); // Triangle is not bipartite
}

void TestKMP() {
    std::vector<int> matches = KMP("ABABDABACDABABCABAB", "ABABCABAB");
    assert(matches.size() == 1 && matches[0] == 10);
}

void TestBipartiteMaxMatching() {
    std::vector<int> adj[2];
    adj[0].push_back(1); // Bipartite graph with one edge
    assert(BipartiteMaxMatching(adj, 1, 1) == 1);
}

void TestHavelHakimi() {
    std::vector<int> degrees = {3, 3, 3}; 
    assert(!HavelHakimi(degrees));
    degrees = {2, 2, 2}; // Possible (triangle)
    assert(HavelHakimi(degrees));
}

void TestFloydWarshall() {
    std::vector<std::pair<int, int>> adj[3];
    adj[0].emplace_back(1, 1);
    adj[1].emplace_back(2, 2);
    adj[0].emplace_back(2, 4);
    auto [no_neg, dist] = FloydWarshall(adj, 3);
    assert(no_neg && dist[0][2] == 3);
}

int main() {
    TestBFS();
    TestDFS();
    TestKruskal();
    TestBellmanFord();
    TestDijkstra();
    TestNumberOfConnectedComponents();
    TestTopologicalSort();
    TestCountStronglyConnectedComponents();
    TestLevenshteinDistance();
    TestHamiltonianCycle();
    TestHasEulerianCycle();
    TestFordFulkerson();
    TestEdmondKarp();
    TestIsBipartite();
    TestKMP();
    TestBipartiteMaxMatching();
    TestHavelHakimi();
    TestFloydWarshall();
    
    return 0;
}