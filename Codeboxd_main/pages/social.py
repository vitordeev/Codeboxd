"""Public discovery and authenticated social pages."""
import reflex as rx
from reflex_components_core.el.elements.media import Img


class CoverImage(Img):
    """Native image with the error event exposed by Reflex."""
    on_error: rx.EventHandler[lambda: []]

from ..state.social import SocialState as S
from ..services.catalog import HOME_COLLECTIONS
from .login import _logo_icon

INPUT = 'w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white'
BUTTON = 'action-button'
CARD = 'rounded-2xl border border-white/10 bg-[#111114] p-5 space-y-4'


def button(text, event=None, **props):
    return rx.el.button(text, on_click=event, type='button', class_name=BUTTON, **props)


def field(label, name, value='', **props):
    return rx.el.label(rx.el.span(label, class_name='block mb-2 text-sm text-gray-300'),
                       rx.el.input(name=name, default_value=value, class_name=INPUT, **props))


def textarea(label, name, value='', **props):
    return rx.el.label(rx.el.span(label, class_name='block mb-2 text-sm text-gray-300'),
                       rx.el.textarea(name=name, default_value=value, class_name=INPUT, **props))


def check(label, name, checked=False):
    return rx.el.label(rx.el.input(type='checkbox', name=name, default_checked=checked), ' '+label,
                       class_name='flex gap-2 items-center text-sm')


def submit(label, **props):
    return rx.el.button(label, type='submit', class_name=BUTTON, **props)


def confirm(label, action, disabled=False):
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(rx.el.button(label, type='button', class_name='quiet-button danger', disabled=disabled)),
        rx.alert_dialog.content(
            rx.alert_dialog.title(label+'?'),
            rx.alert_dialog.description('Esta ação remove o conteúdo. Deseja continuar?'),
            rx.flex(rx.alert_dialog.cancel(rx.button('Cancelar', variant='soft', class_name='confirm-cancel-button')),
                    rx.alert_dialog.action(rx.button('Confirmar exclusão', on_click=action, color_scheme='red', disabled=disabled)),
                    gap='3', justify='end', margin_top='20px', class_name='confirm-dialog-actions'),
            class_name='codeboxd-dialog confirm-dialog'))


def avatar(url, name):
    return rx.cond(url != '', rx.el.img(src=url, alt=name, class_name='avatar'),
                   rx.el.span(rx.icon('user-round', size=22), class_name='avatar avatar-fallback'))


def editor(title, description, content, **props):
    return rx.dialog.root(rx.dialog.content(
        rx.dialog.title(title), rx.dialog.description(description),
        rx.cond(S.notice != '', rx.el.p(S.notice, role='status', class_name='dialog-notice')),
        content, rx.dialog.close(rx.el.button('Fechar', type='button', class_name='quiet-button')),
        class_name='codeboxd-dialog'), **props)


def shell(title, subtitle, *children):
    return rx.el.div(
        rx.el.header(
            rx.el.a(_logo_icon(), rx.el.span('code', rx.el.span('boxd', class_name='brand-yellow')),
                    href='/', class_name='brand', aria_label='Codeboxd — início'),
            rx.el.nav(*[rx.el.a(label, href=href,
                        class_name=rx.cond(S.router.url.path == href, 'nav-link active', 'nav-link')) for label,href in
                        [('Início','/'),('Feed','/feed'),('Listas','/listas'),('Perfil','/conta')]],
                      class_name='main-nav', aria_label='Navegação principal'),
            rx.cond(S.is_authenticated,
                rx.el.div(rx.el.a('Meu perfil',href='/conta'), button('Sair',S.logout_social),class_name='flex items-center gap-4'),
                rx.el.a('Entrar',href='/login',class_name=BUTTON)),
            class_name='site-header'),
        rx.el.main(rx.el.h1(title,class_name='sr-only' if title in ('Sua próxima história começa aqui.', 'Detalhes da obra') else 'text-3xl md:text-4xl font-bold'),
            rx.el.p(subtitle,class_name='sr-only' if title in ('Sua próxima história começa aqui.', 'Detalhes da obra') else 'text-gray-400 mt-3 mb-8'),
            rx.cond(S.notice!='',rx.el.p(S.notice,role='status',class_name='rounded-xl border border-amber-400/25 bg-amber-400/10 p-4 mb-6')),
            rx.cond(S.busy,rx.el.p('Carregando…',role='status',class_name='text-amber-300')),
            rx.fragment(*children),
            class_name='site-main space-y-8'),
        rx.el.footer(rx.el.p('Codeboxd · Suas histórias, sua comunidade.'),
            rx.el.div(rx.el.a('Biblioteca', href='/biblioteca'), rx.el.a('Comunidade', href='/comunidade'), class_name='flex gap-6'),
            class_name='site-footer'),
        class_name='site-shell')


def cover_image(m):
    return rx.el.div(
        rx.el.div(
            rx.el.span('CODEBOXD', class_name='cover-placeholder-brand'),
            rx.el.div(rx.el.span('Capa indisponível', class_name='cover-placeholder-label'),
                      class_name='cover-placeholder-copy'),
            class_name='cover-placeholder', aria_hidden=True),
        rx.cond((m['cover'] != '') & ~S.failed_covers.contains(m['cover']),
            CoverImage.create(src=m['cover'], alt=m['title'], loading='lazy', decoding='async',
                      width='100%', height='100%', on_error=S.cover_failed(m['cover']), class_name='media-cover')),
        class_name='cover-frame')


def media_card(m, search=False):
    content=rx.el.div(
        cover_image(m),
        rx.el.div(rx.el.h3(m['title'],class_name='font-semibold line-clamp-2'),
            rx.el.p(m['kind']+' · '+m['year'],class_name='text-sm text-gray-400 mt-3'),class_name='p-4'),class_name='h-full')
    if search:
        return rx.el.button(content,type='button',on_click=S.open_result(m['key']),class_name='media-card text-left')
    return rx.el.a(content,href='/obra/'+m['id'],class_name='media-card')


def grid(items, render, empty):
    return rx.cond(items.length()>0,
        rx.el.div(rx.foreach(items,render),class_name='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5'),
        rx.el.p(empty,class_name='p-8 border border-dashed border-white/15 rounded-2xl text-gray-400'))


def shelf_arrow(shelf_id, title, direction):
    # IDs and directions are constants defined here, never user input.
    script = """(() => { const row = document.getElementById('%s');
        if (row) row.scrollBy({left: row.clientWidth * .85 * %d,
        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()""" % (shelf_id, direction)
    return rx.el.button(rx.icon('chevron-left' if direction < 0 else 'chevron-right', size=19),
        type='button', on_click=rx.call_script(script), class_name='shelf-arrow',
        aria_label=('Anteriores: ' if direction < 0 else 'Próximos: ') + title,
        aria_controls=shelf_id)


def catalog_shelf(title, subtitle, items, kind, shelf_id, footer=None):
    def card(m, index):
        return rx.el.button(
            rx.el.div(cover_image(m),
                class_name='shelf-poster'),
            rx.el.div(rx.el.h3(m['title'], class_name='shelf-card-title'),
                rx.el.p(m['kind'] + ' · ' + m['year'], class_name='shelf-card-meta'), class_name='shelf-card-copy'),
            type='button', on_click=S.open_featured(m['source'],m['external_id'],kind),
            class_name='shelf-card', key=m['key'])
    return rx.el.section(
        rx.el.div(rx.el.div(rx.el.h3(title,id=shelf_id+'-heading',class_name='shelf-title'),
            rx.el.p(subtitle,class_name='shelf-subtitle')),
            rx.el.div(shelf_arrow(shelf_id,title,-1),shelf_arrow(shelf_id,title,1),class_name='shelf-controls'),
            class_name='catalog-shelf-heading'),
        rx.el.div(rx.foreach(items,card),id=shelf_id,class_name='catalog-rail',
            role='region',aria_label=title,tab_index=0),
        footer if footer is not None else rx.fragment(),
        class_name='catalog-shelf',aria_labelledby=shelf_id+'-heading')


def popular_section(title, items, kind):
    return rx.cond(items.length()>0,catalog_shelf(title,
        'Os títulos em alta no TMDB. Encontre o seu próximo favorito.',items,kind,'popular-'+kind,
        footer=rx.cond(~S.popular_exhausted.contains(kind),
            rx.el.button('Carregar mais filmes' if kind=='movie' else 'Carregar mais séries',
                on_click=S.more_popular(kind),type='button',disabled=S.busy,class_name='shelf-more'))))


def collection_section(key):
    kind,title,subtitle,_ = HOME_COLLECTIONS[key]
    return rx.cond(S.home_collections[key].length()>0,
        catalog_shelf(title,subtitle,S.home_collections[key],kind,key),
        rx.el.section(rx.el.h3(title,class_name='shelf-title'),
            rx.cond(~S.home_loaded,
                rx.el.div(*[rx.el.div(class_name='shelf-skeleton') for _ in range(6)],
                    class_name='catalog-rail',aria_hidden=True),
                rx.el.div(rx.el.p(rx.cond(S.home_collection_errors.contains(key),
                    'Esta seleção está indisponível no momento.', 'Ainda não há títulos nesta seleção.')),
                    rx.el.button('Tentar novamente',on_click=S.retry_home_collections,
                        type='button',disabled=S.busy,class_name='quiet-button'),class_name='shelf-empty')),
            class_name='catalog-shelf'))


def catalog_group(anchor, label, description, icon, *shelves):
    return rx.el.section(
        rx.el.div(rx.el.div(rx.icon(icon,size=22),rx.el.span(label),class_name='catalog-group-label'),
            rx.el.h2(description,class_name='catalog-group-title'),class_name='catalog-group-heading'),
        *shelves,id=anchor,class_name='catalog-group')


def discovery_page():
    return shell('Sua próxima história começa aqui.','Explore, registre e compartilhe o que faz parte do seu mundo.',
        rx.el.form(
            rx.el.div(rx.icon('search', size=24),
                rx.el.input(name='query',placeholder='Pesquisar filmes, séries, animes e livros',aria_label='Buscar título',max_length=200,value=S.search_term,on_change=S.update_search_term),
                rx.el.button('Buscar',type='submit',disabled=S.busy,class_name=BUTTON),class_name='search-box'),
            on_submit=S.search,class_name='space-y-7'),
        rx.el.div(*[rx.el.button(label,type='button',on_click=S.browse_category(value),
            disabled=S.busy,aria_pressed=S.search_active & (S.submitted_query == '') & (S.search_type == value),
            class_name='browse-category') for value,label in
            [('all','Todos'),('movie','Filmes'),('anime','Animes'),('series','Séries'),('book','Livros')]],
            class_name='category-filters',aria_label='Explorar categorias'),
        rx.cond(S.search_active,rx.el.button(rx.icon('arrow-left',size=16),'Voltar aos destaques',
            type='button',on_click=S.show_home_catalog,class_name='quiet-button')),
        rx.cond(~S.search_active & (S.featured_items.length()>0),
            rx.el.div(rx.foreach(S.featured_items[:1],lambda m:rx.el.article(
                rx.cond(((m['backdrop'] != '') & ~S.failed_covers.contains(m['backdrop'])) |
                        ((m['cover'] != '') & ~S.failed_covers.contains(m['cover'])),
                    CoverImage.create(src=rx.cond((m['backdrop'] != '') & ~S.failed_covers.contains(m['backdrop']),m['backdrop'],m['cover']),
                        alt='',class_name='spotlight-image',
                        on_error=S.cover_failed(rx.cond((m['backdrop'] != '') & ~S.failed_covers.contains(m['backdrop']),m['backdrop'],m['cover'])))),
                rx.el.div(rx.el.p('HOJE NO SEU RADAR',class_name='eyebrow'),
                    rx.el.p('Uma pausa. Uma grande história.',class_name='spotlight-kicker'),
                    rx.el.h2(m['title'],class_name='spotlight-title'),
                    rx.el.p(m['kind']+' · '+m['year'],class_name='spotlight-meta'),
                    rx.el.p(m['description'],class_name='spotlight-description'),
                    rx.el.div(button('Conhecer este filme',S.open_featured(m['source'],m['external_id'],'movie')),
                        rx.el.a('Explorar catálogo',href='#home-filmes',class_name='spotlight-secondary'),class_name='spotlight-actions'),
                    class_name='spotlight-copy'),class_name='home-spotlight')),class_name='spotlight-wrapper')),
        rx.cond(S.search_active,
            rx.el.section(rx.el.h2(rx.cond(S.submitted_query != '', 'Resultados da busca', 'Explorar catálogo'),class_name='section-title'),
                rx.el.div(rx.foreach(S.search_results,lambda m:media_card(m,True)),class_name='catalog-grid')),
            rx.cond(S.featured_items.length()==0,rx.el.section(
                rx.el.div(rx.el.p('CADA HISTÓRIA CONTA',class_name='eyebrow'),
                    rx.el.h2('Seu próximo favorito\nestá por aqui.',class_name='hero-title'),
                    rx.el.p('Descubra novas histórias, organize sua biblioteca e compartilhe o que você achou.',class_name='hero-description'),
                    rx.el.a(rx.cond(S.is_authenticated,'Minha biblioteca','Criar minha conta'),
                        href=rx.cond(S.is_authenticated,'/biblioteca','/cadastro'),class_name=BUTTON),class_name='hero-content'),
                rx.el.img(src='/mascot.png',alt='Mascote Codeboxd com uma lupa e um rolo de filme',class_name='hero-mascot'),
                class_name='discovery-hero'))),
        rx.cond(~S.search_active,rx.fragment(
            rx.el.nav(rx.el.span('ESCOLHA SEU UNIVERSO',class_name='catalog-jump-label'),
                *[rx.el.a(rx.icon(icon,size=18),label,href='#'+anchor,class_name='catalog-jump-link')
                    for anchor,label,icon in [('home-filmes','Filmes','clapperboard'),('home-series','Séries','tv'),
                        ('home-livros','Livros','book-open'),('home-animes','Animes','sparkles')]],
                class_name='catalog-jump',aria_label='Ir para uma seção do catálogo'),
            catalog_group('home-filmes','FILMES','Qual vai ser a sessão de hoje?','clapperboard',
                popular_section('Filmes populares',S.popular_movies,'movie'),
                collection_section('movies_now'),collection_section('movies_rated'),collection_section('movies_upcoming')),
            catalog_group('home-series','SÉRIES','Histórias para ficar mais um episódio.','tv',
                popular_section('Séries populares',S.popular_series,'series'),collection_section('series_rated')),
            rx.el.aside(rx.el.div(rx.el.p('SEU REPERTÓRIO, DO SEU JEITO',class_name='eyebrow'),
                rx.el.h2('Viu. Leu. Gostou? Guarde por aqui.'),
                rx.el.p('Monte sua lista, dê sua nota e encontre sua próxima obsessão.')),
                rx.el.a('Organizar minha biblioteca',href='/biblioteca',class_name='quiet-button'),class_name='home-library-banner'),
            catalog_group('home-livros','LIVROS','Vire a página. Descubra outro mundo.','book-open',
                collection_section('books_popular'),collection_section('books_fiction'),collection_section('books_fantasy'),
                collection_section('books_mystery'),collection_section('books_game_theory')),
            catalog_group('home-animes','ANIMES','Universos que vão além da imaginação.','sparkles',
                collection_section('anime_rated'),collection_section('anime_popular'),collection_section('anime_current')))),
        rx.cond(S.search_active & S.has_more_results,button('Carregar mais resultados',S.more_results,disabled=S.busy)),
        rx.cond(False,rx.fragment(
        rx.el.div(rx.el.h2('Na comunidade',class_name='section-title'),
                  rx.el.a('Conhecer pessoas →',href='/comunidade',class_name='text-sm brand-yellow'),class_name='flex items-center justify-between gap-4'),
        rx.cond(S.catalog_items.length()>0,
            rx.el.div(rx.foreach(S.catalog_items,lambda m:media_card(m)),class_name='catalog-grid'),
            rx.el.div(rx.icon('library',size=32),rx.el.p('Sua próxima descoberta começa com uma busca.'),
                rx.el.p('Pesquise uma obra e salve sua primeira experiência.',class_name='text-sm text-gray-400'),class_name='empty-state')))))


def rating_picker():
    return rx.el.div(
        rx.el.div(*[
            rx.el.div(
                rx.el.span('★',class_name='rating-star-base',aria_hidden=True),
                rx.el.span(rx.el.span('★',class_name='rating-star-glyph'),
                    style={'width':rx.cond(S.selected_rating_value >= value,'100%',
                        rx.cond(S.selected_rating_value >= value - 0.5,'50%','0%'))},
                    class_name='rating-star-fill',aria_hidden=True),
                *[rx.el.button(type='button',
                    aria_label='Nota '+str(score).removesuffix('.0').replace('.',',')+' de 5',
                    title=str(score).removesuffix('.0').replace('.',',')+' estrelas',
                    aria_pressed=S.selected_rating_value == score,
                    on_click=S.set_selected_rating(str(score)),
                    class_name='rating-star-option '+position)
                    for score,position in ((value-0.5,'half'),(value,'whole'))],
                class_name='rating-star-control') for value in range(1,6)],
            role='group',aria_label='Sua avaliação em meias estrelas',class_name='rating-stars'),
        rx.el.label(rx.el.span('Sua nota',class_name='text-sm text-gray-400'),
            rx.el.select(rx.el.option('Sem nota',value='0'),
                *[rx.el.option(str(value/2).removesuffix('.0').replace('.',',')+' / 5',
                    value=str(value/2).removesuffix('.0')) for value in range(1,11)],
                name='rating',value=S.selected_rating,on_change=S.set_selected_rating,
                class_name=INPUT),class_name='rating-value-select'),
        rx.el.p('Selecione meia estrela ou uma estrela inteira.',class_name='text-xs text-gray-400'),
        class_name='space-y-2')


def media_page():
    return rx.fragment(shell('Detalhes da obra','Conheça a história e registre sua experiência.',
        rx.el.a(
            rx.el.span(rx.icon('arrow-left',size=17,aria_hidden=True),class_name='media-back-icon'),
            rx.el.span('Voltar à descoberta'),href='/',class_name='media-back-link'),
        rx.cond(S.selected['title']!='',rx.el.div(
            rx.cond(S.media_details_loading,rx.el.p('Carregando informações complementares…',role='status')),
            rx.cond(S.media_details_error!='',rx.el.p(S.media_details_error,role='alert')),
            rx.el.section(
                rx.cond(S.selected['cover']!='',rx.el.img(src=S.selected['cover'],alt='Capa de '+S.selected['title'],class_name='media-detail-poster'),
                    rx.el.div(rx.icon('clapperboard',size=48),class_name='media-detail-poster cover-empty')),
                rx.cond(S.selected['backdrop']!='',rx.el.img(src=S.selected['backdrop'],alt='',aria_hidden=True,class_name='media-detail-backdrop'),rx.fragment()),
                rx.el.div(rx.el.p(S.selected['kind']+'  ·  '+S.selected['year'],class_name='eyebrow'),
                    rx.el.h2(S.selected['title'],class_name='media-detail-title'),
                    rx.el.p(rx.cond(S.selected['description']!='',S.selected['description'],'Descrição ainda não disponível.'),class_name='media-detail-description'),
                    class_name='media-detail-copy'),class_name='media-detail-hero'),
            rx.cond(S.is_authenticated,button('Denunciar obra',S.open_report('media',S.selected['id']))),
            rx.el.section(rx.el.h2('Ficha da obra',class_name='section-title'),
                rx.el.p(rx.cond(S.selected['details']!='',S.selected['details']+'  ·  '+S.selected['kind']+'  ·  '+S.selected['year'],
                    S.selected['kind']+'  ·  '+S.selected['year']),class_name='media-facts'),class_name='space-y-3'),
            rx.cond(S.selected['source']=='tmdb',
                rx.el.section(rx.el.h2('Onde assistir',class_name='section-title'),
                    rx.cond(S.availability.length()>0,
                        rx.el.div(rx.foreach(S.availability,lambda provider:rx.el.a(
                            rx.el.span(provider['name']), href=provider['url'], target='_blank',
                            rel='noopener noreferrer', class_name='availability-chip')),
                            class_name='availability-list'),
                        rx.el.p('Nenhum servico de distribuicao foi informado para o Brasil.',class_name='text-sm text-gray-400')),
                rx.fragment())),
            rx.cond(S.trailers.length()>0,rx.el.section(rx.el.h2('Trailers',class_name='section-title'),
                rx.el.div(rx.foreach(S.trailers,lambda trailer:rx.el.article(
                    rx.el.h3(trailer['title'],class_name='font-semibold mb-3'),
                    rx.el.iframe(src=trailer['embed_url'],title=trailer['title'],loading='lazy',
                        allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share',
                        allow_fullscreen=True,class_name='media-trailer'),class_name='media-trailer-card')),
                    class_name='media-trailer-list')),rx.fragment()),            rx.el.div(rx.el.section(rx.el.h2('O que você achou?',class_name='section-title'),
                rx.cond(S.is_authenticated,rx.cond(S.media_interaction_loading,
                    rx.el.p('Carregando sua avaliação…',role='status'),rx.cond(S.review_editor_open,rx.el.form(
                    rx.el.fieldset(
                    rx.el.input(name='media_key',type='hidden',value=S.selected['key']),
                    rx.el.input(name='status',type='hidden',value=S.selected_status),
                    rx.el.div(rx.foreach([('planned','Quero ver / ler'),('in_progress','Em andamento'),('completed','Concluído'),('dropped','Abandonado')],
                        lambda pair:rx.el.button(pair[1],type='button',on_click=S.set_selected_status(pair[0]),
                            class_name=rx.cond(S.selected_status==pair[0],'status-chip selected','status-chip'))),class_name='media-statuses'),
                    rating_picker(),
                    textarea('Sua crítica detalhada (obrigatória)','review',S.selected_review,required=True,min_length=1,max_length=10000,rows=5,placeholder='Conte o que achou desta obra...'),
                    check('Contém spoilers','spoiler',S.selected_spoiler),
                    submit(rx.cond(S.interaction_saving,'Salvando…','Salvar avaliação'),disabled=S.interaction_saving),
                    disabled=S.interaction_saving,class_name='media-review-form',aria_busy=S.interaction_saving),
                    on_submit=S.submit_interaction.throttle(1000),key=S.selected['key']+S.selected_review,class_name='media-review-form'),
                    rx.el.div(
                        rx.el.p('Avaliação salva',role='status',class_name='font-semibold brand-yellow'),
                        rx.el.p(rx.cond(S.selected_rating=='0','Sem nota','Sua nota: '+S.selected_rating.replace('.',',')+' / 5')),
                        rx.cond(S.selected_review!='',rx.el.p(S.selected_review,class_name='whitespace-pre-wrap')),
                        button('Editar avaliação',S.edit_interaction),class_name=CARD))),
                    rx.el.div(rx.el.h3('Avalie esta obra',class_name='font-semibold'),
                        rx.el.p('Sua nota fica salva apenas neste navegador e não aparece no perfil nem na comunidade.',class_name='text-sm text-gray-400'),
                        rating_picker(),
                        rx.cond(S.notice!='',rx.el.p(S.notice,class_name='text-sm text-amber-300')),
                        rx.el.p('Crie uma conta para publicar uma crítica, salvar na biblioteca, criar posts ou seguir pessoas.',class_name='text-sm text-gray-400'),
                        rx.el.a('Criar conta',href='/cadastro',class_name=BUTTON+' inline-block'),class_name=CARD))),
                rx.el.aside(rx.el.h2('Adicione às suas listas',class_name='section-title'),
                    rx.el.div(
                        rx.el.button('Quero ver / ler',on_click=S.quick_add('planned',0,'Quero ver / ler'),class_name='media-list-link'),
                        rx.el.button('Já assisti / li',on_click=S.quick_add('completed',0,'Já assisti / li'),class_name='media-list-link'),
                        class_name='media-list-grid'),
                    button('Adicionar a outra lista',S.open_media_lists,disabled=S.list_item_saving),
                    rx.cond(S.media_list_open,rx.el.div(
                        rx.el.h3('Escolha uma lista',class_name='font-semibold'),
                        rx.cond(S.media_list_loading,rx.el.p('Carregando suas listas…',role='status'),rx.fragment()),
                        rx.cond(S.media_list_error!='',rx.el.p(S.media_list_error,role='alert'),rx.fragment()),
                        rx.el.select(rx.el.option('Selecione uma lista',value=''),
                            rx.foreach(S.media_list_options,lambda item:rx.el.option(
                                item['title']+rx.cond(item['is_public']=='True',' · Pública',' · Privada'),value=item['id'])),
                            value=S.media_list_target,on_change=S.select_media_list,aria_label='Lista de destino',
                            disabled=S.list_item_saving,class_name=INPUT),
                        button(rx.cond(S.list_item_saving,'Adicionando…','Confirmar inclusão'),S.add_current_media_to_list,
                            disabled=S.list_item_saving | (S.media_list_target=='')),
                        button('Cancelar',S.close_media_lists,disabled=S.list_item_saving),
                        class_name='space-y-3 mt-4'),rx.fragment()),
                    rx.el.a('Abrir minhas listas →',href='/listas',class_name='block brand-yellow mt-4')),
                class_name='review-layout'),
            rx.el.section(rx.el.h2('Outros comentários',class_name='section-title'),
                rx.cond(S.community_reviews.length()>0,
                    rx.el.div(rx.foreach(S.community_reviews,lambda review:rx.el.article(
                        rx.el.div(rx.el.strong(review['author']),
                            rx.cond(review['rating']!='',rx.el.span('  ·  Nota '+review['rating'],class_name='brand-yellow')),
                            rx.cond(review['date']!='',rx.el.span('  ·  '+review['date'],class_name='text-xs text-gray-500')),
                            class_name='flex flex-wrap items-center gap-2'),
                        rx.el.p(review['body'],class_name='text-sm leading-relaxed whitespace-pre-wrap mt-3'),class_name='media-community-review')),
                        class_name='media-community-reviews'),
                    rx.el.p('Ainda não há críticas públicas desta fonte.',class_name='text-sm text-gray-400'))),
            rx.el.section(rx.el.h2('Outras recomendações',class_name='section-title'),
                rx.cond(S.recommendations.length()>0,
                    rx.el.div(rx.foreach(S.recommendations,lambda m:rx.el.button(
                        cover_image(m),
                        rx.el.div(rx.el.h3(m['title'],class_name='font-semibold line-clamp-2'),rx.el.p(m['year'],class_name='text-sm text-gray-400'),class_name='p-4'),
                        on_click=S.open_recommendation(m['source'],m['external_id']),type='button',class_name='media-card text-left')),
                        class_name='media-shelf'),rx.el.p('Ainda não há recomendações desta fonte.',class_name='text-sm text-gray-400')),
                class_name='space-y-4'),class_name='space-y-8'),
            rx.el.p('Escolha uma obra pela página Descobrir.'))),report_dialog())
def spoiler(body, flag):
    return rx.cond(flag=='True',rx.el.details(rx.el.summary('Mostrar conteúdo com spoilers',class_name='cursor-pointer text-amber-300'),
        rx.el.p(body,class_name='whitespace-pre-wrap mt-3')),rx.el.p(body,class_name='whitespace-pre-wrap'))


def interaction(i):
    return rx.el.article(
        rx.el.a(rx.cond(i['cover']!='',rx.el.img(src=i['cover'],alt=i['title'],loading='lazy'),
            rx.icon('book-open',size=28)),href='/obra/'+i['id'],class_name='activity-cover'),
        rx.el.div(rx.el.a(i['title'],href='/obra/'+i['id'],class_name='font-semibold'),
            rx.el.p(i['kind']+' · '+i['status']+' · '+i['rating'],class_name='activity-meta'),
            spoiler(i['review'],i['spoiler']),class_name='min-w-0'),class_name='activity-card')


def library_page():
    return shell('Minha biblioteca','Cada história tem seu momento. Organize as suas.',
        rx.cond(S.library.length()>0,rx.foreach(S.visible_library,interaction),
            rx.cond(~S.busy & ~S.library_loading & (S.library_error=='') & (S.notice==''),
                rx.el.p('Sua biblioteca está vazia. Descubra uma obra e salve sua experiência.'))),
        rx.cond(S.library_error!='',rx.el.p(S.library_error,role='alert')),
        rx.cond(rx.cond(S.library_paginated,S.library_has_more,S.library.length()>S.visible_count),
            button(rx.cond(S.library_loading,'Carregando…',rx.cond(S.library_error!='','Tentar novamente','Mostrar mais')),
                   S.show_more_library,disabled=S.library_loading | S.busy)),
        rx.el.a('Descobrir obras',href='/',class_name='text-[#F5B300]'))


def person(p):
    return rx.el.article(rx.el.a(p['display_name'],href='/perfil/'+p['user_id'],class_name='text-xl font-semibold'),
        rx.el.p('@'+p['username'],class_name='text-[#F5B300]'),rx.el.p(p['bio'],class_name='text-gray-400'),
        rx.cond(S.is_authenticated & (p['user_id']!=S.user_id.to_string()),
            button(rx.cond(S.following_ids.contains(p['user_id']),'Deixar de seguir','Seguir'),S.follow(p['user_id']))),class_name=CARD)


def community_page():
    return shell('Encontre sua comunidade','Conheça outras bibliotecas e acompanhe novas perspectivas.',
                 grid(S.visible_people,person,'Nenhum perfil disponível por enquanto.'),
                 rx.cond(S.people.length()>S.visible_count,button('Mostrar mais',S.show_more)))


def profile_page():
    banner_uploader=rx.cond(S.owns_profile,rx.el.div(
        rx.upload(rx.el.div(rx.icon('image-up',size=18),rx.el.span('Escolher ou arrastar uma imagem para o banner'),
            class_name='profile-upload-prompt'),id='profile_banner_upload',accept={'image/png':['.png'],'image/jpeg':['.jpg','.jpeg'],
                'image/webp':['.webp'],'image/gif':['.gif']},max_files=1,max_size=5*1024*1024,
            class_name='profile-upload-dropzone'),
        rx.cond(rx.selected_files('profile_banner_upload').length()>0,
            rx.el.p(rx.selected_files('profile_banner_upload')[0],class_name='text-sm text-gray-400')),
        button('Enviar banner',S.upload_profile_banner(rx.upload_files(upload_id='profile_banner_upload'))),
        class_name='profile-banner-editor'),rx.fragment())
    profile_form=rx.el.form(field('Nome de usuário','username',S.profile['username'],required=True,pattern='[a-z0-9_]{3,30}',max_length=30),
        field('Nome de exibição','display_name',S.profile['display_name'],required=True,max_length=80),
        textarea('Bio','bio',S.profile['bio'],max_length=1000),field('Foto (URL HTTPS)','avatar_url',S.profile['avatar_url'],type='url'),
        submit('Salvar perfil'),on_submit=S.save_profile,key=S.profile['username'],class_name='editor-form')
    return rx.fragment(shell('Perfil','Histórias, conexões e experiências.',
        rx.el.section(rx.el.div(rx.cond(S.profile['banner_url']!='',rx.el.img(src=S.profile['banner_url'],
                alt='Banner de '+S.profile['display_name'],class_name='profile-banner-image')),
                class_name='profile-banner'),
            rx.el.div(avatar(S.profile['avatar_url'],S.profile['display_name']),
                rx.el.div(rx.el.h2(S.profile['display_name'],class_name='text-2xl font-bold'),
                    rx.el.p('@'+S.profile['username'],class_name='brand-yellow'),rx.el.p(S.profile['bio'],class_name='profile-bio'),class_name='profile-identity'),
                rx.cond(S.owns_profile,rx.dialog.root(
                    rx.dialog.trigger(rx.el.button('Editar perfil',class_name='quiet-button')),
                    rx.dialog.content(rx.dialog.title('Editar perfil'),rx.dialog.description('Conte um pouco sobre você.'),
                        rx.el.p(S.notice,role='status'),banner_uploader,profile_form,
                        rx.dialog.close(rx.el.button('Fechar',class_name='quiet-button')),class_name='codeboxd-dialog')),
                    rx.cond(S.is_authenticated,button(rx.cond(S.following_ids.contains(S.profile['user_id']),'Deixar de seguir','Seguir'),S.follow(S.profile['user_id']),disabled=S.profile_people_loading | (S.profile_people_error!='')))),
                class_name='profile-summary'),class_name='profile-panel'),
        rx.cond(S.profile['user_id']!=S.user_id.to_string(),button('Denunciar perfil',S.open_report('profile',S.profile['user_id']))),
        rx.el.div(*[rx.el.a(rx.el.strong(count),rx.el.span(label),href=href,class_name='profile-stat') for count,label,href in
            [(S.profile_counts['followers'],'Seguidores','#seguidores'),(S.profile_counts['following'],'Seguindo','#seguindo'),
             (S.profile_counts['activities'],'Obras registradas','#atividades')]],class_name='profile-statistics'),
        rx.el.section(rx.el.h2('Avaliações e atividades',class_name='section-title'),
            rx.cond(S.profile_activity_loading,rx.el.p('Carregando atividades…',role='status'),
                rx.cond(S.profile_activity_error!='',rx.el.p(S.profile_activity_error,role='alert',class_name='text-red-400'),
                    rx.cond(S.profile_activity.length()>0,rx.foreach(S.profile_activity,interaction),rx.el.p('Nenhuma experiência registrada.',class_name='empty-state')))),id='atividades',class_name='space-y-4'),
        rx.el.section(rx.el.h2('Seguidores',class_name='section-title'),
            rx.cond(S.profile_people_loading,rx.el.p('Carregando seguidores…',role='status'),
                rx.cond(S.profile_people_error!='',rx.el.p(S.profile_people_error,role='alert',class_name='text-red-400'),grid(S.followers,person,'Ainda não há seguidores.'))),id='seguidores'),
        rx.el.section(rx.el.h2('Seguindo',class_name='section-title'),
            rx.cond(S.profile_people_loading,rx.el.p('Carregando conexões…',role='status'),
                rx.cond(S.profile_people_error!='',rx.el.p(S.profile_people_error,role='alert',class_name='text-red-400'),grid(S.following,person,'Ainda não segue ninguém.'))),id='seguindo')),report_dialog())


def media_select(value='0'):
    return rx.el.label('Obra',rx.el.select(rx.el.option('Sem obra associada',value='0'),
        rx.foreach(S.catalog_items,lambda m:rx.el.option(m['title'],value=m['id'])),
        name='media_id',default_value=value,class_name=INPUT))


def post_media_picker():
    return rx.el.section(
        rx.el.p('Obra associada',class_name='block text-sm text-gray-300'),
        rx.el.div(rx.el.input(type='search',value=S.post_media_query,on_change=S.update_post_media_query,
            placeholder='Pesquisar filme, serie, anime ou livro',class_name=INPUT),
            button(rx.cond(S.post_media_searching,'Pesquisando...','Pesquisar obra'),S.search_post_media),
            class_name='post-media-search'),
        rx.cond((S.post_media_selected['id']!='') | (S.post_media_selected['key']!=''),rx.el.div(
            rx.cond(S.post_media_selected['cover']!='',rx.el.img(src=S.post_media_selected['cover'],
                alt=S.post_media_selected['title'],class_name='post-media-selected-cover')),
            rx.el.strong(S.post_media_selected['title']),
            button('Remover obra',S.clear_post_media),class_name='post-media-selected'),rx.fragment()),
        rx.cond(S.post_media_results.length()>0,rx.el.div(rx.foreach(S.post_media_results,
            lambda item:rx.el.button(
                rx.cond(item['cover']!='',rx.el.img(src=item['cover'],alt='',class_name='post-media-result-cover'),
                    rx.icon('clapperboard',size=22)),
                rx.el.span(item['title'],class_name='font-semibold'),
                rx.el.span(item['kind']+' · '+item['year'],class_name='text-xs text-gray-400'),
                on_click=S.select_post_media(item['key']),type='button',class_name='post-media-result')),
            class_name='post-media-results'),rx.fragment()),
        rx.cond(S.post_media_searching,rx.el.p('Buscando no catalogo...',class_name='text-sm text-gray-400'),rx.fragment()),
        class_name='post-media-picker')


def post_image_picker():
    return rx.el.section(
        rx.el.p('Imagem da publicacao (opcional)',class_name='block text-sm text-gray-300'),
        rx.upload(rx.el.div(rx.icon('image-up',size=22),
            rx.el.span('Escolha ou arraste uma imagem (ate 5 MB)',class_name='text-sm'),
            class_name='post-image-upload-prompt'),id='post_image_upload',
            accept={'image/png':['.png'],'image/jpeg':['.jpg','.jpeg'],'image/webp':['.webp'],
                'image/gif':['.gif']},max_files=1,max_size=5*1024*1024,
            on_drop=S.stage_post_image(rx.upload_files(upload_id='post_image_upload')),
            class_name='post-image-dropzone'),
        rx.cond(rx.selected_files('post_image_upload').length()>0,
            rx.el.div(rx.el.span(rx.selected_files('post_image_upload')[0],class_name='post-image-filename'),
                rx.cond(S.post_image_staging,rx.el.span('Carregando imagem...',role='status'),
                    rx.el.button('Descartar seleção',type='button',
                        on_click=rx.clear_selected_files('post_image_upload'),class_name='quiet-button')),
                class_name='post-image-upload-actions'),rx.fragment()),
        rx.cond(S.post_image_filename!='',rx.el.div(
            rx.el.img(src=rx.get_upload_url(S.post_image_filename),alt='Previa da imagem enviada',
                class_name='post-image-preview'),button('Remover imagem',S.remove_post_image),class_name='space-y-2'),
            rx.cond(S.post_existing_image_url!='',rx.el.img(src=S.post_existing_image_url,
                alt='Imagem atual da publicacao',class_name='post-image-preview'),rx.fragment())),
        class_name='post-image-picker')


def post(p):
    return rx.el.article(
        rx.el.div(
            rx.el.div(rx.el.a(avatar(p['avatar'],p['author']),href='/perfil/'+p['user_id']),
                rx.el.div(rx.el.a(p['author'],href='/perfil/'+p['user_id'],class_name='font-semibold'),
                    rx.el.p(p['published_at'],class_name='text-xs text-gray-500')),
                class_name='flex min-w-0 items-center gap-3 post-author'),
            rx.cond((p['media_id']!='0') & (p['media_id']!=''),rx.el.a(
                rx.cond(p['media_cover']!='',rx.el.img(src=p['media_cover'],alt=p['media_title'],loading='lazy',
                    style={'width':'36px','height':'48px','objectFit':'cover','borderRadius':'6px','flexShrink':'0'},
                    class_name='post-work-thumbnail'),
                    rx.el.span(rx.icon('book-open',size=18),class_name='post-work-placeholder',
                        style={'width':'36px','height':'48px','display':'flex','alignItems':'center',
                            'justifyContent':'center','flexShrink':'0'})),
                rx.el.div(rx.el.span('Obra associada',class_name='text-xs text-gray-400'),
                    rx.el.strong(rx.cond(p['media_title']!='',p['media_title'],'Ver obra'),
                        class_name='block truncate text-sm'),class_name='min-w-0'),
                rx.icon('chevron-right',size=16),href='/obra/'+p['media_id'],title=p['media_title'],
                class_name='ml-auto flex min-w-0 max-w-[55%] items-center gap-2 rounded-lg border border-white/10 px-2 py-1'),
                rx.fragment()),
            class_name='flex flex-wrap items-center justify-between gap-3'),
        rx.cond(p['image_url']!='',rx.el.img(src=p['image_url'],alt='Imagem anexada a publicacao',
            loading='lazy',class_name='post-personal-image')),
        spoiler(p['body'],p['spoiler']),
        rx.el.div(rx.el.button(rx.icon('heart',size=25,fill=rx.cond(S.liked_posts.contains(p['id']),'currentColor','none')),
            on_click=S.like(p['id']),disabled=S.liking_posts.contains(p['id']),
            aria_label=rx.cond(S.liked_posts.contains(p['id']),'Descurtir publicação','Curtir publicação'),
            aria_pressed=S.liked_posts.contains(p['id']),
            class_name=rx.cond(S.liked_posts.contains(p['id']),'post-icon-button post-liked','post-icon-button')),
            rx.el.button(rx.icon('message-circle',size=25),on_click=S.discussion(p['id']),aria_label='Abrir comentários',class_name='post-icon-button'),
            class_name='post-interactions'),
        rx.cond(p['likes_count']!='',rx.el.strong(rx.cond(p['likes_count']=='1','1 curtida',p['likes_count']+' curtidas'),class_name='post-like-count')),
        rx.el.button(rx.cond((p['comments_count']!='') & (p['comments_count']!='0'),'Ver comentários ('+p['comments_count']+')','Adicionar um comentário…'),
            on_click=S.discussion(p['id']),class_name='post-comments-link'),
        rx.cond(S.post_interaction_errors.get(p['id'],'')!='',rx.el.p(S.post_interaction_errors.get(p['id'],''),role='alert',class_name='post-interaction-error')),
        rx.el.div(
            rx.cond(p['user_id']!=S.user_id.to_string(),rx.el.button('Denunciar',on_click=S.open_report('post',p['id']),class_name='quiet-button')),
            rx.cond(p['user_id']==S.user_id.to_string(),rx.fragment(rx.el.button('Editar',on_click=S.edit_post(p['id']),class_name='quiet-button'),confirm('Excluir publicação',S.remove_post(p['id'])))),
            class_name='post-actions'),class_name='post-card')


def comment(c):
    return rx.el.article(rx.el.a(avatar(c.get('avatar',''),c['author']),href='/perfil/'+c['user_id']),
        rx.el.div(rx.el.p(rx.el.a(c['author'],href='/perfil/'+c['user_id'],class_name='comment-author'),' ',c['body'],class_name='comment-text'),
            rx.cond(c['user_id']==S.user_id.to_string(),rx.el.div(
                rx.el.button('Editar',on_click=S.edit_comment(c['id']),disabled=S.comment_saving,class_name='comment-option'),
                rx.el.button('Excluir',on_click=S.remove_comment(c['id']),disabled=S.comment_saving | (S.deleting_comments.length()>0),class_name='comment-option'),class_name='comment-options'),
                rx.el.button('Denunciar',on_click=S.open_report('comment',c['id']),class_name='comment-option')),
            class_name='comment-content'),class_name='post-comment')


def post_discussion():
    return rx.dialog.root(rx.dialog.content(
        rx.el.div(rx.dialog.title('Comentários'),rx.dialog.close(rx.el.button(rx.icon('x',size=20),aria_label='Fechar comentários',class_name='post-icon-button')),class_name='post-discussion-heading'),
        rx.dialog.description('Converse sobre esta publicação.',class_name='post-discussion-description'),
        rx.el.div(
            rx.cond(S.discussion_loading,rx.el.p('Carregando comentários…',role='status',class_name='post-comments-empty'),
                rx.cond(S.comments.length()>0,rx.foreach(S.comments,comment),rx.el.div(rx.icon('message-circle',size=30),
                    rx.el.strong('Ainda não há comentários'),rx.el.p('Seja a primeira pessoa a comentar.'),class_name='post-comments-empty'))),
            class_name='post-comments-list'),
        rx.cond(S.discussion_error!='',rx.el.div(rx.el.p(S.discussion_error,role='alert'),
            rx.el.button('Recarregar comentários',on_click=S.discussion(S.selected_post),disabled=S.discussion_loading | S.comment_saving,class_name='comment-option'),class_name='post-interaction-error')),
        rx.cond(S.edit_comment_id!='',rx.el.div(rx.el.span('Editando comentário'),
            rx.el.button('Cancelar edição',on_click=S.cancel_comment_edit,disabled=S.comment_saving,class_name='comment-option'),class_name='comment-editing')),
        rx.el.form(
            rx.el.input(type='hidden',name='post_id',value=S.selected_post),
            rx.el.input(type='hidden',name='comment_token',value=S.comment_editor_token),
            rx.el.textarea(name='body',value=S.edit_comment_body,on_change=S.set_comment_body,required=True,max_length=2000,
                placeholder='Adicione um comentário…',aria_label='Comentário',disabled=S.comment_saving,class_name='post-comment-input'),
            rx.el.button(rx.cond(S.comment_saving,'Enviando…',rx.cond(S.edit_comment_id!='','Salvar','Publicar')),
                type='submit',disabled=S.comment_saving | S.discussion_loading | (S.deleting_comments.length()>0),class_name='post-comment-submit'),
            on_submit=S.save_comment,class_name='post-comment-composer'),
        class_name='post-discussion-dialog',max_width='640px',width='calc(100vw - 24px)',padding='0'),
        open=S.selected_post!='',on_open_change=S.set_discussion_open)


def report_dialog():
    return rx.cond(S.report_dialog_open,rx.el.div(
        rx.el.section(
            rx.el.h2('Denunciar conteúdo',class_name='text-xl font-bold'),
            rx.el.p('A equipe analisará este conteúdo. O envio do report não o altera nem o remove.',class_name='text-sm text-gray-400'),
            rx.el.form(
                rx.cond(S.report_error != '', rx.el.p(S.report_error, role='alert', class_name='text-sm text-red-400')),
                rx.el.label('Motivo',html_for='report-reason',class_name='block text-sm text-gray-300'),
                rx.el.select(rx.el.option('Spam',value='spam'),rx.el.option('Assédio',value='harassment'),
                    rx.el.option('Conteúdo impróprio',value='inappropriate'),rx.el.option('Outro',value='other'),
                    id='report-reason',name='reason',value=S.report_reason,on_change=S.set_report_reason,class_name=INPUT),
                rx.el.label('Detalhes (obrigatórios)',html_for='report-description',class_name='block text-sm text-gray-300'),
                rx.el.textarea(id='report-description',name='description',required=True,min_length=1,max_length=2000,
                    value=S.report_description,on_change=S.set_report_description,
                    placeholder='Inclua somente o contexto necessário para a análise.',class_name=INPUT),
                rx.el.div(
                    rx.el.button('Cancelar',type='button',on_click=S.close_report,disabled=S.report_sending,class_name='quiet-button'),
                    rx.el.button(rx.cond(S.report_sending,'Enviando…','Enviar report'),type='submit',disabled=S.report_sending,class_name=BUTTON),
                    class_name='flex justify-end gap-3'),
                on_submit=S.submit_report,class_name='space-y-3'),
            class_name='report-dialog-card',role='dialog',aria_modal='true',aria_label='Denunciar conteúdo'),
        class_name='report-dialog-overlay'),rx.fragment())


def feed_page():
    return rx.fragment(shell('Entre histórias','Compartilhe descobertas e acompanhe quem você segue.',
        editor(rx.cond(S.edit_post_id!='','Editar publicação','Criar publicação'),'Compartilhe uma história com sua comunidade.',
            rx.fragment(post_media_picker(),post_image_picker(),
                rx.el.form(textarea('Sua publicação','body',S.edit_post_body,required=True,max_length=5000),
                    rx.el.input(type='hidden',name='post_id',value=S.edit_post_id),
                    rx.el.input(type='hidden',name='editor_token',value=S.post_editor_token),
                    check('Contém spoilers','spoiler',S.edit_post_spoiler),submit(
                        rx.cond(S.post_saving,'Salvando…',rx.cond(S.edit_post_id!='','Salvar edição','Publicar')),
                        disabled=S.post_saving | (rx.selected_files('post_image_upload').length()>0)),
                    on_submit=S.save_post,key=S.edit_post_id,class_name='editor-form')),
            open=S.post_editor_open,on_open_change=S.set_post_editor_open),
        rx.el.div(rx.el.section(
            rx.cond(S.posts.length()>0,rx.foreach(S.visible_posts,post),rx.el.div(rx.icon('messages-square',size=36),
                rx.el.p('Seu feed começa com uma boa história.'),rx.el.a('Encontrar pessoas',href='/comunidade',class_name='brand-yellow'),class_name='empty-state')),
            rx.cond(S.posts.length()>S.visible_count,button('Mostrar mais',S.show_more)),
            class_name='feed-stream'),
            rx.el.aside(button('+ Criar publicação',S.new_post),rx.el.h2('Pessoas da comunidade',class_name='section-title'),
                rx.foreach(S.suggested_people,lambda p:rx.el.a(avatar(p['avatar_url'],p['display_name']),
                    rx.el.div(rx.el.strong(p['display_name']),rx.el.p('@'+p['username'])),href='/perfil/'+p['user_id'],class_name='sidebar-person')),
                rx.el.a('Explorar comunidade →',href='/comunidade',class_name='brand-yellow'),class_name='feed-sidebar'),class_name='feed-layout')),
        post_discussion(),report_dialog())


def list_card(item):
    return rx.el.button(rx.icon('list-video',size=20),rx.el.span(item['title']),
        rx.el.span(rx.cond(item['is_public']=='True','Pública','Privada'),class_name='list-visibility'),rx.icon('chevron-right',size=18),
        on_click=S.open_list(item['id']),type='button',class_name='list-row',disabled=S.list_saving)


def public_list_group(group):
    return rx.el.section(
        rx.el.a(avatar(group['avatar_url'],group['display_name']),
            rx.el.span(group['display_name'],class_name='public-list-owner-name font-semibold'),
            href='/perfil/'+group['user_id'],class_name='public-list-owner'),
        rx.el.div(rx.foreach(group['lists'],list_card),class_name='list-directory'),
        class_name='public-list-group')


def list_item(m):
    return rx.el.article(media_card(m),rx.cond(S.owns_list,confirm('Remover obra',S.remove_list_item(m['id']))),class_name='list-media-item')


def list_media_search():
    return rx.el.section(
        rx.el.h3('Adicionar obras à lista',class_name='font-semibold'),
        rx.el.div(rx.el.input(type='search',value=S.list_media_query,on_change=S.update_list_media_query,
            placeholder='Buscar filmes, séries, animes e livros',aria_label='Buscar obras para a lista',class_name=INPUT),
            button(rx.cond(S.list_media_searching,'Pesquisando…','Buscar obras'),S.search_list_media,
                disabled=S.list_media_searching | S.list_item_saving),class_name='post-media-search'),
        rx.cond(S.list_media_error!='',rx.el.p(S.list_media_error,role='alert'),rx.fragment()),
        rx.cond(S.list_media_searching,rx.el.p('Buscando no catálogo…',role='status'),rx.fragment()),
        rx.el.div(rx.foreach(S.list_media_results,lambda item:rx.el.div(
            rx.cond(item['cover']!='',rx.el.img(src=item['cover'],alt='',class_name='post-media-result-cover'),rx.icon('clapperboard',size=22)),
            rx.el.div(rx.el.strong(item['title']),rx.el.p(item['kind']+' · '+item['year'],class_name='text-sm text-gray-400'),class_name='min-w-0 flex-1'),
            button('Adicionar',S.add_list_result(item['key']),disabled=S.list_item_saving),
            class_name='flex items-center gap-3 rounded-xl border border-white/10 p-3')),class_name='space-y-2'),
        class_name='space-y-3')


def lists_page():
    return shell('Listas','Um lugar para cada história que você quer guardar.',
        rx.el.h2(rx.cond(S.is_authenticated & (S.list_scope=='own'),'Suas listas','Listas públicas'),class_name='section-title'),
        rx.cond(S.is_authenticated,rx.el.div(
            button('Minhas listas',S.change_list_scope('own'),disabled=S.list_saving | (S.list_scope=='own')),
            button('Explorar listas públicas',S.change_list_scope('public'),disabled=S.list_saving | (S.list_scope=='public')),
            class_name='flex flex-wrap gap-3')),
        rx.cond(S.is_authenticated & (S.list_scope=='own'),button('Criar lista',S.new_list,disabled=S.list_saving)),
        editor(rx.cond(S.selected_list['id']=='','Criar lista','Editar lista'),'Organize suas próximas descobertas.',
            rx.el.form(field('Título','title',S.selected_list['title'],required=True,max_length=120),
                textarea('Descrição','description',S.selected_list['description'],max_length=2000),
                check('Lista pública','is_public',S.selected_list['is_public']=='True'),
                submit(rx.cond(S.list_saving,'Salvando…','Salvar lista'),disabled=S.list_saving),
                on_submit=S.save_list,key=S.selected_list['id']+S.selected_list['title'],class_name='editor-form'),
            open=S.list_editor_open,on_open_change=S.set_list_editor_open),
        rx.cond(S.lists.length()>0,
            rx.cond(S.is_authenticated & (S.list_scope=='own'),
                rx.el.div(rx.foreach(S.visible_lists,list_card),class_name='list-directory'),
                rx.el.div(rx.foreach(S.public_list_groups,public_list_group),class_name='public-list-groups')),
            rx.el.p(rx.cond(S.is_authenticated & (S.list_scope=='own'),
                'Você ainda não tem listas. Crie sua primeira coleção.','Nenhuma lista pública disponível.'),class_name='empty-state')),
        rx.cond(S.lists.length()>S.visible_count,button('Mostrar mais',S.show_more)),
        rx.cond(S.selected_list['id']!='',rx.el.section(
            rx.el.div(rx.el.div(rx.el.h2(S.selected_list['title'],class_name='section-title'),rx.el.p(S.selected_list['description'])),
                rx.cond(S.owns_list,rx.el.div(button('Editar lista',S.set_list_editor_open(True),disabled=S.list_saving),
                    confirm('Excluir lista',S.remove_list,disabled=S.list_saving),class_name='post-actions')),
                class_name='list-heading'),
            rx.cond(S.owns_list,list_media_search()),
            rx.cond(S.list_items.length()>0,rx.el.div(rx.foreach(S.list_items,list_item),class_name='catalog-grid'),
                rx.el.p('Esta lista ainda não tem obras.',class_name='empty-state')),class_name='space-y-5')))
