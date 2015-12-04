from pelican import signals
from pelican.contents import Article
from pelican.utils import process_translations
import os

def add_coming_soon(article_generator):
	for draft in article_generator.drafts:
		if hasattr(draft, 'visible_draft') and draft.visible_draft.strip().lower() == "true":
			soon_article = Article(content=None,metadata=draft.metadata)
			soon_article.author = draft.author
			soon_article.slug = draft.slug
			soon_article.source_path = draft.source_path
			article_generator.articles.append(soon_article)

	article_generator.articles, article_generator.translations = process_translations(
	            article_generator.articles,
	            order_by=article_generator.settings['ARTICLE_ORDER_BY'])	

def delete_visible_draft_empty_files(article_generator, writer):
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	for empty_article in article_generator.articles:
		if hasattr(empty_article, 'visible_draft') and empty_article.visible_draft.strip().lower() == "true":
			path_to_delete = os.path.join(article_generator.settings.get('OUTPUT_PATH'), empty_article.save_as)
			print "Deleting " + path_to_delete
			os.remove(path_to_delete)
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

	
def register():
    signals.article_generator_pretaxonomy.connect(add_coming_soon)
    signals.article_writer_finalized.connect(delete_visible_draft_empty_files)