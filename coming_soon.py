import copy
import os

from pelican import logger as pelican_logger
from pelican import signals
from pelican.contents import Article
from pelican.utils import process_translations, order_content


# KNOWN ISSUES
# Can mess up RSS Feed
# Does not delete static content linked with visible_drafts

def _reprocess(article_generator):
    pelican_logger.debug("-- Regenerating articles & their translations and fixing ordering")
    origs, translations = process_translations(
        article_generator.articles, translation_id=article_generator.settings["ARTICLE_TRANSLATION_ID"]
    )
    origs = order_content(origs, article_generator.settings["ARTICLE_ORDER_BY"])
    article_generator.articles, article_generator.translations = origs, translations


def add_coming_soon(article_generator):
    """
    Iterate through drafts and if they are marked as visible, add them to articles list.
    """
    pelican_logger.debug("-- Adding drafts with visible_draft: true to articles list\n")
    for _draft in article_generator.drafts:
        draft = copy.deepcopy(_draft)
        if hasattr(draft, "visible_draft") and draft.visible_draft.strip().lower() == "true":
            if not draft.metadata:
                draft.metadata = {}

            draft.metadata["save_as"] = draft.save_as + ".delete"
            soon_article = Article(content=u"This article will be published soon",
                                   metadata=draft.metadata,
                                   settings=draft.settings,
                                   source_path=draft.source_path)
            # Might be redundant
            soon_article.author = draft.author
            soon_article.slug = draft.slug
            article_generator.articles.append(soon_article)

    _reprocess(article_generator)


def delete_visible_drafts_content(article_generator, writer):
    """
    Delete article output from drafts marked as visible_draft: true
    """
    pelican_logger.debug("-- Deleting output from drafts marked as visible_draft: true so they can't be read\n")
    for article in article_generator.articles:
        if hasattr(article, 'visible_draft') and article.visible_draft.strip().lower() == "true":
            path_to_delete = os.path.join(article_generator.settings.get('OUTPUT_PATH'), article.save_as)
            pelican_logger.debug("Deleting " + path_to_delete)
            if os.path.exists(path_to_delete):
                os.remove(path_to_delete)


def register():
    pelican_logger.debug("-" * 80)
    pelican_logger.debug("Plugin: Coming Soon\n")
    signals.article_generator_pretaxonomy.connect(add_coming_soon)
    signals.article_writer_finalized.connect(delete_visible_drafts_content)
    pelican_logger.debug("-" * 80)
