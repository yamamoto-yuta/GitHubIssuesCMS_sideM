""" transform issue to article data

issue id           -> article slug (directory name)
issue title        -> article title (frontmatter)
issue body         -> article content (markdown)
                      have to deal ![hoge](URL); download images & replace URL
issue labels       -> article tag_ids (frontmatter)
                      have to update `consts/tags.json` (tag_id <--> tag info)
issue closed_at    -> If article is already exists:
                        -> article updated_at
                      else:
                        -> article posted_at
"""
from datetime import datetime
from glob import glob

from models.issue import Issue
from models.article import Article
from models.tags import Tags
from models.resource import Resource
from models.profile import Profile
from models.related import Related
from ogp.image_generator import create_ogp_image
from const import IMAGES_DIR, MD_DIR

def article_build():
    # load issue
    issue = Issue()

    # load article related with the issue
    article = Article.from_article(issue.id)

    # update article by the issue data
    if article is None:
        """ 新規ポスト """
        article = Article(
                    slug=issue.id, 
                    title=issue.title, 
                    markdown=issue.body,
                    tag_ids=[label['id'] for label in issue.get_tag_labels()],
                    posted_at=issue.get_posted_at(),
                    description=issue.ogp_description,
                )
    else:
        """ 既に記事が存在 """
        updated_at = issue.get_updated_at()
        if updated_at is None:
            """ issue側設定が予約投稿 (現在未投稿) """
            article.set_values(
                slug=issue.id,
                title=issue.title,
                markdown=issue.body,
                tag_ids=[label['id'] for label in issue.get_tag_labels()],
                posted_at=issue.get_posted_at(),
                description=issue.ogp_description,
            )
        else:
            """ issue側の予約投稿が未設定もしくは予約投稿時間が現在時刻よりも過去に設定された """
            article_posted_at = datetime.strptime(article.posted_at, "%Y年%m月%d日 %H時%M分") 
            issue_updated_at = datetime.strptime(updated_at, "%Y年%m月%d日 %H時%M分") 
            if article_posted_at > issue_updated_at:
                """ 投稿時間よりも更新時間のほうが過去になってしまう
                投稿時間を修正する
                """
                article.set_values(
                    slug=issue.id,
                    title=issue.title,
                    markdown=issue.body,
                    tag_ids=[label['id'] for label in issue.get_tag_labels()],
                    posted_at=issue.get_posted_at(),
                    description=issue.ogp_description,
                )
            else:
                """ 記事を更新する """
                article.set_values(
                    slug=issue.id,
                    title=issue.title,
                    markdown=issue.body,
                    tag_ids=[label['id'] for label in issue.get_tag_labels()],
                    updated_at=updated_at,
                    description=issue.ogp_description,
                )

    """ 設定パラメータの読み込み """
    profile = Profile.load_profile()
    base_path = ''
    if profile is not None:
        if 'url_subpath' in profile.keys():
            base_path = profile['url_subpath']
    root_url = ''
    if profile is not None:
        if 'root_url' in profile.keys():
            root_url = profile['root_url']

    """ URLに関する処理
    - issue linkをURLに変換
    - RAW URLをパースしてarticle.urlsにリストで保存
    - Image URLをパースしてarticle.imagesにリストで保存
    """
    article.format_url(base_path, root_url)

    """ --- 外部リソースの取得 --- 
    - 外部リンクのOGP取得
    - 画像データの取得
    """
    """ external_metadata.jsonの読み込み """
    resource = Resource.load_resources()

    """ 今回の記事に含まれるURLを設定 """
    external_links = {}
    image_links = {}
    for url in article.urls:
        external_links[url] = {}
    for url in article.images:
        image_links[url] = {}
    resource.set_resources(external_links=external_links, image_links=image_links, base_path=base_path)

    """ OGPと画像を取得 """
    resource.dl_resources()
    """ OGPの保存 """
    resource.save()

    """ 記事内の画像URLをDLした画像PATHに置換する """
    article.replace_images(resource.image_links)

    """ 記事の保存 """
    article.save()

    """ --- サムネイル画像の生成 --- """
    params = {}
    params['ogp_icon_img_path'] = IMAGES_DIR+'/avatar/avatar.png'
    params['title_text'] = article.title
    if profile is None:
        params['author_text'] = ''
    else:
        params['author_text'] = profile['author_name']
    params['slug'] = article.slug
    thumbnail_save_path = IMAGES_DIR+'/thumbnail/'+article.slug+'.jpg'

    create_ogp_image(issue.ogp_img_theme, params, thumbnail_save_path)

    """ --- Tagの更新処理 --- """
    tags = Tags.load_tags()
    if tags is None:
        tags = Tags()

    for label in issue.get_tag_labels():
        tag_id = str(label["id"])
        name = '/'.join(label["name"].split('/')[1:])
        color = label["color"]
        description = label["description"]
        tags.set_tag(tag_id, name, color, description)

    tags.save()

    """ --- 関連記事の算出 --- """
    slugs = [p.split('/')[-1] for p in glob(f'{MD_DIR}/*')]
    articles = [Article.from_article(slug) for slug in slugs]
    related = Related(articles, k=4)
    related_slugs = related.get_related()
    related.save(related_slugs)

