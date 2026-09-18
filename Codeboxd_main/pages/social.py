"""Public discovery and authenticated social pages."""
import reflex as rx
from ..state.social import SocialState as S

INPUT = 'w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white'
BUTTON = 'rounded-xl bg-[#F5B300] px-5 py-3 font-semibold text-black disabled:opacity-50'
CARD = 'rounded-2xl border border-white/10 bg-[#17191c] p-5 space-y-4'


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
            rx.el.a('codeboxd', href='/', class_name='text-2xl font-bold text-[#F5B300]'),
            rx.el.nav(*[rx.el.a(label, href=href, class_name='text-sm hover:text-[#F5B300]') for label,href in
                        [('Descobrir','/'),('Biblioteca','/biblioteca'),('Feed','/feed'),('Comunidade','/comunidade'),('Listas','/listas')]],
                      class_name='flex flex-wrap gap-5', aria_label='Navegação principal'),
            rx.cond(S.is_authenticated,
                rx.el.div(rx.el.a('Meu perfil',href='/conta'), button('Sair',S.logout_social),class_name='flex items-center gap-4'),
                rx.el.a('Entrar',href='/login',class_name=BUTTON)),
            class_name='flex flex-wrap items-center justify-between gap-6 border-b border-white/10 px-6 py-5'),
        rx.el.main(rx.el.h1(title,class_name='text-3xl md:text-4xl font-bold'),
            rx.el.p(subtitle,class_name='text-gray-400 mt-3 mb-8'),
            rx.cond(S.notice!='',rx.el.p(S.notice,role='status',class_name='rounded-xl border border-amber-400/25 bg-amber-400/10 p-4 mb-6')),
            rx.cond(S.busy,rx.el.p('Carregando…',role='status',class_name='text-amber-300')),
            rx.cond(S.busy,rx.el.p('Preparando seu conteúdo…',class_name='py-12 text-gray-400'),rx.fragment(*children)),
            class_name='max-w-6xl mx-auto px-6 py-10 space-y-6'),
        rx.el.footer('CodeBoxd · Filmes, séries, animes e livros. Uma biblioteca de experiências.',
                     class_name='max-w-6xl mx-auto px-6 py-8 text-sm text-gray-500'),
        class_name='min-h-screen bg-[#0d0f11] text-[#f3f2ed]')


def media_card(m, search=False):
    content=rx.el.div(
        rx.cond(m['cover']!='',rx.el.img(src=m['cover'],alt=m['title'],loading='lazy',class_name='w-full aspect-[2/3] object-cover rounded-xl'),
                rx.el.div('Sem capa',class_name='w-full aspect-[2/3] bg-white/5 rounded-xl flex items-center justify-center text-gray-500')),
        rx.el.p(m['kind']+' · '+m['year'],class_name='text-xs uppercase tracking-wide text-[#F5B300] mt-4'),
        rx.el.h2(m['title'],class_name='font-semibold mt-2'),class_name='h-full')
    if search:
        return rx.el.button(content,type='button',on_click=S.open_result(m['key']),class_name=CARD+' text-left hover:border-amber-400/50')
    return rx.el.a(content,href='/obra/'+m['id'],class_name=CARD+' hover:border-amber-400/50')


def grid(items, render, empty):
    return rx.cond(items.length()>0,
        rx.el.div(rx.foreach(items,render),class_name='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5'),
        rx.el.p(empty,class_name='p-8 border border-dashed border-white/15 rounded-2xl text-gray-400'))


def discovery_page():
    return shell('Sua próxima história começa aqui.','Explore, registre e compartilhe o que faz parte do seu mundo.',
        rx.el.form(rx.el.input(name='query',placeholder='Busque um título…',aria_label='Buscar título',max_length=200,class_name=INPUT),
            rx.el.select(*[rx.el.option(label,value=value) for value,label in
                         [('all','Todas as categorias'),('movie','Filmes'),('series','Séries'),('anime','Animes'),('book','Livros')]],
                         name='kind',aria_label='Categoria',class_name=INPUT),
            rx.el.button('Buscar',type='submit',disabled=S.busy,class_name=BUTTON),
            on_submit=S.search,class_name='grid md:grid-cols-[1fr_220px_auto] gap-3'),
        grid(S.search_results,lambda m:media_card(m,True),'Busque por um título para descobrir novas obras.'),
        rx.cond(S.search_results.length()>0,button('Carregar mais resultados',S.more_results,disabled=S.busy)),
        rx.el.h2('Na comunidade',class_name='text-xl font-semibold'),
        grid(S.catalog_items,lambda m:media_card(m),'As obras registradas pela comunidade aparecerão aqui.'))


def media_page():
    return shell('Detalhes da obra','Conheça a história e registre sua experiência.',
        rx.cond(S.selected['title']!='',rx.el.div(
            rx.el.div(rx.cond(S.selected['cover']!='',rx.el.img(src=S.selected['cover'],alt=S.selected['title'],class_name='w-full max-w-xs rounded-2xl'))),
            rx.el.div(rx.el.p(S.selected['kind']+' · '+S.selected['year'],class_name='text-[#F5B300]'),
                rx.el.h2(S.selected['title'],class_name='text-3xl font-bold'),rx.el.p(S.selected['description'],class_name='whitespace-pre-wrap text-gray-300'),
                rx.el.p(S.selected['details'],class_name='text-sm text-gray-400'),
                rx.el.p('Fonte: '+S.selected['source']+' · ID: '+S.selected['external_id'],class_name='text-xs text-gray-500'),
                rx.cond(S.is_authenticated,rx.el.form(
                    rx.el.label('Meu status',rx.el.select(*[rx.el.option(label,value=value) for value,label in
                        [('planned','Quero ver / ler'),('in_progress','Em andamento'),('completed','Concluído'),('dropped','Abandonado')]],
                        name='status',default_value=S.selected_status,class_name=INPUT)),
                    field('Nota (0 = sem nota)','rating',S.selected_rating,type='number',min=0,max=5,step=0.5),
                    textarea('Minha review','review',S.selected_review,max_length=10000),
                    check('Contém spoilers','spoiler',S.selected_spoiler),submit('Salvar experiência'),
                    on_submit=S.save_interaction,key=S.selected['id']+S.selected_review+S.selected_rating,class_name=CARD),
                    rx.el.a('Entre para avaliar e organizar suas obras',href='/login',class_name='text-[#F5B300]')),
                class_name='space-y-5'),class_name='grid md:grid-cols-[240px_1fr] gap-8'),
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
