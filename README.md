
# WCA LangChain Model

  

## Context:

  

The WCA is a global and volunteer-driven organization that “governs competitions for mechanical puzzles that are operated by twisting groups of pieces, commonly known as 'twisty puzzles’” [[1](https://www.worldcubeassociation.org/about)]. As the organization has evolved through expanding its global footprint and spreading the unique passion of solving Rubik’s Cubes, it has needed to adapt to the intricacies of such dramatic growth. With its volunteer base stemming from such a variety of backgrounds, there has been need to establish regulations, policies, and guidelines.

While these documents help to ensure that the variety of Delegates abide by and enforce the same standards across the globe, the sheer quantity/depth of them along with the language barriers that exist within the organization make understanding the depth of these documents a remarkably difficult task. There also exists a wealth of Regulations and Guidelines with which all competitors are expected to be familiar. 

  

The tool developed here seeks to allow for quick responses to address two fundamental use cases:

 1. Questions about the WCA Regulations and Guidelines
 2. Questions about any other WCA document including the following:
    - WCA Bylaws
    - WCA Motions
    - WCA Code of Conduct
    - WCA Vision and Strategy
    - WCA Minutes
    - WCA Financial Reports
    - WCA Competition Requirements Policy
    - WCA Dues System
    - WCA Equipment Funding Policy
    - WCA Logo Usage Policy
    - WCA Regional Organization Support Policy
    - WCA Scramble Accountability Policy
    - WCA Travel Reimbursement Policy
  

## How does it work?

This project leverages the surge of popularity and utility in LLMs as a means of developing a chatbot for a hyper-specific use-case. We lean heavily on the use of LangChain, which is a "framework for developing applications powered by large language models (LLMs)" within Python [[3](https://python.langchain.com/docs/introduction/)]. In particular, we use the RAG pipeline -- which begins by ingesting and indexing the documents we send into it, and a retriever "takes the user query at run time, retrieves the relevant data from the index, [and] then passes that to the model [[4](https://python.langchain.com/docs/tutorials/rag/)]."

## Usage:

  

```

streamlit run app.py

```


  

## Future Steps:

  

- [ ] Adopt this approach for other sports with niche guidelines and policies (e.g., Chess).

- [ ] Continue to refine this approach and investigate methods to improve...
	- [ ] Accuracy
	- [ ] Loading time
	- [ ] User Interface


## Resources:

  

[1] https://www.worldcubeassociation.org/about
[2] https://www.youtube.com/watch?v=wUAUdEw5oxM
[3] https://python.langchain.com/docs/introduction/
[4] https://python.langchain.com/docs/tutorials/rag/