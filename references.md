Reference 1: Kuhn, H.W. (1955), The Hungarian method for the assignment problem†. Naval Research Logistics, 2: 83-97. https://doi.org/10.1002/nav.3800020109

Summary: 
Given an n x n table of scores rating how well each person performs each job, find the one-to-one assignment of persons to jobs that maximizes the total score. Solution method. He shows that results from two Hungarian mathematicians (Konig and Egervary) can be adapted into an efficient algorithm, "the Hungarian method.

Reference 2: Munkres, J. (1957). "Algorithms for the Assignment and Transportation Problems." J. SIAM, 5(1), 32–38.

Summary: Proves the Hungarian algorithm correct, then extends it to the transportation problem (capacity > 1). This is what makes it work for hospitals.

Reference 3: Bertsekas, D. P. (1981). "A new algorithm for the assignment problem." Mathematical Programming, 21(1), 152–171.

Summary: Auction alternative: unassigned doctors bid up prices on hospitals instead of searching augmenting paths. Claims ~10x faster than Hungarian at scale.