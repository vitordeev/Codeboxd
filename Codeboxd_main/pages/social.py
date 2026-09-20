"""Public discovery and authenticated social pages."""
import reflex as rx
from ..state.social import SocialState as S
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


def submit(label):
    return rx.el.button(label, type='submit', class_name=BUTTON)


def confirm(label, action):
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(rx.el.button(label, type='button', class_name='quiet-button danger')),
        rx.alert_dialog.content(
            rx.alert_dialog.title(label+'?'),
            rx.alert_dialog.description('Esta ação remove o conteúdo. Deseja continuar?'),
            rx.flex(rx.alert_dialog.cancel(rx.button('Cancelar', variant='soft')),
                    rx.alert_dialog.action(rx.button('Confirmar exclusão', on_click=action, color_scheme='red')),
                    gap='3', justify='end', margin_top='20px'), class_name='codeboxd-dialog'))


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


def media_card(m, search=False):
    content=rx.el.div(
        rx.cond(m['cover']!='',rx.el.img(src=m['cover'],alt=m['title'],loading='lazy',class_name='media-cover'),
                rx.el.div(rx.icon('clapperboard', size=36), rx.el.span('Capa indisponível'),class_name='media-cover cover-empty')),
        rx.el.div(rx.el.h3(m['title'],class_name='font-semibold line-clamp-2'),
            rx.el.p(m['kind']+' · '+m['year'],class_name='text-sm text-gray-400 mt-3'),class_name='p-4'),class_name='h-full')
    if search:
        return rx.el.button(content,type='button',on_click=S.open_result(m['key']),class_name='media-card text-left')
    return rx.el.a(content,href='/obra/'+m['id'],class_name='media-card')


def grid(items, render, empty):
    return rx.cond(items.length()>0,
        rx.el.div(rx.foreach(items,render),class_name='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5'),
        rx.el.p(empty,class_name='p-8 border border-dashed border-white/15 rounded-2xl text-gray-400'))


def popular_section(title, items, kind):
    return rx.cond(items.length()>0,rx.el.section(rx.el.h2(title,class_name='section-title'),
        rx.el.div(rx.foreach(items,lambda m:rx.el.button(
            rx.el.img(src=m['cover'],alt=m['title'],loading='lazy',class_name='media-cover'),
            rx.el.div(rx.el.h3(m['title'],class_name='font-semibold line-clamp-2'),rx.el.p(m['year'],class_name='text-sm text-gray-400'),class_name='p-4'),
            on_click=S.open_featured(m['source'],m['external_id'],kind),class_name='media-card text-left',type='button')),
            class_name='media-shelf')))


def discovery_page():
    return shell('Sua próxima história começa aqui.','Explore, registre e compartilhe o que faz parte do seu mundo.',
        rx.el.form(
            rx.el.div(rx.icon('search', size=24),
                rx.el.input(name='query',placeholder='Pesquisar filmes, séries, animes e livros',aria_label='Buscar título',max_length=200,value=S.search_term,on_change=S.update_search_term),
                rx.el.button('Buscar',type='submit',disabled=S.busy,class_name=BUTTON),class_name='search-box'),
            rx.el.fieldset(rx.el.legend('Categoria',class_name='sr-only'),
                *[rx.el.label(rx.el.input(type='radio',name='kind',value=value,default_checked=value=='all'),
                              rx.el.span(label),class_name='category-chip') for value,label in
                  [('all','Todos'),('movie','Filmes'),('anime','Animes'),('series','Séries'),('book','Livros')]],
                class_name='category-filters'),
            on_submit=S.search,class_name='space-y-7'),
        rx.cond((S.search_results.length()==0) & (S.featured_items.length()>0),
            rx.el.div(rx.foreach(S.featured_items,lambda m:rx.el.article(
                rx.el.img(src=m['cover'],alt='',class_name='featured-image'),
                rx.el.div(rx.el.p('EM DESTAQUE',class_name='eyebrow'),rx.el.h2(m['title'],class_name='text-2xl font-bold'),
                    rx.el.p(m['description'],class_name='line-clamp-2 text-sm text-gray-300'),
                    button('Ver detalhes',S.open_featured(m['source'],m['external_id'],'movie')),class_name='featured-content'),
                class_name='featured-card')),class_name='featured-grid')),
        rx.cond(S.search_results.length()>0,
            rx.el.section(rx.el.h2('Resultados da busca',class_name='section-title'),
                rx.el.div(rx.foreach(S.search_results,lambda m:media_card(m,True)),class_name='catalog-grid')),
            rx.cond(S.featured_items.length()==0,rx.el.section(
                rx.el.div(rx.el.p('CADA HISTÓRIA CONTA',class_name='eyebrow'),
                    rx.el.h2('Seu próximo favorito\nestá por aqui.',class_name='hero-title'),
                    rx.el.p('Descubra novas histórias, organize sua biblioteca e compartilhe o que você achou.',class_name='hero-description'),
                    rx.el.a(rx.cond(S.is_authenticated,'Minha biblioteca','Criar minha conta'),
                        href=rx.cond(S.is_authenticated,'/biblioteca','/cadastro'),class_name=BUTTON),class_name='hero-content'),
                rx.el.img(src='/mascot.png',alt='Mascote Codeboxd com uma lupa e um rolo de filme',class_name='hero-mascot'),
                class_name='discovery-hero'))),
        rx.cond(S.search_results.length()==0,rx.fragment(
            popular_section('Filmes populares',S.popular_movies,'movie'),
            popular_section('Séries populares',S.popular_series,'series'))),
        rx.cond(S.search_results.length()>0,button('Carregar mais resultados',S.more_results,disabled=S.busy)),
        rx.el.div(rx.el.h2('Na comunidade',class_name='section-title'),
                  rx.el.a('Conhecer pessoas →',href='/comunidade',class_name='text-sm brand-yellow'),class_name='flex items-center justify-between gap-4'),
        rx.cond(S.catalog_items.length()>0,
            rx.el.div(rx.foreach(S.catalog_items,lambda m:media_card(m)),class_name='catalog-grid'),
            rx.el.div(rx.icon('library',size=32),rx.el.p('Sua próxima descoberta começa com uma busca.'),
                rx.el.p('Pesquise uma obra e salve sua primeira experiência.',class_name='text-sm text-gray-400'),class_name='empty-state')))


def media_page():
    return shell('Detalhes da obra','Conheça a história e registre sua experiência.',
        rx.el.a('← Voltar à descoberta',href='/',class_name='text-sm text-gray-400'),
        rx.cond(S.selected['title']!='',rx.el.div(
            rx.el.section(
                rx.el.div(rx.el.p(S.selected['kind']+'  ·  '+S.selected['year'],class_name='eyebrow'),
                    rx.el.h2(S.selected['title'],class_name='media-detail-title'),
                    rx.el.p(rx.cond(S.selected['description']!='',S.selected['description'],'Descrição ainda não disponível.'),class_name='media-detail-description'),
                    rx.cond(S.selected['backdrop']!='',rx.el.img(src=S.selected['backdrop'],alt='Imagem de '+S.selected['title'],class_name='media-detail-poster'),
                        rx.cond(S.selected['cover']!='',rx.el.img(src=S.selected['cover'],alt='Capa de '+S.selected['title'],class_name='media-detail-poster'),
                        rx.el.div(rx.icon('clapperboard',size=48),class_name='media-detail-poster cover-empty'))),
                    class_name='media-detail-copy'),class_name='media-detail-hero'),
            rx.el.section(rx.el.h2('Ficha da obra',class_name='section-title'),
                rx.el.p(rx.cond(S.selected['details']!='',S.selected['details']+'  ·  '+S.selected['kind']+'  ·  '+S.selected['year'],
                    S.selected['kind']+'  ·  '+S.selected['year']),class_name='media-facts'),class_name='space-y-3'),
            rx.cond(S.trailers.length()>0,rx.el.section(rx.el.h2('Trailers',class_name='section-title'),
                rx.el.div(rx.foreach(S.trailers,lambda trailer:rx.el.article(
                    rx.el.h3(trailer['title'],class_name='font-semibold mb-3'),
                    rx.el.iframe(src=trailer['embed_url'],title=trailer['title'],loading='lazy',
                        allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share',
                        allow_fullscreen=True,class_name='media-trailer'),class_name='media-trailer-card')),
                    class_name='media-trailer-list')),rx.fragment()),            rx.el.div(rx.el.section(rx.el.h2('O que você achou?',class_name='section-title'),
                rx.cond(S.is_authenticated,rx.el.form(
                    rx.el.input(name='status',type='hidden',value=S.selected_status),
                    rx.el.div(rx.foreach([('planned','Quero ver / ler'),('in_progress','Em andamento'),('completed','Concluído'),('dropped','Abandonado')],
                        lambda pair:rx.el.button(pair[1],type='button',on_click=S.set_selected_status(pair[0]),
                            class_name=rx.cond(S.selected_status==pair[0],'status-chip selected','status-chip'))),class_name='media-statuses'),
                    rx.el.div(*[rx.el.button('★',type='button',aria_label='Nota '+str(value)+' de 5',
                        on_click=S.set_selected_rating(str(value)),class_name='rating-star') for value in range(1,6)],class_name='rating-stars'),
                    field('Nota (0 = sem nota)','rating',S.selected_rating,type='number',min=0,max=5,step=0.5,placeholder='0 a 5'),
                    textarea('Sua crítica detalhada','review',S.selected_review,max_length=10000,rows=5,placeholder='Conte o que achou desta obra...'),
                    check('Contém spoilers','spoiler',S.selected_spoiler),submit('Salvar avaliação'),
                    on_submit=S.save_interaction,key=S.selected['id']+S.selected_review+S.selected_rating,class_name='media-review-form'),
                    rx.el.div(rx.el.h3('Avalie esta obra',class_name='font-semibold'),
                        rx.el.p('Sua nota fica salva apenas neste navegador e não aparece no perfil nem na comunidade.',class_name='text-sm text-gray-400'),
                        rx.el.div(*[rx.el.button('★',type='button',aria_label='Nota '+str(value)+' de 5',
                            on_click=S.set_selected_rating(str(value)),class_name='rating-star') for value in range(1,6)],class_name='rating-stars'),
                        rx.cond(S.notice!='',rx.el.p(S.notice,class_name='text-sm text-amber-300')),
                        rx.el.p('Crie uma conta para publicar uma crítica, salvar na biblioteca, criar posts ou seguir pessoas.',class_name='text-sm text-gray-400'),
                        rx.el.a('Criar conta',href='/cadastro',class_name=BUTTON+' inline-block'),class_name=CARD))),
                rx.el.aside(rx.el.h2('Adicione às suas listas',class_name='section-title'),
                    rx.el.div(
                        rx.el.button('Quero ver / ler',on_click=S.quick_add('planned',0),class_name='media-list-link'),
                        rx.el.button('Já assisti / li',on_click=S.quick_add('completed',0),class_name='media-list-link'),
                        rx.el.button('Gostei',on_click=S.quick_add('completed',5),class_name='media-list-link'),
                        rx.el.button('Não gostei',on_click=S.quick_add('completed',1),class_name='media-list-link'),
                        class_name='media-list-panel'),
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
                        rx.el.img(src=m['cover'],alt=m['title'],loading='lazy',class_name='media-cover'),
                        rx.el.div(rx.el.h3(m['title'],class_name='font-semibold line-clamp-2'),rx.el.p(m['year'],class_name='text-sm text-gray-400'),class_name='p-4'),
                        on_click=S.open_recommendation(m['source'],m['external_id']),type='button',class_name='media-card text-left')),
                        class_name='media-shelf'),rx.el.p('Ainda não há recomendações desta fonte.',class_name='text-sm text-gray-400')),
                class_name='space-y-4'),class_name='space-y-8'),
            rx.el.p('Escolha uma obra pela página Descobrir.')))
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
        rx.cond(S.library.length()>0,rx.foreach(S.visible_library,interaction),rx.el.p('Sua biblioteca está vazia. Descubra uma obra e salve sua experiência.')),
        rx.cond(S.library.length()>S.visible_count,button('Mostrar mais',S.show_more)),
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
    profile_form=rx.el.form(field('Nome de usuário','username',S.profile['username'],required=True,pattern='[a-z0-9_]{3,30}',max_length=30),
        field('Nome de exibição','display_name',S.profile['display_name'],required=True,max_length=80),
        textarea('Bio','bio',S.profile['bio'],max_length=1000),field('Foto (URL HTTPS)','avatar_url',S.profile['avatar_url'],type='url'),
        submit('Salvar perfil'),on_submit=S.save_profile,key=S.profile['username'],class_name='editor-form')
    return shell('Perfil','Histórias, conexões e experiências.',
        rx.el.section(rx.el.div(class_name='profile-banner'),
            rx.el.div(avatar(S.profile['avatar_url'],S.profile['display_name']),
                rx.el.div(rx.el.h2(S.profile['display_name'],class_name='text-2xl font-bold'),
                    rx.el.p('@'+S.profile['username'],class_name='brand-yellow'),rx.el.p(S.profile['bio'],class_name='profile-bio'),class_name='profile-identity'),
                rx.cond(S.owns_profile,rx.dialog.root(
                    rx.dialog.trigger(rx.el.button('Editar perfil',class_name='quiet-button')),
                    rx.dialog.content(rx.dialog.title('Editar perfil'),rx.dialog.description('Conte um pouco sobre você.'),
                        rx.el.p(S.notice,role='status'),profile_form,
                        rx.dialog.close(rx.el.button('Fechar',class_name='quiet-button')),class_name='codeboxd-dialog')),
                    rx.cond(S.is_authenticated,button(rx.cond(S.following_ids.contains(S.profile['user_id']),'Deixar de seguir','Seguir'),S.follow(S.profile['user_id'])))),
                class_name='profile-summary'),class_name='profile-panel'),
        rx.el.div(*[rx.el.a(rx.el.strong(count),rx.el.span(label),href=href,class_name='profile-stat') for count,label,href in
            [(S.followers.length(),'Seguidores','#seguidores'),(S.following.length(),'Seguindo','#seguindo'),
             (S.profile_activity.length(),'Obras registradas','#atividades')]],class_name='profile-statistics'),
        rx.el.section(rx.el.h2('Avaliações e atividades',class_name='section-title'),
            rx.cond(S.profile_activity.length()>0,rx.foreach(S.profile_activity,interaction),rx.el.p('Nenhuma experiência registrada.',class_name='empty-state')),id='atividades',class_name='space-y-4'),
        rx.el.section(rx.el.h2('Seguidores',class_name='section-title'),grid(S.followers,person,'Ainda não há seguidores.'),id='seguidores'),
        rx.el.section(rx.el.h2('Seguindo',class_name='section-title'),grid(S.following,person,'Ainda não segue ninguém.'),id='seguindo'))


def media_select(value='0'):
    return rx.el.label('Obra',rx.el.select(rx.el.option('Sem obra associada',value='0'),
        rx.foreach(S.catalog_items,lambda m:rx.el.option(m['title'],value=m['id'])),
        name='media_id',default_value=value,class_name=INPUT))


def post(p):
    return rx.el.article(
        rx.el.div(rx.el.a(avatar(p['avatar'],p['author']),href='/perfil/'+p['user_id']),
            rx.el.div(rx.el.a(p['author'],href='/perfil/'+p['user_id'],class_name='font-semibold'),
                rx.el.p(p['published_at'],class_name='text-xs text-gray-500')),class_name='post-author'),
        rx.cond(p['media_cover']!='',rx.el.a(rx.el.img(src=p['media_cover'],alt=p['media_title'],loading='lazy',class_name='post-cover'),href='/obra/'+p['media_id'])),
        rx.cond(p['media_id']!='0',rx.el.a(p['media_title'],href='/obra/'+p['media_id'],class_name='block brand-yellow')),
        spoiler(p['body'],p['spoiler']),
        rx.el.div(rx.el.button(rx.icon('heart',size=18),rx.cond(S.liked_posts.contains(p['id']),'Descurtir','Curtir'),on_click=S.like(p['id']),class_name='quiet-button'),
            rx.el.button(rx.icon('message-circle',size=18),'Comentários',on_click=S.discussion(p['id']),class_name='quiet-button'),
            rx.cond(p['user_id']==S.user_id.to_string(),rx.fragment(rx.el.button('Editar',on_click=S.edit_post(p['id']),class_name='quiet-button'),confirm('Excluir publicação',S.remove_post(p['id'])))),
            class_name='post-actions'),class_name='post-card')


def comment(c):
    return rx.el.article(rx.el.a(c['author'],href='/perfil/'+c['user_id'],class_name='font-semibold'),rx.el.p(c['body'],class_name='whitespace-pre-wrap'),
        rx.cond(c['user_id']==S.user_id.to_string(),rx.el.div(button('Editar',S.edit_comment(c['id'])),
            confirm('Excluir comentário',S.remove_comment(c['id'])),class_name='flex gap-3')),class_name=CARD)


def feed_page():
    return shell('Entre histórias','Compartilhe descobertas e acompanhe quem você segue.',
        editor(rx.cond(S.edit_post_id!='','Editar publicação','Criar publicação'),'Compartilhe uma história com sua comunidade.',
            rx.el.form(textarea('Sua publicação','body',S.edit_post_body,required=True,max_length=5000),media_select(S.edit_post_media),
                check('Contém spoilers','spoiler',S.edit_post_spoiler),submit(rx.cond(S.edit_post_id!='','Salvar edição','Publicar')),
                on_submit=S.save_post,key=S.edit_post_id,class_name='editor-form'),open=S.post_editor_open,on_open_change=S.set_post_editor_open),
        rx.el.div(rx.el.section(
            rx.cond(S.posts.length()>0,rx.foreach(S.visible_posts,post),rx.el.div(rx.icon('messages-square',size=36),
                rx.el.p('Seu feed começa com uma boa história.'),rx.el.a('Encontrar pessoas',href='/comunidade',class_name='brand-yellow'),class_name='empty-state')),
            rx.cond(S.posts.length()>S.visible_count,button('Mostrar mais',S.show_more)),
            rx.cond(S.selected_post!='',rx.el.section(rx.el.h2('Comentários',class_name='section-title'),rx.foreach(S.comments,comment),
                rx.el.form(textarea('Comentário','body',S.edit_comment_body,required=True,max_length=2000),submit('Salvar comentário'),
                    on_submit=S.save_comment,key=S.selected_post+S.edit_comment_id,class_name=CARD),class_name='space-y-4')),
            class_name='feed-stream'),
            rx.el.aside(button('+ Criar publicação',S.new_post),rx.el.h2('Pessoas da comunidade',class_name='section-title'),
                rx.foreach(S.suggested_people,lambda p:rx.el.a(avatar(p['avatar_url'],p['display_name']),
                    rx.el.div(rx.el.strong(p['display_name']),rx.el.p('@'+p['username'])),href='/perfil/'+p['user_id'],class_name='sidebar-person')),
                rx.el.a('Explorar comunidade →',href='/comunidade',class_name='brand-yellow'),class_name='feed-sidebar'),class_name='feed-layout'))


def list_card(item):
    return rx.el.button(rx.icon('list-video',size=20),rx.el.span(item['title']),
        rx.el.span(rx.cond(item['is_public']=='True','Pública','Privada'),class_name='list-visibility'),rx.icon('chevron-right',size=18),
        on_click=S.open_list(item['id']),type='button',class_name='list-row')


def list_item(m):
    return rx.el.article(media_card(m),rx.cond(S.owns_list,confirm('Remover obra',S.remove_list_item(m['id']))),class_name='list-media-item')


def lists_page():
    return shell('Suas listas','Um lugar para cada história que você quer guardar.',
        rx.cond(S.is_authenticated,button('Criar lista',S.new_list)),
        editor(rx.cond(S.selected_list['id']=='','Criar lista','Editar lista'),'Organize suas próximas descobertas.',
            rx.el.form(field('Título','title',S.selected_list['title'],required=True,max_length=120),
                textarea('Descrição','description',S.selected_list['description'],max_length=2000),
                check('Lista pública','is_public',S.selected_list['is_public']=='True'),submit('Salvar lista'),
                on_submit=S.save_list,key=S.selected_list['id']+S.selected_list['title'],class_name='editor-form'),
            open=S.list_editor_open,on_open_change=S.set_list_editor_open),
        rx.cond(S.lists.length()>0,rx.el.div(rx.foreach(S.visible_lists,list_card),class_name='list-directory'),
            rx.el.p('Nenhuma lista disponível. Crie sua primeira coleção.',class_name='empty-state')),
        rx.cond(S.lists.length()>S.visible_count,button('Mostrar mais',S.show_more)),
        rx.cond(S.selected_list['id']!='',rx.el.section(
            rx.el.div(rx.el.div(rx.el.h2(S.selected_list['title'],class_name='section-title'),rx.el.p(S.selected_list['description'])),
                rx.cond(S.owns_list,rx.el.div(button('Editar lista',S.set_list_editor_open(True)),confirm('Excluir lista',S.remove_list),class_name='post-actions')),
                class_name='list-heading'),
            rx.cond(S.owns_list,rx.el.form(media_select(),submit('Adicionar obra'),on_submit=S.add_list_item,class_name='list-add-form')),
            rx.cond(S.list_items.length()>0,rx.el.div(rx.foreach(S.list_items,list_item),class_name='catalog-grid'),
                rx.el.p('Esta lista ainda não tem obras.',class_name='empty-state')),class_name='space-y-5')))
