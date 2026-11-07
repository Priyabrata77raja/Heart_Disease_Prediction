"""Static, general-education content. No medical claims of cure or diagnosis."""

# (name, category, short description, details, image key or None, emoji)
VEG = [
    ("Fruits", "Fruits", "Apples, oranges, guava, papaya and berries.",
     "Whole fruit provides fibre, vitamins and potassium. Prefer whole fruit over juice and watch portion sizes if you monitor blood sugar.", "fruits", "🍎"),
    ("Vegetables", "Vegetables", "Spinach, broccoli, carrots, tomatoes and leafy greens.",
     "Aim for a variety of colours. Steam, roast or lightly sauté with little oil and salt.", "vegetables", "🥦"),
    ("Whole Grains", "Whole grains", "Oats, brown rice, whole wheat and millets.",
     "Whole grains keep more fibre than refined grains. Swap them in gradually for white rice and refined flour.", "whole_grains", "🌾"),
    ("Healthy Fats", "Healthy fats", "Unsalted nuts, seeds and suitable unsaturated oils.",
     "Fats are energy-dense, so keep portions small (for example a small handful of unsalted nuts). Use oils sparingly.", "healthy_fats", "🥜"),
    ("Lentils and Beans", "Plant protein", "Moong dal, masoor dal, chickpeas and rajma.",
     "Pulses give protein and fibre. Cook with moderate oil and salt.", None, "🫘"),
    ("Soy and Tofu", "Plant protein", "Tofu and other suitable soy foods.",
     "Tofu works in stir-fries and curries. Check labels for added salt in processed soy products.", None, "🧈"),
    ("Plain Yogurt", "Dairy", "Unsweetened yogurt or curd.",
     "Choose plain, unsweetened versions and pair with fruit. Ask your clinician which fat level suits you.", None, "🥛"),
    ("Healthy Snacks", "Snacks", "Fresh fruit, unsalted nuts and roasted chickpeas.",
     "Plan snacks ahead so packaged, salty or sugary options are less tempting.", None, "🍿"),
]
NONVEG = [
    ("Fish", "Fish", "Sardines, salmon and mackerel.",
     "Oily fish provide omega-3 fats. Prefer grilling, baking or steaming over deep frying.", "fish", "🐟"),
    ("Skinless Chicken", "Poultry", "Grilled, baked, steamed or lightly cooked.",
     "Remove the skin and avoid deep frying or heavy cream/butter gravies.", "fish", "🍗"),
    ("Eggs", "Eggs", "A convenient protein that can fit a balanced diet.",
     "Boiled or poached eggs need no added fat. How many suit you depends on your overall diet and health; ask your clinician.", "fish", "🥚"),
    ("Fish Curry", "Main meal", "Prepared with moderate oil and salt.",
     "Add vegetables and serve with whole grains. Limit coconut cream and extra salt.", None, "🍛"),
    ("Chicken and Vegetable Soup", "Light meal", "A low-sodium preparation.",
     "Use plenty of vegetables and make your own low-salt stock where possible.", None, "🍲"),
    ("Prawns and Shrimp", "Seafood", "Steamed or grilled.",
     "Season with lemon, garlic and herbs rather than lots of salt or butter.", None, "🦐"),
    ("Fish Salad", "Salad", "Fish combined with fresh vegetables.",
     "Use a light dressing. If using canned fish, check the sodium on the label.", None, "🥗"),
    ("Lean Meat", "Lean protein", "Lean cuts in moderate portions.",
     "Trim visible fat, keep portions modest and prefer stews or grills to frying.", None, "🥩"),
]

ADVICE = [
    ("🩺", "Regular Checkups", "Monitor blood pressure, cholesterol and blood sugar.",
     "Ask a clinician how often you should have blood pressure, cholesterol and blood sugar checked. Keep a record of readings to share at appointments."),
    ("🧘", "Manage Stress", "Practise meditation, yoga and deep breathing.",
     "Try regular walks, breathing exercises, hobbies, enough sleep and talking with someone you trust. Persistent stress or low mood is worth discussing with a professional."),
    ("🚭", "Quit Smoking", "Avoid tobacco and second-hand smoke.",
     "Tobacco harms blood vessels and the heart. A clinician or pharmacist can explain support options for quitting."),
    ("🏃", "Stay Active", "Appropriate physical activity most days.",
     "Many adults aim for about 150 minutes of moderate activity a week, built up gradually. Check with a clinician first if you have symptoms or a heart condition."),
]

LIFESTYLE = [
    ("🏃", "Exercise Regularly", "Build up gradually; many adults aim for ~150 minutes of moderate activity weekly."),
    ("😴", "Get Quality Sleep", "Keep a regular schedule; discuss persistent sleep problems with a clinician."),
    ("🧘", "Manage Stress", "Walking, breathing exercises, hobbies and social support can help."),
    ("💧", "Stay Hydrated", "Drink water regularly through the day, especially in hot weather."),
    ("⚖️", "Maintain a Healthy Weight", "Gradual changes to food and activity are easier to sustain."),
    ("🚭", "Avoid Smoking and Excess Alcohol", "Avoid tobacco; if you drink, ask a clinician what is appropriate for you."),
]

TIPS = ["Maintain a balanced, mostly plant-forward diet", "Be physically active as advised by your clinician",
        "Have blood pressure, cholesterol and sugar checked regularly", "Avoid smoking and limit alcohol"]

DISCLAIMER = ("HeartCare is an educational student project, not a medical device. Nothing here is a diagnosis, "
              "a treatment plan, or a substitute for a qualified healthcare professional.")
