# BDD_June_James_Ansh

## Introduction

This project models the assignment of doctors to hospitals using doctors' rankings and hospital capacities. The goal is to assign each doctor to exactly one hospital while minimizing total assignment loss and respecting each hospital's upper bound. An interference function, `g()`, converts the ranking matrix into assignment costs, allowing the objective to reflect how different rankings are valued. The resulting optimization problem is represented as a minimum cost flow network, where each unit of flow corresponds to one doctor's assignment.

## Assumptions

- Each doctor receives exactly one hospital.
- Doctors will declare their rankings honestly.
- All doctors can be assigned: total hospital capacity is at least the number of doctors, $\sum_{j=1}^{m} C_j \ge n$.
- Hospitals have only upper bounds on the number of doctors they receive; there are no minimum staffing requirements.
- Preferences are one-sided: doctors rank hospitals.
- Rankings are complete, with each rank assigned to only one hospital. Every hospital is an available assignment for every doctor.

## Formulae

Define the input ranking for doctor $i$ and hospital $j$ as $R_{ij}$, where a smaller rank indicates a more preferred hospital.

For rankings submitted by $n$ doctors over $m$ hospitals, the ranking matrix is:

$$
M_R =
\begin{bmatrix}
R_{11} & R_{12} & \cdots & R_{1m} \\
R_{21} & R_{22} & \cdots & R_{2m} \\
\vdots & \vdots & \ddots & \vdots \\
R_{n1} & R_{n2} & \cdots & R_{nm}
\end{bmatrix}.
$$

The **interference function** is denoted by `g()`. It maps $M_R$ to a fixed $n \times m$ matrix of assignment costs, $g(M_R)$, before optimization. Its specific form can be chosen to reflect the intended loss associated with rankings. If $g$ is the identity function, the costs are simply the original rankings.

Define the decision variable $X_{ij}$ as:

$$
X_{ij} =
\begin{cases}
1, & \text{if doctor } i \text{ is assigned to hospital } j, \\
0, & \text{otherwise}.
\end{cases}
$$

The decision matrix is:

$$
M_X =
\begin{bmatrix}
X_{11} & X_{12} & \cdots & X_{1m} \\
X_{21} & X_{22} & \cdots & X_{2m} \\
\vdots & \vdots & \ddots & \vdots \\
X_{n1} & X_{n2} & \cdots & X_{nm}
\end{bmatrix}.
$$

Assignment loss can be represented as:

$$
\sum \left(g(M_R) \odot M_X\right)
= \sum_{i=1}^{n}\sum_{j=1}^{m} [g(M_R)]_{ij}X_{ij}.
$$

Here, $\odot$ denotes element-wise multiplication, and the matrix sum adds all entries. Only the costs of selected assignments contribute to the loss.

The computer optimizes the decision matrix:

$$
\min_{M_X}\; \sum \left(g(M_R) \odot M_X\right),
$$

subject to:

$$
\sum_{j=1}^{m} X_{ij} = 1
\qquad \text{for each doctor } i,
$$

$$
\sum_{i=1}^{n} X_{ij} \le C_j
\qquad \text{for each hospital } j,
$$

$$
X_{ij} \in \{0,1\}.
$$

Here, $C_j$ is the nonnegative integer capacity of hospital $j$. These constraints ensure that every doctor receives exactly one hospital and that hospital capacities are respected.

We can solve this problem using a **minimum cost flow** system with the following network:

$$
S \longrightarrow D_{1\ldots n} \longrightarrow H_{1\ldots m} \longrightarrow T.
$$

$S$ is the source, $D_i$ represents doctor $i$, $H_j$ represents hospital $j$, and $T$ is the sink. Each doctor is connected to every hospital.

| Edge | Capacity | Cost per unit of flow |
| --- | --- | --- |
| $S \to D_i$ | $1$ | $0$ |
| $D_i \to H_j$ | $1$ | $[g(M_R)]_{ij}$ |
| $H_j \to T$ | $C_j$ | $0$ |

When $g$ is the identity function, the cost of $D_i \to H_j$ is $R_{ij}$. The edge $H_j \to T$ limits the total number of doctors assigned to hospital $j$ to $C_j$; each assigned doctor uses one unit of that capacity.

The network must send **exactly $n$ units of flow** from $S$ to $T$ while minimizing total cost. This requirement ensures that all doctors are assigned and rules out the empty, zero-flow solution. Flow conservation requires each doctor's unit of flow to continue through a hospital to the sink.

With integer capacities and a required flow of $n$, a minimum cost integral flow yields the assignment directly: $X_{ij}=1$ when one unit of flow passes through $D_i \to H_j$, and $X_{ij}=0$ otherwise.
