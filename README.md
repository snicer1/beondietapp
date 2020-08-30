1. Running application 

- To run this application you need to have linux and docker and docker-compose installed. 
- When the repository is downloaded, you just need to run coman docker-compose up. 
The image will be built on 8080 application port and 5001 database port. If you want to change
ports, please edit docker-compose.yml file  

2. Testing:
 - Go to 0.0.0.0/graphiql and from folder samples you can add, modify, delete ingredients and receipts. 
 At the beginning please add ingredients (createIngredient from mutationSample), just copy, fulfil fields from example and run on 0.0.0.0/graphiql.
When all needed ingredients are added, you can compose your recipe (createRecipe from mutationSample).

- To check what you added you can use queries from querySample. You can check specific recipe, ingredients or all of receipts, ingredients

