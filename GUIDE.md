# Guide to completing ICS 3202 Practical Exercise 3

This pack contains an editable `design.md` starter. Open it in VS Code, any text editor, or GitHub's file editor. Replace every `TODO`, check the example road connections against the map used in class, and insert your group's measured distances. This is a scaffold, not a completed submission.

## 1. Understand the deliverable

Your group must create one original GitHub repository named **PS-Agents**, with the assignment in **design.md**. That document must contain the answers, digital diagrams, distance calculations, and genuine groupwork evidence. Each member should have their own fork and an identifiable contribution. One member submits the **original repository link** to e-learning before the lecturer's deadline.

The supplied slide deck explains goal formulation, problem formulation, search, execution, path cost and abstraction. It does not supply an extractable class highway map. Use the actual class map or the lecturer's Google Maps reference to confirm the network. The slides' example Nairobi–Nakuru–Nyahururu distances are teaching examples, not measurements for this assignment.

## 2. Assign work and record participation

Hold a real group meeting. Record the date, attendees, work assigned, discussion, and decisions. Suggested allocation:

| Task | Work to produce |
| --- | --- |
| PEAS and environment | Explain the agent and justify all five classifications |
| Network and abstraction | Confirm towns, road connections and both diagrams |
| Measurements and search | Collect distances and carry out uniform-cost search |
| Integration and review | Merge contributions, verify rendering and prepare submission |

Everyone should review the final document. Fill in the member table and minutes in `design.md`. Do not invent attendance, photos or contributions. The brief assigns 50% of the final score to teamwork. Minutes are an allowed alternative to a photo; a photo must show all participating members' faces. Use minutes if your group prefers not to publish faces.

## 3. Complete Question 1

The starter contains a PEAS table for a self-driving trailer. Adapt it to the scenario discussed in class. Explain performance, environment, actuators and sensors separately.

For the five environment dimensions, the starter uses observability, determinism, episodic/sequential, static/dynamic and discrete/continuous. Verify these are the five your lecturer expects. If the lecturer included single-agent/multi-agent instead of one of them, use the lecturer's five; road driving is multi-agent because other drivers act independently.

Keep two levels distinct: actual driving is partially observable, stochastic, sequential, dynamic and continuous; the simplified route-search model can use a known, deterministic, static, discrete graph. Towns are discrete planning states even though steering and braking operate continuously.

## 4. Choose the towns and roads for Question 2

Use the class map to include all four required regions. A possible starting set is:

| Region | Candidate towns to check |
| --- | --- |
| Nairobi | Nairobi |
| Central Highlands | Nyeri, Nyahururu |
| Rift Valley | Naivasha, Nakuru, Narok, Kericho |
| Lake Victoria Basin | Kisii, Kisumu |

These are proposed planning nodes, not a claim that they exactly reproduce the class map. Adjust regional grouping to the lecturer's convention, especially for boundary towns. Add or remove nodes and links to match that map. Do not discard a route just because it initially looks longer: establish its cost first or justify a valid pruning rule.

Abstraction means retaining towns, road links, legal travel direction and distance, while leaving out individual bends, buildings and lane-level actions. At this level an action is 'drive from Nairobi to Naivasha', rather than each steering movement.

Every arrow must represent a valid road segment in your model. An abstract segment can pass through smaller towns that you deliberately omit. Avoid giving one edge a Maps route that silently passes through another retained node; split it at that node so your model remains consistent.

For a two-way road, use two arrows. Reverse distances may differ; measure them separately or state an explicit symmetric-distance assumption. Include only routes your model regards as legal and feasible for the trailer. Ordinary Google Maps driving directions do not by themselves establish truck clearance or weight suitability; state that feasibility is assumed for this classroom distance model unless you verify it separately.

## 5. Measure edge distances with Google Maps

1. Open the Google Maps reference supplied by your lecturer.
2. Choose Directions and driving mode.
3. Enter the first town and the next connected town. Use consistent endpoints, such as the same central landmark whenever a town is used.
4. Select the road corridor represented by your edge. Maps may suggest several alternatives; record the selected corridor or via point.
5. Record the **road distance in kilometres**, access date, endpoints, route description and a copied directions link in the edge table.
6. Repeat for every edge. For reverse arrows, measure separately unless your documented model assumes equal costs.
7. Replace matching `TODO` labels in the graph with these values.

Do not use straight-line 'Measure distance' values. Do not mix the distance from one Maps alternative with another alternative's road corridor. Minimise distance as instructed, even if a different route is faster. Keep the same road/toll avoidance settings throughout.

Example search: 'Nairobi to Naivasha driving distance Google Maps'. Then inspect the actual directions result. A generic search snippet is weaker evidence than your selected directions route.

## 6. Edit the directed graph and search tree

Both diagrams in `design.md` use Mermaid, an editable text diagram format supported in GitHub Markdown. Edit town labels, arrows and distances inside the fenced `mermaid` blocks, then check GitHub's rendered preview.

The graph represents road connectivity and may contain cycles. The search tree represents route histories from Nairobi. Different tree nodes can contain the same town reached by different routes. The starter tree is explicitly a **partial tree**; extend it to reflect your final network and the search you actually perform. State where branches are omitted and why. Do not present a partial illustrative tree as a complete search trace.

Backtracking to an ancestor can be pruned when all edge distances are positive, because it adds cost without improving the route. For graph search, keep the cheapest known cost to each town and discard more expensive duplicates. These are different reasons for pruning; label them accurately.

## 7. Solve Question 3 with uniform-cost search

Use uniform-cost search (equivalent to Dijkstra's method for this non-negative weighted graph). Breadth-first search minimises edge count, which need not minimise distance.

1. Set Nairobi's cumulative cost to 0 and all other towns to infinity.
2. Put Nairobi on the frontier.
3. Remove the frontier town with the smallest cumulative cost `g`.
4. If this removed town is Kisumu, stop: its cost is optimal in the model.
5. Otherwise, examine each outgoing edge. Candidate cost = current `g` + edge distance.
6. If this is cheaper than the stored cost for its destination, replace that cost, record the predecessor, and update the frontier.
7. Repeat. If the frontier empties without reaching Kisumu, no route exists in the graph.
8. Follow predecessors from Kisumu back to Nairobi, reverse the sequence, and add its segment distances.

Record each expansion and the updated frontier in the search table. Use alphabetical order to break equal-cost ties consistently. Do not stop when Kisumu is merely first generated; stop when its minimum-cost entry is removed from the frontier.

Arithmetic example only, using invented numbers: Nairobi → A costs 50 km; A → Kisumu costs 80 km; total = 130 km. Another route costing 40 + 100 = 140 km loses. These numbers are not Kenyan road measurements and must not appear as evidence in your submission.

Comparing two or three selected routes is useful supporting arithmetic, but alone does not prove optimality over a graph containing other routes. The uniform-cost trace supplies that justification. Your conclusion should say 'shortest route within the modelled network and recorded distances', since an abstract class network may omit real roads.

## 8. Create and edit the GitHub repository

Use GitHub in your browser; no terminal setup is required.

1. One group member creates a new repository named exactly `PS-Agents`.
2. Choose visibility that allows the lecturer and team to access it and supports the required forks. A public repository is straightforward if your group is comfortable publishing the contents; check course requirements first.
3. In the repository, use **Add file → Upload files** to upload `design.md` from this pack. Do not upload this guide as your assignment answer.
4. Commit with a useful description, such as 'Add assignment structure'.
5. Open `design.md`, use the pencil/edit control, change the Markdown, preview, and commit.
6. Use Markdown tables for data and Mermaid blocks for diagrams. If adding a photo, upload it into an `images` folder and embed it in `design.md` using `![Group discussion](images/team-photo.jpg)`.

The photo can be stored as a supporting repository asset while appearing inside the same rendered answer document. Do not make the lecturer open a separate document to find any answer.

## 9. Each member forks and contributes

1. Each other member signs into their own GitHub account and opens the original repository.
2. Select **Fork** to create a copy under their account.
3. In that fork, create a branch with a clear name such as `peas-section`.
4. Edit their assigned section of `design.md`, preview, and commit with a meaningful message.
5. Open a pull request from that branch back to the **original** repository's main branch.
6. The integrator reviews and merges the pull request. Resolve overlapping edits if necessary.
7. Add the member's fork and pull-request links to the evidence table. Each member uses **Sync fork** after integration to get the final version.

The original owner already owns the original repository and normally cannot fork it into the same account. Record their original repository and commits; confirm with the lecturer if the phrase 'all members forking' has a special requirement for the owner. Everyone else should create an actual fork, not an unrelated repository with copied files.

A fork alone shows copying, not substantive participation. Real commits, reviewed pull requests, and meeting evidence show the work done. Use the original repo's history as the integration record.

## 10. Final review and submission

- [ ] Repository is named `PS-Agents`; answer file is `design.md`.
- [ ] Course, group and member details are complete.
- [ ] PEAS has all four elements; five environment dimensions have reasons.
- [ ] Town network matches the class/reference map and covers the required regions.
- [ ] Graph is directed and has distances consistent with the edge table.
- [ ] Tree starts at Nairobi, uses abstraction, and explains any omissions/pruning.
- [ ] All distances are measured, sourced and dated; no `TODO` fields remain.
- [ ] Search trace and arithmetic agree; conclusion states the scope of optimality.
- [ ] Genuine minutes or an appropriate group photo appear within `design.md`.
- [ ] Fork and contribution links work for the participating members.
- [ ] Mermaid diagrams, tables and any images render correctly on GitHub.
- [ ] Lecturer can access the original repository.
- [ ] One member submits its URL to e-learning before the stated deadline.

## Reference documentation

- Assignment instructions and the supplied Problem Solving Agents slide deck.
- GitHub file editing: https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files
- GitHub forks: https://docs.github.com/en/pull-requests/how-tos/work-with-forks/fork-a-repo
- Pull requests from forks: https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request-from-a-fork
- Mermaid in GitHub Markdown: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams
