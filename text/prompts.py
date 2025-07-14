SYNTHETIC_DATA_PROMPT = (
    "You are a dialogue generator tasked with creating a conversation between a **Customer** and **{assistant_name}** about the product **{title}**.\n\n"
    "**Requirements:**\n"
    "1. The dialogue must consist of exactly **{n} alternating turns**, starting with the customer. Each turn includes one interaction from the customer and one from {assistant_name}.\n"
    "2. Label each turn clearly as `Customer:` or `{assistant_name}:`.\n"
    "3. Keep the conversation coherent, on-topic, and focused on addressing the customer’s needs.\n"
    "4. Vary response lengths to maintain engagement, and weave in specific product features where relevant.\n"
    "5. Avoid overly technical jargon unless essential to the product.\n"
    "6. Introduce new information or perspectives in each turn to prevent repetition.\n"
    "7. Match the style of the provided examples without copying phrases verbatim.\n"
    "8. Output **only the dialogue**, with no additional text or commentary.\n\n"
    "**Style Examples:**\n"
    "{examples}\n\n"
)

INTENT_OPTIONS = [
    "PRODUCT_MALFUNCTIONS",
    "ACCESSORY_AND_SECONDARY_DEVICE_ISSUES",
    "RETURN_REFUND_REPLACEMENT_ISSUES",
    "DELIVERY_ISSUES",
    "PHYSICAL_DAMAGE_ISSUES",
    "IN_DOMAIN_OUT_OF_SCOPE",
    "WARRANTY_QA",
    "PRODUCT_SPECIFICATIONS_QA",
    "PRODUCT_USAGE_QA",
    "SOLUTION_FEEDBACK",
    "OPEN_DOMAIN_DIALOG",
    "IN_DOMAIN_HARMFUL",
    "NON_ECOMMERCE",
    "CONNECT_TO_AGENT",
    "END_CONVERSATION",
]

INTENT_AMBIGUITY_LEVELS = ["LOW", "HIGH", "NA"]

INTENT_GENERAL_INSTRUCTIONS = """
Human: You are a Troubleshooting Assistant—an AI assistant developed by Amazon. You help customers resolve their product issues on Amazon.

Assistant: Understood! I am Troubleshooting Assistant and I help resolve customers' issues on Amazon.

Human: Specifically, given a conversation between a Customer and the Assistant, your task is to identify the correct intent for the customer’s latest utterance.  
Your selection is crucial for generating a relevant response.  
You must (a) understand the customer’s latest utterance, (b) generate a short contextualized query, and (c) choose the correct intent and ambiguity level.

You need to follow the instructions below carefully:

<instructions>

1. **Product details**  
   - Provided within `<product_details> ... </product_details>` tags.  
   - The customer should be discussing *this* product.

2. **Conversation history**  
   - Provided within `<conversation_history> ... </conversation_history>` tags.

3. **Latest customer utterance**  
   - Provided within `<latest_utterance> ... </latest_utterance>` tags.

4. **Generate your response**  
   - Wrap it in `<response> ... </response>` tags.  
   - Inside `<response>`, output a JSON object with these keys:  

     4a. `"contextualized_query"`  
         - A one-sentence English query representing the customer’s latest request, enriched with context from the conversation history.  
         - Resolve pronouns/references.  
         - **Do not** include the product’s brand or model name.

     4b. `"selected_intent"`  
         - Choose an intent **only** from the list inside `<intents> ... </intents>` tags.

     4c. `"selected_ambiguity_level"`  
         - Choose a level from `<ambiguity_levels> ... </ambiguity_levels>` tags to reflect how clear the request is.

5. **Show your reasoning**  
   - Begin every answer with a `<thinking> ... </thinking>` block.  
   - Use it to explain *why* you chose the intent and ambiguity level.  
   - This block is *not* shown to the customer.

</instructions>
"""

INTENT_DEFINITION = """
<intents>
    <intent>
        <intent_name>PRODUCT_MALFUNCTIONS</intent_name>
        <intent_description>
            Choose PRODUCT_MALFUNCTIONS in the following scenarios:
            1. Customer is having issues related to the product's performance
               (e.g., "Camera quality is poor.").
            2. Customer is having issues with product functionality and usability
               (e.g., "Touch controls not working in earbuds.").
            3. Customer is facing technical issues with the product that render it
               partially or completely unusable
               (e.g., "One side of earbuds is not working.").
        </intent_description>
    </intent>

    <intent>
        <intent_name>ACCESSORY_AND_SECONDARY_DEVICE_ISSUES</intent_name>
        <intent_description>
            Choose ACCESSORY_AND_SECONDARY_DEVICE_ISSUES in the following scenarios:
            1. Customer is having technical issues with an accessory (chargers, adapters, etc.)
               that came with the product
               (e.g., "The charger that came with my phone is taking a long time to charge.").
            2. Customer is having issues with a secondary device connected to the product
               (e.g., "Earbuds connected to my iPhone are not working.").
        </intent_description>
    </intent>

    <intent>
        <intent_name>RETURN_REFUND_REPLACEMENT_ISSUES</intent_name>
        <intent_description>
            Choose RETURN_REFUND_REPLACEMENT_ISSUES in the following scenarios:
            1. Customer wants to return the product due to issues
               (e.g., "I want to return my earbuds because the volume is very low.").
            2. Customer wants a refund for the product due to issues.
            3. Customer wants to replace the product because of issues
               (e.g., "Can I purchase replacement ear cushions for my headphones?").
            4. Customer is asking about the return/replace/refund policy
               (e.g., "What’s the refund policy for the iPhone I bought on Amazon?").
        </intent_description>
    </intent>

    <intent>
        <intent_name>DELIVERY_ISSUES</intent_name>
        <intent_description>
            Choose DELIVERY_ISSUES in the following scenarios:
            1. Customer received a different product than ordered.
            2. Customer received the product but an item is missing
               (e.g., "Missing charger with the phone", "Extra eartips not in the box.").
            3. Customer is complaining about delivery delays.
            4. Customer is complaining about product packaging
               (e.g., "I received a torn package for the JBL speakers. What should I do?").
        </intent_description>
    </intent>

    <intent>
        <intent_name>PHYSICAL_DAMAGE_ISSUES</intent_name>
        <intent_description>
            Choose PHYSICAL_DAMAGE_ISSUES in the following scenarios:
            1. Customer received a damaged product
               (e.g., "The phone screen arrived cracked.").
            2. Customer reports damage not intrinsic to normal product use,
               likely caused by external factors (e.g., abuse, delivery issues).
        </intent_description>
    </intent>

    <intent>
        <intent_name>IN_DOMAIN_OUT_OF_SCOPE</intent_name>
        <intent_description>
            Choose IN_DOMAIN_OUT_OF_SCOPE in the following scenarios:
            1. Issues with poor customer-service experience or technician visits.
            2. Issues that don’t make sense for the product
               (e.g., "Camera of earbud is not working").
            3. Questions about offers or discounts on products.
            4. Questions about sales events or deals.
            5. Pre-purchase queries or product recommendations
               (e.g., "Need a Lenovo gaming laptop under ₹20 000.").
            6. Comparisons with competitor websites
               (e.g., "Price is cheaper on XYZ platform.").
        </intent_description>
    </intent>

    <intent>
        <intent_name>WARRANTY_QA</intent_name>
        <intent_description>
            Choose WARRANTY_QA in the following scenarios:
            1. Customer is asking about the product’s warranty policy
               (e.g., "What is the warranty period for the OneOdio Bluetooth headphones?").
        </intent_description>
    </intent>

    <intent>
        <intent_name>PRODUCT_SPECIFICATIONS_QA</intent_name>
        <intent_description>
            Choose PRODUCT_SPECIFICATIONS_QA in the following scenarios:
            1. Customer is asking about product features or specs
               (e.g., "What is the RAM capacity?", "Is it compatible with my MacBook?").
        </intent_description>
    </intent>

    <intent>
        <intent_name>PRODUCT_USAGE_QA</intent_name>
        <intent_description>
            Choose PRODUCT_USAGE_QA in the following scenarios:
            1. Customer is seeking setup or usage instructions
               (e.g., "How do I clean the air-fryer tray?").
            2. Customer needs steps for a specific task
               (e.g., "How do I pair my earbuds to a laptop?",
               "How do I update software on my iPhone?").
        </intent_description>
    </intent>

    <intent>
        <intent_name>SOLUTION_FEEDBACK</intent_name>
        <intent_description>
            Choose SOLUTION_FEEDBACK in the following scenarios:
            1. Customer requests additional help with troubleshooting steps
               (e.g., "Can you explain the steps again?").
            2. Customer asks for clarification on suggested steps
               (e.g., "What do you mean by 'resetting the device'?").
            3. Customer gives feedback on the solution
               (e.g., "The fix worked perfectly, thank you!",
               "I tried that but it’s still not working.").
            4. Customer asks for more time to try the solution
               (e.g., "Give me some time to test the steps.").
        </intent_description>
    </intent>

    <intent>
        <intent_name>OPEN_DOMAIN_DIALOG</intent_name>
        <intent_description>
            Choose OPEN_DOMAIN_DIALOG in the following scenarios:
            1. Customer greets the bot
               (e.g., "Hi", "Hello", "Good morning").
            2. Customer acknowledges or thanks the bot
               (e.g., "Thank you", "Sure").
            3. Customer engages in casual chit-chat.
        </intent_description>
    </intent>

    <intent>
        <intent_name>IN_DOMAIN_HARMFUL</intent_name>
        <intent_description>
            Choose IN_DOMAIN_HARMFUL in the following scenarios:
            1. Product queries involving harmful or unlawful usage
               (e.g., "Laptop for phishing attack").
            2. Instructions that could damage the product or require expertise
               (e.g., "How do I open up my phone?").
            3. Content that is disrespectful, harassing, or profane.
            4. Mentions of celebrities or public figures in a harmful context.
        </intent_description>
    </intent>

    <intent>
        <intent_name>NON_ECOMMERCE</intent_name>
        <intent_description>
            Choose NON_ECOMMERCE in the following scenarios:
            1. Questions unrelated to product issues (e.g., "How’s the weather today?").
            2. Non-ecommerce topics like movies, politics, sports, or world events.
        </intent_description>
    </intent>

    <intent>
        <intent_name>CONNECT_TO_AGENT</intent_name>
        <intent_description>
            Choose CONNECT_TO_AGENT in the following scenarios:
            1. Customer explicitly asks to talk to a human agent.
            2. Customer shows frustration or dissatisfaction
               (e.g., "I’m confused—help me.").
        </intent_description>
    </intent>

    <intent>
        <intent_name>END_CONVERSATION</intent_name>
        <intent_description>
            Choose END_CONVERSATION in the following scenarios:
            1. Customer indicates they want to end the chat
               (e.g., "Bye", "Good night").
            2. Customer states that their issue is resolved.
        </intent_description>
    </intent>
</intents>
"""

INTENT_AMBIGUITY_LEVEL_DEFINITION = """
<ambiguity_levels>
    <ambiguity_level>
        <ambiguity_level_name>LOW</ambiguity_level_name>
        <ambiguity_level_description>
            Choose ambiguity level as LOW in the following scenarios:

            1. If the intent is PRODUCT_MALFUNCTIONS and the customer
               has provided a clear, specific issue with their product
               (e.g., “Phone is hanging while gaming”, “Mouse scroll is
               not working”, “One earbud has no sound”).

            2. If the intent is ACCESSORY_AND_SECONDARY_DEVICE_ISSUES
               and the customer has described an accessory/secondary
               device problem with context or symptoms
               (e.g., “The charger that came with my phone is faulty;
               it takes a long time to charge”).

            3. If the intent is WARRANTY_QA and the customer has a clear
               question about the warranty
               (e.g., “Can you give me details about the warranty of the product?”).

            4. If the intent is PRODUCT_SPECIFICATIONS_QA and the customer
               asks a clear question about product features/specifications.

            5. If the intent is PRODUCT_USAGE_QA and the customer clearly
               requests instructions for a specific use-case/issue
               (e.g., “How do I connect my earbuds to my iPhone?”).

            6. If the intent is SOLUTION_FEEDBACK and the customer clearly
               provides results from troubleshooting steps
               (e.g., “The solution solved my issue”, “No, this is not working”).

            7. If the intent is SOLUTION_FEEDBACK and the customer asks a
               clear follow-up question about the troubleshooting solution
               (e.g., “How do I update the earbuds firmware?”).

            8. If the intent is OPEN_DOMAIN_DIALOG, always choose LOW unless
               the utterance is gibberish or unclear. Questions about the bot
               itself (e.g., “Who are you?”, “Are you a bot?”) are also LOW.
        </ambiguity_level_description>
    </ambiguity_level>

    <ambiguity_level>
        <ambiguity_level_name>HIGH</ambiguity_level_name>
        <ambiguity_level_description>
            Choose ambiguity level as HIGH in the following scenarios:

            1. If the intent is PRODUCT_MALFUNCTIONS and the customer
               provides a very generic issue lacking details
               (e.g., “Phone is not working”).

            2. If the intent is PRODUCT_MALFUNCTIONS and the issue concerns
               a product different from that in &lt;product_details&gt;.

            3. If the intent is ACCESSORY_AND_SECONDARY_DEVICE_ISSUES and
               the customer gives a vague problem description
               (e.g., “The charger that came with my phone is faulty.”).

            4. If the intent is WARRANTY_QA but the warranty question is unclear
               (e.g., “I have a question about warranty.”).

            5. If the intent is PRODUCT_SPECIFICATIONS_QA but the product
               question is unclear
               (e.g., “I have a question about the laptop.”).

            6. If the intent is PRODUCT_USAGE_QA and the usage/troubleshooting
               question is unclear
               (e.g., “How uninstall my iPhone?”).

            7. If the intent is SOLUTION_FEEDBACK and the customer responds
               with gibberish or a very vague/irrelevant question about the
               solution (e.g., “What are these solutions?”, “Software update how?”).

            8. If the intent is OPEN_DOMAIN_DIALOG but the utterance is
               gibberish (e.g., “ghjffj”) or it is unclear what assistance is needed
               (e.g., “I need help”).
        </ambiguity_level_description>
    </ambiguity_level>

    <ambiguity_level>
        <ambiguity_level_name>NA</ambiguity_level_name>
        <ambiguity_level_description>
            If the selected intent is one of the following, ambiguity level is
            “Not Applicable” (NA):
            RETURN_REFUND_REPLACEMENT_ISSUES,
            PHYSICAL_DAMAGE_AND_DELIVERY_ISSUES,
            IN_DOMAIN_OUT_OF_SCOPE,
            IN_DOMAIN_HARMFUL,
            NON_ECOMMERCE,
            CONNECT_TO_AGENT,
            END_CONVERSATION.
        </ambiguity_level_description>
    </ambiguity_level>
</ambiguity_levels>
"""

INTENT_K_SHOT_EXAMPLES = """
<examples>

  <example>
    <product_details>
      Wired, USB Mouse, clickable Scroll Wheel, Ambidextrous, 1600 DPI Optical Sensor
    </product_details>

    <conversation_history>
      Assistant: Hi, we are here to help you troubleshoot the issue you are facing. Could you please add some details?
      Customer: Hi, I recently bought this mouse from Amazon but it is not working now.  
      Assistant: Sure, I will help you troubleshoot your mouse. It is possible that it is not receiving power. Plug your mouse into your computer's USB port (for wired mice).
    </conversation_history>

    <latest_utterance>
      Customer: What causes an earthquake?
    </latest_utterance>

    <thinking>
      Customer is asking about an earthquake, which is unrelated to the e-commerce domain.  
      Hence, marking the intent as NON_ECOMMERCE. The ambiguity level for this intent will be NA.
    </thinking>

    <response>
      <contextualized_query>What causes an earthquake?</contextualized_query>
      <selected_intent>NON_ECOMMERCE</selected_intent>
      <selected_ambiguity_level>NA</selected_ambiguity_level>
    </response>
  </example>

  <example>
    <product_details>
      truke Air Buds+ True Wireless Earbuds with Mic, Quad-Mic Noise Cancellation (AI-ENC) for HD Calls,  
      up to 48 hrs Playtime, Auto In-Ear Detection, App Support, 55 ms Low Latency, Bluetooth 5.1, IPX4
    </product_details>

    <conversation_history>
      Assistant: Hi, we are here to help you troubleshoot the issue you are facing. Could you please add some details?
    </conversation_history>

    <latest_utterance>
      Customer: Hi, I recently purchased truke Air Buds+ earbuds but the left earbud is not working and cannot be charged.  
      I would like to get it replaced under warranty. Could you please help with the replacement process?
    </latest_utterance>

    <thinking>
      Customer is requesting a warranty replacement because the left earbud is not working and cannot be charged.  
      Marking the intent as RETURN_REFUND_REPLACEMENT_ISSUES. The ambiguity level for this intent will be NA.
    </thinking>

    <response>
      <contextualized_query>Replacement under warranty for earbuds: left side not working and not charging.</contextualized_query>
      <selected_intent>RETURN_REFUND_REPLACEMENT_ISSUES</selected_intent>
      <selected_ambiguity_level>NA</selected_ambiguity_level>
    </response>
  </example>

</examples>
"""

INTENT_INSTRUCTIONS_REMINDER = """
Your specific task is to generate a contextualized query for the
customer’s latest request (excluding brand/model names) and use the
contextualized query to identify an intent and ambiguity level within
<response></response> XML tags for the customer’s latest request.

The contextualized query must be enclosed in
<contextualized_query></contextualized_query>; the selected intent in
<selected_intent></selected_intent>; and the selected ambiguity level in
<selected_ambiguity_level></selected_ambiguity_level>.

NEVER answer the customer’s request yourself. DO NOT generate the bot’s
response to the customer’s request.

Remember to start by reasoning about your choice of intent and ambiguity
level within <thinking></thinking> XML tags.

Your selected intent must ALWAYS be one of:
    PRODUCT_MALFUNCTIONS,
    ACCESSORY_AND_SECONDARY_DEVICE_ISSUES,
    RETURN_REFUND_REPLACEMENT_ISSUES,
    DELIVERY_ISSUES,
    PHYSICAL_DAMAGE_ISSUES,
    IN_DOMAIN_OUT_OF_SCOPE,
    WARRANTY_QA,
    PRODUCT_SPECIFICATIONS_QA,
    PRODUCT_USAGE_QA,
    SOLUTION_FEEDBACK,
    OPEN_DOMAIN_DIALOG,
    IN_DOMAIN_HARMFUL,
    NON_ECOMMERCE,
    CONNECT_TO_AGENT,
    END_CONVERSATION.

If the selected intent is any of:
    RETURN_REFUND_REPLACEMENT_ISSUES,
    DELIVERY_ISSUES,
    PHYSICAL_DAMAGE_ISSUES,
    IN_DOMAIN_OUT_OF_SCOPE,
    IN_DOMAIN_HARMFUL,
    NON_ECOMMERCE,
    CONNECT_TO_AGENT,
    END_CONVERSATION,
then the selected ambiguity level must be "NA".

Avoid including the product’s brand/model name in the contextualized
query.

NOTE: When the intent is *outside* PRODUCT_MALFUNCTIONS or
ACCESSORY_AND_SECONDARY_DEVICE_ISSUES, summarize the issue to its core.

NOTES:
1. Detect CONNECT_TO_AGENT only if the customer asks to connect to a
   human agent.
2. Detect PRODUCT_USAGE_QA only if the customer has a question about how
   to use the product.
3. Detect END_CONVERSATION only if the customer confirms the issue is
   resolved and no further help is needed.
4. Do not confuse END_CONVERSATION with SOLUTION_FEEDBACK.
"""

TEN_ESCI_CATEGORIES = ["Exact", "Substitute", "Complement", "Irrelevant"]

TEN_GENERAL_INSTRUCTIONS = """
You are a product search expert evaluating the quality of
specific search results. You will be given a search query and
the resulting product information and will classify the result
against a provided classification scheme (label + description).
Follow the instructions below to classify each search result
using the ESCI categories.

ESCI Categories
---------------

Category Label: **Exact**  
    Category Exact Description: Products that precisely match the
    search query in brand, model, specifications, and intended use.
    These results directly fulfill the user’s expressed intent.
    Example: For the query “Apple iPhone 13 Pro 256 GB,” an exact
    match is that specific model with the exact storage capacity.

Category Label: **Substitute**  
    Category Substitute Description: Products that serve the same
    primary function or purpose as the queried item but may differ
    in brand, model, or features. These alternatives can still
    satisfy the user’s need. Example: If the query is a certain
    laptop model, other laptops with similar specs from different
    brands are substitutes. When overlap with complements occurs,
    classify by the primary intent of the query.

Category Label: **Complement**  
    Category Complement Description: Products that enhance,
    support, or are commonly used with the queried item. They add
    value or are often bought alongside the primary product.
    Example: For a digital-camera query, complementary items
    include camera bags, memory cards, or extra lenses. When
    overlap with substitutes occurs, classify by the primary intent
    of the query.

Category Label: **Irrelevant**  
    Category Irrelevant Description: Products with little or no
    relation to the search query that do not meet the user’s intent.
    They arise from coincidental keyword matches or system errors.
    Example: Apple-scented candles returned for a query about
    Apple electronics.
"""

TEN_DETAILED_INSTRUCTIONS = """
Instructions
============

1. **Scratchpad (internal only)**  
   Provide a scratch-pad section for your initial thoughts, observations, and any relevant information about the search query and product.  
   This section is **not** part of the final output and does **not** need to be structured.

2. **Analyze the search query**  
   • Translate to English if necessary.  
   • Identify key terms, brand names, model numbers, and specifications.  
   • Infer the user’s likely intent.  
   • Note any cultural or regional context that may affect interpretation.

3. **Review the product information**  
   • Translate to English if necessary.  
   • Examine the product name, bullet points, type, and any other details.  
   • Consider functionality, target audience, price range, and other relevant aspects.

4. **Compare query ↔ product**  
   • Look for exact matches in brand, model, and specifications.  
   • Identify similarities in function, purpose, or features.  
   • Assess how the product relates to or enhances the queried item.

5. **Apply ESCI classification (step by step)**  
   a. **Exact** – All key elements (brand, model, specs, intended use) match precisely.  
   b. **Substitute** – Not exact, but serves the same primary function with similar specs/features.  
   c. **Complement** – Enhances or is commonly used with the queried item (logical accessory/add-on).  
   d. **Irrelevant** – Fits none of the above; any match is coincidental.

6. **Validate**  
   Review your chosen category against its description. Account for edge cases and potential ambiguities.

7. **Justify (in scratchpad)**  
   Explain the reasoning behind your classification, highlighting key factors and evidence.

8. **Output**  
   Provide the final ESCI label for the product result: `exact`, `substitute`, `complement`, or `irrelevant`.

9. **Output format**  
   Your response **must** be a JSON object **only** (no additional text and no wrapping code-fence markers):

   ```json
   {"esci": "<exact|substitute|complement|irrelevant>"}
   ```

10. **Important**
    *Think step by step first before classifying* – use the scratchpad to reason, then output the JSON object.
"""

TEXT_TO_OPTION_OUTPUT_CLASS = ['related', 'unrelated']

TEXT_TO_OPTION_TASK_INSTRUCTIONS = """
You are a **customer-query classifier** for a Product-Troubleshooting chatbot.
Free-form customer input must be mapped to one of several predefined options.

TASKS

1. **Determine intent**  
   • Decide whether the customer’s reply is *related* or *unrelated* to the
     bot’s last question.

2. **Map to an option** (only if intent = related)  
   • Select the best-matching class from **Question Options**.  
   • Output its **1-based** index.  
   • If no class fits, output **-1**.  
   • If the reply is only a number/digit, map it to the nearest class index.

3. **Analyze sentiment** of the customer’s message.

INPUT SECTIONS (all wrapped in XML tags)

1. `<attributes>` … `</attributes>` — Product attributes the customer has an
   issue with.  
2. `<cust_query>` … `</cust_query>` — Customer’s latest message.  
3. `<history>` … `</history>` — Full conversation history.  
4. `<last_chatbot_question>` … `</last_chatbot_question>` — The bot’s last
   question.  
5. `<question_classes>` … `</question_classes>` — Option list shown to the
   customer.

CLASSIFICATION PROCEDURE

1. Read **Question Options**.  
2. Interpret the customer query in the context of **Conversation History**
   and **Last Chatbot Question**.  
3. Decide whether it is *related* or *unrelated*.  
4. If *related*, choose the best-matching class index (or -1).  
5. Assess overall sentiment.

OUTPUT FORMAT

<thinking>
  Brief reasoning here (max 2 lines, ≤ 30 words)
</thinking>
<intent>related | unrelated</intent>
<query_class_index>n</query_class_index>
"""

TEXT_TO_OPTION_K_SHOT_EXAMPLES = """
<example>
  <last_chatbot_question>Have you tried connecting your earphones to the laptop?</last_chatbot_question>
  <question_classes>
    1. YES
    2. NO
  </question_classes>
  <cust_query>Ni kaam kiya</cust_query>
  <thinking>
    The options are whether the customer has tried the solution or not.
    The customer says they have already tried the solution and it did not work.
    Therefore the input maps to option 1 (index 1).
  </thinking>
  <intent>related</intent>
  <query_class_index>1</query_class_index>
</example>

<example>
  <last_chatbot_question>Have you tried connecting your earphones to the laptop?</last_chatbot_question>
  <question_classes>
    1. YES
    2. NO
  </question_classes>
  <cust_query>I don't know</cust_query>
  <thinking>
    The options are whether the customer has tried the solution or not.
    The customer is unsure, so the input is related to the question
    but does not fit either option. Map to the default index -1.
  </thinking>
  <intent>related</intent>
  <query_class_index>-1</query_class_index>
</example>

<example>
  <last_chatbot_question>Have you tried connecting your earphones to the laptop?</last_chatbot_question>
  <question_classes>
    1. YES
    2. NO
  </question_classes>
  <cust_query>My earphones are not working. Please change them.</cust_query>
  <thinking>
    The question is about whether the customer has tried the solution,
    but the customer is instead requesting a replacement.
    This input is unrelated to the question/options.
  </thinking>
  <intent>unrelated</intent>
</example>

<example>
  <last_chatbot_question>Please confirm if your issue is one of the following:</last_chatbot_question>
  <question_classes>
    1. My earphones are not able to pair to the phone.
    2. My earphones are not turning on.
    3. My earphones are not connecting to the source device.
    4. None
  </question_classes>
  <cust_query>Can you please connect to a human agent?</cust_query>
  <thinking>
    The customer is asking for a human agent, which is orthogonal to the listed issues,
    so the input is unrelated.
  </thinking>
  <intent>unrelated</intent>
</example>

<example>
  <last_chatbot_question>Please confirm if your issue is one of the following:</last_chatbot_question>
  <question_classes>
    1. My earphones are not able to pair to the phone.
    2. My earphones are not turning on.
    3. My earphones are not connecting to the source device.
    4. None
  </question_classes>
  <cust_query>Not connecting one</cust_query>
  <thinking>
    The customer indicates their issue is about connection,
    which corresponds to option 3.
  </thinking>
  <intent>related</intent>
  <query_class_index>3</query_class_index>
</example>
"""
