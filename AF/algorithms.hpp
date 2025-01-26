#ifndef GRAPH_ALGORITHMS_H
#define GRAPH_ALGORITHMS_H

#include <vector>
#include <queue>
#include <utility>
#include <algorithm>
#include <numeric>
#include <climits>
#include <tuple>
#include <string>
/*
Function	Inputs	Outputs/Returns
BFS	adj (unweighted), N, start	Distance vector from start node
DFS	adj, N, start	Traversal order vector
Kruskal	adj (weighted), N	(Total MST weight, MST edges)
BellmanFord	adj (directed, weighted), N, start	(Success, distance vector)
Dijkstra	adj (directed, non-neg weights), N, start	Distance vector
NumberOfConnectedComponents	adj, N	Component count
TopologicalSort	adj (DAG), N	Sorted order (or empty if cycle)
CountStronglyConnectedComponents	adj (directed), N	SCC count
LevenshteinDistance	s1, s2	Edit distance
HamiltonianCycle	adj, N	(Exists, cycle path)
HasEulerianCycle	adj (directed), N	Boolean
FordFulkerson	adj (flow), N, source, sink	(Max flow, min cut edges)
EdmondKarp	adj (flow), N, source, sink	Max flow value
IsBipartite	adj, N	Boolean
KMP	text, pattern	Indices of pattern matches
BipartiteMaxMatching	adj (bipartite), m, n	Max matching size
HavelHakimi	Degree sequence	Boolean (graph possible)
FloydWarshall	adj (directed, weighted), N	(No negative cycles, all-pairs distance matrix)
*/
namespace GraphAlgorithms
{

    // BFS for undirected unweighted graphs
    std::vector<int> BFS(const std::vector<int> adj[], int N, int start)
    {
        std::vector<int> dist(N, -1);
        std::queue<int> q;
        dist[start] = 0;
        q.push(start);

        while (!q.empty())
        {
            int u = q.front();
            q.pop();

            for (int v : adj[u])
            {
                if (dist[v] == -1)
                {
                    dist[v] = dist[u] + 1;
                    q.push(v);
                }
            }
        }
        return dist;
    }

    // DFS for undirected unweighted graphs
    void DFSUtil(const std::vector<int> adj[], int u, std::vector<bool> &visited, std::vector<int> &result)
    {
        visited[u] = true;
        result.push_back(u);

        for (int v : adj[u])
        {
            if (!visited[v])
            {
                DFSUtil(adj, v, visited, result);
            }
        }
    }

    std::vector<int> DFS(const std::vector<int> adj[], int N, int start)
    {
        std::vector<bool> visited(N, false);
        std::vector<int> result;
        DFSUtil(adj, start, visited, result);
        return result;
    }

    // Union-Find data structure for Kruskal's algorithm
    class DisjointSetUnion
    {
        std::vector<int> parent, rank;

    public:
        DisjointSetUnion(int n)
        {
            parent.resize(n);
            rank.resize(n, 0);
            for (int i = 0; i < n; ++i)
                parent[i] = i;
        }

        int find(int u)
        {
            if (parent[u] != u)
                parent[u] = find(parent[u]);
            return parent[u];
        }

        void unite(int u, int v)
        {
            u = find(u);
            v = find(v);

            if (u != v)
            {
                if (rank[u] < rank[v])
                    parent[u] = v;
                else
                {
                    parent[v] = u;
                    if (rank[u] == rank[v])
                        rank[u]++;
                }
            }
        }
    };

    // Kruskal's algorithm for undirected weighted graphs
    std::pair<int, std::vector<std::tuple<int, int, int>>> Kruskal(const std::vector<std::pair<int, int>> adj[], int N)
    {
        std::vector<std::tuple<int, int, int>> edges;
        std::vector<std::tuple<int, int, int>> mstEdges;
        int mstWeight = 0;

        // Collect edges (u, v, w) with u < v to avoid duplicates
        for (int u = 0; u < N; ++u)
        {
            for (const auto &[v, w] : adj[u])
            {
                if (u < v)
                {
                    edges.emplace_back(w, u, v);
                }
            }
        }

        // Sort edges by weight
        std::sort(edges.begin(), edges.end());

        DisjointSetUnion dsu(N);
        int edgesAdded = 0;

        for (const auto &[w, u, v] : edges)
        {
            if (dsu.find(u) != dsu.find(v))
            {
                dsu.unite(u, v);
                mstWeight += w;
                mstEdges.emplace_back(u, v, w);
                edgesAdded++;

                if (edgesAdded == N - 1)
                    break;
            }
        }

        if (edgesAdded != N - 1)
            return {-1, {}}; // Graph is disconnected

        return {mstWeight, mstEdges};
    }

    // Bellman-Ford algorithm for directed weighted graphs
    std::pair<bool, std::vector<int>> BellmanFord(const std::vector<std::pair<int, int>> adj[], int N, int start)
    {
        std::vector<int> dist(N, INT_MAX);
        dist[start] = 0;

        // Relax all edges N-1 times
        for (int i = 0; i < N - 1; ++i)
        {
            for (int u = 0; u < N; ++u)
            {
                if (dist[u] == INT_MAX)
                    continue;

                for (const auto &[v, w] : adj[u])
                {
                    if (dist[v] > dist[u] + w)
                    {
                        dist[v] = dist[u] + w;
                    }
                }
            }
        }

        // Check for negative cycles
        for (int u = 0; u < N; ++u)
        {
            if (dist[u] == INT_MAX)
                continue;

            for (const auto &[v, w] : adj[u])
            {
                if (dist[v] > dist[u] + w)
                {
                    return {false, {}}; // Negative cycle detected
                }
            }
        }

        return {true, dist};
    }

    // Dijkstra's algorithm for directed weighted graphs with non-negative weights
    std::vector<int> Dijkstra(const std::vector<std::pair<int, int>> adj[], int N, int start)
    {
        std::vector<int> dist(N, INT_MAX);
        using pii = std::pair<int, int>;
        std::priority_queue<pii, std::vector<pii>, std::greater<pii>> pq;

        dist[start] = 0;
        pq.push({0, start});

        while (!pq.empty())
        {
            auto [d, u] = pq.top();
            pq.pop();

            if (d > dist[u])
                continue;

            for (const auto &[v, w] : adj[u])
            {
                if (dist[v] > dist[u] + w)
                {
                    dist[v] = dist[u] + w;
                    pq.push({dist[v], v});
                }
            }
        }

        return dist;
    }

    // Number of connected components for undirected unweighted graphs
    int NumberOfConnectedComponents(const std::vector<int> adj[], int N)
    {
        std::vector<bool> visited(N, false);
        int count = 0;

        for (int u = 0; u < N; ++u)
        {
            if (!visited[u])
            {
                ++count;
                std::queue<int> q;
                q.push(u);
                visited[u] = true;

                while (!q.empty())
                {
                    int current = q.front();
                    q.pop();

                    for (int v : adj[current])
                    {
                        if (!visited[v])
                        {
                            visited[v] = true;
                            q.push(v);
                        }
                    }
                }
            }
        }

        return count;
    }

    // Topological Sort for directed acyclic graphs (DAG)
    std::vector<int> TopologicalSort(const std::vector<int> adj[], int N)
    {
        std::vector<int> in_degree(N, 0);
        for (int u = 0; u < N; ++u)
        {
            for (int v : adj[u])
            {
                in_degree[v]++;
            }
        }

        std::queue<int> q;
        for (int i = 0; i < N; ++i)
        {
            if (in_degree[i] == 0)
            {
                q.push(i);
            }
        }

        std::vector<int> result;
        int count = 0;

        while (!q.empty())
        {
            int u = q.front();
            q.pop();
            result.push_back(u);
            count++;

            for (int v : adj[u])
            {
                in_degree[v]--;
                if (in_degree[v] == 0)
                {
                    q.push(v);
                }
            }
        }

        if (count != N)
        {
            return {}; // Graph contains a cycle
        }

        return result;
    }

    // Helper function for the first DFS pass in Kosaraju's algorithm
    void DFSPostOrder(int u, const std::vector<int> adj[], std::vector<bool> &visited, std::vector<int> &order)
    {
        visited[u] = true;
        for (int v : adj[u])
        {
            if (!visited[v])
            {
                DFSPostOrder(v, adj, visited, order);
            }
        }
        order.push_back(u);
    }

    // Helper function to reverse the graph
    std::vector<std::vector<int>> reverseGraph(const std::vector<int> adj[], int N)
    {
        std::vector<std::vector<int>> revAdj(N);
        for (int u = 0; u < N; ++u)
        {
            for (int v : adj[u])
            {
                revAdj[v].push_back(u);
            }
        }
        return revAdj;
    }

    // Helper function for the second DFS pass in Kosaraju's algorithm
    void DFSUtilSCC(int u, const std::vector<std::vector<int>> &revAdj, std::vector<bool> &visited)
    {
        visited[u] = true;
        for (int v : revAdj[u])
        {
            if (!visited[v])
            {
                DFSUtilSCC(v, revAdj, visited);
            }
        }
    }

    // Function to count the number of strongly connected components in a directed graph
    int CountStronglyConnectedComponents(const std::vector<int> adj[], int N)
    {
        std::vector<int> order;
        std::vector<bool> visited(N, false);

        // First DFS pass to determine the finishing order
        for (int u = 0; u < N; ++u)
        {
            if (!visited[u])
            {
                DFSPostOrder(u, adj, visited, order);
            }
        }

        // Reverse the graph
        std::vector<std::vector<int>> revAdj = reverseGraph(adj, N);

        // Second DFS pass on reversed graph in reverse finishing order
        std::vector<bool> visitedRev(N, false);
        int sccCount = 0;

        for (int i = order.size() - 1; i >= 0; --i)
        {
            int u = order[i];
            if (!visitedRev[u])
            {
                sccCount++;
                DFSUtilSCC(u, revAdj, visitedRev);
            }
        }

        return sccCount;
    }

    int LevenshteinDistance(const std::string &s1, const std::string &s2)
    {
        int m = s1.size(), n = s2.size();
        std::vector<int> dp(n + 1);
        std::iota(dp.begin(), dp.end(), 0);

        for (int i = 1; i <= m; ++i)
        {
            int prev_diag = dp[0];
            dp[0] = i;
            for (int j = 1; j <= n; ++j)
            {
                int temp = dp[j];
                if (s1[i - 1] == s2[j - 1])
                    dp[j] = prev_diag;
                else
                    dp[j] = 1 + std::min({prev_diag, dp[j - 1], dp[j]});
                prev_diag = temp;
            }
        }
        return dp[n];
    }

    bool HamiltonianCycleUtil(const std::vector<int> adj[], int N, std::vector<int> &path, std::vector<bool> &visited, int pos)
    {
        if (pos == N)
        {
            // Check if the last vertex is connected to the first
            int last = path.back();
            for (int v : adj[last])
            {
                if (v == path[0])
                {
                    return true;
                }
            }
            return false;
        }

        int current = path[pos - 1];
        for (int v : adj[current])
        {
            if (!visited[v])
            {
                visited[v] = true;
                path[pos] = v;

                if (HamiltonianCycleUtil(adj, N, path, visited, pos + 1))
                {
                    return true;
                }

                // Backtrack
                visited[v] = false;
                path[pos] = -1;
            }
        }

        return false;
    }

    std::pair<bool, std::vector<int>> HamiltonianCycle(const std::vector<int> adj[], int N)
    {
        if (N == 0)
        {
            return {false, {}};
        }

        if (N == 1)
        {
            // Check for self-loop
            bool has_cycle = false;
            for (int v : adj[0])
            {
                if (v == 0)
                {
                    has_cycle = true;
                    break;
                }
            }
            return {has_cycle, {0}};
        }

        // Check if all vertices have degree >= 2
        for (int u = 0; u < N; ++u)
        {
            if (adj[u].size() < 2)
            {
                return {false, {}};
            }
        }

        std::vector<int> path(N, -1);
        std::vector<bool> visited(N, false);

        // Start at vertex 0
        path[0] = 0;
        visited[0] = true;

        bool exists = HamiltonianCycleUtil(adj, N, path, visited, 1);

        return {exists, exists ? path : std::vector<int>()};
    }

    bool HasEulerianCycle(const std::vector<int> adj[], int N)
    {
        std::vector<int> in_degree(N, 0);

        // Calculate in-degrees for all vertices
        for (int u = 0; u < N; ++u)
        {
            for (int v : adj[u])
            {
                if (v < 0 || v >= N)
                    continue; // Ensure valid vertex index
                in_degree[v]++;
            }
        }

        // Check if all vertices have equal in-degree and out-degree
        for (int u = 0; u < N; ++u)
        {
            if (in_degree[u] != static_cast<int>(adj[u].size()))
            {
                return false;
            }
        }

        // Check if the graph is strongly connected
        return CountStronglyConnectedComponents(adj, N) == 1;
    }

    std::pair<int, std::vector<std::tuple<int, int, int>>> FordFulkerson(const std::vector<std::pair<int, int>> adj[], int N, int source, int sink)
    {
        struct Edge
        {
            int to, rev, capacity;
        };

        std::vector<std::vector<Edge>> residualGraph(N);

        // Build residual graph with forward and reverse edges
        for (int u = 0; u < N; ++u)
        {
            for (const auto &[v, c] : adj[u])
            {
                int rev_u = residualGraph[v].size();
                int rev_v = residualGraph[u].size();
                residualGraph[u].push_back(Edge{v, rev_u, c});
                residualGraph[v].push_back(Edge{u, rev_v, 0});
            }
        }

        int max_flow = 0;

        // Edmonds-Karp algorithm using BFS to find augmenting paths
        while (true)
        {
            std::vector<int> parent(N, -1);
            std::queue<int> q;
            q.push(source);
            parent[source] = -2;

            bool found = false;
            while (!q.empty() && !found)
            {
                int u = q.front();
                q.pop();

                for (const Edge &e : residualGraph[u])
                {
                    if (parent[e.to] == -1 && e.capacity > 0)
                    {
                        parent[e.to] = u;
                        q.push(e.to);
                        if (e.to == sink)
                        {
                            found = true;
                            break;
                        }
                    }
                }
            }

            if (!found)
                break;

            // Determine the minimum residual capacity on the augmenting path
            int current = sink;
            int min_capacity = INT_MAX;
            while (current != source)
            {
                int prev = parent[current];
                for (const Edge &e : residualGraph[prev])
                {
                    if (e.to == current && e.capacity > 0)
                    {
                        min_capacity = std::min(min_capacity, e.capacity);
                        break;
                    }
                }
                current = prev;
            }

            // Augment the path and update residual capacities
            current = sink;
            while (current != source)
            {
                int prev = parent[current];
                for (Edge &e : residualGraph[prev])
                {
                    if (e.to == current)
                    {
                        e.capacity -= min_capacity;
                        residualGraph[current][e.rev].capacity += min_capacity;
                        break;
                    }
                }
                current = prev;
            }

            max_flow += min_capacity;
        }

        // BFS to find nodes reachable from source in the residual graph
        std::vector<bool> visited(N, false);
        std::queue<int> q_visited;
        q_visited.push(source);
        visited[source] = true;

        while (!q_visited.empty())
        {
            int u = q_visited.front();
            q_visited.pop();

            for (const Edge &e : residualGraph[u])
            {
                if (e.capacity > 0 && !visited[e.to])
                {
                    visited[e.to] = true;
                    q_visited.push(e.to);
                }
            }
        }

        // Collect all original edges that cross from reachable to non-reachable
        std::vector<std::tuple<int, int, int>> min_cut;
        for (int u = 0; u < N; ++u)
        {
            if (visited[u])
            {
                for (const auto &[v, c] : adj[u])
                {
                    if (!visited[v])
                    {
                        min_cut.emplace_back(u, v, c);
                    }
                }
            }
        }

        return {max_flow, min_cut};
    }

    std::vector<std::vector<std::pair<int, int>>> BuildResidualGraph(const std::vector<std::pair<int, int>> adj[], int N, const std::vector<std::vector<int>> &flow)
    {
        std::vector<std::vector<std::pair<int, int>>> residual(N);
        for (int u = 0; u < N; ++u)
        {
            for (size_t i = 0; i < adj[u].size(); ++i)
            {
                const auto &edge = adj[u][i];
                int v = edge.first;
                int capacity = edge.second;
                int f = flow[u][i];

                // Forward edge with residual capacity
                int residual_forward = capacity - f;
                if (residual_forward > 0)
                {
                    residual[u].emplace_back(v, residual_forward);
                }

                // Backward edge with residual capacity
                int residual_backward = f;
                if (residual_backward > 0)
                {
                    residual[v].emplace_back(u, residual_backward);
                }
            }
        }
        return residual;
    }

    int EdmondKarp(const std::vector<std::pair<int, int>> adj[], int N, int source, int sink)
    {
        // Build residual graph using tuples (to, capacity, reverse_edge_index)
        std::vector<std::vector<std::tuple<int, int, int>>> residual(N);
        for (int u = 0; u < N; ++u)
        {
            for (const auto &edge : adj[u])
            {
                int v = edge.first;
                int cap = edge.second;
                residual[u].emplace_back(v, cap, static_cast<int>(residual[v].size()));
                residual[v].emplace_back(u, 0, static_cast<int>(residual[u].size() - 1));
            }
        }

        int max_flow = 0;

        while (true)
        {
            std::vector<int> parent(N, -1);
            std::vector<int> parent_edge(N, -1);
            std::vector<int> min_cap(N, 0);
            std::queue<int> q;
            q.push(source);
            parent[source] = -2;
            min_cap[source] = INT_MAX;

            bool found_path = false;
            while (!q.empty())
            {
                int u = q.front();
                q.pop();

                for (size_t i = 0; i < residual[u].size(); ++i)
                {
                    const auto &edge = residual[u][i];
                    int v = std::get<0>(edge);
                    int cap = std::get<1>(edge);
                    if (cap > 0 && parent[v] == -1)
                    {
                        parent[v] = u;
                        parent_edge[v] = i;
                        min_cap[v] = std::min(min_cap[u], cap);
                        if (v == sink)
                        {
                            // Update flow and residual capacities
                            int flow = min_cap[sink];
                            max_flow += flow;
                            int curr = v;
                            while (curr != source)
                            {
                                int prev = parent[curr];
                                int e_idx = parent_edge[curr];
                                // Update forward edge
                                std::get<1>(residual[prev][e_idx]) -= flow;
                                // Update reverse edge
                                int rev_idx = std::get<2>(residual[prev][e_idx]);
                                std::get<1>(residual[curr][rev_idx]) += flow;
                                curr = prev;
                            }
                            found_path = true;
                            break;
                        }
                        q.push(v);
                    }
                }
                if (found_path)
                    break;
            }

            if (!found_path)
                break;
        }

        return max_flow;
    }

    bool IsBipartite(const std::vector<int> adj[], int N)
    {
        std::vector<int> color(N, -1);
        std::queue<int> q;

        for (int start = 0; start < N; ++start)
        {
            if (color[start] == -1)
            {
                color[start] = 0;
                q.push(start);

                while (!q.empty())
                {
                    int u = q.front();
                    q.pop();

                    for (int v : adj[u])
                    {
                        if (color[v] == -1)
                        {
                            color[v] = color[u] ^ 1; // Toggle color between 0 and 1
                            q.push(v);
                        }
                        else if (color[v] == color[u])
                        {
                            return false;
                        }
                    }
                }
            }
        }
        return true;
    }

    // Helper function to compute the Longest Prefix Suffix (LPS) array for the KMP algorithm
    std::vector<int> ComputeLPS(const std::string &pattern)
    {
        int m = pattern.size();
        std::vector<int> lps(m, 0);
        int len = 0; // Length of the previous longest prefix suffix

        for (int i = 1; i < m;)
        {
            if (pattern[i] == pattern[len])
            {
                len++;
                lps[i] = len;
                i++;
            }
            else
            {
                if (len != 0)
                {
                    len = lps[len - 1];
                }
                else
                {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        return lps;
    }

    // KMP algorithm to find all occurrences of a pattern in a text
    std::vector<int> KMP(const std::string &text, const std::string &pattern)
    {
        std::vector<int> matches;
        int n = text.size();
        int m = pattern.size();
        if (m == 0)
            return matches; // Handle empty pattern case

        std::vector<int> lps = ComputeLPS(pattern);
        int i = 0; // Index for text
        int j = 0; // Index for pattern

        while (i < n)
        {
            if (pattern[j] == text[i])
            {
                i++;
                j++;
            }

            if (j == m)
            {
                // Pattern found at index i - j
                matches.push_back(i - j);
                j = lps[j - 1];
            }
            else if (i < n && pattern[j] != text[i])
            {
                // Mismatch after j matches
                if (j != 0)
                {
                    j = lps[j - 1];
                }
                else
                {
                    i++;
                }
            }
        }

        return matches;
    }

    struct Edge
    {
        int to, rev, capacity;
    };

    namespace
    {
        void add_edge(std::vector<std::vector<Edge>> &graph, int u, int v, int capacity)
        {
            Edge forward = {v, static_cast<int>(graph[v].size()), capacity};
            Edge backward = {u, static_cast<int>(graph[u].size()), 0};
            graph[u].push_back(forward);
            graph[v].push_back(backward);
        }
    }

    int BipartiteMaxMatching(const std::vector<int> adj[], int m, int n)
    {
        const int source = m + n;
        const int sink = source + 1;
        const int total_nodes = sink + 1;
        std::vector<std::vector<Edge>> graph(total_nodes);

        // Connect source to left partition (0 to m-1)
        for (int u = 0; u < m; ++u)
        {
            add_edge(graph, source, u, 1);
        }

        // Connect right partition (m to m+n-1) to sink
        for (int v = m; v < m + n; ++v)
        {
            add_edge(graph, v, sink, 1);
        }

        // Add edges from left to right based on the bipartite graph
        for (int u = 0; u < m; ++u)
        {
            for (int neighbor : adj[u])
            {
                add_edge(graph, u, neighbor, 1);
            }
        }

        int max_flow = 0;
        std::vector<int> parent(total_nodes);

        while (true)
        {
            std::fill(parent.begin(), parent.end(), -1);
            std::queue<int> q;
            q.push(source);
            parent[source] = -2;

            while (!q.empty() && parent[sink] == -1)
            {
                int u = q.front();
                q.pop();

                for (const Edge &e : graph[u])
                {
                    if (parent[e.to] == -1 && e.capacity > 0)
                    {
                        parent[e.to] = u;
                        q.push(e.to);
                    }
                }
            }

            if (parent[sink] == -1)
                break; // No augmenting path found

            // Find minimum residual capacity along the augmenting path
            int flow = INT_MAX;
            for (int v = sink; v != source; v = parent[v])
            {
                int u = parent[v];
                for (const Edge &e : graph[u])
                {
                    if (e.to == v && e.capacity < flow)
                    {
                        flow = e.capacity;
                        break;
                    }
                }
            }

            // Update residual capacities and reverse edges
            for (int v = sink; v != source; v = parent[v])
            {
                int u = parent[v];
                for (Edge &e : graph[u])
                {
                    if (e.to == v)
                    {
                        e.capacity -= flow;
                        graph[v][e.rev].capacity += flow;
                        break;
                    }
                }
            }

            max_flow += flow;
        }

        return max_flow;
    }

    bool HavelHakimi(std::vector<int> degrees)
    {
        // Check if the sum of degrees is even and all degrees are non-negative
        int sum = std::accumulate(degrees.begin(), degrees.end(), 0);
        if (sum % 2 != 0)
            return false;

        for (int d : degrees)
        {
            if (d < 0)
                return false;
        }

        while (true)
        {
            // Remove all zeros from the end to handle trivial cases faster
            std::sort(degrees.begin(), degrees.end(), std::greater<int>());
            if (degrees.empty())
                return true;
            if (degrees.front() == 0)
            {
                // All elements must be zero to be valid
                return std::all_of(degrees.begin(), degrees.end(), [](int d)
                                   { return d == 0; });
            }

            int max_degree = degrees[0];
            degrees.erase(degrees.begin());

            if (max_degree > degrees.size())
            {
                return false;
            }

            for (int i = 0; i < max_degree; ++i)
            {
                if (--degrees[i] < 0)
                {
                    return false;
                }
            }
        }
    }

    std::pair<bool, std::vector<std::vector<int>>> FloydWarshall(const std::vector<std::pair<int, int>> adj[], int N)
    {
        std::vector<std::vector<int>> dist(N, std::vector<int>(N, INT_MAX));

        // Initialize diagonal to 0 and populate direct edges
        for (int i = 0; i < N; ++i)
        {
            dist[i][i] = 0;
            for (const auto &[v, w] : adj[i])
            {
                if (w < dist[i][v])
                {
                    dist[i][v] = w;
                }
            }
        }

        // Compute all-pairs shortest paths
        for (int k = 0; k < N; ++k)
        {
            for (int i = 0; i < N; ++i)
            {
                for (int j = 0; j < N; ++j)
                {
                    if (dist[i][k] != INT_MAX && dist[k][j] != INT_MAX)
                    {
                        dist[i][j] = std::min(dist[i][j], dist[i][k] + dist[k][j]);
                    }
                }
            }
        }

        // Check for negative cycles
        bool hasNegativeCycle = false;
        for (int i = 0; i < N; ++i)
        {
            if (dist[i][i] < 0)
            {
                hasNegativeCycle = true;
                break;
            }
        }

        return {!hasNegativeCycle, dist};
    }

} // namespace GraphAlgorithms

#endif // GRAPH_ALGORITHMS_H