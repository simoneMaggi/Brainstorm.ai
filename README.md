# Brainstorm.AI
Who does remember [Fun Search](https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/) ?


*what if we could harness the creativity of LLMs by identifying and building upon only their very best ideas?*

An LLM contains a compressed knowledge of entire humanity, It must be a perfect mate to brainstorm new ideas with! I made this project for fun in a life period of particular boredom. The idea is very basic.
It is a collaborative brainstorm whiteboard, where people can share different ideas by adding post-it on it. Behind the scene, a LLM will ingest the human ideas, and It will produce new ones directly as post-it. 


## Start the brainstorm now
Add the openai key in the env.template file, and rename It as .env.

Then simply run 
```shell
docker compose build
docker compose up -d
```

The UI will be visibile on the browser at localhost:5000

