'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


import wikipediaapi

from django.contrib import messages


def wiki_page(work_name):
    wikipedia_settings = wikipediaapi.Wikipedia('fr')
    work_wiki_page = wikipedia_settings.page(work_name)
    if work_wiki_page.exists() == True:
        wikipedia_url = work_wiki_page.fullurl
        wikipedia_summary = work_wiki_page.summary[0:500]
        return [wikipedia_url, wikipedia_summary]
    else:
        message = """
                    Le nom de votre oeuvre ne permet pas de trouver une url
                    compatible avec les données de Wikipedia..."""
    return [message]