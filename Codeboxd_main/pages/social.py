"""Public discovery and authenticated social pages."""
import reflex as rx
from ..state.social import SocialState as S
from .login import _logo_icon

INPUT = 'w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white'
BUTTON = 'rounded-xl bg-[#F5B300] px-5 py-3 font-semibold text-black disabled:opacity-50'
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
        rx.alert_dialog.trigger(rx.button(label, color_scheme='red', variant='soft')),
        rx.alert_dialog.content(
            rx.alert_dialog.title(label+'?'),
            rx.alert_dialog.description('Esta ação remove o conteúdo. Deseja continuar?'),
            rx.flex(rx.alert_dialog.cancel(rx.button('Cancelar', variant='soft')),
                    rx.alert_dialog.action(rx.button('Confirmar exclusão', on_click=action, color_scheme='red')),
                    gap='3', justify='end', margin_top='20px')))


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
            rx.cond(S.busy,rx.el.p('Preparando seu conteúdo…',class_name='py-12 text-gray-400'),rx.fragment(*children)),
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


def discovery_page():
    return shell('Sua próxima história começa aqui.','Explore, registre e compartilhe o que faz parte do seu mundo.',
        rx.el.form(
            rx.el.div(rx.icon('search', size=24),
                rx.el.input(name='query',placeholder='Pesquisar filmes, séries, animes e livros',aria_label='Buscar título',max_length=200,default_value=S.search_term),
                rx.el.button('Buscar',type='submit',disabled=S.busy,class_name=BUTTON),class_name='search-box'),
            rx.el.fieldset(rx.el.legend('Categoria',class_name='sr-only'),
                *[rx.el.label(rx.el.input(type='radio',name='kind',value=value,default_checked=value=='all'),
                              rx.el.span(label),class_name='category-chip') for value,label in
                  [('all','Todos'),('movie','Filmes'),('anime','Animes'),('series','Séries'),('book','Livros')]],
                class_name='category-filters'),
            on_submit=S.search,class_name='space-y-7'),
        rx.cond(S.search_results.length()>0,
            rx.el.section(rx.el.h2('Resultados da busca',class_name='section-title'),
                rx.el.div(rx.foreach(S.search_results,lambda m:media_card(m,True)),class_name='catalog-grid')),
            rx.el.section(
                rx.el.div(rx.el.p('CADA HISTÓRIA CONTA',class_name='eyebrow'),
                    rx.el.h2('Seu próximo favorito\nestá por aqui.',class_name='hero-title'),
                    rx.el.p('Descubra novas histórias, organize sua biblioteca e compartilhe o que você achou.',class_name='hero-description'),
                    rx.el.a(rx.cond(S.is_authenticated,'Minha biblioteca','Criar minha conta'),
                        href=rx.cond(S.is_authenticated,'/biblioteca','/cadastro'),class_name=BUTTON),class_name='hero-content'),
                rx.el.img(src='/mascot.png',alt='Mascote Codeboxd com uma lupa e um rolo de filme',class_name='hero-mascot'),
                class_name='discovery-hero')),
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
                rx.cond(S.selected['cover']!='',rx.el.img(src=S.selected['cover'],alt=S.selected['title']),
                    rx.el.div(rx.icon('clapperboard',size=48),class_name='media-cover cover-empty rounded-2xl')),
                rx.el.div(rx.el.p(S.selected['kind']+' · '+S.selected['year'],class_name='eyebrow'),
                    rx.el.h2(S.selected['title'],class_name='text-3xl md:text-4xl font-bold'),
                    rx.el.p(rx.cond(S.selected['description']!='',S.selected['description'],'Sinopse ainda não disponível.'),class_name='whitespace-pre-wrap text-gray-200 leading-relaxed mt-5'),
                    rx.el.p(S.selected['details'],class_name='text-sm text-gray-300 mt-5'),
                    class_name='min-w-0'),class_name='media-hero'),
            rx.el.div(rx.el.section(rx.el.h2('O que você achou?',class_name='section-title'),
                rx.cond(S.is_authenticated,rx.el.form(
                    rx.el.label('Meu status',rx.el.select(*[rx.el.option(label,value=value) for value,label in
                        [('planned','Quero ver / ler'),('in_progress','Em andamento'),('completed','Concluído'),('dropped','Abandonado')]],
                        name='status',default_value=S.selected_status,class_name=INPUT)),
                    field('Nota (0 = sem nota)','rating',S.selected_rating,type='number',min=0,max=5,step=0.5),
                    textarea('Minha avaliação','review',S.selected_review,max_length=10000,rows=5,placeholder='Conte o que achou desta história…'),
                    check('Contém spoilers','spoiler',S.selected_spoiler),submit('Salvar avaliação'),
                    on_submit=S.save_interaction,key=S.selected['id']+S.selected_review+S.selected_rating,class_name=CARD),
                    rx.el.div(rx.el.p('Entre para avaliar e organizar suas obras.'),rx.el.a('Entrar',href='/login',class_name=BUTTON+' inline-block'),class_name=CARD))),
                rx.el.aside(rx.el.h2('Suas histórias organizadas',class_name='section-title'),
                    rx.el.div(rx.el.p('Use o status da avaliação para guardar o que quer ver ou ler e registrar o que já concluiu.',class_name='text-gray-400 leading-relaxed'),
                        rx.el.a('Minha biblioteca →',href='/biblioteca',class_name='block brand-yellow'),
                        rx.el.a('Minhas listas →',href='/listas',class_name='block brand-yellow'),class_name=CARD)),
                class_name='review-layout'),class_name='space-y-6'),
                rx.el.p('Escolha uma obra pela página Descobrir.')))


def spoiler(body, flag):
    return rx.cond(flag=='True',rx.el.details(rx.el.summary('Mostrar conteúdo com spoilers',class_name='cursor-pointer text-amber-300'),
        rx.el.p(body,class_name='whitespace-pre-wrap mt-3')),rx.el.p(body,class_name='whitespace-pre-wrap'))


def interaction(i):
    return rx.el.article(rx.el.a(i['title'],href='/obra/'+i['id'],class_name='text-xl font-semibold'),
        rx.el.p(i['kind']+' · '+i['status']+' · '+i['rating']),spoiler(i['review'],i['spoiler']),class_name=CARD)


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
    return shell('Perfil','Histórias, conexões e experiências.',
        rx.el.div(rx.cond(S.profile['avatar_url']!='',rx.el.img(src=S.profile['avatar_url'],alt='Foto de perfil',class_name='w-24 h-24 rounded-full object-cover')),
            rx.el.h2(S.profile['display_name'],class_name='text-2xl font-bold'),rx.el.p('@'+S.profile['username']),
            rx.el.p(S.profile['bio']),rx.el.p(S.profile_stats,class_name='text-[#F5B300]'),class_name=CARD),
        rx.cond(S.owns_profile,rx.el.form(field('Nome de usuário','username',S.profile['username'],required=True,pattern='[a-z0-9_]{3,30}',max_length=30),
            field('Nome de exibição','display_name',S.profile['display_name'],required=True,max_length=80),
            textarea('Bio','bio',S.profile['bio'],max_length=1000),field('Foto (URL HTTPS)','avatar_url',S.profile['avatar_url'],type='url'),
            submit('Salvar perfil'),on_submit=S.save_profile,key=S.profile['username'],class_name=CARD)),
        rx.el.h2('Atividades',class_name='text-xl font-semibold'),
        rx.cond(S.profile_activity.length()>0,rx.foreach(S.profile_activity,interaction),rx.el.p('Nenhuma experiência registrada.')),
        rx.el.h2('Seguidores',class_name='text-xl font-semibold'),grid(S.followers,person,'Ainda não há seguidores.'),
        rx.el.h2('Seguindo',class_name='text-xl font-semibold'),grid(S.following,person,'Ainda não segue ninguém.'))


def media_select(value='0'):
    return rx.el.label('Obra',rx.el.select(rx.el.option('Sem obra associada',value='0'),
        rx.foreach(S.catalog_items,lambda m:rx.el.option(m['title'],value=m['id'])),
        name='media_id',default_value=value,class_name=INPUT))


def post(p):
    return rx.el.article(rx.el.a(p['author'],href='/perfil/'+p['user_id'],class_name='font-semibold'),
        rx.el.p(p['published_at'],class_name='text-xs text-gray-500'),
        rx.cond(p['media_id']!='0',rx.el.a(p['media_title'],href='/obra/'+p['media_id'],class_name='block text-[#F5B300]')),
        spoiler(p['body'],p['spoiler']),
        rx.el.div(button(rx.cond(S.liked_posts.contains(p['id']),'Descurtir','Curtir'),S.like(p['id'])),
            button('Comentários',S.discussion(p['id'])),
            rx.cond(p['user_id']==S.user_id.to_string(),rx.fragment(button('Editar',S.edit_post(p['id'])),confirm('Excluir publicação',S.remove_post(p['id'])))),
            class_name='flex flex-wrap gap-3'),class_name=CARD)


def comment(c):
    return rx.el.article(rx.el.a(c['author'],href='/perfil/'+c['user_id'],class_name='font-semibold'),rx.el.p(c['body'],class_name='whitespace-pre-wrap'),
        rx.cond(c['user_id']==S.user_id.to_string(),rx.el.div(button('Editar',S.edit_comment(c['id'])),
            confirm('Excluir comentário',S.remove_comment(c['id'])),class_name='flex gap-3')),class_name=CARD)


def feed_page():
    return shell('Entre histórias','Compartilhe descobertas e acompanhe quem você segue.',
        rx.el.form(textarea('Sua publicação','body',S.edit_post_body,required=True,max_length=5000),media_select(S.edit_post_media),
            check('Contém spoilers','spoiler',S.edit_post_spoiler),submit(rx.cond(S.edit_post_id!='','Salvar edição','Publicar')),
            rx.cond(S.edit_post_id!='',button('Cancelar edição',S.cancel_post)),on_submit=S.save_post,key=S.edit_post_id,class_name=CARD),
        rx.cond(S.posts.length()>0,rx.foreach(S.visible_posts,post),rx.el.p('Nenhuma publicação por aqui. Siga pessoas na Comunidade ou publique sua primeira descoberta.')),
        rx.cond(S.posts.length()>S.visible_count,button('Mostrar mais',S.show_more)),
        rx.cond(S.selected_post!='',rx.el.section(rx.el.h2('Comentários',class_name='text-xl font-semibold'),rx.foreach(S.comments,comment),
            rx.el.form(textarea('Comentário','body',S.edit_comment_body,required=True,max_length=2000),submit('Salvar comentário'),
                on_submit=S.save_comment,key=S.selected_post+S.edit_comment_id,class_name=CARD),class_name='space-y-4')))


def list_card(item):
    return rx.el.button(rx.el.h2(item['title'],class_name='text-xl font-semibold'),rx.el.p(item['description']),
        rx.el.p(rx.cond(item['is_public']=='True','Pública','Privada'),class_name='text-sm text-[#F5B300]'),
        on_click=S.open_list(item['id']),type='button',class_name=CARD+' text-left')


def list_item(m):
    return rx.el.article(rx.el.a(m['title'],href='/obra/'+m['id']),
        rx.cond(S.owns_list,confirm('Remover obra',S.remove_list_item(m['id']))),class_name=CARD)


def lists_page():
    return shell('Listas para cada universo','Coleções da comunidade e seleções feitas por você.',
        rx.cond(S.is_authenticated,button('Criar lista',S.new_list)),grid(S.visible_lists,list_card,'Nenhuma lista disponível.'),
        rx.cond(S.lists.length()>S.visible_count,button('Mostrar mais',S.show_more)),
        rx.cond(S.selected_list['user_id']!='',rx.el.section(
            rx.el.h2(S.selected_list['title'],class_name='text-2xl font-bold'),rx.el.p(S.selected_list['description']),
            rx.cond(S.owns_list,rx.fragment(rx.el.form(field('Título','title',S.selected_list['title'],required=True,max_length=120),
                textarea('Descrição','description',S.selected_list['description'],max_length=2000),check('Lista pública','is_public',S.selected_list['is_public']=='True'),
                submit('Salvar lista'),on_submit=S.save_list,key=S.selected_list['id']+S.selected_list['title'],class_name=CARD),
                rx.cond(S.selected_list['id']!='',rx.fragment(rx.el.form(media_select(),submit('Adicionar obra'),on_submit=S.add_list_item,class_name=CARD),
                    confirm('Excluir lista',S.remove_list))))),
            rx.cond(S.list_items.length()>0,rx.foreach(S.list_items,list_item),rx.el.p('Esta lista ainda não tem obras.')),class_name='space-y-5')))
