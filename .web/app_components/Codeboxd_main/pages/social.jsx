
import {ReflexEvent,applyEventActions,getBackendURL,getRefValue,getRefValues,isNotNullOrUndefined,isTrue,pyAnd,pyOr,refs} from "$/utils/state"
import {Link as ReactRouterLink} from "react-router"
import {StateContexts,UploadFilesContext,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect,useRef} from "react"
import {jsx} from "@emotion/react"
import {} from "react-dropzone"
import {useDropzone} from "react-dropzone"
import LucideImageUp from "lucide-react/dist/esm/icons/image-up.mjs"
import LucideBookOpen from "lucide-react/dist/esm/icons/book-open.mjs"
import LucideClapperboard from "lucide-react/dist/esm/icons/clapperboard.mjs"
import LucideUserRound from "lucide-react/dist/esm/icons/user-round.mjs"
import LucideHeart from "lucide-react/dist/esm/icons/heart.mjs"
import LucideMessageCircle from "lucide-react/dist/esm/icons/message-circle.mjs"
import LucideListVideo from "lucide-react/dist/esm/icons/list-video.mjs"
import LucideChevronRight from "lucide-react/dist/esm/icons/chevron-right.mjs"
import env from "$/env.json"
import {AlertDialog as RadixThemesAlertDialog,Button as RadixThemesButton,Dialog as RadixThemesDialog,Flex as RadixThemesFlex} from "@radix-ui/themes"








export const Reactrouterlink_link_32e708c2740e9a227cc42f586e2893f0_3e8caf1e = memo(({children}) => {
    const reflex___state____state = useContext(StateContexts.reflex___state____state)



    return(
        jsx(ReactRouterLink,{className:((reflex___state____state.router_rx_state_?.["url"]?.["path"]?.valueOf?.() === "/"?.valueOf?.()) ? "nav-link active" : "nav-link"),to:"/"},children)
    )
});
Reactrouterlink_link_32e708c2740e9a227cc42f586e2893f0_3e8caf1e.displayName = "ReactRouterLink";

export const Reactrouterlink_link_17a812742929f73506d36d8a3494c25b_3e8caf1e = memo(({children}) => {
    const reflex___state____state = useContext(StateContexts.reflex___state____state)



    return(
        jsx(ReactRouterLink,{className:((reflex___state____state.router_rx_state_?.["url"]?.["path"]?.valueOf?.() === "/feed"?.valueOf?.()) ? "nav-link active" : "nav-link"),to:"/feed"},children)
    )
});
Reactrouterlink_link_17a812742929f73506d36d8a3494c25b_3e8caf1e.displayName = "ReactRouterLink";

export const Reactrouterlink_link_bcf68a862811847fcff36da128483dc0_3e8caf1e = memo(({children}) => {
    const reflex___state____state = useContext(StateContexts.reflex___state____state)



    return(
        jsx(ReactRouterLink,{className:((reflex___state____state.router_rx_state_?.["url"]?.["path"]?.valueOf?.() === "/listas"?.valueOf?.()) ? "nav-link active" : "nav-link"),to:"/listas"},children)
    )
});
Reactrouterlink_link_bcf68a862811847fcff36da128483dc0_3e8caf1e.displayName = "ReactRouterLink";

export const Reactrouterlink_link_fa41ef291ebfce671cd99241838e40b6_3e8caf1e = memo(({children}) => {
    const reflex___state____state = useContext(StateContexts.reflex___state____state)



    return(
        jsx(ReactRouterLink,{className:((reflex___state____state.router_rx_state_?.["url"]?.["path"]?.valueOf?.() === "/conta"?.valueOf?.()) ? "nav-link active" : "nav-link"),to:"/conta"},children)
    )
});
Reactrouterlink_link_fa41ef291ebfce671cd99241838e40b6_3e8caf1e.displayName = "ReactRouterLink";

export const Button_button_2da6545e7c295f612e685f778be402af_3e8caf1e = memo(({children}) => {
    const on_click_c6cae790485c63f5e2efc828e431c884 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.logout_social", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"action-button",onClick:on_click_c6cae790485c63f5e2efc828e431c884,type:"button"},children)
    )
});
Button_button_2da6545e7c295f612e685f778be402af_3e8caf1e.displayName = "Button";

export const Cond_comp_815323f75e4bb980b73321564381d1c5_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_authenticated_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_815323f75e4bb980b73321564381d1c5_3e8caf1e.displayName = "Cond";

export const Bare_comp_407dc2fcd8eac0fae070a7ae691a16a2_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.notice_rx_state_
    )
});
Bare_comp_407dc2fcd8eac0fae070a7ae691a16a2_3e8caf1e.displayName = "Bare";

export const Cond_comp_aabd254f41ab0c389ddd6ae341ee343e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.notice_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_aabd254f41ab0c389ddd6ae341ee343e_3e8caf1e.displayName = "Cond";

export const Cond_comp_75319a6900675157a81618c158bb669e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_75319a6900675157a81618c158bb669e_3e8caf1e.displayName = "Cond";

export const Input_input_af190dd64b56ad4528a0ebc25702564b_3e8caf1e = memo(({children}) => {
    const on_change_a2ed309d1251c6194d599a3466ab7958 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.update_search_term", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{"aria-label":"Buscar t\u00edtulo",maxLength:200,name:"query",onChange:on_change_a2ed309d1251c6194d599a3466ab7958,placeholder:"Pesquisar filmes, s\u00e9ries, animes e livros",value:(isNotNullOrUndefined(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_term_rx_state_) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_term_rx_state_ : "")},)
    )
});
Input_input_af190dd64b56ad4528a0ebc25702564b_3e8caf1e.displayName = "Input";

export const Button_button_590fed6d8f4fa39046477b5908040d57_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{className:"action-button",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_,type:"submit"},children)
    )
});
Button_button_590fed6d8f4fa39046477b5908040d57_3e8caf1e.displayName = "Button";

export const Form_form_b850e5f3b981f114831930b310e3ba27_3e8caf1e = memo(({children}) => {
    

    const handleSubmit_6fb44539deacea9637fbea9007233dde = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.search", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"space-y-7",onSubmit:handleSubmit_6fb44539deacea9637fbea9007233dde},children)
    )
});
Form_form_b850e5f3b981f114831930b310e3ba27_3e8caf1e.displayName = "Form";

export const Button_button_520a25cf8db2daa7f2a3f4ce903f765f_3e8caf1e = memo(({children}) => {
    const on_click_2f6e1f9036ef4d95db9d621bf857af64 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.browse_category", ({ ["kind"] : "all" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{"aria-pressed":pyAnd(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_, () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.submitted_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))), () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_type_rx_state_?.valueOf?.() === "all"?.valueOf?.()))),className:"browse-category",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_,onClick:on_click_2f6e1f9036ef4d95db9d621bf857af64,type:"button"},children)
    )
});
Button_button_520a25cf8db2daa7f2a3f4ce903f765f_3e8caf1e.displayName = "Button";

export const Button_button_50a0cac83e5aa508201879e0b5280a2b_3e8caf1e = memo(({children}) => {
    const on_click_ef57eec1710b663637da459f3b0d6098 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.browse_category", ({ ["kind"] : "movie" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{"aria-pressed":pyAnd(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_, () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.submitted_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))), () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_type_rx_state_?.valueOf?.() === "movie"?.valueOf?.()))),className:"browse-category",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_,onClick:on_click_ef57eec1710b663637da459f3b0d6098,type:"button"},children)
    )
});
Button_button_50a0cac83e5aa508201879e0b5280a2b_3e8caf1e.displayName = "Button";

export const Button_button_0f65532692211b8f2e5ffce1a427b6c6_3e8caf1e = memo(({children}) => {
    const on_click_398295c1d2dc80022950f902a097a926 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.browse_category", ({ ["kind"] : "anime" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{"aria-pressed":pyAnd(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_, () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.submitted_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))), () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_type_rx_state_?.valueOf?.() === "anime"?.valueOf?.()))),className:"browse-category",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_,onClick:on_click_398295c1d2dc80022950f902a097a926,type:"button"},children)
    )
});
Button_button_0f65532692211b8f2e5ffce1a427b6c6_3e8caf1e.displayName = "Button";

export const Button_button_bdafac68590a50a867812b62dbe21f42_3e8caf1e = memo(({children}) => {
    const on_click_bb42b91543cd50f9ad779efc1e7c1843 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.browse_category", ({ ["kind"] : "series" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{"aria-pressed":pyAnd(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_, () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.submitted_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))), () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_type_rx_state_?.valueOf?.() === "series"?.valueOf?.()))),className:"browse-category",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_,onClick:on_click_bb42b91543cd50f9ad779efc1e7c1843,type:"button"},children)
    )
});
Button_button_bdafac68590a50a867812b62dbe21f42_3e8caf1e.displayName = "Button";

export const Button_button_39bead7fdf09e9431f49406dba28997b_3e8caf1e = memo(({children}) => {
    const on_click_4f598c473ba49203dcea18abed18d94b = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.browse_category", ({ ["kind"] : "book" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{"aria-pressed":pyAnd(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_, () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.submitted_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))), () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_type_rx_state_?.valueOf?.() === "book"?.valueOf?.()))),className:"browse-category",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_,onClick:on_click_4f598c473ba49203dcea18abed18d94b,type:"button"},children)
    )
});
Button_button_39bead7fdf09e9431f49406dba28997b_3e8caf1e.displayName = "Button";

export const Button_button_8d13aab184464f6f93bedd5471c817f6_3e8caf1e = memo(({children}) => {
    const on_click_c5f9406221b6c4029113e9b358927357 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.show_home_catalog", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"quiet-button",onClick:on_click_c5f9406221b6c4029113e9b358927357,type:"button"},children)
    )
});
Button_button_8d13aab184464f6f93bedd5471c817f6_3e8caf1e.displayName = "Button";

export const Cond_comp_7fe36fec14edd6c24901313b75a7d5ce_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_7fe36fec14edd6c24901313b75a7d5ce_3e8caf1e.displayName = "Cond";

export const Foreach_comp_bdf2bb1dc67d22ba9c7f9cd1132b4e2a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.featured_items_rx_state_.slice(undefined, 1) ?? [],((m_rx_state_,index_2916023fdf20ae65a7d934e9163d918b)=>(jsx("article",{className:"home-spotlight",key:index_2916023fdf20ae65a7d934e9163d918b},jsx(Fragment,{},(pyOr(pyAnd(!((m_rx_state_?.["backdrop"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["backdrop"])))), () => (pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))))?(jsx(Fragment,{},jsx("img",{alt:"",className:"spotlight-image",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : (pyAnd(!((m_rx_state_?.["backdrop"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["backdrop"])))) ? m_rx_state_?.["backdrop"] : m_rx_state_?.["cover"]) }), ({  })))], args, ({  })))),src:(pyAnd(!((m_rx_state_?.["backdrop"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["backdrop"])))) ? m_rx_state_?.["backdrop"] : m_rx_state_?.["cover"])},))):(jsx(Fragment,{},)))),jsx("div",{className:"spotlight-copy"},jsx("p",{className:"eyebrow"},"HOJE NO SEU RADAR"),jsx("p",{className:"spotlight-kicker"},"Uma pausa. Uma grande hist\u00f3ria."),jsx("h2",{className:"spotlight-title"},m_rx_state_?.["title"]),jsx("p",{className:"spotlight-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])),jsx("p",{className:"spotlight-description"},m_rx_state_?.["description"]),jsx("div",{className:"spotlight-actions"},jsx("button",{className:"action-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "movie" }), ({  })))], [_e], ({  })))),type:"button"},"Conhecer este filme"),jsx(ReactRouterLink,{className:"spotlight-secondary",to:"#home-filmes"},"Explorar cat\u00e1logo")))))))
    )
});
Foreach_comp_bdf2bb1dc67d22ba9c7f9cd1132b4e2a_3e8caf1e.displayName = "Foreach";

export const Cond_comp_798cb3c023fc07196adc1fe8dcb66f34_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (pyAnd(!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_), () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.featured_items_rx_state_.length > 0)))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_798cb3c023fc07196adc1fe8dcb66f34_3e8caf1e.displayName = "Cond";

export const Bare_comp_be91ff8435405c24d985a0357043f1f6_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.submitted_query_rx_state_?.valueOf?.() === ""?.valueOf?.())) ? "Resultados da busca" : "Explorar cat\u00e1logo")
    )
});
Bare_comp_be91ff8435405c24d985a0357043f1f6_3e8caf1e.displayName = "Bare";

export const Foreach_comp_f63399fee8d592d42f1effad0ec6d857_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_results_rx_state_ ?? [],((m_rx_state_,index_d6e58b3860b8357b8bd97cda1f35fdd9)=>(jsx("button",{className:"media-card text-left",key:index_d6e58b3860b8357b8bd97cda1f35fdd9,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_result", ({ ["key"] : m_rx_state_?.["key"] }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"h-full"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},))))),jsx("div",{className:"p-4"},jsx("h3",{className:"font-semibold line-clamp-2"},m_rx_state_?.["title"]),jsx("p",{className:"text-sm text-gray-400 mt-3"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"]))))))))
    )
});
Foreach_comp_f63399fee8d592d42f1effad0ec6d857_3e8caf1e.displayName = "Foreach";

export const Bare_comp_711d1e6e040c1f6d8509928446da6fe1_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_authenticated_rx_state_ ? "Minha biblioteca" : "Criar minha conta")
    )
});
Bare_comp_711d1e6e040c1f6d8509928446da6fe1_3e8caf1e.displayName = "Bare";

export const Reactrouterlink_link_163778b05ce3df8c26fe624559fe37cd_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx(ReactRouterLink,{className:"action-button",to:(reflex___state____state__codeboxd_main___state___session____session_state.is_authenticated_rx_state_ ? "/biblioteca" : "/cadastro")},children)
    )
});
Reactrouterlink_link_163778b05ce3df8c26fe624559fe37cd_3e8caf1e.displayName = "ReactRouterLink";

export const Cond_comp_ed523783f784af688cc4295f880ecbb4_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.featured_items_rx_state_.length?.valueOf?.() === 0?.valueOf?.())?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_ed523783f784af688cc4295f880ecbb4_3e8caf1e.displayName = "Cond";

export const Button_button_013958e01ea488fcc197019f0124454f_3e8caf1e = memo(({children}) => {
    const on_click_a559090071c1fdc327308c7d3134b72a = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('popular-movie');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"popular-movie","aria-label":"Anteriores: Filmes populares",className:"shelf-arrow",onClick:on_click_a559090071c1fdc327308c7d3134b72a,type:"button"},children)
    )
});
Button_button_013958e01ea488fcc197019f0124454f_3e8caf1e.displayName = "Button";

export const Button_button_831e81121427749b7eaa62ce426d040b_3e8caf1e = memo(({children}) => {
    const on_click_dcd3640d6a6d2b1ff2e000df9d80da05 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('popular-movie');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"popular-movie","aria-label":"Pr\u00f3ximos: Filmes populares",className:"shelf-arrow",onClick:on_click_dcd3640d6a6d2b1ff2e000df9d80da05,type:"button"},children)
    )
});
Button_button_831e81121427749b7eaa62ce426d040b_3e8caf1e.displayName = "Button";

export const Foreach_comp_347233595fc3070577b0628e3f2f2ead_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.popular_movies_rx_state_ ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "movie" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_347233595fc3070577b0628e3f2f2ead_3e8caf1e.displayName = "Foreach";

export const Button_button_d343b3f670dacad1999860070060cf9b_3e8caf1e = memo(({children}) => {
    const on_click_8e9f6ed1382956e8666e2258cadf7a6d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.more_popular", ({ ["kind"] : "movie" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{className:"shelf-more",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_,onClick:on_click_8e9f6ed1382956e8666e2258cadf7a6d,type:"button"},children)
    )
});
Button_button_d343b3f670dacad1999860070060cf9b_3e8caf1e.displayName = "Button";

export const Cond_comp_ec2cd304c6d56463488aecc94f38526d_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.popular_exhausted_rx_state_.includes("movie"))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_ec2cd304c6d56463488aecc94f38526d_3e8caf1e.displayName = "Cond";

export const Cond_comp_99c24b8c1d9e7d02b06be6ffd5941dcb_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.popular_movies_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_99c24b8c1d9e7d02b06be6ffd5941dcb_3e8caf1e.displayName = "Cond";

export const Button_button_7cf0ca5a794b009a22bf77be2ec82257_3e8caf1e = memo(({children}) => {
    const on_click_1259c6d579c25b0c36a74ffae3d307e5 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('movies_now');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"movies_now","aria-label":"Anteriores: Agora nos cinemas",className:"shelf-arrow",onClick:on_click_1259c6d579c25b0c36a74ffae3d307e5,type:"button"},children)
    )
});
Button_button_7cf0ca5a794b009a22bf77be2ec82257_3e8caf1e.displayName = "Button";

export const Button_button_558edb7b54839c54b53927b4f598bb40_3e8caf1e = memo(({children}) => {
    const on_click_1bec5fc4f9c9aca8e73ba9dab451674a = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('movies_now');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"movies_now","aria-label":"Pr\u00f3ximos: Agora nos cinemas",className:"shelf-arrow",onClick:on_click_1bec5fc4f9c9aca8e73ba9dab451674a,type:"button"},children)
    )
});
Button_button_558edb7b54839c54b53927b4f598bb40_3e8caf1e.displayName = "Button";

export const Foreach_comp_77f2ecb997489fd3eea4d77e3b78ceb2_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["movies_now"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "movie" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_77f2ecb997489fd3eea4d77e3b78ceb2_3e8caf1e.displayName = "Foreach";

export const Bare_comp_05983f84a87df7eb3a8e976c354794d9_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("movies_now") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_05983f84a87df7eb3a8e976c354794d9_3e8caf1e.displayName = "Bare";

export const Button_button_ec9b414d3e0b104eec68f3311a7541fa_3e8caf1e = memo(({children}) => {
    const on_click_77846084c957a81ab548234460010c62 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.retry_home_collections", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{className:"quiet-button",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_,onClick:on_click_77846084c957a81ab548234460010c62,type:"button"},children)
    )
});
Button_button_ec9b414d3e0b104eec68f3311a7541fa_3e8caf1e.displayName = "Button";

export const Cond_comp_afa74e80ed6051d573be36d0a40a7fa3_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_loaded_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_afa74e80ed6051d573be36d0a40a7fa3_3e8caf1e.displayName = "Cond";

export const Cond_comp_88914ddf65bab9bd713180766046b5dc_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["movies_now"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_88914ddf65bab9bd713180766046b5dc_3e8caf1e.displayName = "Cond";

export const Button_button_9335fa1f8da66e18f50dc3153fcc2b87_3e8caf1e = memo(({children}) => {
    const on_click_21cfbe510b7859bb5ed11e937d9fa17e = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('movies_rated');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"movies_rated","aria-label":"Anteriores: Filmes muito bem avaliados",className:"shelf-arrow",onClick:on_click_21cfbe510b7859bb5ed11e937d9fa17e,type:"button"},children)
    )
});
Button_button_9335fa1f8da66e18f50dc3153fcc2b87_3e8caf1e.displayName = "Button";

export const Button_button_82f068b39a26e96d0ac00f4b39faf0b7_3e8caf1e = memo(({children}) => {
    const on_click_8e49fb89d5dc451a2a181242237accb3 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('movies_rated');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"movies_rated","aria-label":"Pr\u00f3ximos: Filmes muito bem avaliados",className:"shelf-arrow",onClick:on_click_8e49fb89d5dc451a2a181242237accb3,type:"button"},children)
    )
});
Button_button_82f068b39a26e96d0ac00f4b39faf0b7_3e8caf1e.displayName = "Button";

export const Foreach_comp_45270bfcb335f2f64f23d63b6a89e46c_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["movies_rated"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "movie" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_45270bfcb335f2f64f23d63b6a89e46c_3e8caf1e.displayName = "Foreach";

export const Bare_comp_54490488eaf72ef11b5afd8ac8713a10_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("movies_rated") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_54490488eaf72ef11b5afd8ac8713a10_3e8caf1e.displayName = "Bare";

export const Cond_comp_1e4d571e3debac1e90e3063546d3f364_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["movies_rated"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_1e4d571e3debac1e90e3063546d3f364_3e8caf1e.displayName = "Cond";

export const Button_button_e42a6f7c3b20641ccfb94280d419826e_3e8caf1e = memo(({children}) => {
    const on_click_2bc927baeec1fe6e32bf281710c48fa7 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('movies_upcoming');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"movies_upcoming","aria-label":"Anteriores: No radar: pr\u00f3ximos filmes",className:"shelf-arrow",onClick:on_click_2bc927baeec1fe6e32bf281710c48fa7,type:"button"},children)
    )
});
Button_button_e42a6f7c3b20641ccfb94280d419826e_3e8caf1e.displayName = "Button";

export const Button_button_48e70c9e87f9ce0ccf5770840e708ab7_3e8caf1e = memo(({children}) => {
    const on_click_3d52607bb62a04cf24553729e35df1be = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('movies_upcoming');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"movies_upcoming","aria-label":"Pr\u00f3ximos: No radar: pr\u00f3ximos filmes",className:"shelf-arrow",onClick:on_click_3d52607bb62a04cf24553729e35df1be,type:"button"},children)
    )
});
Button_button_48e70c9e87f9ce0ccf5770840e708ab7_3e8caf1e.displayName = "Button";

export const Foreach_comp_b0dfe52837907a26c6322570be65e38b_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["movies_upcoming"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "movie" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_b0dfe52837907a26c6322570be65e38b_3e8caf1e.displayName = "Foreach";

export const Bare_comp_34a1733e579b177fd27379e11662e844_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("movies_upcoming") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_34a1733e579b177fd27379e11662e844_3e8caf1e.displayName = "Bare";

export const Cond_comp_a8052c845bea6c3ce56b348e7c713aa6_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["movies_upcoming"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_a8052c845bea6c3ce56b348e7c713aa6_3e8caf1e.displayName = "Cond";

export const Button_button_47a7eb1f8c6845b61c2dab2f29351674_3e8caf1e = memo(({children}) => {
    const on_click_8e89d67d2fb919cabbdadca5cb3e5659 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('popular-series');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"popular-series","aria-label":"Anteriores: S\u00e9ries populares",className:"shelf-arrow",onClick:on_click_8e89d67d2fb919cabbdadca5cb3e5659,type:"button"},children)
    )
});
Button_button_47a7eb1f8c6845b61c2dab2f29351674_3e8caf1e.displayName = "Button";

export const Button_button_70ad035dde5b3d90e382794feb079a93_3e8caf1e = memo(({children}) => {
    const on_click_4cd9287f1a9036d6196e750f4198174f = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('popular-series');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"popular-series","aria-label":"Pr\u00f3ximos: S\u00e9ries populares",className:"shelf-arrow",onClick:on_click_4cd9287f1a9036d6196e750f4198174f,type:"button"},children)
    )
});
Button_button_70ad035dde5b3d90e382794feb079a93_3e8caf1e.displayName = "Button";

export const Foreach_comp_058962c68e1303690bb31988a64eb08a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.popular_series_rx_state_ ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "series" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_058962c68e1303690bb31988a64eb08a_3e8caf1e.displayName = "Foreach";

export const Button_button_67b15ca603fdebbad835bf483332bad6_3e8caf1e = memo(({children}) => {
    const on_click_4d89b3c41e66816c6e92dcc4eae84781 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.more_popular", ({ ["kind"] : "series" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{className:"shelf-more",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_,onClick:on_click_4d89b3c41e66816c6e92dcc4eae84781,type:"button"},children)
    )
});
Button_button_67b15ca603fdebbad835bf483332bad6_3e8caf1e.displayName = "Button";

export const Cond_comp_1680afeca99a2d908fe91b279dc7c3d5_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.popular_exhausted_rx_state_.includes("series"))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_1680afeca99a2d908fe91b279dc7c3d5_3e8caf1e.displayName = "Cond";

export const Cond_comp_750b315a1bac5631f371f1b39e5a1f60_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.popular_series_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_750b315a1bac5631f371f1b39e5a1f60_3e8caf1e.displayName = "Cond";

export const Button_button_8d2f4c6f3ee76775a160cd02ab58f35f_3e8caf1e = memo(({children}) => {
    const on_click_5c59fb70583a519d0c56d7779aeba7f7 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('series_rated');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"series_rated","aria-label":"Anteriores: S\u00e9ries muito bem avaliadas",className:"shelf-arrow",onClick:on_click_5c59fb70583a519d0c56d7779aeba7f7,type:"button"},children)
    )
});
Button_button_8d2f4c6f3ee76775a160cd02ab58f35f_3e8caf1e.displayName = "Button";

export const Button_button_ff8d4613cbe6c864319e88e801e5c1ab_3e8caf1e = memo(({children}) => {
    const on_click_c7054c8a82d6529ce02ef5a794a47d1c = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('series_rated');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"series_rated","aria-label":"Pr\u00f3ximos: S\u00e9ries muito bem avaliadas",className:"shelf-arrow",onClick:on_click_c7054c8a82d6529ce02ef5a794a47d1c,type:"button"},children)
    )
});
Button_button_ff8d4613cbe6c864319e88e801e5c1ab_3e8caf1e.displayName = "Button";

export const Foreach_comp_7ba3dfb0237393e85400b6f8e775c20f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["series_rated"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "series" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_7ba3dfb0237393e85400b6f8e775c20f_3e8caf1e.displayName = "Foreach";

export const Bare_comp_784907f3b0f09d5e7b7ae71c6f75232a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("series_rated") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_784907f3b0f09d5e7b7ae71c6f75232a_3e8caf1e.displayName = "Bare";

export const Cond_comp_79368ca9a7d76cbfb0edc12324c88d7e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["series_rated"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_79368ca9a7d76cbfb0edc12324c88d7e_3e8caf1e.displayName = "Cond";

export const Button_button_ce45acd98be122cf5561566d3db3d8ff_3e8caf1e = memo(({children}) => {
    const on_click_0ec79e19b5130cfa25953ca825bbdb1f = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_popular');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"books_popular","aria-label":"Anteriores: Livros conhecidos e populares",className:"shelf-arrow",onClick:on_click_0ec79e19b5130cfa25953ca825bbdb1f,type:"button"},children)
    )
});
Button_button_ce45acd98be122cf5561566d3db3d8ff_3e8caf1e.displayName = "Button";

export const Button_button_11d2b09790357f233c6c5d7fb8c97977_3e8caf1e = memo(({children}) => {
    const on_click_56794afdaec6466c99b07b2d74f491e9 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_popular');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"books_popular","aria-label":"Pr\u00f3ximos: Livros conhecidos e populares",className:"shelf-arrow",onClick:on_click_56794afdaec6466c99b07b2d74f491e9,type:"button"},children)
    )
});
Button_button_11d2b09790357f233c6c5d7fb8c97977_3e8caf1e.displayName = "Button";

export const Foreach_comp_62ce7320e143b496cb1766c010503a76_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_popular"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "book" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_62ce7320e143b496cb1766c010503a76_3e8caf1e.displayName = "Foreach";

export const Bare_comp_917ef9da3b4b4aed19d9d27cb350885e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("books_popular") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_917ef9da3b4b4aed19d9d27cb350885e_3e8caf1e.displayName = "Bare";

export const Cond_comp_55824746a6e127e1a49f7cbf2d12d8cc_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_popular"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_55824746a6e127e1a49f7cbf2d12d8cc_3e8caf1e.displayName = "Cond";

export const Button_button_7ea784b98e9b931350d22403c10051b2_3e8caf1e = memo(({children}) => {
    const on_click_8c5d619e65a1b008e029972b3ca028e1 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_fiction');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"books_fiction","aria-label":"Anteriores: Sua pr\u00f3xima leitura",className:"shelf-arrow",onClick:on_click_8c5d619e65a1b008e029972b3ca028e1,type:"button"},children)
    )
});
Button_button_7ea784b98e9b931350d22403c10051b2_3e8caf1e.displayName = "Button";

export const Button_button_cad3edeffcffeb78fe01dc9597f94995_3e8caf1e = memo(({children}) => {
    const on_click_11be31653bdeef507e9e1815f113624d = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_fiction');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"books_fiction","aria-label":"Pr\u00f3ximos: Sua pr\u00f3xima leitura",className:"shelf-arrow",onClick:on_click_11be31653bdeef507e9e1815f113624d,type:"button"},children)
    )
});
Button_button_cad3edeffcffeb78fe01dc9597f94995_3e8caf1e.displayName = "Button";

export const Foreach_comp_44b039da9b89c101de0f3453f9c7d8a8_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_fiction"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "book" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_44b039da9b89c101de0f3453f9c7d8a8_3e8caf1e.displayName = "Foreach";

export const Bare_comp_7eef2b1de053dbb84f9ac1343580ef03_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("books_fiction") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_7eef2b1de053dbb84f9ac1343580ef03_3e8caf1e.displayName = "Bare";

export const Cond_comp_036a7a064427cf92c4519280d4db0d5a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_fiction"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_036a7a064427cf92c4519280d4db0d5a_3e8caf1e.displayName = "Cond";

export const Button_button_5e0688668b97827f597adc9e13f60c1a_3e8caf1e = memo(({children}) => {
    const on_click_bef57cea62557b7ac19827f1e600cdad = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_fantasy');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"books_fantasy","aria-label":"Anteriores: Livros de fantasia",className:"shelf-arrow",onClick:on_click_bef57cea62557b7ac19827f1e600cdad,type:"button"},children)
    )
});
Button_button_5e0688668b97827f597adc9e13f60c1a_3e8caf1e.displayName = "Button";

export const Button_button_ee8af6fe685fb643b746a6155c07bf84_3e8caf1e = memo(({children}) => {
    const on_click_1c75a86c60be5a2bc278cea89a7553c6 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_fantasy');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"books_fantasy","aria-label":"Pr\u00f3ximos: Livros de fantasia",className:"shelf-arrow",onClick:on_click_1c75a86c60be5a2bc278cea89a7553c6,type:"button"},children)
    )
});
Button_button_ee8af6fe685fb643b746a6155c07bf84_3e8caf1e.displayName = "Button";

export const Foreach_comp_20ef60c587df00c0de5421c83ab0fb2a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_fantasy"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "book" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_20ef60c587df00c0de5421c83ab0fb2a_3e8caf1e.displayName = "Foreach";

export const Bare_comp_ae4b577bc0fb22874931dd18d077b222_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("books_fantasy") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_ae4b577bc0fb22874931dd18d077b222_3e8caf1e.displayName = "Bare";

export const Cond_comp_0dd2754a01161ea3e1f139dc5af1e242_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_fantasy"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_0dd2754a01161ea3e1f139dc5af1e242_3e8caf1e.displayName = "Cond";

export const Button_button_1e0abe30128e208f6e2d874920215315_3e8caf1e = memo(({children}) => {
    const on_click_b637042974079ee8be994c277e2d8172 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_mystery');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"books_mystery","aria-label":"Anteriores: Mist\u00e9rios entre p\u00e1ginas",className:"shelf-arrow",onClick:on_click_b637042974079ee8be994c277e2d8172,type:"button"},children)
    )
});
Button_button_1e0abe30128e208f6e2d874920215315_3e8caf1e.displayName = "Button";

export const Button_button_cb1394e24d1334c3b7d451f459702622_3e8caf1e = memo(({children}) => {
    const on_click_7c3055fad0d8401201eec2989bc9e31e = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_mystery');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"books_mystery","aria-label":"Pr\u00f3ximos: Mist\u00e9rios entre p\u00e1ginas",className:"shelf-arrow",onClick:on_click_7c3055fad0d8401201eec2989bc9e31e,type:"button"},children)
    )
});
Button_button_cb1394e24d1334c3b7d451f459702622_3e8caf1e.displayName = "Button";

export const Foreach_comp_29b984a7e4efb44a6897eb90adc53634_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_mystery"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "book" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_29b984a7e4efb44a6897eb90adc53634_3e8caf1e.displayName = "Foreach";

export const Bare_comp_a67474f8c0befd53d6aebb48aa84dcfc_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("books_mystery") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_a67474f8c0befd53d6aebb48aa84dcfc_3e8caf1e.displayName = "Bare";

export const Cond_comp_bde798d7cbbe5d7d6580f3f6c0c21b9b_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_mystery"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_bde798d7cbbe5d7d6580f3f6c0c21b9b_3e8caf1e.displayName = "Cond";

export const Button_button_2d80d48bc7b5ca018dfc37cbf8b7da0f_3e8caf1e = memo(({children}) => {
    const on_click_e133b6990ce1cc42a34ae6a7e82615f3 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_game_theory');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"books_game_theory","aria-label":"Anteriores: Teoria dos Jogos",className:"shelf-arrow",onClick:on_click_e133b6990ce1cc42a34ae6a7e82615f3,type:"button"},children)
    )
});
Button_button_2d80d48bc7b5ca018dfc37cbf8b7da0f_3e8caf1e.displayName = "Button";

export const Button_button_0e470ea4af87679c02968eeefbfd82ab_3e8caf1e = memo(({children}) => {
    const on_click_17a8e790b3ba6c343c7b353f208ffbd5 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_game_theory');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"books_game_theory","aria-label":"Pr\u00f3ximos: Teoria dos Jogos",className:"shelf-arrow",onClick:on_click_17a8e790b3ba6c343c7b353f208ffbd5,type:"button"},children)
    )
});
Button_button_0e470ea4af87679c02968eeefbfd82ab_3e8caf1e.displayName = "Button";

export const Foreach_comp_da6a6b40d3dac18cfaa698a8e513f547_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_game_theory"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "book" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_da6a6b40d3dac18cfaa698a8e513f547_3e8caf1e.displayName = "Foreach";

export const Bare_comp_c299cfbfd35a3ae2c340072f1110b683_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("books_game_theory") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_c299cfbfd35a3ae2c340072f1110b683_3e8caf1e.displayName = "Bare";

export const Cond_comp_609ab7592a05df532ea1340b761a2dc0_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_game_theory"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_609ab7592a05df532ea1340b761a2dc0_3e8caf1e.displayName = "Cond";

export const Button_button_06cbcd57f090b811725dea653537a5d1_3e8caf1e = memo(({children}) => {
    const on_click_c71ddc52e9b56886fa751f4199149833 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('anime_rated');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"anime_rated","aria-label":"Anteriores: Animes muito bem avaliados",className:"shelf-arrow",onClick:on_click_c71ddc52e9b56886fa751f4199149833,type:"button"},children)
    )
});
Button_button_06cbcd57f090b811725dea653537a5d1_3e8caf1e.displayName = "Button";

export const Button_button_834d1131f7793103a19ec363f563ca11_3e8caf1e = memo(({children}) => {
    const on_click_297747bf7786e60c304128a8c3bbe622 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('anime_rated');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"anime_rated","aria-label":"Pr\u00f3ximos: Animes muito bem avaliados",className:"shelf-arrow",onClick:on_click_297747bf7786e60c304128a8c3bbe622,type:"button"},children)
    )
});
Button_button_834d1131f7793103a19ec363f563ca11_3e8caf1e.displayName = "Button";

export const Foreach_comp_8a1bbe0ff9f17f31018d266c102d0065_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["anime_rated"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "anime" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_8a1bbe0ff9f17f31018d266c102d0065_3e8caf1e.displayName = "Foreach";

export const Bare_comp_b298636ff799d30e5fcb76b65b93cfab_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("anime_rated") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_b298636ff799d30e5fcb76b65b93cfab_3e8caf1e.displayName = "Bare";

export const Cond_comp_9248b37a8a549081a2abbdc283e4be70_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["anime_rated"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_9248b37a8a549081a2abbdc283e4be70_3e8caf1e.displayName = "Cond";

export const Button_button_14d5b4b6db91712f2a827bb25a0e54e5_3e8caf1e = memo(({children}) => {
    const on_click_1beb5c297986f619351dda53c9b734f4 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('anime_popular');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"anime_popular","aria-label":"Anteriores: Animes populares",className:"shelf-arrow",onClick:on_click_1beb5c297986f619351dda53c9b734f4,type:"button"},children)
    )
});
Button_button_14d5b4b6db91712f2a827bb25a0e54e5_3e8caf1e.displayName = "Button";

export const Button_button_53fa6db8efa975d55e4ae10aa64d2654_3e8caf1e = memo(({children}) => {
    const on_click_6638f0ee70f06e608337eb19a6a8bb8e = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('anime_popular');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"anime_popular","aria-label":"Pr\u00f3ximos: Animes populares",className:"shelf-arrow",onClick:on_click_6638f0ee70f06e608337eb19a6a8bb8e,type:"button"},children)
    )
});
Button_button_53fa6db8efa975d55e4ae10aa64d2654_3e8caf1e.displayName = "Button";

export const Foreach_comp_063875a285f979b15f1e90bdcc5c897f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["anime_popular"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "anime" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_063875a285f979b15f1e90bdcc5c897f_3e8caf1e.displayName = "Foreach";

export const Bare_comp_835b7653ead7b86b82ca4144b6ccf98e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("anime_popular") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_835b7653ead7b86b82ca4144b6ccf98e_3e8caf1e.displayName = "Bare";

export const Cond_comp_1fcab5845e846b9da0a03d93c441e10b_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["anime_popular"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_1fcab5845e846b9da0a03d93c441e10b_3e8caf1e.displayName = "Cond";

export const Button_button_01621a8ad9ec0ae0e277c50f9e75f081_3e8caf1e = memo(({children}) => {
    const on_click_64b7b773124fbc6f016a96db7b9acc40 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('anime_current');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"anime_current","aria-label":"Anteriores: Animes em destaque agora",className:"shelf-arrow",onClick:on_click_64b7b773124fbc6f016a96db7b9acc40,type:"button"},children)
    )
});
Button_button_01621a8ad9ec0ae0e277c50f9e75f081_3e8caf1e.displayName = "Button";

export const Button_button_add3e7cd340f8022bfcdcbe372ba7410_3e8caf1e = memo(({children}) => {
    const on_click_1113bd99c8ce0c3aba781bd7d562beee = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('anime_current');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-controls":"anime_current","aria-label":"Pr\u00f3ximos: Animes em destaque agora",className:"shelf-arrow",onClick:on_click_1113bd99c8ce0c3aba781bd7d562beee,type:"button"},children)
    )
});
Button_button_add3e7cd340f8022bfcdcbe372ba7410_3e8caf1e.displayName = "Button";

export const Foreach_comp_faa74fba55818112f4dc64382171d93a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["anime_current"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "anime" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_faa74fba55818112f4dc64382171d93a_3e8caf1e.displayName = "Foreach";

export const Bare_comp_8748cbad5a039e2974cd275a52471cf7_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("anime_current") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_8748cbad5a039e2974cd275a52471cf7_3e8caf1e.displayName = "Bare";

export const Cond_comp_711d69f9d847bdf7be8a8b55aed82bc3_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["anime_current"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_711d69f9d847bdf7be8a8b55aed82bc3_3e8caf1e.displayName = "Cond";

export const Cond_comp_123d1305d3f56aad31436f2b67c9381e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_123d1305d3f56aad31436f2b67c9381e_3e8caf1e.displayName = "Cond";

export const Button_button_e285a8558f1e38c2f03c0a3fe10955ac_3e8caf1e = memo(({children}) => {
    const on_click_5c2f66104c1a55d4cbd2f2e8c82ff32c = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.more_results", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{className:"action-button",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_,onClick:on_click_5c2f66104c1a55d4cbd2f2e8c82ff32c,type:"button"},children)
    )
});
Button_button_e285a8558f1e38c2f03c0a3fe10955ac_3e8caf1e.displayName = "Button";

export const Cond_comp_664b1c8118513ba73ae961d69ae9fb74_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (pyAnd(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_, () => (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.has_more_results_rx_state_))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_664b1c8118513ba73ae961d69ae9fb74_3e8caf1e.displayName = "Cond";

export const Foreach_comp_58836b00fee949783efcfb17b887d1b8_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.catalog_items_rx_state_ ?? [],((m_rx_state_,index_a11d272e345ae0206655af59b2295c9b)=>(jsx(ReactRouterLink,{className:"media-card",key:index_a11d272e345ae0206655af59b2295c9b,to:("/obra/"+m_rx_state_?.["id"])},jsx("div",{className:"h-full"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},))))),jsx("div",{className:"p-4"},jsx("h3",{className:"font-semibold line-clamp-2"},m_rx_state_?.["title"]),jsx("p",{className:"text-sm text-gray-400 mt-3"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"]))))))))
    )
});
Foreach_comp_58836b00fee949783efcfb17b887d1b8_3e8caf1e.displayName = "Foreach";

export const Cond_comp_d58f68820efcbd0480a9d900aa65d090_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.catalog_items_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d58f68820efcbd0480a9d900aa65d090_3e8caf1e.displayName = "Cond";

export const Img_img_4d07f02b618509eeb627e767a03cb40b_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{alt:("Banner de "+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["display_name"]),className:"profile-banner-image",src:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["banner_url"]},)
    )
});
Img_img_4d07f02b618509eeb627e767a03cb40b_3e8caf1e.displayName = "Img";

export const Cond_comp_939dbb80337ead8c18f35f485eabf776_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["banner_url"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_939dbb80337ead8c18f35f485eabf776_3e8caf1e.displayName = "Cond";

export const Img_img_cbc32d710090e407ec9e228e05ee1fd5_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{alt:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["display_name"],className:"avatar",src:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["avatar_url"]},)
    )
});
Img_img_cbc32d710090e407ec9e228e05ee1fd5_3e8caf1e.displayName = "Img";

export const Cond_comp_883e844d72d637a30eb5ac956475282c_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["avatar_url"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_883e844d72d637a30eb5ac956475282c_3e8caf1e.displayName = "Cond";

export const Bare_comp_146959cd723e0bbdb9b7c28c233ace4b_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["display_name"]
    )
});
Bare_comp_146959cd723e0bbdb9b7c28c233ace4b_3e8caf1e.displayName = "Bare";

export const Bare_comp_02eb389169891ba9baf7f9179eace85c_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ("@"+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["username"])
    )
});
Bare_comp_02eb389169891ba9baf7f9179eace85c_3e8caf1e.displayName = "Bare";

export const Bare_comp_13e9cc313cdaeddc9ed3a652a3697c90_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["bio"]
    )
});
Bare_comp_13e9cc313cdaeddc9ed3a652a3697c90_3e8caf1e.displayName = "Bare";

export const Styledupload_comp_52c56c59e4d939d0a41743e26e285ec6_3e8caf1e = memo(({children}) => {
    const ref_profile_banner_upload = useRef(null); refs["ref_profile_banner_upload"] = ref_profile_banner_upload;
const [filesById, setFilesById] = useContext(UploadFilesContext);
const on_drop_7021fe1b08685bf503a9b970df95f421 = useCallback(((_ev_0) => ((e => setFilesById(filesById => {
    const updatedFilesById = Object.assign({}, filesById);
    updatedFilesById["profile_banner_upload"] = e;
    return updatedFilesById;
  })
    )(_ev_0))), [addEvents, ReflexEvent, filesById, setFilesById])
const on_drop_rejected_2fcedbdc0771e7617b4270e2d1ac8cc9 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("_call_function", ({ ["function"] : (() => (refs['__toast']?.["error"]("", ({ ["title"] : "Files not Accepted", ["description"] : _ev_0.map(((osizayzf) => (osizayzf?.["file"]?.["path"]+": "+osizayzf?.["errors"].map(((wnkiegyk) => wnkiegyk?.["message"])).join(", ")))).join("\n\n"), ["closeButton"] : true, ["style"] : ({ ["whiteSpace"] : "pre-line" }) })))), ["callback"] : null }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const { getRootProps: xdvxrcsn, getInputProps: udaxihhe, isDragActive: bacghqta} = useDropzone(({ ["accept"] : ({ ["image/png"] : [".png"], ["image/jpeg"] : [".jpg", ".jpeg"], ["image/webp"] : [".webp"], ["image/gif"] : [".gif"] }), ["maxFiles"] : 1, ["maxSize"] : 5242880, ["multiple"] : true, ["id"] : "profile_banner_upload", ["onDrop"] : on_drop_7021fe1b08685bf503a9b970df95f421, ["onDropRejected"] : on_drop_rejected_2fcedbdc0771e7617b4270e2d1ac8cc9 }));



    return(
        jsx(Fragment,{},jsx("div",{className:"rx-Upload profile-upload-dropzone",css:({ ["border"] : "1px dashed var(--accent-12)", ["padding"] : "5em", ["textAlign"] : "center" }),id:"profile_banner_upload",ref:ref_profile_banner_upload,...xdvxrcsn()},jsx("input",{type:"file",...udaxihhe()},),jsx("div",{className:"profile-upload-prompt"},jsx(LucideImageUp,{size:18},),jsx("span",{},"Escolher ou arrastar uma imagem para o banner"))))
    )
});
Styledupload_comp_52c56c59e4d939d0a41743e26e285ec6_3e8caf1e.displayName = "StyledUpload";

export const Bare_comp_854a0e8c3b3c9095a3f4483ac230d265_3e8caf1e = memo(({children}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);



    return(
        (filesById["profile_banner_upload"] ? filesById["profile_banner_upload"].map((f) => f.name) : [])?.at?.(0)
    )
});
Bare_comp_854a0e8c3b3c9095a3f4483ac230d265_3e8caf1e.displayName = "Bare";

export const Cond_comp_e2b6b6bedb5d0ac52f202f3d2dbe34ce_3e8caf1e = memo(({children}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);



    return(
        (((filesById["profile_banner_upload"] ? filesById["profile_banner_upload"].map((f) => f.name) : []).length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_e2b6b6bedb5d0ac52f202f3d2dbe34ce_3e8caf1e.displayName = "Cond";

export const Button_button_59efad5c39f275b2a4cb8cded7ca3aaf_3e8caf1e = memo(({children}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);
const on_click_033087e95cb787663e2a9934b8e09f58 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.upload_profile_banner", ({ ["files"] : filesById?.["profile_banner_upload"], ["upload_param_name"] : "files", ["upload_id"] : "profile_banner_upload", ["extra_headers"] : ({  }) }), ({  }), "uploadFiles"))], [_e], ({  })))), [addEvents, ReflexEvent, filesById, setFilesById])



    return(
        jsx("button",{className:"action-button",onClick:on_click_033087e95cb787663e2a9934b8e09f58,type:"button"},children)
    )
});
Button_button_59efad5c39f275b2a4cb8cded7ca3aaf_3e8caf1e.displayName = "Button";

export const Cond_comp_398109de95718c9f73dcfa12a4d3a029_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.owns_profile_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_398109de95718c9f73dcfa12a4d3a029_3e8caf1e.displayName = "Cond";

export const Input_input_7a65065c4f4de38a6aad93d439efa92f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["username"],maxLength:30,name:"username",pattern:"[a-z0-9_]{3,30}",required:true},)
    )
});
Input_input_7a65065c4f4de38a6aad93d439efa92f_3e8caf1e.displayName = "Input";

export const Input_input_ac1a26ac3d2d08de7f0072b30712e84a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["display_name"],maxLength:80,name:"display_name",required:true},)
    )
});
Input_input_ac1a26ac3d2d08de7f0072b30712e84a_3e8caf1e.displayName = "Input";

export const Textarea_textarea_38f23f2a28914eff07da557dd7bd522f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("textarea",{className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["bio"],maxLength:1000,name:"bio"},)
    )
});
Textarea_textarea_38f23f2a28914eff07da557dd7bd522f_3e8caf1e.displayName = "Textarea";

export const Input_input_b1a77e9844b8aa413d0a796c778023c0_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["avatar_url"],name:"avatar_url",type:"url"},)
    )
});
Input_input_b1a77e9844b8aa413d0a796c778023c0_3e8caf1e.displayName = "Input";

export const Form_form_d8ad10e50f75670909c8e8ccef4c14d7_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)

    const handleSubmit_6d9a0a036bae4dc9603996435cfe8a08 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.save_profile", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"editor-form",key:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["username"],onSubmit:handleSubmit_6d9a0a036bae4dc9603996435cfe8a08},children)
    )
});
Form_form_d8ad10e50f75670909c8e8ccef4c14d7_3e8caf1e.displayName = "Form";

export const Bare_comp_42a3d32e57f64962b99c2c40b8db0790_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_ids_rx_state_.includes(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["user_id"]) ? "Deixar de seguir" : "Seguir")
    )
});
Bare_comp_42a3d32e57f64962b99c2c40b8db0790_3e8caf1e.displayName = "Bare";

export const Button_button_4d92c5408dc063eae163ddc09a688cba_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const on_click_57f4377352c30294f0af654f002579ed = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.follow", ({ ["uid"] : reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["user_id"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state])



    return(
        jsx("button",{className:"action-button",onClick:on_click_57f4377352c30294f0af654f002579ed,type:"button"},children)
    )
});
Button_button_4d92c5408dc063eae163ddc09a688cba_3e8caf1e.displayName = "Button";

export const Button_button_5c14aa79be9763a1f1809caf67306c14_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const on_click_454da6800a09ad9ed7f52dfda1af67c9 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_report", ({ ["target_type"] : "profile", ["target_id"] : reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["user_id"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state])



    return(
        jsx("button",{className:"action-button",onClick:on_click_454da6800a09ad9ed7f52dfda1af67c9,type:"button"},children)
    )
});
Button_button_5c14aa79be9763a1f1809caf67306c14_3e8caf1e.displayName = "Button";

export const Cond_comp_5ae4d5417ebcafc13c11c96dd283ab9f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_5ae4d5417ebcafc13c11c96dd283ab9f_3e8caf1e.displayName = "Cond";

export const Bare_comp_e0a38a2883c11adbf8aff495f1ea1cd9_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.followers_rx_state_.length
    )
});
Bare_comp_e0a38a2883c11adbf8aff495f1ea1cd9_3e8caf1e.displayName = "Bare";

export const Bare_comp_339a8dd5ea63f29bbba7c91bb6d1c554_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_rx_state_.length
    )
});
Bare_comp_339a8dd5ea63f29bbba7c91bb6d1c554_3e8caf1e.displayName = "Bare";

export const Bare_comp_b3bf54026b2bdf4dd26e76e5f73c2edb_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_activity_rx_state_.length
    )
});
Bare_comp_b3bf54026b2bdf4dd26e76e5f73c2edb_3e8caf1e.displayName = "Bare";

export const Foreach_comp_1bb634360a7d42eee88001e5da7756e1_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_activity_rx_state_ ?? [],((i_rx_state_,index_7ad83d5035b5d7c68cd58964d6e1d614)=>(jsx("article",{className:"activity-card",key:index_7ad83d5035b5d7c68cd58964d6e1d614},jsx(ReactRouterLink,{className:"activity-cover",to:("/obra/"+i_rx_state_?.["id"])},jsx(Fragment,{},(!((i_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:i_rx_state_?.["title"],loading:"lazy",src:i_rx_state_?.["cover"]},))):(jsx(Fragment,{},jsx(LucideBookOpen,{size:28},)))))),jsx("div",{className:"min-w-0"},jsx(ReactRouterLink,{className:"font-semibold",to:("/obra/"+i_rx_state_?.["id"])},i_rx_state_?.["title"]),jsx("p",{className:"activity-meta"},((((i_rx_state_?.["kind"]+" \u00b7 ")+i_rx_state_?.["status"])+" \u00b7 ")+i_rx_state_?.["rating"])),jsx(Fragment,{},((i_rx_state_?.["spoiler"]?.valueOf?.() === "True"?.valueOf?.())?(jsx(Fragment,{},jsx("details",{},jsx("summary",{className:"cursor-pointer text-amber-300"},"Mostrar conte\u00fado com spoilers"),jsx("p",{className:"whitespace-pre-wrap mt-3"},i_rx_state_?.["review"])))):(jsx(Fragment,{},jsx("p",{className:"whitespace-pre-wrap"},i_rx_state_?.["review"]))))))))))
    )
});
Foreach_comp_1bb634360a7d42eee88001e5da7756e1_3e8caf1e.displayName = "Foreach";

export const Cond_comp_9aaf13dbbb35dff8362e04770a55bcf5_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_activity_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_9aaf13dbbb35dff8362e04770a55bcf5_3e8caf1e.displayName = "Cond";

export const Foreach_comp_0461b1d6327886e4e483ba336b4d8c1a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.followers_rx_state_ ?? [],((p_rx_state_,index_7caa5359f2f7fef3ebd24122578682c4)=>(jsx("article",{className:"rounded-2xl border border-white/10 bg-[#111114] p-5 space-y-4",key:index_7caa5359f2f7fef3ebd24122578682c4},jsx(ReactRouterLink,{className:"text-xl font-semibold",to:("/perfil/"+p_rx_state_?.["user_id"])},p_rx_state_?.["display_name"]),jsx("p",{className:"text-[#F5B300]"},("@"+p_rx_state_?.["username"])),jsx("p",{className:"text-gray-400"},p_rx_state_?.["bio"]),jsx(Fragment,{},(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state.is_authenticated_rx_state_, () => (!((p_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.()))))?(jsx(Fragment,{},jsx("button",{className:"action-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.follow", ({ ["uid"] : p_rx_state_?.["user_id"] }), ({  })))], [_e], ({  })))),type:"button"},(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_ids_rx_state_.includes(p_rx_state_?.["user_id"]) ? "Deixar de seguir" : "Seguir")))):(jsx(Fragment,{},))))))))
    )
});
Foreach_comp_0461b1d6327886e4e483ba336b4d8c1a_3e8caf1e.displayName = "Foreach";

export const Cond_comp_48f2bcd64e5230d88c5af5a41dc57241_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.followers_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_48f2bcd64e5230d88c5af5a41dc57241_3e8caf1e.displayName = "Cond";

export const Foreach_comp_4a9474bd9ae08cf7c2da7fdb37378478_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_rx_state_ ?? [],((p_rx_state_,index_7caa5359f2f7fef3ebd24122578682c4)=>(jsx("article",{className:"rounded-2xl border border-white/10 bg-[#111114] p-5 space-y-4",key:index_7caa5359f2f7fef3ebd24122578682c4},jsx(ReactRouterLink,{className:"text-xl font-semibold",to:("/perfil/"+p_rx_state_?.["user_id"])},p_rx_state_?.["display_name"]),jsx("p",{className:"text-[#F5B300]"},("@"+p_rx_state_?.["username"])),jsx("p",{className:"text-gray-400"},p_rx_state_?.["bio"]),jsx(Fragment,{},(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state.is_authenticated_rx_state_, () => (!((p_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.()))))?(jsx(Fragment,{},jsx("button",{className:"action-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.follow", ({ ["uid"] : p_rx_state_?.["user_id"] }), ({  })))], [_e], ({  })))),type:"button"},(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_ids_rx_state_.includes(p_rx_state_?.["user_id"]) ? "Deixar de seguir" : "Seguir")))):(jsx(Fragment,{},))))))))
    )
});
Foreach_comp_4a9474bd9ae08cf7c2da7fdb37378478_3e8caf1e.displayName = "Foreach";

export const Cond_comp_54a9d3fea8e650732a185ab77abbf9ea_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_54a9d3fea8e650732a185ab77abbf9ea_3e8caf1e.displayName = "Cond";

export const Select_select_64f2977b2a5bfa89727214940e5d35f9_3e8caf1e = memo(({children}) => {
    const ref_report_reason = useRef(null); refs["ref_report_reason"] = ref_report_reason;
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("select",{className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.report_reason_rx_state_,id:"report-reason",name:"reason",ref:ref_report_reason},children)
    )
});
Select_select_64f2977b2a5bfa89727214940e5d35f9_3e8caf1e.displayName = "Select";

export const Button_button_4b65566d2b61eaa480906b6a44132d98_3e8caf1e = memo(({children}) => {
    const on_click_a2e4e7fb8948596b9268fa2b1b074334 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.close_report", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{className:"quiet-button",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.report_sending_rx_state_,onClick:on_click_a2e4e7fb8948596b9268fa2b1b074334,type:"button"},children)
    )
});
Button_button_4b65566d2b61eaa480906b6a44132d98_3e8caf1e.displayName = "Button";

export const Bare_comp_a3ba5b83e85e69b9fd57bb82d7751c34_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.report_sending_rx_state_ ? "Enviando\u2026" : "Enviar report")
    )
});
Bare_comp_a3ba5b83e85e69b9fd57bb82d7751c34_3e8caf1e.displayName = "Bare";

export const Button_button_e9f2a9c29eacf1126daf69358f19141b_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{className:"action-button",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.report_sending_rx_state_,type:"submit"},children)
    )
});
Button_button_e9f2a9c29eacf1126daf69358f19141b_3e8caf1e.displayName = "Button";

export const Form_form_80a9498f530532f6fc934ab5d3db2fdb_3e8caf1e = memo(({children}) => {
    

    const handleSubmit_92f30877f9fc4fbd51c1bf783375a8ee = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["report_reason"] : getRefValue(refs["ref_report_reason"]), ["report_description"] : getRefValue(refs["ref_report_description"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.submit_report", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"space-y-3",onSubmit:handleSubmit_92f30877f9fc4fbd51c1bf783375a8ee},children)
    )
});
Form_form_80a9498f530532f6fc934ab5d3db2fdb_3e8caf1e.displayName = "Form";

export const Cond_comp_26cd95f5f87f25b4396543053c7e46d3_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.report_dialog_open_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_26cd95f5f87f25b4396543053c7e46d3_3e8caf1e.displayName = "Cond";

export const Styledupload_comp_ec1a92cc28e13b026039e00b2de4d5ee_3e8caf1e = memo(({children}) => {
    const ref_profile_banner_upload = useRef(null); refs["ref_profile_banner_upload"] = ref_profile_banner_upload;
const [filesById, setFilesById] = useContext(UploadFilesContext);
const on_drop_7021fe1b08685bf503a9b970df95f421 = useCallback(((_ev_0) => ((e => setFilesById(filesById => {
    const updatedFilesById = Object.assign({}, filesById);
    updatedFilesById["profile_banner_upload"] = e;
    return updatedFilesById;
  })
    )(_ev_0))), [addEvents, ReflexEvent, filesById, setFilesById])
const on_drop_rejected_51f7597a906ee6a527ceb347e5723946 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("_call_function", ({ ["function"] : (() => (refs['__toast']?.["error"]("", ({ ["title"] : "Files not Accepted", ["description"] : _ev_0.map(((dmioulfl) => (dmioulfl?.["file"]?.["path"]+": "+dmioulfl?.["errors"].map(((lgviwvuc) => lgviwvuc?.["message"])).join(", ")))).join("\n\n"), ["closeButton"] : true, ["style"] : ({ ["whiteSpace"] : "pre-line" }) })))), ["callback"] : null }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const { getRootProps: zbxordmc, getInputProps: dcmdllti, isDragActive: rjutlsgw} = useDropzone(({ ["accept"] : ({ ["image/png"] : [".png"], ["image/jpeg"] : [".jpg", ".jpeg"], ["image/webp"] : [".webp"], ["image/gif"] : [".gif"] }), ["maxFiles"] : 1, ["maxSize"] : 5242880, ["multiple"] : true, ["id"] : "profile_banner_upload", ["onDrop"] : on_drop_7021fe1b08685bf503a9b970df95f421, ["onDropRejected"] : on_drop_rejected_51f7597a906ee6a527ceb347e5723946 }));



    return(
        jsx(Fragment,{},jsx("div",{className:"rx-Upload profile-upload-dropzone",css:({ ["border"] : "1px dashed var(--accent-12)", ["padding"] : "5em", ["textAlign"] : "center" }),id:"profile_banner_upload",ref:ref_profile_banner_upload,...zbxordmc()},jsx("input",{type:"file",...dcmdllti()},),jsx("div",{className:"profile-upload-prompt"},jsx(LucideImageUp,{size:18},),jsx("span",{},"Escolher ou arrastar uma imagem para o banner"))))
    )
});
Styledupload_comp_ec1a92cc28e13b026039e00b2de4d5ee_3e8caf1e.displayName = "StyledUpload";

export const Img_img_b1dd6e348a6b6d0c0afce2de11ad7e56_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{alt:("Capa de "+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["title"]),className:"media-detail-poster",src:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["cover"]},)
    )
});
Img_img_b1dd6e348a6b6d0c0afce2de11ad7e56_3e8caf1e.displayName = "Img";

export const Cond_comp_b23b03da4603758b1ef121bc8896178a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_b23b03da4603758b1ef121bc8896178a_3e8caf1e.displayName = "Cond";

export const Img_img_66a43c90a52141d1489aa88f7cbe6c58_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{alt:"","aria-hidden":true,className:"media-detail-backdrop",src:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["backdrop"]},)
    )
});
Img_img_66a43c90a52141d1489aa88f7cbe6c58_3e8caf1e.displayName = "Img";

export const Cond_comp_4f998186a9ec03f6c13b1c5e78f246e8_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["backdrop"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_4f998186a9ec03f6c13b1c5e78f246e8_3e8caf1e.displayName = "Cond";

export const Bare_comp_b6d0048d30c3005ff5b988215d118df4_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["kind"]+"  \u00b7  ")+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["year"])
    )
});
Bare_comp_b6d0048d30c3005ff5b988215d118df4_3e8caf1e.displayName = "Bare";

export const Bare_comp_41f0fb9f123e1807dae9a3483c8c6be9_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["title"]
    )
});
Bare_comp_41f0fb9f123e1807dae9a3483c8c6be9_3e8caf1e.displayName = "Bare";

export const Bare_comp_54ec2025047183607961c71834d6a5f2_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["description"]?.valueOf?.() === ""?.valueOf?.())) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["description"] : "Descri\u00e7\u00e3o ainda n\u00e3o dispon\u00edvel.")
    )
});
Bare_comp_54ec2025047183607961c71834d6a5f2_3e8caf1e.displayName = "Bare";

export const Button_button_c1687ab8e1da4f163c7a05d6e45725ff_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const on_click_c63fe4ea54a340c4b2dcabcaf3c79a95 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_report", ({ ["target_type"] : "media", ["target_id"] : reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["id"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state])



    return(
        jsx("button",{className:"action-button",onClick:on_click_c63fe4ea54a340c4b2dcabcaf3c79a95,type:"button"},children)
    )
});
Button_button_c1687ab8e1da4f163c7a05d6e45725ff_3e8caf1e.displayName = "Button";

export const Bare_comp_caaec90f1fbef75a1d1708006a0b08c4_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["details"]?.valueOf?.() === ""?.valueOf?.())) ? ((((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["details"]+"  \u00b7  ")+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["kind"])+"  \u00b7  ")+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["year"]) : ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["kind"]+"  \u00b7  ")+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["year"]))
    )
});
Bare_comp_caaec90f1fbef75a1d1708006a0b08c4_3e8caf1e.displayName = "Bare";

export const Foreach_comp_7d89ea8f503bab7134e1b839fbb9f807_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.availability_rx_state_ ?? [],((provider_rx_state_,index_ae78fbd9c4182a4290fd7edfdcfb33fb)=>(jsx(ReactRouterLink,{className:"availability-chip",key:index_ae78fbd9c4182a4290fd7edfdcfb33fb,rel:"noopener noreferrer",target:"_blank",to:provider_rx_state_?.["url"]},jsx("span",{},provider_rx_state_?.["name"])))))
    )
});
Foreach_comp_7d89ea8f503bab7134e1b839fbb9f807_3e8caf1e.displayName = "Foreach";

export const Cond_comp_a46304a888484f23bae76b38cde96e9f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.availability_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_a46304a888484f23bae76b38cde96e9f_3e8caf1e.displayName = "Cond";

export const Cond_comp_af9661d6586cc5c9c59f6d00bc36afab_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["source"]?.valueOf?.() === "tmdb"?.valueOf?.())?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_af9661d6586cc5c9c59f6d00bc36afab_3e8caf1e.displayName = "Cond";

export const Foreach_comp_18bef35e0330824876a1e214bf08b347_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.trailers_rx_state_ ?? [],((trailer_rx_state_,index_cebaefce5ad24547f5a0831c19887371)=>(jsx("article",{className:"media-trailer-card",key:index_cebaefce5ad24547f5a0831c19887371},jsx("h3",{className:"font-semibold mb-3"},trailer_rx_state_?.["title"]),jsx("iframe",{allow:"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share",className:"media-trailer",css:({ ["allowFullscreen"] : true }),loading:"lazy",src:trailer_rx_state_?.["embed_url"],title:trailer_rx_state_?.["title"]},)))))
    )
});
Foreach_comp_18bef35e0330824876a1e214bf08b347_3e8caf1e.displayName = "Foreach";

export const Cond_comp_9fae35b2b2b4ffad7cee9e7263de1017_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.trailers_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_9fae35b2b2b4ffad7cee9e7263de1017_3e8caf1e.displayName = "Cond";

export const Input_input_ac4c9ec8dce1a89d1ea59cf328a91bd1_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{name:"status",type:"hidden",value:(isNotNullOrUndefined(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_status_rx_state_) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_status_rx_state_ : "")},)
    )
});
Input_input_ac4c9ec8dce1a89d1ea59cf328a91bd1_3e8caf1e.displayName = "Input";

export const Foreach_comp_92ec5447afb9851d6daa282f82b0155c_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call([["planned", "Quero ver / ler"], ["in_progress", "Em andamento"], ["completed", "Conclu\u00eddo"], ["dropped", "Abandonado"]] ?? [],((pair_rx_state_,index_aa829a0cc9015e7fae3205fae921b0eb)=>(jsx("button",{className:((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_status_rx_state_?.valueOf?.() === pair_rx_state_?.at?.(0)?.valueOf?.()) ? "status-chip selected" : "status-chip"),key:index_aa829a0cc9015e7fae3205fae921b0eb,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_selected_status", ({ ["value"] : pair_rx_state_?.at?.(0) }), ({  })))], [_e], ({  })))),type:"button"},pair_rx_state_?.at?.(1)))))
    )
});
Foreach_comp_92ec5447afb9851d6daa282f82b0155c_3e8caf1e.displayName = "Foreach";

export const Button_button_afc7bc9e8adf850019839230eead5f40_3e8caf1e = memo(({children}) => {
    const on_click_adc242d37c187bd0026fd1a6ada9816d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_selected_rating", ({ ["value"] : "1" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-label":"Nota 1 de 5",className:"rating-star",onClick:on_click_adc242d37c187bd0026fd1a6ada9816d,type:"button"},children)
    )
});
Button_button_afc7bc9e8adf850019839230eead5f40_3e8caf1e.displayName = "Button";

export const Button_button_7c8bb9ff62d025fd4dc005d10734cc66_3e8caf1e = memo(({children}) => {
    const on_click_befc5c44e812728540b1b3e54d8277a6 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_selected_rating", ({ ["value"] : "2" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-label":"Nota 2 de 5",className:"rating-star",onClick:on_click_befc5c44e812728540b1b3e54d8277a6,type:"button"},children)
    )
});
Button_button_7c8bb9ff62d025fd4dc005d10734cc66_3e8caf1e.displayName = "Button";

export const Button_button_9804f59977d6a2fe445c8b639f3e5a2e_3e8caf1e = memo(({children}) => {
    const on_click_f6c9e21e8a3b9c223c6630c6082a379f = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_selected_rating", ({ ["value"] : "3" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-label":"Nota 3 de 5",className:"rating-star",onClick:on_click_f6c9e21e8a3b9c223c6630c6082a379f,type:"button"},children)
    )
});
Button_button_9804f59977d6a2fe445c8b639f3e5a2e_3e8caf1e.displayName = "Button";

export const Button_button_d471b4436757643ea5bb148b902de90e_3e8caf1e = memo(({children}) => {
    const on_click_c3f559b7f0addb6b77ddd44ba3a6363c = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_selected_rating", ({ ["value"] : "4" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-label":"Nota 4 de 5",className:"rating-star",onClick:on_click_c3f559b7f0addb6b77ddd44ba3a6363c,type:"button"},children)
    )
});
Button_button_d471b4436757643ea5bb148b902de90e_3e8caf1e.displayName = "Button";

export const Button_button_6df0f897993e4037ad5cae3ee8f645c3_3e8caf1e = memo(({children}) => {
    const on_click_f7ba70710eb556b2bdb1686401631a57 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_selected_rating", ({ ["value"] : "5" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{"aria-label":"Nota 5 de 5",className:"rating-star",onClick:on_click_f7ba70710eb556b2bdb1686401631a57,type:"button"},children)
    )
});
Button_button_6df0f897993e4037ad5cae3ee8f645c3_3e8caf1e.displayName = "Button";

export const Valuenumberinput_input_129c8a87e5d3964352a87f9d79575306_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rating_rx_state_,max:5,min:0,name:"rating",placeholder:"0 a 5",step:0.5,type:"number"},)
    )
});
Valuenumberinput_input_129c8a87e5d3964352a87f9d79575306_3e8caf1e.displayName = "ValueNumberInput";

export const Textarea_textarea_fce99647119f65130360363db109f626_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("textarea",{className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_review_rx_state_,maxLength:10000,name:"review",placeholder:"Conte o que achou desta obra...",rows:5},)
    )
});
Textarea_textarea_fce99647119f65130360363db109f626_3e8caf1e.displayName = "Textarea";

export const Checkboxinput_input_097b620cfd27adca1787f7a221c0b5e0_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{defaultChecked:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_spoiler_rx_state_,name:"spoiler",type:"checkbox"},)
    )
});
Checkboxinput_input_097b620cfd27adca1787f7a221c0b5e0_3e8caf1e.displayName = "CheckboxInput";

export const Form_form_ee3931626db9893fa5aa9fb426d87a38_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)

    const handleSubmit_e392c02d48849663aadc71bbfb94e025 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.save_interaction", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"media-review-form",key:((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["id"]+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_review_rx_state_)+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rating_rx_state_),onSubmit:handleSubmit_e392c02d48849663aadc71bbfb94e025},children)
    )
});
Form_form_ee3931626db9893fa5aa9fb426d87a38_3e8caf1e.displayName = "Form";

export const Button_button_c9ca02bad51f7cd6489cd3747863c7f5_3e8caf1e = memo(({children}) => {
    const on_click_9d96b913db1de3a5a81d29bba43d3f7e = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.quick_add", ({ ["status"] : "planned", ["rating"] : 0, ["list_title"] : "Quero ver / ler" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"media-list-link",onClick:on_click_9d96b913db1de3a5a81d29bba43d3f7e},children)
    )
});
Button_button_c9ca02bad51f7cd6489cd3747863c7f5_3e8caf1e.displayName = "Button";

export const Button_button_f053b968c021f859f13eccc1e140d660_3e8caf1e = memo(({children}) => {
    const on_click_345153183042d95bf3d0ebcc946ea7fd = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.quick_add", ({ ["status"] : "completed", ["rating"] : 0, ["list_title"] : "J\u00e1 assisti / li" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"media-list-link",onClick:on_click_345153183042d95bf3d0ebcc946ea7fd},children)
    )
});
Button_button_f053b968c021f859f13eccc1e140d660_3e8caf1e.displayName = "Button";

export const Foreach_comp_6ed8fd4bf65c844b09ddb677775b55a6_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.community_reviews_rx_state_ ?? [],((review_rx_state_,index_00515bbf9f83dc82e44a0e394ec66593)=>(jsx("article",{className:"media-community-review",key:index_00515bbf9f83dc82e44a0e394ec66593},jsx("div",{className:"flex flex-wrap items-center gap-2"},jsx("strong",{},review_rx_state_?.["author"]),jsx(Fragment,{},(!((review_rx_state_?.["rating"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("span",{className:"brand-yellow"},("  \u00b7  Nota "+review_rx_state_?.["rating"])))):(jsx(Fragment,{},)))),jsx(Fragment,{},(!((review_rx_state_?.["date"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("span",{className:"text-xs text-gray-500"},("  \u00b7  "+review_rx_state_?.["date"])))):(jsx(Fragment,{},))))),jsx("p",{className:"text-sm leading-relaxed whitespace-pre-wrap mt-3"},review_rx_state_?.["body"])))))
    )
});
Foreach_comp_6ed8fd4bf65c844b09ddb677775b55a6_3e8caf1e.displayName = "Foreach";

export const Cond_comp_793ae46d2e7516f8423f5cbaee33b9c8_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.community_reviews_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_793ae46d2e7516f8423f5cbaee33b9c8_3e8caf1e.displayName = "Cond";

export const Foreach_comp_ed47f63467e3132be41dcdd3a14827ec_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.recommendations_rx_state_ ?? [],((m_rx_state_,index_ca847a6a8c001ae491d3a2b9809ad161)=>(jsx("button",{className:"media-card text-left",key:index_ca847a6a8c001ae491d3a2b9809ad161,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_recommendation", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"] }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},))))),jsx("div",{className:"p-4"},jsx("h3",{className:"font-semibold line-clamp-2"},m_rx_state_?.["title"]),jsx("p",{className:"text-sm text-gray-400"},m_rx_state_?.["year"]))))))
    )
});
Foreach_comp_ed47f63467e3132be41dcdd3a14827ec_3e8caf1e.displayName = "Foreach";

export const Cond_comp_5c7367c1871e37bc2fd7e5dea8cb9e45_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.recommendations_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_5c7367c1871e37bc2fd7e5dea8cb9e45_3e8caf1e.displayName = "Cond";

export const Cond_comp_c423b64e878a756966d2972d22e76d82_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["title"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_c423b64e878a756966d2972d22e76d82_3e8caf1e.displayName = "Cond";

export const Foreach_comp_8937258c3f0b8d58183824c082ee409e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_library_rx_state_ ?? [],((i_rx_state_,index_7ad83d5035b5d7c68cd58964d6e1d614)=>(jsx("article",{className:"activity-card",key:index_7ad83d5035b5d7c68cd58964d6e1d614},jsx(ReactRouterLink,{className:"activity-cover",to:("/obra/"+i_rx_state_?.["id"])},jsx(Fragment,{},(!((i_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:i_rx_state_?.["title"],loading:"lazy",src:i_rx_state_?.["cover"]},))):(jsx(Fragment,{},jsx(LucideBookOpen,{size:28},)))))),jsx("div",{className:"min-w-0"},jsx(ReactRouterLink,{className:"font-semibold",to:("/obra/"+i_rx_state_?.["id"])},i_rx_state_?.["title"]),jsx("p",{className:"activity-meta"},((((i_rx_state_?.["kind"]+" \u00b7 ")+i_rx_state_?.["status"])+" \u00b7 ")+i_rx_state_?.["rating"])),jsx(Fragment,{},((i_rx_state_?.["spoiler"]?.valueOf?.() === "True"?.valueOf?.())?(jsx(Fragment,{},jsx("details",{},jsx("summary",{className:"cursor-pointer text-amber-300"},"Mostrar conte\u00fado com spoilers"),jsx("p",{className:"whitespace-pre-wrap mt-3"},i_rx_state_?.["review"])))):(jsx(Fragment,{},jsx("p",{className:"whitespace-pre-wrap"},i_rx_state_?.["review"]))))))))))
    )
});
Foreach_comp_8937258c3f0b8d58183824c082ee409e_3e8caf1e.displayName = "Foreach";

export const Cond_comp_fa0792af65cdfe0af287cda45275b637_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.library_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_fa0792af65cdfe0af287cda45275b637_3e8caf1e.displayName = "Cond";

export const Button_button_7c120b9cf531ea74f8f6d7b3cc28097f_3e8caf1e = memo(({children}) => {
    const on_click_9efc09e834df01cf738ce33703737286 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.show_more", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"action-button",onClick:on_click_9efc09e834df01cf738ce33703737286,type:"button"},children)
    )
});
Button_button_7c120b9cf531ea74f8f6d7b3cc28097f_3e8caf1e.displayName = "Button";

export const Cond_comp_c75a83a1d506437bbb41d8dddbe8ecf0_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.library_rx_state_.length > reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_count_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_c75a83a1d506437bbb41d8dddbe8ecf0_3e8caf1e.displayName = "Cond";

export const Foreach_comp_2f17a512cddc8a69160a7008385f79db_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_people_rx_state_ ?? [],((p_rx_state_,index_7caa5359f2f7fef3ebd24122578682c4)=>(jsx("article",{className:"rounded-2xl border border-white/10 bg-[#111114] p-5 space-y-4",key:index_7caa5359f2f7fef3ebd24122578682c4},jsx(ReactRouterLink,{className:"text-xl font-semibold",to:("/perfil/"+p_rx_state_?.["user_id"])},p_rx_state_?.["display_name"]),jsx("p",{className:"text-[#F5B300]"},("@"+p_rx_state_?.["username"])),jsx("p",{className:"text-gray-400"},p_rx_state_?.["bio"]),jsx(Fragment,{},(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state.is_authenticated_rx_state_, () => (!((p_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.()))))?(jsx(Fragment,{},jsx("button",{className:"action-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.follow", ({ ["uid"] : p_rx_state_?.["user_id"] }), ({  })))], [_e], ({  })))),type:"button"},(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_ids_rx_state_.includes(p_rx_state_?.["user_id"]) ? "Deixar de seguir" : "Seguir")))):(jsx(Fragment,{},))))))))
    )
});
Foreach_comp_2f17a512cddc8a69160a7008385f79db_3e8caf1e.displayName = "Foreach";

export const Cond_comp_8d4151efe6cc483296236f8ed0e1817d_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_people_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_8d4151efe6cc483296236f8ed0e1817d_3e8caf1e.displayName = "Cond";

export const Cond_comp_f33fb370e565c8bb41c9f5322b1916bc_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.people_rx_state_.length > reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_count_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_f33fb370e565c8bb41c9f5322b1916bc_3e8caf1e.displayName = "Cond";

export const Bare_comp_3b5485faabfbd6df3ed0506edf89f200_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_post_id_rx_state_?.valueOf?.() === ""?.valueOf?.())) ? "Editar publica\u00e7\u00e3o" : "Criar publica\u00e7\u00e3o")
    )
});
Bare_comp_3b5485faabfbd6df3ed0506edf89f200_3e8caf1e.displayName = "Bare";

export const Input_input_1e4d27ddb0318f701960dcc698827b15_3e8caf1e = memo(({children}) => {
    const on_change_36bd4ee87662fb80ee062da768bdd4f1 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.update_post_media_query", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white",onChange:on_change_36bd4ee87662fb80ee062da768bdd4f1,placeholder:"Pesquisar filme, serie, anime ou livro",type:"search",value:(isNotNullOrUndefined(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_query_rx_state_) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_query_rx_state_ : "")},)
    )
});
Input_input_1e4d27ddb0318f701960dcc698827b15_3e8caf1e.displayName = "Input";

export const Bare_comp_cc8faf2598131ffd5c44f179c2af87e4_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_searching_rx_state_ ? "Pesquisando..." : "Pesquisar obra")
    )
});
Bare_comp_cc8faf2598131ffd5c44f179c2af87e4_3e8caf1e.displayName = "Bare";

export const Button_button_0ed579189e8e716cbdc7400067a9dcb8_3e8caf1e = memo(({children}) => {
    const on_click_69e437f7f41afc88d6f5c4e09893b4d1 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.search_post_media", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"action-button",onClick:on_click_69e437f7f41afc88d6f5c4e09893b4d1,type:"button"},children)
    )
});
Button_button_0ed579189e8e716cbdc7400067a9dcb8_3e8caf1e.displayName = "Button";

export const Img_img_48cce1b6a536400fb52334d419200169_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{alt:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_selected_rx_state_?.["title"],className:"post-media-selected-cover",src:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_selected_rx_state_?.["cover"]},)
    )
});
Img_img_48cce1b6a536400fb52334d419200169_3e8caf1e.displayName = "Img";

export const Cond_comp_1c7823907bbbea1e1f9335667908428f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_selected_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_1c7823907bbbea1e1f9335667908428f_3e8caf1e.displayName = "Cond";

export const Bare_comp_0b1c54b93b064c2e21dbf9225a09671d_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_selected_rx_state_?.["title"]
    )
});
Bare_comp_0b1c54b93b064c2e21dbf9225a09671d_3e8caf1e.displayName = "Bare";

export const Button_button_6f98fb6a5bd993609481aeacb39b3475_3e8caf1e = memo(({children}) => {
    const on_click_cd37c59f1b5e64c99007a0b773824cfa = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.clear_post_media", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"action-button",onClick:on_click_cd37c59f1b5e64c99007a0b773824cfa,type:"button"},children)
    )
});
Button_button_6f98fb6a5bd993609481aeacb39b3475_3e8caf1e.displayName = "Button";

export const Cond_comp_086bf57f69a2928bff31cb7a93762421_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_selected_rx_state_?.["id"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_086bf57f69a2928bff31cb7a93762421_3e8caf1e.displayName = "Cond";

export const Foreach_comp_6f0715604e0e3b0ac7bb5d2ff6b38c4d_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_results_rx_state_ ?? [],((item_rx_state_,index_79f668c22851fd4174aef168543ca57f)=>(jsx("button",{className:"post-media-result",key:index_79f668c22851fd4174aef168543ca57f,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.select_post_media", ({ ["key"] : item_rx_state_?.["key"] }), ({  })))], [_e], ({  })))),type:"button"},jsx(Fragment,{},(!((item_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:"",className:"post-media-result-cover",src:item_rx_state_?.["cover"]},))):(jsx(Fragment,{},jsx(LucideClapperboard,{size:22},))))),jsx("span",{className:"font-semibold"},item_rx_state_?.["title"]),jsx("span",{className:"text-xs text-gray-400"},((item_rx_state_?.["kind"]+" \u00b7 ")+item_rx_state_?.["year"]))))))
    )
});
Foreach_comp_6f0715604e0e3b0ac7bb5d2ff6b38c4d_3e8caf1e.displayName = "Foreach";

export const Cond_comp_958947a25ff1b24950af32c5a66abcde_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_results_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_958947a25ff1b24950af32c5a66abcde_3e8caf1e.displayName = "Cond";

export const Cond_comp_098f216767d43693f93ebafaeae14106_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_searching_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_098f216767d43693f93ebafaeae14106_3e8caf1e.displayName = "Cond";

export const Styledupload_comp_757dac4f83297d1f3c05844be18a8148_3e8caf1e = memo(({children}) => {
    const ref_post_image_upload = useRef(null); refs["ref_post_image_upload"] = ref_post_image_upload;
const [filesById, setFilesById] = useContext(UploadFilesContext);
const on_drop_9f1deeb86bc3599517b16d1ee2c8d7b3 = useCallback(((_ev_0) => ((e => setFilesById(filesById => {
    const updatedFilesById = Object.assign({}, filesById);
    updatedFilesById["post_image_upload"] = e;
    return updatedFilesById;
  })
    )(_ev_0))), [addEvents, ReflexEvent, filesById, setFilesById])
const on_drop_rejected_bedc1fe7e7d4fcbcbc646af9fb7688c4 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("_call_function", ({ ["function"] : (() => (refs['__toast']?.["error"]("", ({ ["title"] : "Files not Accepted", ["description"] : _ev_0.map(((pmuoeieh) => (pmuoeieh?.["file"]?.["path"]+": "+pmuoeieh?.["errors"].map(((xrrixsns) => xrrixsns?.["message"])).join(", ")))).join("\n\n"), ["closeButton"] : true, ["style"] : ({ ["whiteSpace"] : "pre-line" }) })))), ["callback"] : null }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const { getRootProps: miuwrhvk, getInputProps: tufrxhfo, isDragActive: yybhbzkm} = useDropzone(({ ["accept"] : ({ ["image/png"] : [".png"], ["image/jpeg"] : [".jpg", ".jpeg"], ["image/webp"] : [".webp"], ["image/gif"] : [".gif"] }), ["maxFiles"] : 1, ["maxSize"] : 5242880, ["multiple"] : true, ["id"] : "post_image_upload", ["onDrop"] : on_drop_9f1deeb86bc3599517b16d1ee2c8d7b3, ["onDropRejected"] : on_drop_rejected_bedc1fe7e7d4fcbcbc646af9fb7688c4 }));



    return(
        jsx(Fragment,{},jsx("div",{className:"rx-Upload post-image-dropzone",css:({ ["border"] : "1px dashed var(--accent-12)", ["padding"] : "5em", ["textAlign"] : "center" }),id:"post_image_upload",ref:ref_post_image_upload,...miuwrhvk()},jsx("input",{type:"file",...tufrxhfo()},),jsx("div",{className:"post-image-upload-prompt"},jsx(LucideImageUp,{size:22},),jsx("span",{className:"text-sm"},"Escolha ou arraste uma imagem (ate 5 MB)"))))
    )
});
Styledupload_comp_757dac4f83297d1f3c05844be18a8148_3e8caf1e.displayName = "StyledUpload";

export const Bare_comp_033fd497db417e3a41f3cacf3147ea7d_3e8caf1e = memo(({children}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);



    return(
        (filesById["post_image_upload"] ? filesById["post_image_upload"].map((f) => f.name) : [])?.at?.(0)
    )
});
Bare_comp_033fd497db417e3a41f3cacf3147ea7d_3e8caf1e.displayName = "Bare";

export const Button_button_386372eab9e9c4d33ffcbd027f03ff13_3e8caf1e = memo(({children}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);
const on_click_2c3ba9fadeccd7196edb54699494f273 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.stage_post_image", ({ ["files"] : filesById?.["post_image_upload"], ["upload_param_name"] : "files", ["upload_id"] : "post_image_upload", ["extra_headers"] : ({  }) }), ({  }), "uploadFiles"))], [_e], ({  })))), [addEvents, ReflexEvent, filesById, setFilesById])



    return(
        jsx("button",{className:"action-button",onClick:on_click_2c3ba9fadeccd7196edb54699494f273,type:"button"},children)
    )
});
Button_button_386372eab9e9c4d33ffcbd027f03ff13_3e8caf1e.displayName = "Button";

export const Cond_comp_03e73c090cf0ecfd2b822bfc813178d7_3e8caf1e = memo(({children}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);



    return(
        (((filesById["post_image_upload"] ? filesById["post_image_upload"].map((f) => f.name) : []).length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_03e73c090cf0ecfd2b822bfc813178d7_3e8caf1e.displayName = "Cond";

export const Img_img_ff7f96b735ebbe2c2f2687453441b7c9_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{alt:"Previa da imagem enviada",className:"post-image-preview",src:(getBackendURL(env.UPLOAD)+"/"+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_image_filename_rx_state_)},)
    )
});
Img_img_ff7f96b735ebbe2c2f2687453441b7c9_3e8caf1e.displayName = "Img";

export const Button_button_907fe87570e91472d3a86b82f43e9ef6_3e8caf1e = memo(({children}) => {
    const on_click_a8d1605ed6b97a09112897d4cec16d7d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.remove_post_image", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"action-button",onClick:on_click_a8d1605ed6b97a09112897d4cec16d7d,type:"button"},children)
    )
});
Button_button_907fe87570e91472d3a86b82f43e9ef6_3e8caf1e.displayName = "Button";

export const Img_img_4f9440dfe6e787ddafb78ff640ccf130_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{alt:"Imagem atual da publicacao",className:"post-image-preview",src:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_existing_image_url_rx_state_},)
    )
});
Img_img_4f9440dfe6e787ddafb78ff640ccf130_3e8caf1e.displayName = "Img";

export const Cond_comp_08dc654ce7a3655821018d07ca22ff69_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_existing_image_url_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_08dc654ce7a3655821018d07ca22ff69_3e8caf1e.displayName = "Cond";

export const Cond_comp_5eda26a2256572d45403a924b5dea28e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_image_filename_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_5eda26a2256572d45403a924b5dea28e_3e8caf1e.displayName = "Cond";

export const Textarea_textarea_aa0f0f385c439041b5ef3b1c6372c021_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("textarea",{className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_post_body_rx_state_,maxLength:5000,name:"body",required:true},)
    )
});
Textarea_textarea_aa0f0f385c439041b5ef3b1c6372c021_3e8caf1e.displayName = "Textarea";

export const Checkboxinput_input_8de2f3d454eb091f1928faccbb309450_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{defaultChecked:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_post_spoiler_rx_state_,name:"spoiler",type:"checkbox"},)
    )
});
Checkboxinput_input_8de2f3d454eb091f1928faccbb309450_3e8caf1e.displayName = "CheckboxInput";

export const Bare_comp_14cfd6a79521cec85968ddb0f34d894b_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_post_id_rx_state_?.valueOf?.() === ""?.valueOf?.())) ? "Salvar edi\u00e7\u00e3o" : "Publicar")
    )
});
Bare_comp_14cfd6a79521cec85968ddb0f34d894b_3e8caf1e.displayName = "Bare";

export const Form_form_98560903d428e2789987ea54d6cf49ae_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)

    const handleSubmit_ca206bf780d813677b06b40e5159cd02 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.save_post", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"editor-form",key:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_post_id_rx_state_,onSubmit:handleSubmit_ca206bf780d813677b06b40e5159cd02},children)
    )
});
Form_form_98560903d428e2789987ea54d6cf49ae_3e8caf1e.displayName = "Form";

export const Dialogroot_dialog__root_ec32a7d5458ece84aa515088038f1029_3e8caf1e = memo(({children}) => {
    const on_open_change_41982dc794bba4a11020357952e82780 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_post_editor_open", ({ ["value"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx(RadixThemesDialog.Root,{onOpenChange:on_open_change_41982dc794bba4a11020357952e82780,open:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_editor_open_rx_state_},children)
    )
});
Dialogroot_dialog__root_ec32a7d5458ece84aa515088038f1029_3e8caf1e.displayName = "DialogRoot";

export const Foreach_comp_5d549214d7ac5ae95c6748d7d32ad2d6_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_posts_rx_state_ ?? [],((p_rx_state_,index_b2f659fbd211c7b9b4e6d70355930a4a)=>(jsx("article",{className:"post-card",key:index_b2f659fbd211c7b9b4e6d70355930a4a},jsx("div",{className:"post-author"},jsx(ReactRouterLink,{to:("/perfil/"+p_rx_state_?.["user_id"])},jsx(Fragment,{},(!((p_rx_state_?.["avatar"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:p_rx_state_?.["author"],className:"avatar",src:p_rx_state_?.["avatar"]},))):(jsx(Fragment,{},jsx("span",{className:"avatar avatar-fallback"},jsx(LucideUserRound,{size:22},))))))),jsx("div",{},jsx(ReactRouterLink,{className:"font-semibold",to:("/perfil/"+p_rx_state_?.["user_id"])},p_rx_state_?.["author"]),jsx("p",{className:"text-xs text-gray-500"},p_rx_state_?.["published_at"]))),jsx(Fragment,{},(!((p_rx_state_?.["media_cover"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx(ReactRouterLink,{to:("/obra/"+p_rx_state_?.["media_id"])},jsx("img",{alt:p_rx_state_?.["media_title"],className:"post-cover",loading:"lazy",src:p_rx_state_?.["media_cover"]},)))):(jsx(Fragment,{},)))),jsx(Fragment,{},(!((p_rx_state_?.["media_id"]?.valueOf?.() === "0"?.valueOf?.()))?(jsx(Fragment,{},jsx(ReactRouterLink,{className:"block brand-yellow",to:("/obra/"+p_rx_state_?.["media_id"])},p_rx_state_?.["media_title"]))):(jsx(Fragment,{},)))),jsx(Fragment,{},(!((p_rx_state_?.["image_url"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:"Imagem anexada a publicacao",className:"w-full max-h-[600px] rounded-2xl object-contain bg-[#171714]",loading:"lazy",src:p_rx_state_?.["image_url"]},))):(jsx(Fragment,{},)))),jsx(Fragment,{},((p_rx_state_?.["spoiler"]?.valueOf?.() === "True"?.valueOf?.())?(jsx(Fragment,{},jsx("details",{},jsx("summary",{className:"cursor-pointer text-amber-300"},"Mostrar conte\u00fado com spoilers"),jsx("p",{className:"whitespace-pre-wrap mt-3"},p_rx_state_?.["body"])))):(jsx(Fragment,{},jsx("p",{className:"whitespace-pre-wrap"},p_rx_state_?.["body"]))))),jsx("div",{className:"post-actions"},jsx("button",{className:"quiet-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.like", ({ ["pid"] : p_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},jsx(LucideHeart,{size:18},),(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.liked_posts_rx_state_.includes(p_rx_state_?.["id"]) ? "Descurtir" : "Curtir")),jsx("button",{className:"quiet-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.discussion", ({ ["pid"] : p_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},jsx(LucideMessageCircle,{size:18},),(!((p_rx_state_?.["comments_count"]?.valueOf?.() === ""?.valueOf?.())) ? (p_rx_state_?.["comments_count"]+" coment\u00e1rios") : "Coment\u00e1rios")),jsx(Fragment,{},(!((p_rx_state_?.["likes_count"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("span",{className:"text-sm text-gray-400"},(p_rx_state_?.["likes_count"]+" curtidas")))):(jsx(Fragment,{},)))),jsx(Fragment,{},(!((p_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.()))?(jsx(Fragment,{},jsx("button",{className:"quiet-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_report", ({ ["target_type"] : "post", ["target_id"] : p_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Denunciar"))):(jsx(Fragment,{},)))),jsx(Fragment,{},((p_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.())?(jsx(Fragment,{},jsx("button",{className:"quiet-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.edit_post", ({ ["pid"] : p_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Editar"),jsx(RadixThemesAlertDialog.Root,{},jsx(RadixThemesAlertDialog.Trigger,{},jsx("button",{className:"quiet-button danger",type:"button"},"Excluir publica\u00e7\u00e3o")),jsx(RadixThemesAlertDialog.Content,{className:"codeboxd-dialog confirm-dialog"},jsx(RadixThemesAlertDialog.Title,{},"Excluir publica\u00e7\u00e3o?"),jsx(RadixThemesAlertDialog.Description,{},"Esta a\u00e7\u00e3o remove o conte\u00fado. Deseja continuar?"),jsx(RadixThemesFlex,{className:"confirm-dialog-actions",css:({ ["gap"] : "3", ["marginTop"] : "20px" }),justify:"end"},jsx(RadixThemesAlertDialog.Cancel,{},jsx(RadixThemesButton,{className:"confirm-cancel-button",variant:"soft"},"Cancelar")),jsx(RadixThemesAlertDialog.Action,{},jsx(RadixThemesFlex,{},jsx(RadixThemesButton,{color:"red",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.remove_post", ({ ["pid"] : p_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Confirmar exclus\u00e3o")))))))):(jsx(Fragment,{},)))))))))
    )
});
Foreach_comp_5d549214d7ac5ae95c6748d7d32ad2d6_3e8caf1e.displayName = "Foreach";

export const Cond_comp_0e3140c1593044b23337b0008f5af456_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.posts_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_0e3140c1593044b23337b0008f5af456_3e8caf1e.displayName = "Cond";

export const Cond_comp_90039c26d97859e06a8fc32feee50d45_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.posts_rx_state_.length > reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_count_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_90039c26d97859e06a8fc32feee50d45_3e8caf1e.displayName = "Cond";

export const Button_button_9efdc2fe3aab04053abb4f5da54657e5_3e8caf1e = memo(({children}) => {
    const on_click_8221dc93568f0bc2a5a036556ba69910 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.close_discussion", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"action-button",onClick:on_click_8221dc93568f0bc2a5a036556ba69910,type:"button"},children)
    )
});
Button_button_9efdc2fe3aab04053abb4f5da54657e5_3e8caf1e.displayName = "Button";

export const Foreach_comp_3ba458750fae92423bbe6d6f62be37f0_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.comments_rx_state_ ?? [],((c_rx_state_,index_14cb4ac1dced3e8e8e828d07386fb759)=>(jsx("article",{className:"rounded-2xl border border-white/10 bg-[#111114] p-5 space-y-4",key:index_14cb4ac1dced3e8e8e828d07386fb759},jsx(ReactRouterLink,{className:"font-semibold",to:("/perfil/"+c_rx_state_?.["user_id"])},c_rx_state_?.["author"]),jsx("p",{className:"whitespace-pre-wrap"},c_rx_state_?.["body"]),jsx(Fragment,{},((c_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.())?(jsx(Fragment,{},jsx("div",{className:"flex gap-3"},jsx("button",{className:"action-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.edit_comment", ({ ["cid"] : c_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),type:"button"},"Editar"),jsx(RadixThemesAlertDialog.Root,{},jsx(RadixThemesAlertDialog.Trigger,{},jsx("button",{className:"quiet-button danger",type:"button"},"Excluir coment\u00e1rio")),jsx(RadixThemesAlertDialog.Content,{className:"codeboxd-dialog confirm-dialog"},jsx(RadixThemesAlertDialog.Title,{},"Excluir coment\u00e1rio?"),jsx(RadixThemesAlertDialog.Description,{},"Esta a\u00e7\u00e3o remove o conte\u00fado. Deseja continuar?"),jsx(RadixThemesFlex,{className:"confirm-dialog-actions",css:({ ["gap"] : "3", ["marginTop"] : "20px" }),justify:"end"},jsx(RadixThemesAlertDialog.Cancel,{},jsx(RadixThemesButton,{className:"confirm-cancel-button",variant:"soft"},"Cancelar")),jsx(RadixThemesAlertDialog.Action,{},jsx(RadixThemesFlex,{},jsx(RadixThemesButton,{color:"red",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.remove_comment", ({ ["cid"] : c_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Confirmar exclus\u00e3o"))))))))):(jsx(Fragment,{},jsx("button",{className:"quiet-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_report", ({ ["target_type"] : "comment", ["target_id"] : c_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Denunciar")))))))))
    )
});
Foreach_comp_3ba458750fae92423bbe6d6f62be37f0_3e8caf1e.displayName = "Foreach";

export const Cond_comp_6a5874690760cb53f1e50876cc374c93_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.comments_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_6a5874690760cb53f1e50876cc374c93_3e8caf1e.displayName = "Cond";

export const Textarea_textarea_3e21265038b028455f3d238d7cf90a5b_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("textarea",{className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_comment_body_rx_state_,maxLength:2000,name:"body",required:true},)
    )
});
Textarea_textarea_3e21265038b028455f3d238d7cf90a5b_3e8caf1e.displayName = "Textarea";

export const Bare_comp_84a16bd546914afcd9ed2faa905957d6_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_comment_id_rx_state_?.valueOf?.() === ""?.valueOf?.())) ? "Salvar edi\u00e7\u00e3o" : "Comentar")
    )
});
Bare_comp_84a16bd546914afcd9ed2faa905957d6_3e8caf1e.displayName = "Bare";

export const Form_form_72877d02e5a532d313c56faab87b3d8e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)

    const handleSubmit_cf3049f6fcf796f9ab787c78b7120590 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.save_comment", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"rounded-2xl border border-white/10 bg-[#111114] p-5 space-y-4",key:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_post_rx_state_+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_comment_id_rx_state_),onSubmit:handleSubmit_cf3049f6fcf796f9ab787c78b7120590},children)
    )
});
Form_form_72877d02e5a532d313c56faab87b3d8e_3e8caf1e.displayName = "Form";

export const Cond_comp_1c8c5d6fca2427ebc08a5b97b183630a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_post_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_1c8c5d6fca2427ebc08a5b97b183630a_3e8caf1e.displayName = "Cond";

export const Button_button_b3a09a0c10d633d0bd75a5583b30eb30_3e8caf1e = memo(({children}) => {
    const on_click_5513d5b7c38dfbe621da7ee3e02d8fcb = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.new_post", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"action-button",onClick:on_click_5513d5b7c38dfbe621da7ee3e02d8fcb,type:"button"},children)
    )
});
Button_button_b3a09a0c10d633d0bd75a5583b30eb30_3e8caf1e.displayName = "Button";

export const Foreach_comp_b5a5e992b3426309a69745f73ae9e402_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.suggested_people_rx_state_ ?? [],((p_rx_state_,index_b79fa401edc9820db9a777f8095aac35)=>(jsx(ReactRouterLink,{className:"sidebar-person",key:index_b79fa401edc9820db9a777f8095aac35,to:("/perfil/"+p_rx_state_?.["user_id"])},jsx(Fragment,{},(!((p_rx_state_?.["avatar_url"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:p_rx_state_?.["display_name"],className:"avatar",src:p_rx_state_?.["avatar_url"]},))):(jsx(Fragment,{},jsx("span",{className:"avatar avatar-fallback"},jsx(LucideUserRound,{size:22},)))))),jsx("div",{},jsx("strong",{},p_rx_state_?.["display_name"]),jsx("p",{},("@"+p_rx_state_?.["username"])))))))
    )
});
Foreach_comp_b5a5e992b3426309a69745f73ae9e402_3e8caf1e.displayName = "Foreach";

export const Button_button_d58163fee7ac23c4ae57997c2e0e07df_3e8caf1e = memo(({children}) => {
    const on_click_71af9dfb457562c8e1287528fc04ef54 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.new_list", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"action-button",onClick:on_click_71af9dfb457562c8e1287528fc04ef54,type:"button"},children)
    )
});
Button_button_d58163fee7ac23c4ae57997c2e0e07df_3e8caf1e.displayName = "Button";

export const Bare_comp_6256830d90b16469efb7c7cef4a09982_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["id"]?.valueOf?.() === ""?.valueOf?.()) ? "Criar lista" : "Editar lista")
    )
});
Bare_comp_6256830d90b16469efb7c7cef4a09982_3e8caf1e.displayName = "Bare";

export const Input_input_8b6a8a460b21b52b3bd1e968196b74e0_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["title"],maxLength:120,name:"title",required:true},)
    )
});
Input_input_8b6a8a460b21b52b3bd1e968196b74e0_3e8caf1e.displayName = "Input";

export const Textarea_textarea_385d25b160864f58c858e5f201d62e0e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("textarea",{className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["description"],maxLength:2000,name:"description"},)
    )
});
Textarea_textarea_385d25b160864f58c858e5f201d62e0e_3e8caf1e.displayName = "Textarea";

export const Checkboxinput_input_07389bd859f729c637ba348fcd09abe3_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{defaultChecked:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["is_public"]?.valueOf?.() === "True"?.valueOf?.()),name:"is_public",type:"checkbox"},)
    )
});
Checkboxinput_input_07389bd859f729c637ba348fcd09abe3_3e8caf1e.displayName = "CheckboxInput";

export const Form_form_4a8dc68c9036bb0c3003895d037698d6_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)

    const handleSubmit_491f8b8cc97885b608f19c9769a01f1d = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.save_list", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"editor-form",key:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["id"]+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["title"]),onSubmit:handleSubmit_491f8b8cc97885b608f19c9769a01f1d},children)
    )
});
Form_form_4a8dc68c9036bb0c3003895d037698d6_3e8caf1e.displayName = "Form";

export const Dialogroot_dialog__root_3a8e68f84178e042e8bdc2f56ad96b07_3e8caf1e = memo(({children}) => {
    const on_open_change_4e0c9a0544c5cf5d3a8a741a2c0299c5 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_list_editor_open", ({ ["value"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx(RadixThemesDialog.Root,{onOpenChange:on_open_change_4e0c9a0544c5cf5d3a8a741a2c0299c5,open:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.list_editor_open_rx_state_},children)
    )
});
Dialogroot_dialog__root_3a8e68f84178e042e8bdc2f56ad96b07_3e8caf1e.displayName = "DialogRoot";

export const Foreach_comp_5532dca625ba9111c4be5271c605f7f4_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_lists_rx_state_ ?? [],((item_rx_state_,index_57cd0006aad4871bf650118959598197)=>(jsx("button",{className:"list-row",key:index_57cd0006aad4871bf650118959598197,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_list", ({ ["lid"] : item_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),type:"button"},jsx(LucideListVideo,{size:20},),jsx("span",{},item_rx_state_?.["title"]),jsx("span",{className:"list-visibility"},((item_rx_state_?.["is_public"]?.valueOf?.() === "True"?.valueOf?.()) ? "P\u00fablica" : "Privada")),jsx(LucideChevronRight,{size:18},)))))
    )
});
Foreach_comp_5532dca625ba9111c4be5271c605f7f4_3e8caf1e.displayName = "Foreach";

export const Cond_comp_d621396f2efa447b5175e8b705f0db4c_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.lists_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d621396f2efa447b5175e8b705f0db4c_3e8caf1e.displayName = "Cond";

export const Cond_comp_61bb19f363d0c63a2a8ff4d1bfd4ad07_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.lists_rx_state_.length > reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_count_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_61bb19f363d0c63a2a8ff4d1bfd4ad07_3e8caf1e.displayName = "Cond";

export const Bare_comp_0e87ad9e81f5bbfd322490e26bc95991_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["title"]
    )
});
Bare_comp_0e87ad9e81f5bbfd322490e26bc95991_3e8caf1e.displayName = "Bare";

export const Bare_comp_800d0d260b7b2758821004228d190d68_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["description"]
    )
});
Bare_comp_800d0d260b7b2758821004228d190d68_3e8caf1e.displayName = "Bare";

export const Button_button_15d0541e9c5c8dd0988c89e3bbf6dca3_3e8caf1e = memo(({children}) => {
    const on_click_8e026e7f771610b08ef7090dd5b3ff63 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_list_editor_open", ({ ["value"] : true }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"action-button",onClick:on_click_8e026e7f771610b08ef7090dd5b3ff63,type:"button"},children)
    )
});
Button_button_15d0541e9c5c8dd0988c89e3bbf6dca3_3e8caf1e.displayName = "Button";

export const Button_button_2e4975427be8a38a3f08c060eae74bad_3e8caf1e = memo(({children}) => {
    const on_click_628f0773fb680d34f1479c6c23c94c23 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.remove_list", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{color:"red",onClick:on_click_628f0773fb680d34f1479c6c23c94c23},children)
    )
});
Button_button_2e4975427be8a38a3f08c060eae74bad_3e8caf1e.displayName = "Button";

export const Cond_comp_664d139b25926413264343b2e2256f98_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.owns_list_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_664d139b25926413264343b2e2256f98_3e8caf1e.displayName = "Cond";

export const Foreach_comp_64ac4696de1e14ea9aa080828ed81697_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.catalog_items_rx_state_ ?? [],((m_rx_state_,index_aab90c2deded1104d10fcc39d8d93f6d)=>(jsx("option",{key:index_aab90c2deded1104d10fcc39d8d93f6d,value:m_rx_state_?.["id"]},m_rx_state_?.["title"]))))
    )
});
Foreach_comp_64ac4696de1e14ea9aa080828ed81697_3e8caf1e.displayName = "Foreach";

export const Form_form_91b8a8259c08c75cf566d7bdbd995ad1_3e8caf1e = memo(({children}) => {
    

    const handleSubmit_ac7926ab17097d78e3c882671fb5bf2c = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.add_list_item", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"list-add-form",onSubmit:handleSubmit_ac7926ab17097d78e3c882671fb5bf2c},children)
    )
});
Form_form_91b8a8259c08c75cf566d7bdbd995ad1_3e8caf1e.displayName = "Form";

export const Foreach_comp_efab3aaf1293148e5ea6579a41d08a7f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.list_items_rx_state_ ?? [],((m_rx_state_,index_ba7ecc92fc504ecb76a5c94a6da09b0e)=>(jsx("article",{className:"list-media-item",key:index_ba7ecc92fc504ecb76a5c94a6da09b0e},jsx(ReactRouterLink,{className:"media-card",to:("/obra/"+m_rx_state_?.["id"])},jsx("div",{className:"h-full"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},))))),jsx("div",{className:"p-4"},jsx("h3",{className:"font-semibold line-clamp-2"},m_rx_state_?.["title"]),jsx("p",{className:"text-sm text-gray-400 mt-3"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"]))))),jsx(Fragment,{},(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.owns_list_rx_state_?(jsx(Fragment,{},jsx(RadixThemesAlertDialog.Root,{},jsx(RadixThemesAlertDialog.Trigger,{},jsx("button",{className:"quiet-button danger",type:"button"},"Remover obra")),jsx(RadixThemesAlertDialog.Content,{className:"codeboxd-dialog confirm-dialog"},jsx(RadixThemesAlertDialog.Title,{},"Remover obra?"),jsx(RadixThemesAlertDialog.Description,{},"Esta a\u00e7\u00e3o remove o conte\u00fado. Deseja continuar?"),jsx(RadixThemesFlex,{className:"confirm-dialog-actions",css:({ ["gap"] : "3", ["marginTop"] : "20px" }),justify:"end"},jsx(RadixThemesAlertDialog.Cancel,{},jsx(RadixThemesButton,{className:"confirm-cancel-button",variant:"soft"},"Cancelar")),jsx(RadixThemesAlertDialog.Action,{},jsx(RadixThemesFlex,{},jsx(RadixThemesButton,{color:"red",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.remove_list_item", ({ ["mid"] : m_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Confirmar exclus\u00e3o")))))))):(jsx(Fragment,{},))))))))
    )
});
Foreach_comp_efab3aaf1293148e5ea6579a41d08a7f_3e8caf1e.displayName = "Foreach";

export const Cond_comp_45bad6310b9bf5a3b3003925630243f6_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.list_items_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_45bad6310b9bf5a3b3003925630243f6_3e8caf1e.displayName = "Cond";

export const Cond_comp_36955990ed20cb5e972be66613c15559_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["id"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_36955990ed20cb5e972be66613c15559_3e8caf1e.displayName = "Cond";
