<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/kunalKumar-13/kunalKumar-13/main/assets/header-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/kunalKumar-13/kunalKumar-13/main/assets/header-light.svg">
  <img src="https://raw.githubusercontent.com/kunalKumar-13/kunalKumar-13/main/assets/header-light.svg" width="100%" alt="Kunal Kumar. Software engineer and open-source maintainer. Area Approver at Music Blocks (Sugar Labs); Computer Science at BITS Pilani.">
</picture>

I study Computer Science at BITS Pilani and write software for a living. This year I interned at Emergent (YC S24), Pronto and Ostrius AI, and I help maintain [Music Blocks](https://github.com/sugarlabs/musicblocks), the music programming environment from Sugar Labs, where I look after releases, security and infrastructure.

Most of what I build circles one question: how do you let software, AI included, act on its own without trusting it more than you can check?

[Portfolio](https://portfolio-wheat-seven-ojx94tfxx1.vercel.app/) &nbsp;·&nbsp; [LinkedIn](https://www.linkedin.com/in/sainkunal) &nbsp;·&nbsp; [Email](mailto:kunalsain0324@gmail.com) &nbsp;·&nbsp; [LeetCode](https://leetcode.com/u/sain_kunal13)

<br/>

## Experience

| Where | What I did | When |
|:--|:--|:--|
| **Pronto** | Software Engineering Intern. Rebuilt partner onboarding (V2) and the referral onboarding flow; worked through crash reports and fixed what they pointed to. | Aug&nbsp;–&nbsp;Sep&nbsp;2026 |
| **Emergent** (YC S24) | Frontend Engineering Intern. Shipped 24+ production fixes to a React/TypeScript AI app builder, and built the partner-perks upgrade flow end to end. | Jun&nbsp;–&nbsp;Aug&nbsp;2026 |
| **Ostrius AI** | Software Engineering Intern. Owned a full-stack application, including authentication, verification flows and input validation. | Apr&nbsp;–&nbsp;Jun&nbsp;2026 |
| **BITS Pilani** | Teaching Assistant, Data Structures & Algorithms. Ran problem-solving sessions for 50+ students. | May&nbsp;–&nbsp;Jun&nbsp;2026 |

<br/>

## Open source

I'm the **Area Approver for Release, Security & Infrastructure** at Music Blocks and a Reviewer for Blocks & Runtime, as listed in its [MAINTAINERS.md](https://github.com/sugarlabs/musicblocks/blob/master/MAINTAINERS.md). That means I review and merge changes to the release and CI pipeline of a tool children use in classrooms.

<!-- open-source:start -->
**75 merged pull requests** upstream: Sugar Labs 36 · Plone 11 · Zeus 10 · fortran-lang 6 · MetaBrainz 6 · Django 5 · OpenStreetMap 1. And **56 pull requests reviewed** on Music Blocks.
<!-- open-source:end -->

| Project | A few of the changes |
|:--|:--|
| Music Blocks | Releases no longer fail when the notes pass GitHub's 125k-character limit ([#9866](https://github.com/sugarlabs/musicblocks/pull/9866)). The container image is built and smoke-tested in CI ([#8718](https://github.com/sugarlabs/musicblocks/pull/8718)). Every workflow has least-privilege permissions and a timeout ([#8638](https://github.com/sugarlabs/musicblocks/pull/8638)). The service worker had never registered in production; now it does, and serves pages network-first ([#9955](https://github.com/sugarlabs/musicblocks/pull/9955)). |
| Django | A transform over an annotation alias in `values()` read the wrong field or crashed; a release blocker ([#21922](https://github.com/django/django/pull/21922)). |
| Zeus | Keychain recovery groups orphaned data by key and restores one copy of each ([#4774](https://github.com/ZeusLN/zeus/pull/4774)). Slide-to-pay waits until the embedded Lightning node is ready to send ([#5776](https://github.com/ZeusLN/zeus/pull/5776)). |
| ListenBrainz | Test coverage for the listen store, cover-art cache and email verification ([#3858](https://github.com/metabrainz/listenbrainz-server/pull/3858), [#3859](https://github.com/metabrainz/listenbrainz-server/pull/3859), [#3860](https://github.com/metabrainz/listenbrainz-server/pull/3860)). |
| fortran-lang | Environment-variable setters in stdlib ([#1208](https://github.com/fortran-lang/stdlib/pull/1208)); setup-fpm builds from source on Linux ARM64 ([#61](https://github.com/fortran-lang/setup-fpm/pull/61)). |

<br/>

## Selected projects

| Project | What it is | Built with |
|:--|:--|:--|
| **[Attest](https://github.com/kunalKumar-13/attest)** | Checks AI-proposed actions before they change financial records. An LLM suggests which orders explain a bank settlement; an independent verifier re-derives the answer without reading the suggestion, and only proven results are posted. On 500 held-out settlements: proof precision 0.952 and no wrong postings. The LLM was right in 27 of 63 hard cases, so its output is treated as a hint, never as evidence. | Python, Rust |
| **[Recall](https://github.com/kunalKumar-13/Recall-me)** | A local-first continuity OS. One keystroke brings back the tabs, files and chats you had open. No accounts, no cloud, no telemetry. [Live](https://web-seven-puce-99.vercel.app) | Python, TypeScript |
| **[Typeahead](https://github.com/kunalKumar-13/typeahead)** | Autocomplete over 120k real queries: an in-memory trie, three Redis nodes on a consistent-hash ring, and batched writes behind a write-ahead log. | Python, Redis |
| **[Support Triage](https://github.com/kunalKumar-13/deterministic-support-triage)** | Ticket triage where code owns the control flow and the LLM is a constrained analyst. Policy decides escalation, not the model. | Python |
| **[Web Agent](https://github.com/kunalKumar-13/Web-Agent)** | Perceive, decide, act: finds the right form out of nine by role matching instead of hardcoded selectors. | TypeScript, Playwright |
| **[PDFChat](https://github.com/kunalKumar-13/PDF-Reviewer)** | Page-cited answers from a PDF, or an honest refusal when the document doesn't say. [Live](https://pdf-reviewer-ten.vercel.app) | Python, FastAPI |

<details>
<summary>Other projects</summary>

<br/>

[Forge AI](https://github.com/kunalKumar-13/Video-AI), a LangGraph pipeline from story to storyboard ·
[NotebookLM](https://github.com/kunalKumar-13/NotebookLM), RAG over PDFs and CSVs ·
[StudyGenie](https://github.com/kunalKumar-13/StudyGenie), a study assistant that skips retrieval when it isn't needed ·
[HTTP Server](https://github.com/kunalKumar-13/multi-threaded-http-server), HTTP/1.1 on raw sockets ·
[Ride Sharing API](https://github.com/kunalKumar-13/rideSharingApp), Spring Boot with JWT ·
[Minutes](https://github.com/kunalKumar-13/minutes), meeting notes with full-text search ·
[Finovo](https://github.com/kunalKumar-13/Finovo-Finance), a multi-currency finance dashboard ·
[Yapster](https://github.com/kunalKumar-13/yapster), real-time chat on Socket.IO ·
[DevStash](https://github.com/kunalKumar-13/Devstash), a snippet manager ·
[Island Adventure](https://github.com/kunalKumar-13/Game-Dev), a canvas RPG

</details>

<br/>

## Recognition

- **Activate AI Fellow**, one of 15 selected from 500+ applicants
- **Ethereum Scholar Fellow**, inaugural cohort
- **Delegate**, Harvard Project for Asian and International Relations (HPAIR) 2026
- **Vice President**, Open Source Club: contributor onboarding and first upstream pull requests

<br/>

## Tools

| Area | Tools |
|:--|:--|
| Languages | Python, TypeScript and JavaScript daily; Rust, Java, C++, Go, SQL |
| Backend | FastAPI, Node.js, PostgreSQL, Redis |
| Frontend | React, Next.js |
| AI | PyTorch, FAISS, LlamaIndex, OR-Tools |
| Infrastructure | Docker, Kubernetes, GitHub Actions, Linux |

<br/>

<div align="center">

### 👾 and pac-man eats the rest

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/kunalKumar-13/kunalKumar-13/output/pacman-contribution-graph-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/kunalKumar-13/kunalKumar-13/output/pacman-contribution-graph.svg">
  <img alt="pac-man eating Kunal's contribution graph" src="https://raw.githubusercontent.com/kunalKumar-13/kunalKumar-13/output/pacman-contribution-graph.svg" width="100%">
</picture>

</div>
