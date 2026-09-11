# CEB promotion copy

## Title

I fed documents to AI all afternoon. Then I found out it had never read the CEB files.

## Copy

This project started with a batch of documents my wife gave me.

I did what most people do now: I uploaded the material to AI and started working. The upload looked fine. The conversation looked fine. The analysis looked fine. Later, when I checked the source, I discovered that some files were Founder CEB documents and the actual text had never been read.

The uncomfortable part is that a failed parse does not always look like a failure. The system may not say, “I cannot open this.” It may continue with a plausible summary. You think the material was part of the reasoning, when it was not.

DOC and DOCX are usually manageable. PDF fits the AI workflow much more naturally. CEB sits in the awkward middle: the Founder reader can be slow, its export flow is inconvenient, and one-file-at-a-time export becomes absurd when a folder contains ten or twenty documents.

So I built CEB.

Drop in a folder and get:

- PDF for human review;
- Markdown for AI processing;
- TXT for plain-text workflows;
- JSON reports with version, page count, algorithm, hash, and output paths.

CEB does not pretend that every legacy file is universally solvable. The current release is limited to verified Founder CEB v3 paths and fails clearly on structures it does not understand. That is a feature for document work: if the source was not read, say so.

A small format problem can become a large operational problem. A batch conversion entry point turns it back into a short, checkable step in the workflow.

Open source project: **CEB | Founder CEB to PDF, Markdown and TXT for AI-readable enterprise workflows.**

X: [Who Is the Expert](https://x.com/dboy_yi2025)

Xiaohongshu: [谁是专家](https://www.xiaohongshu.com/user/profile/64dd6c680000000001011d25)

WeChat: search for **谁是专家**

![Search for 谁是专家 on WeChat](../assets/wechat-who-is-expert.png)

## One-line version

The problem is not always that AI is not smart enough. Sometimes the source was never readable in the first place. CEB batch-converts verified Founder CEB files into PDF, Markdown, and TXT so legacy material can re-enter an AI-readable workflow.
