import google.generativeai as palm
import asyncio
from pyppeteer import launch
import config

async def scrape_reviews(url):
    # list of all review
    reviews = []
    # launch browser
    browser = await launch({"headless": True, "args": ["--window-size=800,3200"]})
    page = await browser.newPage()
    await page.setViewport({"width": 800, "height": 3200})
    await page.goto(url)
    # click 'show more reviews'
    try:
        await page.waitForSelector(".M77dve")
        more_rev = await element.querySelector(".M77dve")
        await page.evaluate("button => button.click()" ,more_rev)
    except:
        pass
    # iterate - find the reviews - add to list
    await page.waitForSelector(".jftiEf")
    elements = await page.querySelectorAll(".jftiEf")
    for element in elements:
         try:
            await page.waitForSelector(".w8nwRe")
            more_btn = await element.querySelector(".w8nwRe")
            await page.evaluate("button => button.click()", more_btn)
            await page.waitFor(1500)
         except:
             pass
         await page.waitForSelector(".wiI7pd")
         snippet = await element.querySelector(".wiI7pd")
         text = await page.evaluate("selected => selected.textContent", snippet)
         reviews.append(text)

    await browser.close()
    return reviews
# LLM model for summarization
def summerize(reviews, model):
     prompt = "I collected some reviews of a place I was considering visiting.\nCan you summerize the reviews for me?\nI want to generally know what people like or dislike.\n"
     print(prompt)

     for review in reviews:
        prompt += "\n" + review

     completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=800,
    )
     return completion.result

palm.configure(api_key=config.API_Key)
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

url = input("Enter a URL: ")
reviews = asyncio.get_event_loop().run_until_complete(scrape_reviews(url))
result = summerize(reviews,model)
print(result)