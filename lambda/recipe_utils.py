import logging
import recipes
import random

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

RECIPE_IMAGES = {
    'TREE': "https://mesquite.s3-us-west-2.amazonaws.com/TREE.jpg",
    'SAP': "https://mesquite.s3-us-west-2.amazonaws.com/SAP.jpg",
    'POD': "https://mesquite.s3-us-west-2.amazonaws.com/PODS.jpg",
    'OPOD': "https://mesquite.s3-us-west-2.amazonaws.com/OPEN-PODS.jpg",
    'GPOD': "https://mesquite.s3-us-west-2.amazonaws.com/GROUND+PODS.jpg",
    'BLEAF': "https://mesquite.s3-us-west-2.amazonaws.com/BRANCH-LEAFS.jpg",
    'MES': 'https://mesquite.s3-us-west-2.amazonaws.com/mesquitetree.jpg',
    'MES-POD': 'https://mesquite.s3-us-west-2.amazonaws.com/mesquitepods.jpg'
}

RECIPE_DEFAULT_IMAGE = "https://mesquite.s3-us-west-2.amazonaws.com/TREE.jpg"


def get_sauce_item(request):
    """
    Returns an object containing the recipe (sauce) ID & spoken value by the User from the JSON request
    Values are computing from slot "Item" or from Alexa.Presentation.APL.UserEvent arguments
    """
    sauce_item = {'id': None, 'spoken': None}
    logger.debug("get_sauce_item passed request: {}".format(request))
    if(request.object_type == 'Alexa.Presentation.APL.UserEvent'):
        sauce_item['id'] = request.arguments[1]
    else:
        itemSlot = request.intent.slots["Item"]
        # Capture spoken value by the user
        if(itemSlot and itemSlot.value):
            sauce_item['spoken'] = itemSlot.value

        if(itemSlot and
                itemSlot.resolutions and
                itemSlot.resolutions.resolutions_per_authority[0] and
                itemSlot.resolutions.resolutions_per_authority[0].status and
                str(itemSlot.resolutions.resolutions_per_authority[0].status.code) == 'StatusCode.ER_SUCCESS_MATCH'):
            sauce_item['id'] = itemSlot.resolutions.resolutions_per_authority[0].values[0].value.id

    return sauce_item


def get_sauce_image(id):
    """
    Returns the image url of a specified recipe id
    """
    url = RECIPE_IMAGES[id]
    if(url):
        return url
    else:
        return RECIPE_DEFAULT_IMAGE


def get_locale_specific_recipes(locale):
    """
    Returns the recipe dictionary for a specific locale
    """
    if locale[:2] in recipes.translations:
        return recipes.translations[locale[:2]]
    return recipes.translations[locale[:2]]


def get_random_recipe(handler_input):
    """
    Returns a random localized recipe from the list of available recipes
    """
    locale = handler_input.request_envelope.request.locale
    randRecipe = random.choice(
        list(get_locale_specific_recipes(locale).items()))
    return randRecipe[1]
