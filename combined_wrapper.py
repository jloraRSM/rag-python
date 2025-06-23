from typing import List, Dict, Any
from rag_source_base import RAGSourceBase
from vectorize_wrapper import VectorizeWrapper
import re

class CombinedWrapper(RAGSourceBase):
    """RAG source that combines document retrieval with recipe search."""
    
    def __init__(self):
        # Initialize the Vectorize wrapper for document retrieval
        self.vectorize = VectorizeWrapper()
        
        # Initialize built-in recipes
        self.recipes = {
            "chocolate": {
                "title": "Rich Chocolate Brownies",
                "readyInMinutes": 45,
                "servings": 16,
                "ingredients": [
                    "1 cup unsalted butter",
                    "2 cups granulated sugar",
                    "4 large eggs",
                    "2 teaspoons vanilla extract",
                    "1 cup unsweetened cocoa powder",
                    "1 cup all-purpose flour",
                    "¼ teaspoon salt",
                    "1 cup semi-sweet chocolate chips"
                ],
                "instructions": """
1. Preheat oven to 350°F (175°C). Line a 9x13 inch pan with parchment paper.
2. Melt butter in a large microwave-safe bowl.
3. Stir in sugar until well combined.
4. Add eggs one at a time, mixing well after each addition.
5. Stir in vanilla extract.
6. Add cocoa powder, flour, and salt. Mix until just combined.
7. Fold in chocolate chips.
8. Pour into prepared pan and spread evenly.
9. Bake for 30-35 minutes until a toothpick comes out with a few moist crumbs.
10. Cool completely before cutting into squares."""
            },
            "almonds": {
                "title": "Honey Roasted Almonds",
                "readyInMinutes": 25,
                "servings": 8,
                "ingredients": [
                    "3 cups raw almonds",
                    "⅓ cup honey",
                    "2 tablespoons olive oil",
                    "1 teaspoon sea salt",
                    "½ teaspoon ground cinnamon",
                    "¼ teaspoon ground nutmeg",
                    "Optional: ¼ teaspoon cayenne pepper for spicy version"
                ],
                "instructions": """
1. Preheat oven to 325°F (165°C). Line a baking sheet with parchment paper.
2. In a large bowl, combine honey and olive oil.
3. Add almonds and stir until well coated.
4. Mix salt, cinnamon, and nutmeg (and cayenne if using) in a small bowl.
5. Sprinkle spice mixture over almonds and stir to coat evenly.
6. Spread almonds in a single layer on prepared baking sheet.
7. Roast for 15-20 minutes, stirring once halfway through.
8. Let cool completely. They will become crunchier as they cool.
9. Store in an airtight container."""
            },
            "apples": {
                "title": "Classic Apple Pie",
                "readyInMinutes": 75,
                "servings": 8,
                "ingredients": [
                    "6 cups sliced apples (Granny Smith or Honeycrisp)",
                    "1 tablespoon lemon juice",
                    "¾ cup granulated sugar",
                    "¼ cup brown sugar",
                    "3 tablespoons all-purpose flour",
                    "1 teaspoon ground cinnamon",
                    "¼ teaspoon ground nutmeg",
                    "¼ teaspoon salt",
                    "2 pie crusts (homemade or store-bought)",
                    "2 tablespoons butter",
                    "1 egg (for egg wash)"
                ],
                "instructions": """
1. Preheat oven to 425°F (220°C).
2. In a large bowl, toss sliced apples with lemon juice.
3. Mix together sugars, flour, cinnamon, nutmeg, and salt.
4. Add sugar mixture to apples and toss to coat.
5. Line a 9-inch pie dish with one pie crust.
6. Pour apple mixture into crust and dot with butter pieces.
7. Cover with second crust, crimp edges, and cut slits for venting.
8. Beat egg and brush over top crust.
9. Bake for 45-50 minutes until crust is golden and filling bubbles.
10. Cool for at least 30 minutes before serving."""
            },
            "bananas": {
                "title": "Moist Banana Bread",
                "readyInMinutes": 70,
                "servings": 12,
                "ingredients": [
                    "3 very ripe bananas, mashed",
                    "⅓ cup melted butter",
                    "½ cup granulated sugar",
                    "1 large egg",
                    "1 teaspoon vanilla extract",
                    "1 teaspoon baking soda",
                    "¼ teaspoon salt",
                    "1½ cups all-purpose flour",
                    "Optional: ½ cup chopped walnuts or chocolate chips"
                ],
                "instructions": """
1. Preheat oven to 350°F (175°C). Grease a 9x5 inch loaf pan.
2. In a large bowl, mix mashed bananas with melted butter.
3. Stir in sugar, egg, and vanilla extract.
4. Sprinkle baking soda and salt over mixture.
5. Stir in flour until just combined.
6. Fold in nuts or chocolate chips if using.
7. Pour batter into prepared pan.
8. Bake for 50-60 minutes until a toothpick comes out clean.
9. Let cool in pan for 10 minutes.
10. Remove from pan and cool completely on wire rack."""
            },
            "avocados": {
                "title": "Guacamole and Fresh Tortilla Chips",
                "readyInMinutes": 30,
                "servings": 6,
                "ingredients": [
                    "3 ripe avocados",
                    "1 lime, juiced",
                    "1 red onion, finely diced",
                    "2 Roma tomatoes, diced",
                    "1/3 cup fresh cilantro, chopped",
                    "1 jalapeño pepper, seeded and minced",
                    "2 cloves garlic, minced",
                    "½ teaspoon salt",
                    "For the chips:",
                    "12 corn tortillas",
                    "2 tablespoons olive oil",
                    "1 teaspoon salt"
                ],
                "instructions": """
1. For the guacamole:
   - Cut avocados in half, remove pit, and scoop into a bowl
   - Mash avocados with a fork, leaving some chunks
   - Add lime juice and mix well
   - Fold in onion, tomatoes, cilantro, jalapeño, and garlic
   - Season with salt and adjust to taste
   - Cover with plastic wrap pressed against surface and refrigerate

2. For the tortilla chips:
   - Preheat oven to 350°F (175°C)
   - Cut each tortilla into 6 wedges
   - Arrange on baking sheets in a single layer
   - Brush both sides with olive oil and sprinkle with salt
   - Bake 12-15 minutes until crisp and lightly golden
   - Let cool for 5 minutes before serving

Serve guacamole with fresh tortilla chips. To prevent browning, keep the pit in the guacamole and plastic wrap pressed directly on surface."""
            },
            "chia": {
                "title": "Overnight Chia Pudding with Berry Compote",
                "readyInMinutes": 15,
                "servings": 4,
                "ingredients": [
                    "For the chia pudding:",
                    "½ cup chia seeds",
                    "2 cups almond milk (or any plant-based milk)",
                    "2 tablespoons maple syrup",
                    "1 teaspoon vanilla extract",
                    "Pinch of salt",
                    "For the berry compote:",
                    "2 cups mixed berries (fresh or frozen)",
                    "2 tablespoons maple syrup",
                    "1 tablespoon lemon juice",
                    "Optional toppings:",
                    "Sliced almonds",
                    "Fresh berries",
                    "Coconut flakes"
                ],
                "instructions": """
1. For the chia pudding:
   - In a large bowl, whisk together almond milk, maple syrup, vanilla, and salt
   - Add chia seeds and whisk well
   - Let sit for 5 minutes, then whisk again to prevent clumping
   - Cover and refrigerate overnight (or at least 4 hours)

2. For the berry compote:
   - In a saucepan, combine berries, maple syrup, and lemon juice
   - Bring to a simmer over medium heat
   - Cook for 5-10 minutes until berries break down and sauce thickens
   - Let cool completely

3. To serve:
   - Stir the chia pudding well
   - Divide into serving bowls
   - Top with berry compote
   - Add optional toppings as desired

Store separately in airtight containers for up to 5 days."""
            },
            "lentils": {
                "title": "Spiced Lentil and Vegetable Soup",
                "readyInMinutes": 45,
                "servings": 6,
                "ingredients": [
                    "1½ cups red lentils, rinsed",
                    "2 tablespoons olive oil",
                    "1 large onion, diced",
                    "3 carrots, diced",
                    "3 celery stalks, diced",
                    "4 garlic cloves, minced",
                    "2 teaspoons ground cumin",
                    "1 teaspoon ground turmeric",
                    "1 teaspoon ground coriander",
                    "½ teaspoon red pepper flakes",
                    "1 can (14 oz) diced tomatoes",
                    "6 cups vegetable broth",
                    "2 cups fresh spinach",
                    "1 lemon, juiced",
                    "Salt and pepper to taste",
                    "Fresh cilantro for garnish"
                ],
                "instructions": """
1. Heat olive oil in a large pot over medium heat.
2. Add onion, carrots, and celery. Cook until softened, about 5 minutes.
3. Add garlic and spices (cumin, turmeric, coriander, red pepper flakes).
4. Cook for 1 minute until fragrant, stirring constantly.
5. Add lentils, diced tomatoes, and vegetable broth.
6. Bring to a boil, then reduce heat and simmer for 20-25 minutes.
7. Add spinach and cook until wilted, about 2 minutes.
8. Stir in lemon juice and season with salt and pepper.
9. Serve hot, garnished with fresh cilantro.

Note: This soup will thicken as it cools. Add more broth when reheating if desired."""
            }
        }

    def _check_recipe_keywords(self, text: str) -> bool:
        """Check if the text contains recipe-related keywords."""
        recipe_keywords = [
            r"recipe",
            r"cook",
            r"make",
            r"prepare",
            r"how to",
            r"ingredients",
            r"instructions",
            r"bake",
            r"roast"
        ]
        return any(re.search(keyword, text.lower()) for keyword in recipe_keywords)

    def _get_recipe_matches(self, question: str) -> List[Dict[str, Any]]:
        """Get matching recipes for the question."""
        matching_recipes = []
        for keyword, recipe in self.recipes.items():
            if keyword in question.lower():
                doc = {
                    "title": f"🥘 {recipe['title']}",  # Added emoji to distinguish recipe results
                    "content": f"Recipe for {recipe['title']}\n\n"
                              f"⏱️ Ready in: {recipe['readyInMinutes']} minutes\n"
                              f"👥 Servings: {recipe['servings']}\n\n"
                              f"📝 Ingredients:\n" + 
                              "\n".join([f"• {ing}" for ing in recipe["ingredients"]]) +
                              f"\n\n👨‍🍳 Instructions:\n{recipe['instructions']}"
                }
                matching_recipes.append(doc)
        return matching_recipes

    def retrieve_documents(self, question: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve both relevant documents and recipes based on the question.
        
        Args:
            question: The query string
            num_results: Number of results to return
            
        Returns:
            List of documents with relevant content, including recipes if applicable
        """
        documents = []
        
        # Always get RAG results first
        rag_docs = self.vectorize.retrieve_documents(question, num_results)
        documents.extend(rag_docs)
        
        # If the question seems recipe-related, add recipe results
        if self._check_recipe_keywords(question):
            recipe_docs = self._get_recipe_matches(question)
            if recipe_docs:
                documents.extend(recipe_docs)
            else:
                # Add available recipes info if no specific recipe found
                documents.append({
                    "title": "📖 Available Recipes",
                    "content": "I don't have a specific recipe that matches your request, but I know recipes for: " + 
                              ", ".join(self.recipes.keys()) + ".\n" +
                              "Try asking for one of these recipes!"
                })
        
        return documents[:num_results]

    def get_required_env_vars(self) -> List[str]:
        """Get list of required environment variables."""
        # Return Vectorize requirements since we're using it
        return self.vectorize.get_required_env_vars() 